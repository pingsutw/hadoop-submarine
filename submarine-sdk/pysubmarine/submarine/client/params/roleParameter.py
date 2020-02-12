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

from submarine.proto.SubmarineServerProtocol_pb2 import RoleParameterProto
from submarine.client.params import Resource


class RoleParameter:
    def __init__(self, role, replicas=1, resources=Resource(2, 2048),
                 launch_command="", docker_image=None):
        """
        The entry spec of Job. It contains some which describe the info about the job task.
        """
        self._role = role.upper()
        self._replicas = replicas
        self._launch_command = launch_command
        self._docker_image = docker_image
        self._resources = resources

    @property
    def role(self):
        """name of task. e.g. ps, worker, master, evaluator"""
        return self._role

    @property
    def replicas(self):
        """number of tasks of the job"""
        return self._replicas

    @property
    def launch_command(self):
        """String name of the tag."""
        return self._launch_command

    @property
    def docker_image(self):
        """docker image of the job."""
        return self._docker_image

    @property
    def resources(self):
        return self._resources

    def to_proto(self):
        proto = RoleParameterProto(resource_proto=self.resources.to_proto())
        proto.role = self.role
        proto.replicas = self.replicas
        proto.launch_command = self.launch_command
        if self.docker_image is not None:
            proto.docker_image = self.docker_image
        return proto


def createEmptyRole(name):
    return RoleParameter(role=name, replicas=0)
