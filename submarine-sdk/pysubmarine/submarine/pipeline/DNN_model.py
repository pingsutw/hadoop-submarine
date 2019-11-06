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

from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow import keras
from tensorflow.keras import layers


class DNN_Keras:
    def __init__(self,  **kwargs):
        self.model = self.build_model()
        print(self.model.summary())

    def build_model(self):
        inputs = keras.Input(shape=(17,), name='taxi_data')
        x = layers.Dense(64, activation='relu')(inputs)
        x = layers.Dense(64, activation='relu')(x)
        outputs = layers.Dense(2, activation='softmax')(x)
        model = keras.Model(inputs=inputs, outputs=outputs, name='DNN')
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=keras.optimizers.RMSprop(),
                      metrics=['accuracy'])
        return model

    def fit(self, features, label_features):
        self.model.fit(features, label_features, batch_size=64,
                       epochs=10, validation_split=0.2)

    def evaluate(self, data, label):
        return self.model.evaluate(data, label)

    def predict(self, features):
        self.model.predict(features)
