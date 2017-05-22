from xosresource import XOSResource
from service import XOSService
from services.metronet.models import *

class XOSMetronetUNI(XOSResource):
    provides = "tosca.nodes.UserNetworkInterface"
    xos_model = UserNetworkInterface
    copyin_props = ['tenant','vlanIds', 'cpe_id', 'latlng', 'name']

class XOSMetronetEnterpriseLocation(XOSResource):
    provides = "tosca.nodes.EnterpriseLocation"
    xos_model = EnterpriseLocation
    copyin_props = ['name', 'cord_site_ip', 'cord_site_port', 'cord_site_username', 'cord_site_password', 'cord_site_type']

class XOSMetronetOnosModel(XOSResource):
    provides = "tosca.nodes.OnosModel"
    xos_model = OnosModel
    copyin_props = ['name', 'onos_ip', 'onos_port', 'onos_username', 'onos_password', 'onos_type']

class XOSMetronetBandwithProfile(XOSResource):
    provides = "tosca.nodes.BandwidthProfile"
    xos_model = BandwidthProfile
    copyin_props = ['cbs', 'ebs', 'cir', 'eir', 'name']

class XOSMetronetELine(XOSResource):
    provides = "tosca.nodes.ELine"
    xos_model = ELine
    copyin_props = ['name', 'connect_point_1_id', 'connect_point_2_id', 'vlanids', 'cord_site_name', 'bwp']