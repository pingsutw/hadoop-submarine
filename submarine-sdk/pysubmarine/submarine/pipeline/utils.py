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

import os
import pandas as pd
from os.path import basename, splitext, abspath
import tensorflow as tf

from submarine.constants import TENSORFLOW, PANDAS, CSV


def get_from_registry(key, registry):
    if hasattr(key, 'upper'):
        key = key.upper()
    if key in registry:
        return registry[key]
    else:
        raise ValueError(
            'Key {} not supported, available options: {}'.format(
                key, registry.keys()
            )
        )


def readDataSet(data_type, source_url):
    _, fileExtension = splitext(source_url)
    if data_type == PANDAS:
        if fileExtension == CSV:
            data_set = pd.read_csv(source_url)
            columns = data_set.columns
            return data_set, columns
    elif data_type == TENSORFLOW:
        if fileExtension == CSV:
            data_set = tf.keras.utils.get_file("data.csv", 'file://' + abspath(source_url))
            return data_set, None
    return None, None
