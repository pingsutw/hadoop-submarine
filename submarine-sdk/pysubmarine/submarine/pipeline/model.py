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

from submarine.pipeline.model_registry import classifier_model_registry
from submarine.pipeline.utils import get_from_registry
from submarine.pipeline.evaluate import accuracy
from submarine.pipeline.pusher import push2local
import submarine.pipeline.serving

from submarine.constants import LOCAL


class Model:
    def __init__(self, model, engine, data, registry, distributed=False):
        self.model = get_from_registry(model, registry)
        self.distributed = distributed
        self.engine = engine
        self.registry = registry
        self.data = data
        self.input = None
        self.output = None

    def train(self, feature, label_feature):
        self.input = feature
        self.output = label_feature
        self.model.fit(self.data.valid_set[feature], self.data.valid_set[label_feature])

    def predict(self):
        pass

    def evaluate(self, label_features):
        return accuracy(self.model, self.data, label_features)

    def push(self, destination, storage=LOCAL):
        if storage == LOCAL:
            push2local(destination, self.model, self.input)

    def serve(self, model, model_columns):
        submarine.pipeline.serving.pickle(model, model_columns)
