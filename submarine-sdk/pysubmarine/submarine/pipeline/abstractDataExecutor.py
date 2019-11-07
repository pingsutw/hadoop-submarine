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

from abc import abstractmethod, ABC
from submarine.constants import FILL_WITH_CONST


class dataExecutor(ABC):
    @abstractmethod
    def readDataSet(self, source_url):
        pass

    @abstractmethod
    def concatenate(self, train_df, valid_df, test_df):
        pass

    @abstractmethod
    def split(self, dataframe, partition):
        pass

    @abstractmethod
    def handle_missing_values(self, dataframe, feature, strategy=FILL_WITH_CONST):
        pass

    @abstractmethod
    def label_encoder(self, dataframe, feature):
        pass

    @abstractmethod
    def where(self, dataframe, condition, x, y):
        pass

    @abstractmethod
    def greater(self, x, y):
        pass

    @abstractmethod
    def multiply(self, x, y):
        pass
