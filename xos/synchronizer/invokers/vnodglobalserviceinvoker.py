import json
from synchronizers.metronetwork.invokers.invoker import Invoker
from services.metronetwork.models import ServiceSpoke
from services.metronetwork.models import BandwidthProfile
from services.metronetwork.models import NetworkEdgeToEdgePointConnection

class VnodGlobalServiceInvoker(Invoker):

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

        if hasattr(obj, 'bwpname'):
            bwprofile = BandwidthProfile.objects.get(name=obj.bwpname)
            obj.bandwidthProfile = bwprofile

        if hasattr(obj, 'pointtopointsid'):
            connection = NetworkEdgeToEdgePointConnection.objects.get(sid=obj.pointtopointsid)
            obj.metronetworkpointtopoint = connection

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
        if hasattr(obj, 'spokes_createbuffer'):
            scratchpad = json.loads(obj.spokes_createbuffer)
            spokes = scratchpad['spokes']

            for spokeid in spokes:
                spoke = ServiceSpoke.objects.get(name=spokeid)
                obj.spokes.add(spoke)
