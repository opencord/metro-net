from xos.logger import Logger, logging
from core.models.netw import *
from synchronizers.metronetwork.providers.metronetworkprovider import MetroNetworkProvider

import requests, json
from requests.auth import HTTPBasicAuth

logger = Logger(level=logging.INFO)


class MetroNetworkRestProvider(MetroNetworkProvider):
    def __init__(self, networkdevice, **args):
        MetroNetworkProvider.__init__(self, networkdevice, **args)

    def get_network_ports(self):

        objs = []

        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password

        resp = requests.get("{}/mef-sca-api/SCA_ETH_FPP_UNI_N".format(restCtrlUrl),
                            auth=HTTPBasicAuth(username, password))

        if resp.status_code == 200:
            for uni in resp.json():
                hostname = uni['transportPort']['Hostname']
                port = uni['transportPort']['Port']

                # Default values
                bwpCfgCbs = 0
                bwpCfgEbs = 0
                bwpCfgCir = 0
                bwpCfgEir = 0

                if 'interfaceCfgIngressBwp' in uni:
                    bwpCfgCbs = uni['interfaceCfgIngressBwp']['bwpCfgCbs']
                    bwpCfgEbs = uni['interfaceCfgIngressBwp']['bwpCfgEbs']
                    bwpCfgCir = uni['interfaceCfgIngressBwp']['bwpCfgCir']
                    bwpCfgEir = uni['interfaceCfgIngressBwp']['bwpCfgEir']

                uniPort = NetworkEdgePort()
                uniPort.element = self.networkdevice
                uniPort.pid = "{}.{}/{}".format(self.networkdevice.id, hostname, port)
                uniPort.bwpCfgCbs = bwpCfgCbs
                uniPort.bwpCfgEbs = bwpCfgEbs
                uniPort.bwpCfgCir = bwpCfgCir
                uniPort.bwpCfgEir = bwpCfgEir

                objs.append(uniPort)

            return objs

        else:
            raise Exception("OnosApiError: get_network_ports()")

    def get_network_links(self):

        objs = []

        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password

        resp = requests.get("{}/mef-sca-api/SCA_ETH_FDFr_EC/findByState?state=Active".format(restCtrlUrl),
                            auth=HTTPBasicAuth(username, password))

        if resp.status_code == 200:
            for evc in resp.json():
                id = evc['id']
                evcServiceType = evc['evcServiceType']

                if (evcServiceType == "Point_To_Point"):
                    uni1 = evc['SCA_ETH_Flow_Points'][0]
                    hostname = uni1['scaEthFppUniN']['transportPort']['Hostname']
                    port = uni1['scaEthFppUniN']['transportPort']['Port']

                    if 'interfaceCfgIngressBwp' in uni1['scaEthFppUniN']:
                        bwpCfgCbs = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
                        bwpCfgEbs = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
                        bwpCfgCir = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
                        bwpCfgEir = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

                    edgePort1 = NetworkEdgePort()
                    edgePort1.element = self.networkdevice
                    edgePort1.pid = "{}.{}/{}".format(self.networkdevice.id, hostname, port)
                    edgePort1.bwpCfgCbs = bwpCfgCbs
                    edgePort1.bwpCfgEbs = bwpCfgEbs
                    edgePort1.bwpCfgCir = bwpCfgCir
                    edgePort1.bwpCfgEir = bwpCfgEir

                    uni2 = evc['SCA_ETH_Flow_Points'][1]
                    hostname = uni2['scaEthFppUniN']['transportPort']['Hostname']
                    port = uni2['scaEthFppUniN']['transportPort']['Port']

                    if 'interfaceCfgIngressBwp' in uni1['scaEthFppUniN']:
                        bwpCfgCbs = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
                        bwpCfgEbs = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
                        bwpCfgCir = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
                        bwpCfgEir = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

                    edgePort2 = NetworkEdgePort()
                    edgePort2.element = self.networkdevice
                    edgePort2.pid = "{}.{}/{}".format(self.networkdevice.id, hostname, port)
                    edgePort2.bwpCfgCbs = bwpCfgCbs
                    edgePort2.bwpCfgEbs = bwpCfgEbs
                    edgePort2.bwpCfgCir = bwpCfgCir
                    edgePort2.bwpCfgEir = bwpCfgEir

                edgeToEdgeConnectivity = NetworkEdgeToEdgePointConnection()
                edgeToEdgeConnectivity.sid = id
                edgeToEdgeConnectivity.type = evcServiceType
                edgeToEdgeConnectivity.uni1 = edgePort1
                edgeToEdgeConnectivity.uni2 = edgePort2
                edgeToEdgeConnectivity.operstate = "active"
                edgeToEdgeConnectivity.adminstate = "enabled"

                objs.append(edgeToEdgeConnectivity)

            return objs

        else:
            raise Exception("OnosApiError: get_network_links()")

    def create_point_to_point_connectivity(self, obj):

        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password

        evcServiceType = obj.type
        # evcServiceType = "Point_To_Point"

        uni1 = obj.uni1
        uni1Id = uni1.pid
        uni1IdToken = (uni1Id.split('.', 1))[1].split('/', 1)
        uni1Hostname = uni1IdToken[0]
        uni1Port = uni1IdToken[1]
        uni1BwpCfgCbs = uni1.bwpCfgCbs
        uni1BwpCfgEbs = uni1.bwpCfgEbs
        uni1BwpCfgCir = uni1.bwpCfgCir
        uni1BwpCfgEir = uni1.bwpCfgEir

        uni2 = obj.uni2
        uni2Id = uni2.pid
        uni2IdToken = (uni2Id.split('.', 1))[1].split('/', 1)
        uni2Hostname = uni2IdToken[0]
        uni2Port = uni2IdToken[1]
        uni2BwpCfgCbs = uni2.bwpCfgCbs
        uni2BwpCfgEbs = uni2.bwpCfgEbs
        uni2BwpCfgCir = uni2.bwpCfgCir
        uni2BwpCfgEir = uni2.bwpCfgEir

        data = {
            "evcServiceType": evcServiceType,
            "SCA_ETH_Flow_Points": [
                {
                    "scaEthFppUniN": {"transportPort": {"Hostname": uni1Hostname, "Port": uni1Port},
                                      "interfaceCfgIngressBwp": {"bwpCfgCbs": uni1BwpCfgCbs,
                                                                 "bwpCfgEbs": uni1BwpCfgEbs,
                                                                 "bwpCfgCir": uni1BwpCfgCir,
                                                                 "bwpCfgEir": uni1BwpCfgEir}}},
                {
                    "scaEthFppUniN": {"transportPort": {"Hostname": uni2Hostname, "Port": uni2Port},
                                      "interfaceCfgIngressBwp": {"bwpCfgCbs": uni2BwpCfgCbs,
                                                                 "bwpCfgEbs": uni2BwpCfgEbs,
                                                                 "bwpCfgCir": uni2BwpCfgCir,
                                                                 "bwpCfgEir": uni2BwpCfgEir}}}]
        }

        headers = {'Content-Type': 'application/json'}

        resp = requests.post('{}/mef-sca-api/SCA_ETH_FDFr_EC'.format(restCtrlUrl),
                             data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(username, password))

        if resp.status_code == 201:
            result = resp.json()
            message = result['message']

            msg_token = message.split()
            for i, token in enumerate(msg_token):
                if token == 'id':
                    service_id = msg_token[i + 1]
                    obj.sid = service_id
                    obj.adminstate = "enabled"
                    obj.operstate = "active"

                    return True

        elif resp.status_code == 204:
            obj.adminstate = "invalid"  # what's the meaning?
            obj.operstate = "inactive"
            obj.backend_status = '204 - No network resource'
            return False

        elif resp.status_code == 500:
            obj.adminstate = "enabled"
            obj.operstate = "inactive"
            obj.backend_status = '500 - Internal Server Error'
            return False

        else:
            raise Exception("OnosApiError: create_point_to_point_connectivity()")

    def delete_point_to_point_connectivity(self, obj):

        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password
        evcId = obj.sid

        resp = requests.delete("{}/mef-sca-api/SCA_ETH_FDFr_EC/{}".format(restCtrlUrl, evcId),
                               auth=HTTPBasicAuth(username, password))

        if resp.status_code == 200:
            obj.adminstate = 'disabled'
            obj.operstate = 'inactive'
            return True

        elif resp.status_code == 204:
            obj.adminstate = "invalid"  # what's the meaning?
            obj.backend_status = '204 - No such network resource: {}'.format(evcId)
            return False

        elif resp.status_code == 500:
            obj.adminstate = "disabled"
            obj.backend_status = '500 - Internal Server Error'
            return False

        else:
            raise Exception("OnosApiError: delete_point_to_point_connectivity()")
