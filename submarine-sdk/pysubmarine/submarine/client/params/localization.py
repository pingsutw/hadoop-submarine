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

from submarine.proto.SubmarineServerProtocol_pb2 import LocalizationProto


class Localization:
    def __init__(self, remote_uri, local_path='./', mount_permission='rw'):
        """
        Specify localization to make remote/local file/directory available
        to all container(Docker). (ro permission is not supported yet)
        :param remote_uri:
        :param local_path: Path to the directory of files to write in submarine containers
        :param mount_permission:
        """
        self._remote_uri = remote_uri
        self._local_path = local_path
        self._mount_permission = mount_permission

    @property
    def remote_uri(self):
        """The RemoteUri can be a file or directory in local or HDFS or s3 or abfs or http"""
        return self._remote_uri

    @property
    def local_path(self):
        """Path to the directory of files to write in submarine containers"""
        return self._local_path

    @property
    def mount_permission(self):
        """permission of file/directory."""
        return self._mount_permission

    def to_proto(self):
        proto = LocalizationProto()
        proto.remote_uri = self.remote_uri
        proto.local_path = self.local_path
        proto.mount_permission = self.mount_permission
        return proto
