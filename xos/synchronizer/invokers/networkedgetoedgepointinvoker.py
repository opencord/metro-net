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
