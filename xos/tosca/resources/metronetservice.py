import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate

from services.metronetwork.models import MetroNetworkService, NetworkDevice

from service import XOSService
from xosresource import XOSResource


class XOSMetroNetworkService(XOSService):
    provides = "tosca.nodes.MetroNetworkService"
    xos_model = MetroNetworkService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "versionNumber"]


class MetroNetworkDevice(XOSResource):
    provides = "tosca.nodes.MetroNetworkDevice"
    xos_model = NetworkDevice
    copyin_props = ["name", "administrativeState", "username", "password", "authType", "restCtrlUrl"]
