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

from submarine.pipeline.data import Data
from submarine.pipeline.model import Model
from submarine.pipeline.model_registry import classifier_model_registry

import tensorflow as tf
import pandas as pd
from submarine.constants import LOCAL
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

if __name__ == "__main__":
    print("Tensorflow version :", tf.version.VERSION)

    # Data ingestion
    taxi_data = Data(source_url="data/taxi_data/data.csv", data_type="pandas", runtime="LOCAL")

    # Data Transform
    taxi_data.handle_missing_values(taxi_data.columns, 'FILL_WITH_CONST')
    taxi_data.label_encoder(['company', 'payment_type'])
    taxi_data['tips'] = Data.greater(taxi_data['tips'], Data.multiply(taxi_data['fare'], 0.2))
    taxi_data.split([0.6, 0.2, 0.2])  # [train, valid, test]

    # TODO: Visualize data

    # Training
    features = taxi_data.columns.drop('tips')
    label_feature = 'tips'
    xgboost = Model(model='DNN_keras', runtime='local', data=taxi_data,
                    registry=classifier_model_registry, feature=features, label_feature=label_feature)
    xgboost.train()

    # Evaluate
    loss, acc = xgboost.evaluate()
    print("Xgboost accuracy :", acc)
