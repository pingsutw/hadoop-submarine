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

from submarine.client.params import Localization


def _check(localization, remote_uri, local_path, mount_permission):
    assert type(localization) == Localization
    assert localization.remote_uri == remote_uri
    assert localization.local_path == local_path
    assert localization.mount_permission == mount_permission


def test_createLocalization():
    remote_uri = "hdfs:///user/yarn/submarine"
    local_uri = "./"
    mount_permission = "rw"

    localization = Localization(remote_uri, local_uri, mount_permission,)
    _check(localization, remote_uri, local_uri, mount_permission)
