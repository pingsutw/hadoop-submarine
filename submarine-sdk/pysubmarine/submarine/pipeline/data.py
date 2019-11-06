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

import pandas as pd
import submarine.pipeline.split
import submarine.pipeline.utils
from submarine.pipeline.transform import df_label_encoder, df_handle_missing_values,\
    df_where, df_greater, df_concatenate, df_multiply


class Data:
    def __init__(self, source_url, data_type, runtime):
        self.source_url = source_url
        self.data_type = data_type
        self.runtime = runtime
        self.training_set = None
        self.valid_set = None
        self.test_set = None
        self.data_set = None
        self.columns = None

        self.data_set, self.columns = \
            submarine.pipeline.utils.readDataSet(data_type, source_url)

    def __getitem__(self, key):
        return self.data_set[key]

    def __setitem__(self, key, value):
        self.data_set[key] = value

    def concatenate(self):
        df_concatenate(self.training_set, self.valid_set, self.test_set)

    def split(self, partition):
        self.training_set, self.valid_set, self.test_set = \
            submarine.pipeline.split.split_df(self.data_set, partition)

    def handle_missing_values(self, features, strategy):
        for feature in features:
            df_handle_missing_values(self.data_set, feature, strategy)

    def label_encoder(self, features):
        for feature in features:
            df_label_encoder(self.data_set, feature)

    def where(self, condition, x, y):
        return df_where(self.data_set, condition, x, y)

    @staticmethod
    def greater(x, y):
        return df_greater(x, y)

    @staticmethod
    def multiply(x, y):
        return df_multiply(x, y)
