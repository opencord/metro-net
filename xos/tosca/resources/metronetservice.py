import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate

from services.metronetwork.models import *

from service import XOSService
from xosresource import XOSResource


class XOSMetroNetworkSystem(XOSResource):
    provides = "tosca.nodes.MetroNetworkSystem"
    xos_model = MetroNetworkSystem
    copyin_props = ["name", "administrativeState", "restUrl"]

class MetroNetworkDevice(XOSResource):
    provides = "tosca.nodes.MetroNetworkDevice"
    xos_model = NetworkDevice
    copyin_props = ["id", "name", "administrativeState", "username", "password", "authType", "restCtrlUrl"]
