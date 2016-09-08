import random

from xos.logger import Logger, logging
from services.metronetwork.models import *
from synchronizers.metronetwork.providers.metronetworkprovider import MetroNetworkProvider

logger = Logger(level=logging.INFO)


class MetroNetworkTestProvider(MetroNetworkProvider):
    def __init__(self, networkdevice, **args):
        MetroNetworkProvider.__init__(self, networkdevice, **args)

    # Method for retrieving all network ports from the backend system
    def get_network_ports(self):
        # Our Test Network Consists of 6 ports - two on each of three internal switches

        objs = []

        # For The Test Provider we don't handle re-sync for anything but the Metro Test Network
        if self.networkdevice.id != 'TestMetroNet':
            return objs

        # Ok - in the test class we cheat and create the adjunct NetworkDevices Devices
        device1 = NetworkDevice()
        device1.id = 'TestCORD1Net'
        device1.administrativeState = 'enabled'
        device1.restCtrlUrl = 'testCordPod1.onlab.net:8000'
        device1.username = 'karaf'
        device1.password = 'karaf'
        objs.append(device1)

        device2 = NetworkDevice()
        device2.id = 'TestCORD2Net'
        device2.administrativeState = 'enabled'
        device2.restCtrlUrl = 'testCordPod2.onlabl.net:8000'
        device2.username = 'karaf'
        device2.password = 'karaf'
        objs.append(device2)

        # Ok - here we go creating ports - its 4 ports for each CORD Pod and 2 for MetroNetwork

        # Metro Network Switch
        port1 = NetworkPort()
        port1.element = self.networkdevice
        port1.pid = self.networkdevice.id + "." + "of:000000001/1"
        objs.append(port1)

        port2 = NetworkPort()
        port2.element = self.networkdevice
        port2.pid = self.networkdevice.id + "." + "of:000000001/2"
        objs.append(port2)

        # CORD POD1
        cordpod1device = NetworkDevice()
        cordpod1device.id = 'TestCORD1Net'

        port3 = NetworkEdgePort()
        port3.element = cordpod1device
        port3.pid = cordpod1device.id + "." + "of:000000001/1"
        port3.bwpCfgCbs = 1000000
        port3.bwpCfgEbs = 1000000
        port3.bwpCfgEir = 1000000
        port3.bwpCfgCir = 1000000
        port3.bwpCfgCir = 1000000
        objs.append(port3)

        port4 = NetworkPort()
        port4.element = cordpod1device
        port4.pid = cordpod1device.id + "." + "of:000000001/2"
        objs.append(port4)

        # Internal Switch 3
        port5 = NetworkEdgePort()
        port5.element = cordpod1device
        port5.pid = cordpod1device.id + "." + "of:000000001/3"
        port5.bwpCfgCbs = 1000000
        port5.bwpCfgEbs = 1000000
        port5.bwpCfgEir = 1000000
        port5.bwpCfgCir = 1000000
        port5.bwpCfgCir = 1000000
        objs.append(port5)

        port6 = NetworkPort()
        port6.element = cordpod1device
        port6.capacity = 1000000000
        port6.usedCapacity = 1000000000
        port6.pid = cordpod1device.id + "." + "of:000000001/4"
        objs.append(port6)

        # CORD POD2
        cordpod2device = NetworkDevice()
        cordpod2device.id = 'TestCORD2Net'

        port7 = NetworkEdgePort()
        port7.element = cordpod2device
        port7.pid = cordpod2device.id + "." + "of:000000001/1"
        port7.bwpCfgCbs = 1000000
        port7.bwpCfgEbs = 1000000
        port7.bwpCfgEir = 1000000
        port7.bwpCfgCir = 1000000
        port7.bwpCfgCir = 1000000
        objs.append(port7)

        port8 = NetworkPort()
        port8.element = cordpod2device
        port8.pid = cordpod2device.id + "." + "of:000000001/2"
        objs.append(port8)

        # Internal Switch 3
        port9 = NetworkEdgePort()
        port9.element = cordpod2device
        port9.pid = cordpod2device.id + "." + "of:000000001/3"
        port9.bwpCfgCbs = 1000000
        port9.bwpCfgEbs = 1000000
        port9.bwpCfgEir = 1000000
        port9.bwpCfgCir = 1000000
        port9.bwpCfgCir = 1000000
        objs.append(port9)

        port10 = NetworkPort()
        port10.element = cordpod2device
        port10.pid = cordpod2device.id + "." + "of:000000001/4"
        objs.append(port10)

        return objs

    def get_network_ports_for_deletion(self):

        objs = []

        # For The Test Provider we don't handle re-sync for anything but the Metro Test Network
        if self.networkdevice.id != 'TestMetroNet':
            return objs

        allports = MetroNetworkProvider.get_network_ports_for_deletion(self)

        for port in allports:
            objs.append(port)

        # Ok - in the test class we cheat and take down the adjunct Fake NetworkDevices Devices
        device1 = NetworkDevice()
        device1.id = 'TestCORD1Net'
        objs.append(device1)

        device2 = NetworkDevice()
        device2.id = 'TestCORD2Net'
        objs.append(device2)

        return objs

    def get_network_links(self):

        objs = []

        # Metro Link Connectivity object - Point to Point
        metronetconnectivity = NetworkPointToPointConnection()
        port1 = NetworkPort()
        port1.pid = self.networkdevice.id + "." + "of:000000001/1"
        port2 = NetworkPort()
        port2.pid = self.networkdevice.id + "." + "of:000000001/2"
        metronetconnectivity.src = port1
        metronetconnectivity.dest = port2
        metronetconnectivity.type = 'direct'
        metronetconnectivity.operstate = 'active'
        metronetconnectivity.adminstate = 'enabled'
        metronetconnectivity.sid = 'MetroNetworkPointToPointConnectivity_1'
        objs.append(metronetconnectivity)

        # CORDPOD1 Connectivity object - Point to Point
        cordpod1device = NetworkDevice()
        cordpod1device.id = 'TestCORD1Net'

        cordpod1connectivity = NetworkPointToPointConnection()
        port6 = NetworkPort()
        port6.pid = cordpod1device.id + "." + "of:000000001/4"
        port4 = NetworkPort()
        port4.pid = cordpod1device.id + "." + "of:000000001/2"
        cordpod1connectivity.src = port6
        cordpod1connectivity.dest = port4
        cordpod1connectivity.type = 'direct'
        cordpod1connectivity.operstate = 'active'
        cordpod1connectivity.adminstate = 'enabled'
        cordpod1connectivity.sid = 'CordPod1PointToPointConnectivity_1'
        objs.append(cordpod1connectivity)

        # CORDPOD2 Connectivity object - Point to Point
        cordpod2device = NetworkDevice()
        cordpod2device.id = 'TestCORD2Net'

        cordpod2connectivity = NetworkPointToPointConnection()
        port8 = NetworkPort()
        port8.pid = cordpod2device.id + "." + "of:000000001/2"
        port10 = NetworkPort()
        port10.pid = cordpod2device.id + "." + "of:000000001/4"
        cordpod2connectivity.src = port10
        cordpod2connectivity.dest = port8
        cordpod2connectivity.type = 'direct'
        cordpod2connectivity.operstate = 'active'
        cordpod2connectivity.adminstate = 'enabled'
        cordpod2connectivity.sid = 'CordPod2PointToPointConnectivity_1'
        objs.append(cordpod2connectivity)

        # InterLink object between CORDPOD1 and MetroNet
        interlink1 = NetworkInterLink()
        interlink1.src = port1
        interlink1.dest = port6
        interlink1.state = 'active'
        objs.append(interlink1)

        # InterLink object between CORDPOD2 and MetroNet
        interlink2 = NetworkInterLink()
        interlink2.src = port2
        interlink2.dest = port10
        interlink2.state = 'active'
        objs.append(interlink2)

        # Edge to Edge Point Connectivity Objects
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection()
        port3 = NetworkEdgePort()
        port3.pid = cordpod1device.id + "." + "of:000000001/1"
        port7 = NetworkEdgePort()
        port7.pid = cordpod2device.id + "." + "of:000000001/1"
        edgetoedgeconnectivity.uni1 = port3
        edgetoedgeconnectivity.uni2 = port7
        edgetoedgeconnectivity.type = 'direct'
        edgetoedgeconnectivity.operstate = 'active'
        edgetoedgeconnectivity.adminstate = 'enabled'
        edgetoedgeconnectivity.sid = 'EdgePointToEdgePointConnectivity_1'
        objs.append(edgetoedgeconnectivity)

        return objs

    def get_network_links_for_deletion(self):

        # For now we'll rely on cascade deletes in the port area - so from the test provider nothing to do
        objs = []
        return objs

    def create_point_to_point_connectivity(self, obj):

        # Ok - here is what we'll do to simulate the 'real world' - get a random number between 1 and 10
        # 1-7 is considered 'successful' 8 is considered a transient error - 9 is a configuration problem
        # 10 is a - resource exhausted problem - there you go!!
        scenario = random.randint(1, 10)

        if (scenario >= 1 and scenario <= 7):
            obj.adminstate = 'enabled'
            obj.operstate = 'active'
            return True
        elif (scenario == 8):
            obj.adminstate = 'enabled'
            obj.operstate = 'inactive'
            obj.backend_status = '8 - Transient Server Error'
            return False
        elif (scenario == 9):
            obj.adminstate = 'invalid'
            obj.operstate = 'inactive'
            obj.backend_status = '9 - Configuration Error'
            return False
        else:
            obj.adminstate = 'enabled'
            obj.operstate = 'inactive'
            obj.backend_status = '10 - Resource Exhaustion'
            return False

    def delete_point_to_point_connectivity(self, obj):

        # Ok - here is what we'll do to simulate the 'real world' - get a random number between 1 and 10
        # 1-8 is considered 'successful' 8 is considered a transient error - 9 is a configuration problem
        scenario = random.randint(1, 10)

        if (scenario >= 1 and scenario <= 8):
            obj.adminstate = 'disabled'
            obj.operstate = 'inactive'
            return True
        elif (scenario == 9):
            obj.adminstate = 'disabled'
            obj.backend_status = '8 - Transient Server Error'
            return False
        else:
            obj.adminstate = 'invalid'
            obj.backend_status = '9 - Configuration Error'
            return False
