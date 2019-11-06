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

import logging
from submarine.exceptions import PreprocessingException
from sklearn import preprocessing
import numpy as np
import pandas as pd
from submarine.constants import FILL_WITH_CONST

logger = logging.getLogger(__name__)


def df_handle_missing_values(data_all, feature, strategy=FILL_WITH_CONST):
    if feature is None:
        raise PreprocessingException("features must need a value")

    if strategy == FILL_WITH_CONST:
        if data_all[feature].dtype == 'object':
            data_all[feature].fillna(value='', inplace=True)
        else:
            data_all[feature].fillna(value=0, inplace=True)

    return data_all


def df_label_encoder(data_all, feature):
    labelencoder = preprocessing.LabelEncoder()
    labelencoder.fit(data_all[feature])
    data_all[feature] = labelencoder.transform(data_all[feature])
    return data_all


def df_where(data_all, condition, x, y):
    return data_all.where(condition, x, y)


def df_greater(x, y):
    return x.gt(y)


def df_multiply(x, y):
    return x.multiply(y)


def df_concatenate(train_df, valid_df, test_df):
    train_size = len(train_df)
    valid_size = len(valid_df) if valid_df is not None else 0
    test_size = len(test_df) if test_df is not None else 0
    concatenated_df = pd.concat([train_df, valid_df, test_df], ignore_index=True)
    split = np.array(
        [0] * train_size + [1] * valid_size + [2] * test_size,
        dtype=np.int8
    )
    concatenated_df = concatenated_df.assign(split=pd.Series(split).values)
    return concatenated_df
