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

import grpc

from submarine.proto.SubmarineServerProtocol_pb2 import ParameterProto, RunParameterProto,\
    TensorFlowRunJobParameterProto, PyTorchRunJobParameterProto
from submarine.proto.SubmarineServerProtocol_pb2_grpc import SubmarineServerProtocolStub
from submarine.client.params import createEmptyRole
from submarine.exceptions import SubmarineException

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host, port, security_disabled=True, keytab=None, principal=None,
                 distribute_keytab=None, queue=None):
        """
         API Client for Submarine
        :param host: host name or ip of submarine server
        :param port: port of submarine server
        """
        self.host = host
        self.port = port
        self.security_disabled = security_disabled
        self.keytab = keytab
        self.principal = principal
        self.distribute_keytab = distribute_keytab
        self.queue = queue

    def submitJob(self, name, workers, ps=None, tensorboard=None, tensorboard_enabled=False,
                  localizations=None, framework='tensorflow', conf=None):

        runParameter = RunParameterProto(
            name=name, localizations=[loc.to_proto() for loc in [localizations] if loc],
            conf_pairs=conf, worker_parameter=workers.to_proto(),
            security_disabled=self.security_disabled,
            keytab=self.keytab, principal=self.principal, distribute_keytab=self.distribute_keytab)

        if framework.lower() == 'tensorflow':
            if tensorboard is None:
                tensorboard = createEmptyRole("tensorboard")
            tfRunJobParameter = TensorFlowRunJobParameterProto(
                run_parameter_proto=runParameter, ps_parameter=ps.to_proto(),
                tensorboard_enabled=tensorboard_enabled,
                tensor_board_parameter=tensorboard.to_proto())
            parameter = ParameterProto(
                framework=framework, tensorflow_run_job_parameter=tfRunJobParameter)
        elif framework.lower() == 'pytorch':
            pytorchParameter = PyTorchRunJobParameterProto(run_parameter_proto=runParameter)
            parameter = ParameterProto(
                framework=framework, pytorch_run_job_parameter=pytorchParameter)
        else:
            raise SubmarineException("submarine only support pytorch and tensorflow now!")

        with grpc.insecure_channel('{0}:{1}'.format(self.host, self.port)) as channel:
            stub = SubmarineServerProtocolStub(channel)
            response = stub.SubmitJob(parameter)
        app_id = response.application_id
        logging.info("Submarine job is submitted, the job id is %s", app_id)
        return app_id
