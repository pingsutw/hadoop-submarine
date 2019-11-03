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
logger = logging.getLogger(__name__)


def split_df(dataframe, partition):
    # df = pd.read_csv(input_path, header=header)
    if len(partition) != 3:
        raise PreprocessingException("Partition size should equal 3")
    if (partition[0] + partition[1] + partition[2]) != 1:
        raise PreprocessingException("Partition sum should equal 1")

    data_len = dataframe.shape[0]
    train_len = int(data_len*partition[0])
    valid_len = int(data_len*partition[1])

    data = {'train': dataframe.iloc[:train_len, ],
            'valid': dataframe.iloc[train_len:(train_len + valid_len), ],
            'test': dataframe.iloc[(train_len + valid_len):-1, ]}

    return data
