import random
import json

from xos.logger import Logger, logging
from services.metronetwork.models import *
from synchronizers.metronetwork.providers.metronetworkprovider import MetroNetworkProvider

logger = Logger(level=logging.INFO)


class MetroNetworkTestProvider(MetroNetworkProvider):
    def __init__(self, networkdevice, **args):
        MetroNetworkProvider.__init__(self, networkdevice, **args)

    # Method for retrieving all network ports from the backend system
    def get_network_ports(self):
        #
        # Our Test Network Consists of three NetworkDevices (which correspond to ONOS instances):
        #
        #                    ONOS1-CORDPOD1
        #                    ONOS2-MetroNetwork
        #                    ONOW3-CORDPOD2
        #
        #
        #    Uni-NetworkEdgePort3--
        #    Uni-NetworkEdgePort11-
        #    Uni-NetworkEdgePort5--ONOS1-CORDPOD1-NetworkPort6
        #            NetworkPort4--                     |
        #                                        NetworkPort1-ONOS2-MetroNetwork
        #                                        NetworkPort2-
        #                                             |
        #    Uni-NetworkEdgePort7--ONOS3-CORDPOD2-NetworkPort10
        #    Uni-NetworkEdgePort9--
        #    Uni-NetworkEdgePort12-
        #        NetworkPort8--
        #
        #  Note: NetworkPorts can be endpoints of Interlinks and NetworkPointToPointConnections
        #              they can be seem as a simple port.
        #        NetworkEdgePorts are UNIs in the network, so are specicially user facing.
        #
        #
        # InterLinks - Port1 - Port6
        #              Port2 - Port10
        #
        # NetworkPointToPointConnections: Port1 - Port2
        #                                 Port4 - Port6
        #                                 Port8 - Port10
        #
        # NetworkEdgeToEdgePointConnections: Port3 - Port7
        #
        # NetworkMultipointConnection: Port11 - Port5 - Port9 - Port12

        objs = []

        # For The Test Provider we don't handle re-sync for anything but the Metro Test Network
        if self.networkdevice.id != 'TestMetroNet':
            return objs

        # Ok - in the test class we cheat and create one NetworkDevice with 8 NetworkEdgePorts
        device1 = NetworkDevice()
        device1.id = 'TestCORDNet'
        device1.administrativeState = 'enabled'
        device1.restCtrlUrl = 'testCordPod1.onlab.net:8000'
        device1.username = 'karaf'
        device1.password = 'karaf'
        objs.append(device1)

        port1 = NetworkEdgePort()
        port1.element = device1
        port1.pid = device1.id + "." + "of:000000001/1"
        port1.bwpCfgCbs = 1000000
        port1.bwpCfgEbs = 1000000
        port1.bwpCfgEir = 1000000
        port1.bwpCfgCir = 1000000
        port1.location = "San Francisco"
        port1.name = "Central Office 1"
        port1.latlng = "[-122.419416, 37.774929]"
        objs.append(port1)

        port2 = NetworkEdgePort()
        port2.element = device1
        port2.pid = device1.id + "." + "of:000000001/2"
        port2.bwpCfgCbs = 1000000
        port2.bwpCfgEbs = 1000000
        port2.bwpCfgEir = 1000000
        port2.bwpCfgCir = 1000000
        port2.location = "San Jose"
        port2.name = "Central Office 2"
        port2.latlng = "[-121.886329, 37.338208]"
        objs.append(port2)

        port3 = NetworkEdgePort()
        port3.element = device1
        port3.pid = device1.id + "." + "of:000000001/3"
        port3.bwpCfgCbs = 1000000
        port3.bwpCfgEbs = 1000000
        port3.bwpCfgEir = 1000000
        port3.bwpCfgCir = 1000000
        port3.location = "Palo Alto"
        port3.name = "Central Office 3"
        port3.latlng = "[-122.143019, 37.441883]"
        objs.append(port3)

        port4 = NetworkEdgePort()
        port4.element = device1
        port4.pid = device1.id + "." + "of:000000001/4"
        port4.bwpCfgCbs = 1000000
        port4.bwpCfgEbs = 1000000
        port4.bwpCfgEir = 1000000
        port4.bwpCfgCir = 1000000
        port4.location = "Oakland"
        port4.name = "Central Office 4"
        port4.latlng = "[-122.271114, 37.804364]"
        objs.append(port4)

        port5 = NetworkEdgePort()
        port5.element = device1
        port5.pid = device1.id + "." + "of:000000001/5"
        port5.bwpCfgCbs = 1000000
        port5.bwpCfgEbs = 1000000
        port5.bwpCfgEir = 1000000
        port5.bwpCfgCir = 1000000
        port5.location = "San Rafael"
        port5.name = "Central Office 5"
        port5.latlng = "[-122.531087, 37.973535]"
        objs.append(port5)

        port6 = NetworkEdgePort()
        port6.element = device1
        port6.pid = device1.id + "." + "of:000000001/6"
        port6.bwpCfgCbs = 1000000
        port6.bwpCfgEbs = 1000000
        port6.bwpCfgEir = 1000000
        port6.bwpCfgCir = 1000000
        port6.location = "San Mateo"
        port6.name = "Central Office 6"
        port6.latlng = "[-122.325525, 37.562992]"
        objs.append(port6)

        port7 = NetworkEdgePort()
        port7.element = device1
        port7.pid = device1.id + "." + "of:000000001/7"
        port7.bwpCfgCbs = 1000000
        port7.bwpCfgEbs = 1000000
        port7.bwpCfgEir = 1000000
        port7.bwpCfgCir = 1000000
        port7.location = "Hayward"
        port7.name = "Central Office 7"
        port7.latlng = "[-122.080796, 37.668821]"
        objs.append(port7)

        port8 = NetworkEdgePort()
        port8.element = device1
        port8.pid = device1.id + "." + "of:000000001/8"
        port8.bwpCfgCbs = 1000000
        port8.bwpCfgEbs = 1000000
        port8.bwpCfgEir = 1000000
        port8.bwpCfgCir = 1000000
        port8.location = "Fremont"
        port8.name = "Central Office 8"
        port8.latlng = "[-121.988572, 37.548270]"
        objs.append(port8)

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
        device1.id = 'TestCORDNet'
        objs.append(device1)

        return objs

    def get_network_links(self):

        objs = []

        # Connectivity object - Point to Point
        cordpod1device = NetworkDevice()
        cordpod1device.id = 'TestCORDNet'

        # Edge to Edge Point Connectivity Objects
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection()
        edgetoedgeconnectivity.uni1_createbuffer = cordpod1device.id + "." + "of:000000001/1"
        edgetoedgeconnectivity.uni2_createbuffer = cordpod1device.id + "." + "of:000000001/2"
        edgetoedgeconnectivity.type = 'direct'
        edgetoedgeconnectivity.operstate = 'active'
        edgetoedgeconnectivity.adminstate = 'enabled'
        edgetoedgeconnectivity.sid = 'EdgeToEdgePointConnectivity_1'
        objs.append(edgetoedgeconnectivity)


        # Multipoint to Multipoint Connectivity Objects
        multipoint2multipointconnectivity=NetworkMultipointToMultipointConnection()
        multipoint2multipointconnectivity.operstate = 'active'
        multipoint2multipointconnectivity.adminstate = 'enabled'
        multipoint2multipointconnectivity.type = 'ethernet'
        multipoint2multipointconnectivity.sid = 'MultipointToMultipointConnectivity_1'

        #
        # Create JSON array for post-save behaviour
        #
        eps = []
        eps.append(cordpod1device.id + "." + "of:000000001/3")
        eps.append(cordpod1device.id + "." + "of:000000001/4")
        eps.append(cordpod1device.id + "." + "of:000000001/5")

        myjsonstr = {'eps': eps, 'foo':0, 'bar':0}
        multipoint2multipointconnectivity.eps_createbuffer = json.dumps(myjsonstr)
        objs.append(multipoint2multipointconnectivity)

        # Edge to Multipoint Connectivity Objects
        edge2multipointconnectivity = NetworkEdgeToMultipointConnection()
        edge2multipointconnectivity.operstate = 'active'
        edge2multipointconnectivity.adminstate = 'enabled'
        edge2multipointconnectivity.type = 'ethernet'
        edge2multipointconnectivity.sid = 'EdgeToMultipointConnectivity_1'
        edge2multipointconnectivity.root_createbuffer = cordpod1device.id + "." + "of:000000001/7"
        #
        # Create JSON array for post-save behaviour
        #
        eps = []
        eps.append(cordpod1device.id + "." + "of:000000001/6")
        eps.append(cordpod1device.id + "." + "of:000000001/8")

        myjsonstr = {'eps': eps, 'foo': 0, 'bar': 0}
        edge2multipointconnectivity.eps_createbuffer = json.dumps(myjsonstr)
        objs.append(edge2multipointconnectivity)


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
