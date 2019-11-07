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

from submarine.pipeline.utils import get_from_registry
from submarine.pipeline.dataExecutor_registry import dataExecutor_registry
from submarine.exceptions import PreprocessingException


class DataManager:
    def __init__(self, source_url, data_type, runtime):
        self.source_url = source_url
        self.data_type = data_type
        self.runtime = runtime
        self.executor = get_from_registry(data_type, dataExecutor_registry)()
        self.training_set = None
        self.valid_set = None
        self.test_set = None
        self.data_set, self.columns = \
            self.executor.readDataSet(source_url)

    def concatenate(self):
        self.executor.concatenate(self.training_set, self.valid_set, self.test_set)

    def splitData(self, partition):
        self.training_set, self.valid_set, self.test_set = \
            self.executor.split(self.data_set, partition)

    def handle_missing_values(self, features, strategy):
        if features is None:
            raise PreprocessingException("features must need a value")
        for feature in features:
            self.data_set = self.executor.handle_missing_values(self.data_set, feature, strategy)

    def label_encoder(self, features):
        for feature in features:
            self.data_set = self.executor.label_encoder(self.data_set, feature)

    def where(self, condition, x, y):
        return self.executor.where(self.data_set, condition, x, y)

    def greater(self, x, y):
        return self.executor.greater(x, y)

    def multiply(self, x, y):
        return self.executor.multiply(x, y)
