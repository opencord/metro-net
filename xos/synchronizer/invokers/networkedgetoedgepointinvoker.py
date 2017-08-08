
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
from services.metronetwork.models import NetworkEdgePort


class NetworkEdgeToEdgePointInvoker(Invoker):
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
        # src and dst fields
        if hasattr(obj, 'uni1_createbuffer'):
            uni1port = NetworkEdgePort.objects.get(pid=obj.uni1_createbuffer)
            uni2port = NetworkEdgePort.objects.get(pid=obj.uni2_createbuffer)
            obj.uni1 = uni1port
            obj.uni2 = uni2port

    # Method for handline post save semantics
    #      content here would be model specific but could include handling Many-to-Many relationship
    #      creation - which must occur post save
    #
    # obj     - Whatever obj was just saved
    # returns - N/A - this is a pure invoke() call
    #
    def postsave(self, obj):
        pass
