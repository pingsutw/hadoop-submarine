#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#!/usr/bin/env bash
###########################################################################################################
# NAME: buildAndDeploy.sh
#
# DESCRIPTION:
# This script will send the $PROJECT_NAME.zip generated after running `gradle dist` to `user`@`hostname`.
#
#
# INPUT:
# $1 - user
# $2 - hostname
#
#
# OUTPUT:
# $DEPLOY_LOG: log file that includes all tasks.
#
#
# ENVIRONMENT VARIABLES:
#
#
# NOTES:
# Run this script in tony-history-server/ folder.
#
#
# EXIT CODE:
# 0 - Success
# 1 - Cleaning step failed
# 2 - Bundling distribution zip step failed
# 3 - Copying to remote host failed
#
#
# CHANGELOG:
# OCT 24 2018 PHAT TRAN
# OCT 31 2018 PHAT TRAN - Added project name variable for copying task
# NOV 22 2018 PHAT TRAN - Added version variable for copying task
############################################################################################################
set -ex

DEPLOY_LOG=deploy.log
PROJECT_NAME=tony-history-server
VERSION=0.1.5

echo "Cleaning up old builds..." | tee $DEPLOY_LOG
../gradlew clean createPlayBinaryZipDist 2>&1 | tee -a $DEPLOY_LOG
echo | tee -a $DEPLOY_LOG

echo "Copying over to $1@$2..." | tee -a $DEPLOY_LOG
scp build/distributions/${PROJECT_NAME}-${VERSION}.zip $1@$2: 2>&1 | tee -a $DEPLOY_LOG
echo | tee -a $DEPLOY_LOG

echo "Deployed to $1@$2!" | tee -a $DEPLOY_LOG