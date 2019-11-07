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
from xgboost import XGBClassifier
from submarine.pipeline.evaluate import accuracy
from submarine.pipeline.abstract_model import abstract_model


class xgboost(abstract_model):
    def __init__(self,  **kwargs):
        super(abstract_model, self).__init__()
        self.model = None
        self.build_model()

    def build_model(self):
        self.model = XGBClassifier(n_estimators=100)

    def fit(self, features, label_features):
        self.model.fit(features, label_features)

    def evaluate(self, features, label_features):
        return None, accuracy(self.model, features, label_features)

    def predict(self, features):
        self.model.predict(features)
