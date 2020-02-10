#!/usr/bin/env bash
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

set -ex

PROTOS="../../submarine-commons/commons-rpc/src/main/proto/"
python -m grpc_tools.protoc -I../../submarine-commons/commons-rpc/src/main/proto/ --python_out=./submarine/proto --grpc_python_out=./submarine/proto ../../submarine-commons/commons-rpc/src/main/proto/SubmarineServerProtocol.proto

OLD_IMPORT="import SubmarineServerProtocol_pb2 as SubmarineServerProtocol__pb2"
NEW_IMPORT="import submarine.proto.SubmarineServerProtocol_pb2 as SubmarineServerProtocol__pb2"
sed -i -e "s/${OLD_IMPORT}/${NEW_IMPORT}/g" "submarine/proto/SubmarineServerProtocol_pb2_grpc.py"

