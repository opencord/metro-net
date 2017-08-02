import os
import sys
import requests
import json
from synchronizers.new_base.syncstep import SyncStep
from synchronizers.new_base.modelaccessor import *
#from xos.logger import Logger, logging

from requests.auth import HTTPBasicAuth
#logger = Logger(level=logging.INFO)

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)


class SyncMetroNetEline(SyncStep):
    provides = [ELine]

    observes = ELine

    requested_interval = 0

    def __init__(self, *args, **kwargs):
        super(SyncMetroNetEline, self).__init__(*args, **kwargs)

    def get_onos_global_addr(self, onos):
        #Fetching ip and port from the Global ONOS, append the CE specif API

        onos_url = "http://%s:%s/onos/" % (onos.onos_ip, onos.onos_port)
        evc_endpoint = "carrierethernet/evc"
        return onos_url + evc_endpoint

    def get_onos_global_auth(self, onos):
        #Fetching username and password from the Global ONOS

        return HTTPBasicAuth(onos.onos_username, onos.onos_password)

    def sync_record(self, evc):
        print "POST %s " % (evc)
        #logger.info("Syncing Edited EVC: %s" % evc.name)
        # Fetch the bwp from the DB
        bwp = BandwidthProfile.objects.get(name=evc.bwp)

        # json to configure ONOS to start the EVC.
        # {
        #     "evcId": "evc1",
        #     "evcCfgId": "evpl1",
        #     "uniList": [
        #         "netconf:192.168.56.10:830/0",
        #         "netconf:192.168.56.20:830/0"
        #     ],
        #     "evcType": "POINT_TO_POINT",
        #     "vlanId": 100,
        #     "cir": "400",
        #     "eir": "200",
        #     "cbs": "3000",
        #     "ebs": "2000"
        # }

        data = {}
        data["evcId"] = evc.name
        data["evcCfgId"] = evc.name
        data["uniList"] = [evc.connect_point_1_id, evc.connect_point_2_id]
        data["evcType"] = "POINT_TO_POINT"
        data["vlanId"] = evc.vlanids.split(",")
        data["cbs"] = bwp.cbs
        data["ebs"] = bwp.ebs
        data["cir"] = bwp.cir
        data["eir"] = bwp.eir
        print "data %s" % data
        # assuming that the CPEs are controller by the fabric ONOS
        onos = OnosModel.objects.get(onos_type="global")
        onos_addr = self.get_onos_global_addr(onos)

        # FIXME - hardcoded auth
        auth = self.get_onos_global_auth(onos)

        print "POST %s for app %s, data = %s" % (onos_addr, evc.name, data)

        r = requests.post(onos_addr, data=json.dumps(data), auth=auth)
        #TODO XOS might fail to connect to ONOS.
        if (r.status_code != 200):
            print r
            raise Exception("Received error from EVC Installation update (%d)" % r.status_code)

    def delete_record(self, evc):
        # TODO evaluate what to in this case.
        print "Syncing delete EVC: %s" % evc.name
        #logger.info("Syncing delete EVC: %s" % evc.name)
