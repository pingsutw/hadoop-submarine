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

if __name__ == "__main__":
    data = pd.read_csv("data/taxi_data/data.csv")
    data_transformed = submarine.pipeline.transform.handle_missing_values(data, data.columns)
    data = submarine.pipeline.split.split_df(data_transformed, [0.5, 0.2, 0.3])

    print(data['valid'].isnull().sum()[data['valid'].isnull().sum() > 0])
    # print(data['fare'].dtype)
    # data = submarine.pipeline.split.split_df(df, [0.5, 0.2, 0.3])


    #print(data['train'].dtypes)

