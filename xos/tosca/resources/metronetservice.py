import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate

from services.metronetwork.models import MetroNetworkService

from service import XOSService

class XOSMetroNetworkService(XOSService):
    provides = "tosca.nodes.MetroNetworkService"
    xos_model = MetroNetworkService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "versionNumber"]
