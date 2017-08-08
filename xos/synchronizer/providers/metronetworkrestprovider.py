
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from xos.logger import Logger, logging
from services.metronetwork.models import *
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

    def get_network_eline_link(self, networkDevice, evc):

        sid = evc['id']
        uni1 = evc['SCA_ETH_Flow_Points'][0]
        hostname = uni1['scaEthFppUniN']['transportPort']['Hostname']
        port = uni1['scaEthFppUniN']['transportPort']['Port']

        edgePort1 = NetworkEdgePort()
        edgePort1.element = networkDevice
        edgePort1.pid = "{}.{}/{}".format(networkDevice.id, hostname, port)

        if 'interfaceCfgIngressBwp' in uni1['scaEthFppUniN']:
            edgePort1.bwpCfgCbs = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
            edgePort1.bwpCfgEbs = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
            edgePort1.bwpCfgCir = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
            edgePort1.bwpCfgEir = uni1['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

        uni2 = evc['SCA_ETH_Flow_Points'][1]
        hostname = uni2['scaEthFppUniN']['transportPort']['Hostname']
        port = uni2['scaEthFppUniN']['transportPort']['Port']

        edgePort2 = NetworkEdgePort()
        edgePort2.element = networkDevice
        edgePort2.pid = "{}.{}/{}".format(networkDevice.id, hostname, port)

        if 'interfaceCfgIngressBwp' in uni1['scaEthFppUniN']:
            edgePort2.bwpCfgCbs = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
            edgePort2.bwpCfgEbs = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
            edgePort2.bwpCfgCir = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
            edgePort2.bwpCfgEir = uni2['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

        edgeToEdgeConnectivity = NetworkEdgeToEdgePointConnection()
        edgeToEdgeConnectivity.sid = sid
        edgeToEdgeConnectivity.type = "Point_To_Point"
        edgeToEdgeConnectivity.uni1 = edgePort1
        edgeToEdgeConnectivity.uni2 = edgePort2
        edgeToEdgeConnectivity.operstate = "active"
        edgeToEdgeConnectivity.adminstate = "enabled"

        return(edgeToEdgeConnectivity)

    def get_network_elan_link(self, networkDevice, evc):

        sid = evc['id']
        eps = []

        for ep in evc['SCA_ETH_Flow_Points']:
            hostname = ep['scaEthFppUniN']['transportPort']['Hostname']
            port = ep['scaEthFppUniN']['transportPort']['Port']

            edgePort = NetworkEdgePort()
            edgePort.element = networkDevice
            edgePort.pid = "{}.{}/{}".format(networkDevice.id, hostname, port)

            if 'interfaceCfgIngressBwp' in ep['scaEthFppUniN']:
                edgePort.bwpCfgCbs = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
                edgePort.bwpCfgEbs = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
                edgePort.bwpCfgCir = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
                edgePort.bwpCfgEir = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

            eps.append(edgePort)

        multipointToMultipointConnectivity = NetworkMultipointToMultipointConnection()
        multipointToMultipointConnectivity.sid = sid
        multipointToMultipointConnectivity.type = "Multipoint_To_Multipoint"
        multipointToMultipointConnectivity.eps = eps
        multipointToMultipointConnectivity.operstate = "active"
        multipointToMultipointConnectivity.adminstate = "enabled"

        return(multipointToMultipointConnectivity)

    def get_network_etree_link(self, networkDevice, evc):

        sid = evc['id']
        eps = []

        root = evc['SCA_ETH_Flow_Points'][0]
        hostname = root['scaEthFppUniN']['transportPort']['Hostname']
        port = root['scaEthFppUniN']['transportPort']['Port']

        edgePort = NetworkEdgePort()
        edgePort.element = networkDevice
        edgePort.pid = "{}.{}/{}".format(networkDevice.id, hostname, port)

        if 'interfaceCfgIngressBwp' in root['scaEthFppUniN']:
            edgePort.bwpCfgCbs = root['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
            edgePort.bwpCfgEbs = root['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
            edgePort.bwpCfgCir = root['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
            edgePort.bwpCfgEir = root['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

        edgeToMultipointConnectivity = NetworkEdgeToMultipointConnection()
        edgeToMultipointConnectivity.sid = sid
        edgeToMultipointConnectivity.type = "Root_Multipoint"
        edgeToMultipointConnectivity.root = edgePort

        for ep in evc['SCA_ETH_Flow_Points'][1:]:
            hostname = ep['scaEthFppUniN']['transportPort']['Hostname']
            port = ep['scaEthFppUniN']['transportPort']['Port']

            edgePort = NetworkEdgePort()
            edgePort.element = networkDevice
            edgePort.pid = "{}.{}/{}".format(networkDevice.id, hostname, port)

            if 'interfaceCfgIngressBwp' in ep['scaEthFppUniN']:
                edgePort.bwpCfgCbs = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCbs']
                edgePort.bwpCfgEbs = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEbs']
                edgePort.bwpCfgCir = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgCir']
                edgePort.bwpCfgEir = ep['scaEthFppUniN']['interfaceCfgIngressBwp']['bwpCfgEir']

            eps.append(edgePort)

        edgeToMultipointConnectivity.eps = eps
        edgeToMultipointConnectivity.operstate = "active"
        edgeToMultipointConnectivity.adminstate = "enabled"

        return(edgeToMultipointConnectivity)

    def get_network_links(self):

        objs = []

        networkDevice = self.networkdevice
        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password

        resp = requests.get("{}/mef-sca-api/SCA_ETH_FDFr_EC/findByState?state=Active".format(restCtrlUrl),
                            auth=HTTPBasicAuth(username, password))

        if resp.status_code == 200:
            for evc in resp.json():
                evcServiceType = evc['evcServiceType']
                if (evcServiceType == "Point_To_Point"):
                    objs.append(self.get_network_eline_link(networkDevice, evc))
                elif (evcServiceType == "Multipoint_To_Multipoint"):
                    objs.append(self.get_network_elan_link(networkDevice, evc))
                elif (evcServiceType == "Root_Multipoint"):
                    objs.append(self.get_network_etree_link(networkDevice, evc))
                else:
                    raise Exception("OnosApiError: get_network_links() - unknown link type")
        else:
            raise Exception("OnosApiError: get_network_links()")

        return objs

    def create_point_to_point_connectivity_json_data(self, obj):

        p2p_json_data = {}
        p2p_json_data["evcServiceType"] = "Point_To_Point"

        uni1 = obj.uni1
        uni1Id = uni1.pid
        uni1IdToken = (uni1Id.split('.', 1))[1].split('/', 1)
        uni1Hostname = uni1IdToken[0]
        uni1Port = uni1IdToken[1]
        uni1BwpCfgCbs = uni1.bwpCfgCbs
        uni1BwpCfgEbs = uni1.bwpCfgEbs
        uni1BwpCfgCir = uni1.bwpCfgCir
        uni1BwpCfgEir = uni1.bwpCfgEir

        uni1_json_data = {}
        uni1_json_data['scaEthFppUniN'] = {}
        uni1_json_data['scaEthFppUniN']['ceVlanId'] = obj.vlanid
        uni1_json_data['scaEthFppUniN']["transportPort"] = {}
        uni1_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"] = {}

        uni1_json_data['scaEthFppUniN']["transportPort"]["Hostname"] = uni1Hostname
        uni1_json_data['scaEthFppUniN']["transportPort"]["Port"] = uni1Port
        uni1_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCbs"] = uni1BwpCfgCbs
        uni1_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEbs"] = uni1BwpCfgEbs
        uni1_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCir"] = uni1BwpCfgCir
        uni1_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEir"] = uni1BwpCfgEir

        uni2 = obj.uni2
        uni2Id = uni2.pid
        uni2IdToken = (uni2Id.split('.', 1))[1].split('/', 1)
        uni2Hostname = uni2IdToken[0]
        uni2Port = uni2IdToken[1]
        uni2BwpCfgCbs = uni2.bwpCfgCbs
        uni2BwpCfgEbs = uni2.bwpCfgEbs
        uni2BwpCfgCir = uni2.bwpCfgCir
        uni2BwpCfgEir = uni2.bwpCfgEir

        uni2_json_data = {}
        uni2_json_data['scaEthFppUniN'] = {}
        uni2_json_data['scaEthFppUniN']['ceVlanId'] = obj.vlanid
        uni2_json_data['scaEthFppUniN']["transportPort"] = {}
        uni2_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"] = {}

        uni2_json_data['scaEthFppUniN']["transportPort"]["Hostname"] = uni2Hostname
        uni2_json_data['scaEthFppUniN']["transportPort"]["Port"] = uni2Port
        uni2_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCbs"] = uni2BwpCfgCbs
        uni2_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEbs"] = uni2BwpCfgEbs
        uni2_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCir"] = uni2BwpCfgCir
        uni2_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEir"] = uni2BwpCfgEir

        p2p_json_data["SCA_ETH_Flow_Points"] = []
        p2p_json_data["SCA_ETH_Flow_Points"].append(uni1_json_data)
        p2p_json_data["SCA_ETH_Flow_Points"].append(uni2_json_data)

        return p2p_json_data

    # nchoi: create elan service json data
    def create_multipoint_to_multipoint_connectivity_json_data(self, obj):

        mp2mp_json_data = {}
        mp2mp_json_data["evcServiceType"] = "Multipoint_To_Multipoint"
        mp2mp_json_data["SCA_ETH_Flow_Points"] = []

        for ep in obj.eps.all():
            uniId = ep.pid
            uniIdToken = (uniId.split('.', 1))[1].split('/', 1)
            uniHostname = uniIdToken[0]
            uniPort = uniIdToken[1]
            uniBwpCfgCbs = ep.bwpCfgCbs
            uniBwpCfgEbs = ep.bwpCfgEbs
            uniBwpCfgCir = ep.bwpCfgCir
            uniBwpCfgEir = ep.bwpCfgEir

            uni_json_data = {}
            uni_json_data['scaEthFppUniN'] = {}
            uni_json_data['scaEthFppUniN']['ceVlanId'] = obj.vlanid
            uni_json_data['scaEthFppUniN']["transportPort"] = {}
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"] = {}

            uni_json_data['scaEthFppUniN']["transportPort"]["Hostname"] = uniHostname
            uni_json_data['scaEthFppUniN']["transportPort"]["Port"] = uniPort
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCbs"] = uniBwpCfgCbs
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEbs"] = uniBwpCfgEbs
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCir"] = uniBwpCfgCir
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEir"] = uniBwpCfgEir

            mp2mp_json_data["SCA_ETH_Flow_Points"].append(uni_json_data)

        return mp2mp_json_data

    # nchoi: create etree service json data
    def create_root_multipoint_connectivity_json_data(self, obj):

        r2mp_json_data = {}
        r2mp_json_data["evcServiceType"] = "Root_Multipoint"
        r2mp_json_data["SCA_ETH_Flow_Points"] = []

        root = obj.root
        uniId = root.pid
        uniIdToken = (uniId.split('.', 1))[1].split('/', 1)
        uniHostname = uniIdToken[0]
        uniPort = uniIdToken[1]
        uniBwpCfgCbs = root.bwpCfgCbs
        uniBwpCfgEbs = root.bwpCfgEbs
        uniBwpCfgCir = root.bwpCfgCir
        uniBwpCfgEir = root.bwpCfgEir

        uni_json_data = {}
        uni_json_data['scaEthFppUniN'] = {}
        uni_json_data['scaEthFppUniN']['ceVlanId'] = obj.vlanid
        uni_json_data['scaEthFppUniN']["transportPort"] = {}
        uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"] = {}

        uni_json_data['scaEthFppUniN']["transportPort"]["Hostname"] = uniHostname
        uni_json_data['scaEthFppUniN']["transportPort"]["Port"] = uniPort
        uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCbs"] = uniBwpCfgCbs
        uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEbs"] = uniBwpCfgEbs
        uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCir"] = uniBwpCfgCir
        uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEir"] = uniBwpCfgEir

        r2mp_json_data["SCA_ETH_Flow_Points"].append(uni_json_data)

        for ep in obj.eps.all():
            uniId = ep.pid
            uniIdToken = (uniId.split('.', 1))[1].split('/', 1)
            uniHostname = uniIdToken[0]
            uniPort = uniIdToken[1]
            uniBwpCfgCbs = ep.bwpCfgCbs
            uniBwpCfgEbs = ep.bwpCfgEbs
            uniBwpCfgCir = ep.bwpCfgCir
            uniBwpCfgEir = ep.bwpCfgEir

            uni_json_data = {}
            uni_json_data['scaEthFppUniN'] = {}
            uni_json_data['scaEthFppUniN']['ceVlanId'] = obj.vlanid
            uni_json_data['scaEthFppUniN']["transportPort"] = {}
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"] = {}

            uni_json_data['scaEthFppUniN']["transportPort"]["Hostname"] = uniHostname
            uni_json_data['scaEthFppUniN']["transportPort"]["Port"] = uniPort
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCbs"] = uniBwpCfgCbs
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEbs"] = uniBwpCfgEbs
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgCir"] = uniBwpCfgCir
            uni_json_data['scaEthFppUniN']["interfaceCfgIngressBwp"]["bwpCfgEir"] = uniBwpCfgEir

            r2mp_json_data["SCA_ETH_Flow_Points"].append(uni_json_data)

        return r2mp_json_data

    def create_network_connectivity(self, obj):

        restCtrlUrl = self.networkdevice.restCtrlUrl
        username = self.networkdevice.username
        password = self.networkdevice.password

        evcServiceType = obj.type
        if (evcServiceType == "Point_To_Point"):
            network_connectivity_json_data = self.create_point_to_point_connectivity_json_data(obj)
        elif (evcServiceType == "Multipoint_To_Multipoint"):
            network_connectivity_json_data = self.create_multipoint_to_multipoint_connectivity_json_data(obj)
        elif (evcServiceType == "Root_Multipoint"):
            network_connectivity_json_data = self.create_root_multipoint_connectivity_json_data(obj)
        else:
            raise Exception("OnosApiError: get_network_links() - unknown link type")

        headers = {'Content-Type': 'application/json'}
        resp = requests.post('{}/mef-sca-api/SCA_ETH_FDFr_EC'.format(restCtrlUrl),
                             data=json.dumps(network_connectivity_json_data), headers=headers, auth=HTTPBasicAuth(username, password))

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
            raise Exception("OnosApiError: create_network_connectivity()")

    def delete_network_connectivity(self, obj):

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
            raise Exception("OnosApiError: delete_network_connectivity()")
