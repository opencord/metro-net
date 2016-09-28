from services.metronetwork.models import *
from synchronizers.metronetwork.invokers.networkmultipointtomultipointinvoker import NetworkMultipointToMultipointInvoker
from synchronizers.metronetwork.invokers.networkedgetoedgepointinvoker import NetworkEdgeToEdgePointInvoker
from synchronizers.metronetwork.invokers.networkedgetomultipointinvoker import NetworkEdgeToMultipointInvoker


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
        else:
            return None
