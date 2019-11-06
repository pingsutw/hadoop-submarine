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
from submarine.pipeline.utils import get_from_registry
from submarine.constants import LOCAL


class Model:
    def __init__(self, model, runtime, data, registry, feature, label_feature, distributed=False, **kwargs):
        self.model = get_from_registry(model, registry)(**kwargs)
        self.distributed = distributed
        self.runtime = runtime
        self.registry = registry
        self.data = data
        self.feature = feature
        self.label_feature = label_feature

    def train(self):
        self.model.fit(self.data.training_set[self.feature], self.data.training_set[self.label_feature])

    def predict(self):
        return self.model.predict(self.feature)

    def evaluate(self):
        # dataset = tf.data.Dataset.from_tensor_slices((self.data[self.feature].values, target.values))
        return self.model.evaluate(self.data.valid_set[self.feature], self.data.valid_set[self.label_feature])
