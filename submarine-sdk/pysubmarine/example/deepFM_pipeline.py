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
from tensorflow.python.keras.utils import tf_utils

from submarine.pipeline.model import deepFM
import tensorflow as tf

COLUMNS_MAX_TOKENS = [('numeric', 13), ('categorical', 26)]
DEFAULT_VALUES = [[0], [''], ['']]


def _decode_tsv(line):
    columns = tf.decode_csv(line, record_defaults=DEFAULT_VALUES, field_delim='\t')
    y = columns[0]

    feat_columns = dict(zip((t[0] for t in COLUMNS_MAX_TOKENS), columns[1:]))
    X = {}
    for colname, max_tokens in COLUMNS_MAX_TOKENS:
        # 调用string_split时，第一个参数必须是一个list，所以要把columns[colname]放在[]中
        # 这时每个kv还是'k:v'这样的字符串
        kvpairs = tf.string_split([feat_columns[colname]], ',').values[:max_tokens]

        # k,v已经拆开, kvpairs是一个SparseTensor，因为每个kvpair格式相同，都是"k:v"
        # 既不会出现"k"，也不会出现"k:v1:v2:v3:..."
        # 所以，这时的kvpairs实际上是一个满阵
        kvpairs = tf.string_split(kvpairs, ':')

        # kvpairs是一个[n_valid_pairs,2]矩阵
        kvpairs = tf.reshape(kvpairs.values, kvpairs.dense_shape)

        feat_ids, feat_vals = tf.split(kvpairs, num_or_size_splits=2, axis=1)
        feat_ids = tf.string_to_number(feat_ids, out_type=tf.int32)
        feat_vals = tf.string_to_number(feat_vals, out_type=tf.float32)

        # 不能调用squeeze, squeeze的限制太多, 当原始矩阵有1行或0行时，squeeze都会报错
        X[colname + "_ids"] = tf.reshape(feat_ids, shape=[-1])
        X[colname + "_values"] = tf.reshape(feat_vals, shape=[-1])

    return X, y


def input_fn2(data_file, batch_size=32, num_epochs=1, batches_per_shuffle=256):
    # ----------- prepare padding
    pad_shapes = {}
    pad_values = {}
    for c, max_tokens in COLUMNS_MAX_TOKENS:
        pad_shapes[c + "_ids"] = tf.TensorShape([max_tokens])
        pad_shapes[c + "_values"] = tf.TensorShape([max_tokens])

        pad_values[c + "_ids"] = -1  # 0 is still valid token-id, -1 for padding
        pad_values[c + "_values"] = 0.0

    # no need to pad labels
    pad_shapes = (pad_shapes, tf.TensorShape([]))
    pad_values = (pad_values, 0)

    # ----------- define reading ops
    dataset = tf.data.TextLineDataset(data_file).skip(1)  # skip the header
    dataset = dataset.map(_decode_tsv, num_parallel_calls=4)

    if batches_per_shuffle > 0:
        dataset = dataset.shuffle(batches_per_shuffle * batch_size)

    dataset = dataset.repeat(num_epochs)
    dataset = dataset.padded_batch(batch_size=batch_size,
                                   padded_shapes=pad_shapes,
                                   padding_values=pad_values)

    iterator = dataset.make_one_shot_iterator()
    dense_Xs, ys = iterator.get_next()

    # ----------- convert dense to sparse
    # sparse_Xs = {}
    # for c, _ in COLUMNS_MAX_TOKENS:
    #     for suffix in ["ids", "values"]:
    #         k = "{}_{}".format(c, suffix)
    #         sparse_Xs[k] = tf_utils.to_sparse_input_and_drop_ignore_values(dense_Xs[k])
    # ----------- return
    return dense_Xs, ys


def input_fn(filenames, batch_size=32, num_epochs=1, perform_shuffle=False):
    print('Parsing', filenames)

    def decode_libsvm(line):
        columns = tf.string_split([line], ' ')
        labels = tf.string_to_number(columns.values[0], out_type=tf.float32)
        splits = tf.string_split(columns.values[1:], ':')
        id_vals = tf.reshape(splits.values, splits.dense_shape)
        feat_ids, feat_vals = tf.split(id_vals, num_or_size_splits=2, axis=1)
        feat_ids = tf.string_to_number(feat_ids, out_type=tf.int32)
        feat_vals = tf.string_to_number(feat_vals, out_type=tf.float32)
        return {"feat_ids": feat_ids, "feat_vals": feat_vals}, labels

    # Extract lines from input files using the Dataset API, can pass one filename or filename list
    dataset = tf.data.TextLineDataset(filenames).map(decode_libsvm, num_parallel_calls=10).prefetch(500000)

    # Randomizes input using a window of 256 elements (read into memory)
    if perform_shuffle:
        dataset = dataset.shuffle(buffer_size=256)

    # epochs from blending together.
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)  # Batch size to use

    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    # with tf.Session() as sess:
    #     print(sess.run(batch_features))
    return batch_features, batch_labels


def main(_):
    print('Start deepFM pipeline :')

    tr_files = './data/criteo/whole_train.tsv'
    va_files = './data/criteo/whole_test.tsv'
    model_dir = './DeepFM'

    num_threads = 8
    num_epochs = 10
    batch_size = 64
    log_steps = 1000
    optimizer = 'adam'

    field_size = 39
    feature_size = 1024
    embedding_size = 0
    learning_rate = 0.0005
    l2_reg = 0.0001
    deep_layers = '256,128,64'
    dropout = '0.5,0.5,0.5'
    loss_type = 'log_loss'
    batch_norm_decay = 0.9
    batch_norm = False

    model_params = {
        "field_size": field_size,
        "feature_size": feature_size,
        "embedding_size": embedding_size,
        "learning_rate": learning_rate,
        "l2_reg": l2_reg,
        "deep_layers": deep_layers,
        "dropout": dropout,
        "loss_type": loss_type,
        "batch_norm_decay": batch_norm_decay,
        "batch_norm": batch_norm,
    }

    config = tf.estimator.RunConfig().replace(
        session_config=tf.ConfigProto(device_count={'GPU': 0, 'CPU': num_threads}),
        log_step_count_steps=log_steps, save_summary_steps=log_steps)
    model = deepFM(model_dir, config, model_params, optimizer)

    train_spec = tf.estimator.TrainSpec(
        input_fn=lambda: input_fn(tr_files, num_epochs=num_epochs, batch_size=batch_size))
    eval_spec = tf.estimator.EvalSpec(input_fn=lambda: input_fn(va_files, num_epochs=1, batch_size=batch_size),
                                      steps=None, start_delay_secs=1000, throttle_secs=1200)

    tf.estimator.train_and_evaluate(model, train_spec, eval_spec)


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
