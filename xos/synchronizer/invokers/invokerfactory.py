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
