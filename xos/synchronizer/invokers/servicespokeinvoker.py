import json
from synchronizers.metronetwork.invokers.invoker import Invoker
from core.models import Site
from services.metronetwork.models import RemotePort


class ServiceSpokeInvoker(Invoker):
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
        if hasattr(obj, 'sitename'):
            site = Site.objects.get(login_base=obj.sitename)
            obj.vnodlocalsite = site

        if hasattr(obj, 'remoteportname'):
            remoteport = RemotePort.objects.get(name=obj.remoteportname)
            obj.vnodlocalport = remoteport

    # Method for handline post save semantics
    #      content here would be model specific but could include handling Many-to-Many relationship
    #      creation - which must occur post save
    #
    # obj     - Whatever obj was just saved
    # returns - N/A - this is a pure invoke() call
    #
    def postsave(self, obj):
        pass