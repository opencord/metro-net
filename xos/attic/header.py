# models.py -  Metro Network Service

from django.db import models
from django.db.models import *
from core.models import Service
from core.models import PlCoreBase
from core.models import Site

METRONETWORK_KIND = "metronet"
SERVICE_NAME = 'metronet'
SERVICE_NAME_ELINE_VERBOSE = 'E-Line Service'
SERVICE_NAME_ELAN_VERBOSE = 'E-LAN Service'
SERVICE_NAME_ETREE_VERBOSE = 'E-Tree Service'

