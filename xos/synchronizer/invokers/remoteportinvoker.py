import json
from synchronizers.metronetwork.invokers.invoker import Invoker
from core.models import Site
from services.metronetwork.models import NetworkEdgePort

class RemotePortInvoker(Invoker):
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
        # Now that the Site and EdgePorts are created set the foreign keys
        if hasattr(obj, 'sitename'):
            site = Site.objects.get(login_base=obj.sitename)
            obj.remoteportsite = site

        if hasattr(obj, 'edgeportname'):
            edgeport = NetworkEdgePort.objects.get(pid=obj.edgeportname)
            obj.edgeport = edgeport

    # Method for handline post save semantics
    #      content here would be model specific but could include handling Many-to-Many relationship
    #      creation - which must occur post save
    #
    # obj     - Whatever obj was just saved
    # returns - N/A - this is a pure invoke() call
    #
    def postsave(self, obj):
        pass