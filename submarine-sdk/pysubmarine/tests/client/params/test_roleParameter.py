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

from submarine.client.params import RoleParameter, Resource


def _check(roleParameter, role, replicas, resources,
           launch_command, docker_image):
    assert type(roleParameter) == RoleParameter
    assert roleParameter.role == role
    assert roleParameter.replicas == replicas
    assert roleParameter.resources == resources
    assert roleParameter.launch_command == launch_command
    assert roleParameter.docker_image == docker_image


def test_createRoleParameter():
    role = 'PS'
    replicas = 3
    resource = Resource(vcores=1, memory=2048, gpu=3)
    launch_command = "python mnist.py"
    docker_image = 'apache/submarine'

    roleParameter = RoleParameter(role=role, replicas=replicas, resources=resource,
                                  launch_command=launch_command, docker_image=docker_image)
    _check(roleParameter, role, replicas, resource, launch_command, docker_image)
