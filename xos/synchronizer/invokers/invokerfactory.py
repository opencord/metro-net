
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


from services.metronetwork.models import *
from synchronizers.metronetwork.invokers.networkmultipointtomultipointinvoker import NetworkMultipointToMultipointInvoker
from synchronizers.metronetwork.invokers.networkedgetoedgepointinvoker import NetworkEdgeToEdgePointInvoker
from synchronizers.metronetwork.invokers.networkedgetomultipointinvoker import NetworkEdgeToMultipointInvoker
from synchronizers.metronetwork.invokers.servicespokeinvoker import ServiceSpokeInvoker
from synchronizers.metronetwork.invokers.vnodglobalserviceinvoker import VnodGlobalServiceInvoker
from synchronizers.metronetwork.invokers.remoteportinvoker import RemotePortInvoker


class InvokerFactory(object):
    @staticmethod
    def getinvoker(obj):
        #
        # Here is where we build various invokers
        #
        if isinstance(obj, NetworkMultipointToMultipointConnection):
            return NetworkMultipointToMultipointInvoker()
        elif isinstance(obj, NetworkEdgeToEdgePointConnection):
            return NetworkEdgeToEdgePointInvoker()
        elif isinstance(obj, NetworkEdgeToMultipointConnection):
            return NetworkEdgeToMultipointInvoker()
        elif isinstance(obj, ServiceSpoke):
            return ServiceSpokeInvoker()
        elif isinstance(obj, VnodGlobalService):
            return VnodGlobalServiceInvoker()
        elif isinstance(obj, RemotePort):
            return RemotePortInvoker()
        else:
            return None
