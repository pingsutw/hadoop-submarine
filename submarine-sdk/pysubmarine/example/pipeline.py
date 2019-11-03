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

import submarine.pipeline.split
import submarine.pipeline.transform
import pandas as pd
import tensorflow as tf
import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.externals import joblib


pd.set_option('display.max_columns', None)

if __name__ == "__main__":

    data = pd.read_csv("data/taxi_data/data.csv")
    data_transformed = submarine.pipeline.transform.handle_missing_values(data, data.columns)
    data_transformed['tips'] = np.where(data_transformed['fare'] * 0.2 < data_transformed['tips'], 1, 0)
    print("Number of company types :", len(data_transformed['company'].unique()))
    print("Number of payment types: ", len(data_transformed['payment_type'].unique()))
    data_transformed = submarine.pipeline.transform\
        .labelEncoder(data_transformed, ['company', 'payment_type'])
    # print(data_transformed['tips'].head())
    # print(data_transformed.head())
    # print(data_transformed.describe())
    data = submarine.pipeline.split.split_df(data_transformed, [0.5, 0.2, 0.3])
    x_train = data['train'].drop('tips', axis=1)
    y_train = data['train']['tips']

    # Training
    xg_cls = xgb.XGBClassifier(n_estimators=200, max_depth=50)
    xg_cls.fit(x_train, y_train)

    # Pusher
    model_file_name = 'model.pkl'
    model_columns_file_name = 'model_columns.pkl'
    model_columns = list(x_train.columns)
    joblib.dump(model_columns, model_columns_file_name)
    joblib.dump(xg_cls, model_file_name)

    # Evaluate
    x_test = data['test'].drop('tips', axis=1)
    y_test = data['test']['tips']
    # print(x_test.iloc[0, ].to_json())

    y_pred = xg_cls.predict(x_test)
    score = accuracy_score(y_test, y_pred)
    print("score :", score)
    print("class name :", type(xg_cls))

