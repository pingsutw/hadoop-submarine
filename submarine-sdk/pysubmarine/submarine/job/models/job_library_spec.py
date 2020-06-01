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

# coding: utf-8

"""
    Submarine Experiment API

    The Submarine REST API allows you to create, list, and get experiments. TheAPI is hosted under the /v1/jobs route on the Submarine server. For example,to list experiments on a server hosted at http://localhost:8080, accesshttp://localhost:8080/api/v1/jobs/  # noqa: E501

    The version of the OpenAPI document: 0.4.0-SNAPSHOT
    Contact: submarine-dev@submarine.apache.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from submarine.job.configuration import Configuration


class JobLibrarySpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'version': 'str',
        'image': 'str',
        'cmd': 'str',
        'env_vars': 'dict(str, str)'
    }

    attribute_map = {
        'name': 'name',
        'version': 'version',
        'image': 'image',
        'cmd': 'cmd',
        'env_vars': 'envVars'
    }

    def __init__(self, name=None, version=None, image=None, cmd=None, env_vars=None, local_vars_configuration=None):  # noqa: E501
        """JobLibrarySpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._version = None
        self._image = None
        self._cmd = None
        self._env_vars = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if version is not None:
            self.version = version
        if image is not None:
            self.image = image
        if cmd is not None:
            self.cmd = cmd
        if env_vars is not None:
            self.env_vars = env_vars

    @property
    def name(self):
        """Gets the name of this JobLibrarySpec.  # noqa: E501


        :return: The name of this JobLibrarySpec.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this JobLibrarySpec.


        :param name: The name of this JobLibrarySpec.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def version(self):
        """Gets the version of this JobLibrarySpec.  # noqa: E501


        :return: The version of this JobLibrarySpec.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this JobLibrarySpec.


        :param version: The version of this JobLibrarySpec.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def image(self):
        """Gets the image of this JobLibrarySpec.  # noqa: E501


        :return: The image of this JobLibrarySpec.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this JobLibrarySpec.


        :param image: The image of this JobLibrarySpec.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def cmd(self):
        """Gets the cmd of this JobLibrarySpec.  # noqa: E501


        :return: The cmd of this JobLibrarySpec.  # noqa: E501
        :rtype: str
        """
        return self._cmd

    @cmd.setter
    def cmd(self, cmd):
        """Sets the cmd of this JobLibrarySpec.


        :param cmd: The cmd of this JobLibrarySpec.  # noqa: E501
        :type: str
        """

        self._cmd = cmd

    @property
    def env_vars(self):
        """Gets the env_vars of this JobLibrarySpec.  # noqa: E501


        :return: The env_vars of this JobLibrarySpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._env_vars

    @env_vars.setter
    def env_vars(self, env_vars):
        """Sets the env_vars of this JobLibrarySpec.


        :param env_vars: The env_vars of this JobLibrarySpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._env_vars = env_vars

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, JobLibrarySpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobLibrarySpec):
            return True

        return self.to_dict() != other.to_dict()
