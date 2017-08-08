
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys

from synchronizers.metronetwork.providers.metronetworktestprovider import MetroNetworkTestProvider
from synchronizers.metronetwork.providers.metronetworkrestprovider import MetroNetworkRestProvider


class ProviderFactory(object):
    @staticmethod
    def getprovider(networkdevice):

        undertest = False

        # We either return Test or Rest
        # By convention a NetworkDevice with name TestDomain will use test objects
        if networkdevice.id == 'TestMetroNet' or networkdevice.id == 'TestCORD1Net' or networkdevice.id == 'TestCORD2Net':
            undertest = True

        if undertest:
            return MetroNetworkTestProvider(networkdevice)
        else:
            return MetroNetworkRestProvider(networkdevice)
