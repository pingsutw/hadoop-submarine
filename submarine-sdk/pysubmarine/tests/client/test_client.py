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

from mock import patch
from unittest.mock import ANY
import pytest
from submarine.client import Client

from submarine.exceptions import SubmarineException
from submarine.proto.SubmarineServerProtocol_pb2_grpc import SubmarineServerProtocolStub
from submarine.client.params import RoleParameter, Localization, Resource
import submarine.proto.SubmarineServerProtocol_pb2


def __init__(self, channel):
    def mocked_submit(params):
        class mocked_response:
            application_id = 'application-123456789'

        return mocked_response()

    self.SubmitJob = mocked_submit


# Submarine client parameters
host = 'submarine'
port = 8980
security_disabled = True
keytab = 'keytabPath'
principal = 'testPrincipal'
distribute_keytab = True
queue = 'submarine'
client = Client(host=host, port=port, security_disabled=security_disabled, keytab=keytab,
                principal=principal, distribute_keytab=distribute_keytab, queue=queue)

# Submarine job parameters
name = 'test_rpc'
docker_image = 'apache/submarine:latest'
launch_command = 'python mnist.py'


def test_client_initialize():
    assert client.host == host
    assert client.port == port
    assert client.security_disabled == security_disabled
    assert client.keytab == keytab
    assert client.principal == principal
    assert client.distribute_keytab == distribute_keytab
    assert client.queue == queue


@patch.object(SubmarineServerProtocolStub, '__init__', __init__)
def test_submit_tf_job(mocker):
    framework = 'tensorflow'
    Resources = Resource(vcores=4, memory=2048)

    # create worker spec
    workers = RoleParameter('worker', replicas=2, resources=Resources,
                            launch_command=launch_command, docker_image=docker_image)
    # create ps spec
    ps = RoleParameter('ps', replicas=1, resources=Resources,
                       launch_command=launch_command, docker_image=docker_image)
    # create tensorboard spec
    tensorboard = RoleParameter('tensorboard', replicas=1, resources=Resources,
                                docker_image=docker_image)

    localizations = Localization(
        remote_uri="hdfs:///user/yarn/submarine",
        local_path="./",
        mount_permission="rw")

    conf = ["tony.containers.envs=SKIP_HADOOP_PATH=true"]

    spyRunParameter = mocker.spy(submarine.client.client, 'RunParameterProto')
    spyParameter = mocker.spy(submarine.client.client, 'ParameterProto')
    spyTensorflowParameter = mocker.spy(submarine.client.client, 'TensorFlowRunJobParameterProto')

    client.submitJob(name=name, ps=ps, workers=workers, tensorboard=tensorboard,
                     tensorboard_enabled=True, localizations=localizations,
                     framework=framework, conf=conf)

    spyRunParameter.assert_called_with(
        name=name, localizations=[loc.to_proto() for loc in [localizations]], conf_pairs=conf,
        worker_parameter=workers.to_proto(), security_disabled=security_disabled,
        keytab=keytab, principal=principal, distribute_keytab=distribute_keytab)

    spyTensorflowParameter.assert_called_once_with(run_parameter_proto=ANY,
                                                   ps_parameter=ps.to_proto(),
                                                   tensorboard_enabled=True,
                                                   tensor_board_parameter=tensorboard.to_proto())

    spyParameter.assert_called_once_with(framework=framework, tensorflow_run_job_parameter=ANY)


@patch.object(SubmarineServerProtocolStub, '__init__', __init__)
def test_submit_tf_job_without_tensorboard(mocker):
    Resources = Resource(vcores=4, memory=2048)

    workers = RoleParameter('worker', replicas=2, resources=Resources,
                            launch_command=launch_command, docker_image=docker_image)
    ps = RoleParameter('ps', replicas=1, resources=Resources,
                       launch_command=launch_command, docker_image=docker_image)
    spyCreateEmptyRole = mocker.spy(submarine.client.client, 'createEmptyRole')

    client.submitJob(name=name, ps=ps, workers=workers, framework='tensorflow')
    spyCreateEmptyRole.assert_called_once()


@patch.object(SubmarineServerProtocolStub, '__init__', __init__)
def test_submit_pytorch_job(mocker):
    framework = 'pytorch'
    Resources = Resource(vcores=4, memory=2048)

    workers = RoleParameter('worker', replicas=2, resources=Resources,
                            launch_command=launch_command, docker_image=docker_image)

    localizations = Localization(
        remote_uri="hdfs:///user/yarn/submarine",
        local_path="./",
        mount_permission="rw")

    conf = ["tony.containers.envs=SKIP_HADOOP_PATH=true"]

    spyRunParameter = mocker.spy(submarine.client.client, 'RunParameterProto')
    spyParameter = mocker.spy(submarine.client.client, 'ParameterProto')
    spyPytorchParameter = mocker.spy(submarine.client.client, 'PyTorchRunJobParameterProto')

    client.submitJob(name=name, workers=workers, tensorboard_enabled=False,
                     localizations=localizations, framework=framework, conf=conf)

    spyRunParameter.assert_called_with(
        name=name, localizations=[loc.to_proto() for loc in [localizations]], conf_pairs=conf,
        worker_parameter=workers.to_proto(), security_disabled=security_disabled,
        keytab=keytab, principal=principal, distribute_keytab=distribute_keytab)

    spyPytorchParameter.assert_called_once_with(run_parameter_proto=ANY)
    spyParameter.assert_called_once_with(framework=framework, pytorch_run_job_parameter=ANY)


@patch.object(SubmarineServerProtocolStub, '__init__', __init__)
def test_submit_unsupported_framework_job(mocker):
    framework = 'caffe'
    Resources = Resource(vcores=4, memory=2048)
    workers = RoleParameter('worker', replicas=2, resources=Resources,
                            launch_command=launch_command, docker_image=docker_image)

    with pytest.raises(SubmarineException,
                       match="submarine only support pytorch and tensorflow now!"):
        client.submitJob(name=name, workers=workers, framework=framework)
