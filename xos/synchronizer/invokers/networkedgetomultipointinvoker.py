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
        scratchpad = json.loads(obj.eps_createbuffer)
        eps = scratchpad['eps']

        for ep in eps:
            port = NetworkEdgePort.objects.get(pid=ep)
            obj.eps.add(port)
