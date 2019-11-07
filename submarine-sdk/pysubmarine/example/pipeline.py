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

from submarine.pipeline.dataManager import DataManager
from submarine.pipeline.modelManager import ModelManager
from submarine.pipeline.model_registry import classifier_model_registry

import tensorflow as tf
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

if __name__ == "__main__":
    print("Tensorflow version :", tf.version.VERSION)

    # Data ingestion
    dataManager = DataManager(source_url="data/taxi_data/data.csv", data_type="pandas", runtime="LOCAL")
    # Data Transform
    dataManager.handle_missing_values(dataManager.data_set.columns, 'FILL_WITH_CONST')
    dataManager.label_encoder(['company', 'payment_type'])
    dataManager.data_set['tips'] = dataManager.greater(
        dataManager.data_set['tips'], dataManager.multiply(dataManager.data_set['fare'], 0.2))
    dataManager.splitData([0.6, 0.2, 0.2])  # [train, valid, test]

    # TODO: Visualize data

    # Training
    features = dataManager.data_set.columns.drop('tips')
    label_feature = 'tips'
    modelManager = ModelManager(model='xgboost', runtime='local',
                                training_data=dataManager.training_set, validation_data=dataManager.valid_set,
                                registry=classifier_model_registry, feature=features, label_feature=label_feature)
    modelManager.train()

    # Evaluate
    loss, acc = modelManager.evaluate()
    print("Xgboost accuracy :", acc)
