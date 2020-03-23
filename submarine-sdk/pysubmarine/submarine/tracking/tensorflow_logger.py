# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import submarine
import gorilla
# pylint: disable=E0611
import tensorflow
from tensorflow.python.summary.writer.event_file_writer import EventFileWriter

_metric_queue = []
settings = gorilla.Settings(allow_hit=True, store_hit=True)

logger = logging.getLogger(__name__)


def _log_event(event):
    """
    Extracts metric information from the event protobuf
    """
    if event.WhichOneof('what') == 'summary':
        summary = event.summary
        for v in summary.value:
            if v.HasField('simple_value'):
                submarine.log_metric(key=v.tag, value=v.simple_value, step=event.step,
                                     worker_index="local")


@gorilla.patch(EventFileWriter, settings=settings)
def add_event(self, *args):
    _log_event(*args)
    original = gorilla.get_original_attribute(EventFileWriter, 'add_event')

    return original(self, *args)

# @gorilla.patch(tensorflow.estimator.Estimator, settings=settings)
# def train(self, *args, **kwargs):
#     original = gorilla.get_original_attribute(tensorflow.estimator.Estimator, 'train')
#     # Checking step and max_step parameters for logging
#     if len(args) >= 3:
#         submarine.log_param('steps', args[2], 'local')
#         if len(args) >= 4:
#             submarine.log_param('max_steps', args[3], 'local')
#     if 'steps' in kwargs:
#         submarine.log_param('steps', kwargs['steps'], 'local')
#     if 'max_steps' in kwargs:
#         submarine.log_param('max_steps', kwargs['max_steps'], 'local')
#
#     return original(self, *args, **kwargs)
