from xosresource import XOSResource
from service import XOSService
from services.metronetwork.models import *

class XOSMetroNetworkSystem(XOSResource):
    provides = "tosca.nodes.MetroNetworkSystem"
    xos_model = MetroNetworkSystem
    copyin_props = ["name", "administrativeState", "restUrl"]

class MetroNetworkDevice(XOSResource):
    provides = "tosca.nodes.MetroNetworkDevice"
    xos_model = NetworkDevice
    copyin_props = ["id", "name", "administrativeState", "username", "password", "authType", "restCtrlUrl"]
