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


from submarine.constants import FILL_WITH_CONST
from submarine.pipeline.abstractDataExecutor import dataExecutor
from pyspark.sql import SparkSession


def get_dtype(dataframe, column):
    return [dtype for name, dtype in dataframe if name == column][0]


class sparkExecutor(dataExecutor):
    def __init__(self):
        self.spark = SparkSession.builder.master("local").appName("spark_test").getOrCreate()

    def readDataSet(self, source_url):
        dataframe = self.spark.read.csv("data.csv", header=True)
        columns = dataframe.columns
        return dataframe, columns

    def concatenate(self, train_df, valid_df, test_df):
        pass

    def split(self, dataframe, partition):
        pass

    def handle_missing_values(self, dataframe, feature, strategy=FILL_WITH_CONST):
        if strategy == FILL_WITH_CONST:
            if get_dtype(dataframe, feature) == 'StringType':
                dataframe.na.fill({feature: ''})
            else:
                dataframe.na.fill({feature: 0})

        return dataframe

    def label_encoder(self, ata_all, feature):
        pass

    def where(self, data_all, condition, x, y):
        pass

    def greater(self, x, y):
        pass

    def multiply(self, x, y):
        pass
