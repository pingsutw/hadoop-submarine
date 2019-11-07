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

from os.path import splitext
import pandas as pd
from submarine.constants import CSV
import numpy as np

from submarine.exceptions import PreprocessingException
from sklearn import preprocessing
from submarine.constants import FILL_WITH_CONST
from submarine.pipeline.abstractDataExecutor import dataExecutor

import logging
logger = logging.getLogger(__name__)


class pandasExecutor(dataExecutor):
    def readDataSet(self, source_url):
        _, file_extension = splitext(source_url)
        if file_extension == CSV:
            dataframe = pd.read_csv(source_url)
            columns = dataframe.columns
            return dataframe, columns

    def concatenate(self, train_df, valid_df, test_df):
        concatenated_df = pd.concat([train_df, valid_df, test_df], ignore_index=0)
        return concatenated_df

    def split(self, dataframe, partition):
        if len(partition) != 3:
            raise PreprocessingException("Partition size should equal 3")
        if (partition[0] + partition[1] + partition[2]) != 1:
            raise PreprocessingException("Partition sum should equal 1")

        data_len = dataframe.shape[0]
        train_len = int(data_len*partition[0])
        valid_len = int(data_len*partition[1])

        train = dataframe.iloc[:train_len, ]
        valid = dataframe.iloc[train_len:(train_len + valid_len), ]
        test = dataframe.iloc[(train_len + valid_len):-1, ]
        return train, valid, test

    def handle_missing_values(self, dataframe, feature, strategy=FILL_WITH_CONST):
        if strategy == FILL_WITH_CONST:
            if dataframe[feature].dtype == 'object':
                dataframe[feature].fillna(value='', inplace=True)
            else:
                dataframe[feature].fillna(value=0, inplace=True)

        return dataframe

    def label_encoder(self, dataframe, feature):
        labelencoder = preprocessing.LabelEncoder()
        labelencoder.fit(dataframe[feature])
        dataframe[feature] = labelencoder.transform(dataframe[feature])
        return dataframe

    def where(self, dataframe, condition, x, y):
        return dataframe.where(condition, x, y)

    def greater(self, x, y):
        return x.gt(y)

    def multiply(self, x, y):
        return x.multiply(y)
