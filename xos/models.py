# models.py -  Metro Network Service

from django.db import models
from core.models import Service

METRONETWORK_KIND = "metronetwork"
SERVICE_NAME = 'metronetwork'
SERVICE_NAME_VERBOSE = 'Metro Network Service'

class MetroNetworkService(Service):

    KIND = METRONETWORK_KIND

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_VERBOSE

    ADMINISTRATIVE_STATE = (
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    restUrl = models.CharField(verbose_name="Rest URL",
                               max_length=256,
                               editable=True)

    administrativeState = models.CharField(choices=ADMINISTRATIVE_STATE,
                                           default='disabled',
                                           verbose_name="AdministrativeState",
                                           max_length=16,
                                           editable=True)

    operationalState = models.CharField(choices=OPERATIONALSTATE,
                                        verbose_name="OperationalState",
                                        max_length=256,
                                        editable=True)

    def __init__(self, *args, **kwargs):
        super(MetroNetworkService, self).__init__(*args, **kwargs)

    def getAdminstrativeState(self):
         return self.administrativeState

    def setAdminstrativeState(self, value):
        self.administrativeState = value

    def getOperationalState(self):
        return self.operationalState

    def getRestUrl(self):
        return self.restUrl