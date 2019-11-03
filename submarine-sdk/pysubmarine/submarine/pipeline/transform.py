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

logger = logging.getLogger(__name__)


def handle_missing_values(data_all, features, missing_strategy='FILL_WITH_CONST'):
    if features is None:
        raise PreprocessingException("features must have a value")
    for feature in features:
        if missing_strategy == 'FILL_WITH_CONST':
            data_all[feature].fillna(value=0, inplace=True)

    return data_all


def labelEncoder(data_all, features):
    le = preprocessing.LabelEncoder()
    for feature in features:
        le.fit(data_all[feature])
        data_all[feature] = le.transform(data_all[feature])
    return data_all
