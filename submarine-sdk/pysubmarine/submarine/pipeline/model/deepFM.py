# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf


def deepFM(model_dir, config, model_params, optimizer='adam'):
    def batch_norm_layer(x, train_phase, scope_bn, batch_norm_decay):
        bn_train = tf.contrib.layers.batch_norm(x, decay=batch_norm_decay, center=True, scale=True,
                                                updates_collections=None, is_training=True, reuse=None, scope=scope_bn)
        bn_infer = tf.contrib.layers.batch_norm(x, decay=batch_norm_decay, center=True, scale=True,
                                                updates_collections=None, is_training=False, reuse=True, scope=scope_bn)
        z = tf.cond(tf.cast(train_phase, tf.bool), lambda: bn_train, lambda: bn_infer)
        return z

    def model_fn(features, labels, mode, params):
        field_size = params["field_size"]
        feature_size = params["feature_size"]
        embedding_size = params["embedding_size"]
        l2_reg = params["l2_reg"]
        learning_rate = params["learning_rate"]
        batch_norm_decay = params["batch_norm_decay"]
        batch_norm = params["batch_norm"]
        layers = list(map(int, params["deep_layers"].split(',')))
        dropout = list(map(float, params["dropout"].split(',')))

        # ------build weights------
        FM_B = tf.get_variable(name='fm_bias', shape=[1], initializer=tf.constant_initializer(0.0))
        FM_W = tf.get_variable(name='fm_w', shape=[feature_size], initializer=tf.glorot_normal_initializer())
        FM_V = tf.get_variable(name='fm_v', shape=[feature_size, embedding_size],
                               initializer=tf.glorot_normal_initializer())

        # ------build feature-------
        feat_ids = features['feat_ids']
        feat_ids = tf.reshape(feat_ids, shape=[-1, field_size])
        feat_vals = features['feat_vals']
        feat_vals = tf.reshape(feat_vals, shape=[-1, field_size])

        # ------build f(x)------
        with tf.variable_scope("First-order"):
            feat_weights = tf.nn.embedding_lookup(FM_W, feat_ids)  # None * F * 1
            y_w = tf.reduce_sum(tf.multiply(feat_weights, feat_vals), 1)

        with tf.variable_scope("Second-order"):
            embeddings = tf.nn.embedding_lookup(FM_V, feat_ids)  # None * F * K
            feat_vals = tf.reshape(feat_vals, shape=[-1, field_size, 1])
            embeddings = tf.multiply(embeddings, feat_vals)  # vij*xi
            sum_square = tf.square(tf.reduce_sum(embeddings, 1))
            square_sum = tf.reduce_sum(tf.square(embeddings), 1)
            y_v = 0.5 * tf.reduce_sum(tf.subtract(sum_square, square_sum), 1)  # None * 1

        with tf.variable_scope("Deep-part"):
            if batch_norm:
                if mode == tf.estimator.ModeKeys.TRAIN:
                    train_phase = True
                else:
                    train_phase = False

            deep_inputs = tf.reshape(embeddings, shape=[-1, field_size * embedding_size])  # None * (F*K)

            for i in range(len(layers)):
                deep_inputs = tf.contrib.layers.fully_connected(inputs=deep_inputs, num_outputs=layers[i],
                                                                weights_regularizer=tf.contrib.layers.l2_regularizer(
                                                                    l2_reg), scope='mlp%d' % i)
                if batch_norm:
                    deep_inputs = batch_norm_layer(deep_inputs, train_phase=train_phase,
                                                   scope_bn='bn_%d' % i, batch_norm_decay=batch_norm_decay)
                if mode == tf.estimator.ModeKeys.TRAIN:
                    deep_inputs = tf.nn.dropout(deep_inputs, keep_prob=dropout[i])

            y_deep = tf.contrib.layers.fully_connected(inputs=deep_inputs, num_outputs=1, activation_fn=tf.identity, \
                                                       weights_regularizer=tf.contrib.layers.l2_regularizer(l2_reg),
                                                       scope='deep_out')
            y_d = tf.reshape(y_deep, shape=[-1])

        with tf.variable_scope("DeepFM-out"):
            y_bias = FM_B * tf.ones_like(y_d, dtype=tf.float32)
            y = y_bias + y_w + y_v + y_d
            pred = tf.sigmoid(y)

        predictions = {"prob": pred}
        export_outputs = {
            tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: tf.estimator.export.PredictOutput(
                predictions)}
        # Provide an estimator spec for `ModeKeys.PREDICT`
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=predictions,
                export_outputs=export_outputs)

        # ------build loss------
        loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y, labels=labels)) + \
               l2_reg * tf.nn.l2_loss(FM_W) + \
               l2_reg * tf.nn.l2_loss(FM_V)

        # Provide an estimator spec for `ModeKeys.EVAL`
        eval_metric_ops = {
            "auc": tf.metrics.auc(labels, pred)
        }
        if mode == tf.estimator.ModeKeys.EVAL:
            return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=predictions,
                loss=loss,
                eval_metric_ops=eval_metric_ops)

        if optimizer == 'adam':
            op = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-8)
        elif optimizer == 'adagrad':
            op = tf.train.AdagradOptimizer(learning_rate=learning_rate, initial_accumulator_value=1e-8)
        elif optimizer == 'momentum':
            op = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.95)
        elif optimizer == 'ftrl':
            op = tf.train.FtrlOptimizer(learning_rate)
        else:
            raise TypeError("Invalid optimizer :", optimizer)

        train_op = op.minimize(loss, global_step=tf.train.get_global_step())

        # Provide an estimator spec for `ModeKeys.TRAIN` modes
        if mode == tf.estimator.ModeKeys.TRAIN:
            return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=predictions,
                loss=loss,
                train_op=train_op)

    return tf.estimator.Estimator(model_fn=model_fn, model_dir=model_dir, params=model_params, config=config)
