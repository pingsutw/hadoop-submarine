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

from submarine.proto.SubmarineServerProtocol_pb2 import ResourceProto


class Resource:
    def __init__(self, vcores=2, memory=2048, gpu=0):
        self._vcores = vcores
        self._memory = memory
        self._gpu = gpu

    @property
    def vcores(self):
        """number of cpu in a task."""
        return self._vcores

    @property
    def memory(self):
        """number of memory in a task."""
        return self._memory

    @property
    def gpu(self):
        """number if gpu in a task"""
        return self._gpu

    def to_proto(self):
        resource_map = {'vcores': self.vcores,
                        'memory-mb': self.memory}
        if self.gpu > 0:
            resource_map.update({'yarn.io/gpu': self.gpu})

        return ResourceProto(resource_map=resource_map)
