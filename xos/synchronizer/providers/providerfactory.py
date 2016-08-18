import sys

from synchronizers.metronetwork.providers.metronetworktestprovider import MetroNetworkTestProvider
from synchronizers.metronetwork.providers.metronetworkrestprovider import MetroNetworkRestProvider


class ProviderFactory(object):
    @staticmethod
    def getprovider(networkdevice):

        undertest = False

        # We either return Test or Rest
        # By convention a NetworkDevice with name TestDomain will use test objects
        if networkdevice.id == 'TestMetroNet' or networkdevice.id == 'TestCORD1Net' or networkdevice.id == 'TestCORD2Net':
            undertest = True

        if undertest:
            return MetroNetworkTestProvider(networkdevice)
        else:
            return MetroNetworkRestProvider(networkdevice)
