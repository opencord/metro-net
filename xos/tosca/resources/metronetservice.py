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

class VnodGlobalService(XOSService):
    provides = "tosca.nodes.VNodGlobalService"
    xos_model = VnodGlobalService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "versionNumber"]

    def get_xos_args(self):
        args = super(VnodGlobalService, self).get_xos_args()

        profile = self.get_requirement("tosca.relationships.UsesBandwidthProfile", throw_exception=False)
        if profile:
            profile = self.get_xos_object(BandwidthProfile, name=profile)
            args["bandwidthProfile"] = profile
        return args

class XOSMetronetBandwithProficle(XOSResource):
    provides = "tosca.nodes.EcordBandwidthProfile"
    xos_model = BandwidthProfile
    copyin_props = ['bwpcfgcbs','bwpcfgebs','bwpcfgcir','bwpcfgeir','name']

class XOSMetronetUNI(XOSResource):
    provides = "tosca.nodes.EcordUserNetworkInterface"
    xos_model = UserNetworkInterface
    copyin_props = ['enabled','capacity','bw_used','vlanIds', 'location', 'latlng', 'name']