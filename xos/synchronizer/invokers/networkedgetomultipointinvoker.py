
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


import json
from synchronizers.metronetwork.invokers.invoker import Invoker
from services.metronetwork.models import NetworkEdgeToMultipointConnection, NetworkEdgePort

class NetworkEdgeToMultipointInvoker(Invoker):

    def __init__(self, **args):
        pass

    # Method for handline pre save semantics
    #      content here would be model specific but could include handling Many-to-Many relationship
    #      creation - which must occur post save
    #
    # obj     - Whatever obj was just saved
    # returns - None - this is a pure invoke() call, return type is None
    #
    def presave(self, obj):
        # Now that the Ports are created - get a proper reference to them and update the
        # root field
        if hasattr(obj, 'root_createbuffer'):
            rootEdgePort = NetworkEdgePort.objects.get(pid=obj.root_createbuffer)
            obj.root = rootEdgePort


    # Method for handline post save semantics
    #      content here would be model specific but could include handling Many-to-Many relationship
    #      creation - which must occur post save
    #
    # obj     - Whatever obj was just saved
    # returns - N/A - this is a pure invoke() call
    #
    def postsave(self, obj):
        #
        # Ok - we need to handle the multipoint many-to-many relationships in here
        #
        # By design convnetion we will look for them in the 'backend_register' object field
        # this is a json field that is general purpose - we will expect to find a JSON array
        # called 'eps' that just containts a reference to a bunch of NetworkEdgePorts
        #
        #
        if hasattr(obj, 'eps_createbuffer'):
            scratchpad = json.loads(obj.eps_createbuffer)
            eps = scratchpad['eps']

            for ep in eps:
                port = NetworkEdgePort.objects.get(pid=ep)
                obj.eps.add(port)
