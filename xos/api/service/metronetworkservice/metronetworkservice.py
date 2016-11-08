from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, filters, status
from api.xosapi_helpers import PlusModelSerializer, XOSViewSet, ReadOnlyField
from services.metronetwork.models import *
from random import randint
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers as jsonserializer

class MetroNetworkSystemSerializer(PlusModelSerializer):
        id = ReadOnlyField()
        humanReadableName = serializers.SerializerMethodField("getHumanReadableName")

        class Meta:
            model = MetroNetworkSystem
            fields = ('humanReadableName',
                      'id',
                      'restUrl',
                      'administrativeState',
                      'operationalState')

        def getHumanReadableName(self, obj):
            return obj.name

class MetroNetworkSystemViewSet(XOSViewSet):
    base_name = "metronetworksystem"
    method_name = "metronetworksystem"
    method_kind = "viewset"
    queryset = MetroNetworkSystem.objects.all()
    serializer_class = MetroNetworkSystemSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(MetroNetworkSystemViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):
        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)


class NetworkEdgePortSerializer(PlusModelSerializer):
    id = ReadOnlyField()
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")

    class Meta:
        model = NetworkEdgePort
        fields = ('humanReadableName',
                  'pid',
                  'id',
                  'element',
                  'bwpCfgCbs',
                  'bwpCfgEbs',
                  'bwpCfgCir',
                  'bwpCfgEir',
                  'name',
                  'location',
                  'latlng')


    def getHumanReadableName(self, obj):
        return obj.id

class NetworkEdgePortViewSet(XOSViewSet):
    base_name = "UNI"
    method_name = "UNI"
    method_kind = "viewset"
    queryset = NetworkEdgePort.objects.all()
    serializer_class = NetworkEdgePortSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(NetworkEdgePortViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):
        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

class NetworkEdgeToEdgePointConnectionSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    uni1 = NetworkEdgePortSerializer(required=True, read_only=False)
    uni2 = NetworkEdgePortSerializer(required=True, read_only=False)

    class Meta:
        model = NetworkEdgeToEdgePointConnection

        fields = ('humanReadableName',
                  'sid',
                  'id',
                  'type',
                  'uni1',
                  'uni2',
                  'operstate',
                  'adminstate'
                  )

    def getHumanReadableName(self, obj):
        return obj.id

class NetworkEdgeToEdgePointConnectionViewSet(XOSViewSet):
    base_name = "ELINE"
    method_name = "ELINE"
    method_kind = "viewset"
    queryset = NetworkEdgeToEdgePointConnection.get_service_objects().all()
    serializer_class = NetworkEdgeToEdgePointConnectionSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(NetworkEdgeToEdgePointConnectionViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):

        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        ELineConnectionToDelete = NetworkEdgeToEdgePointConnection.objects.get(pk=pk)

        if (ELineConnectionToDelete):
            ELineConnectionToDelete.adminstate = 'deactivationrequested'
            ELineConnectionToDelete.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def create(self, validated_data):

        ELineConnection = NetworkEdgeToEdgePointConnection()
        ELineConnection.sid = validated_data.data.get('sid')
        ELineConnection.adminstate = validated_data.data.get('adminstate')
        ELineConnection.operstate = validated_data.data.get('operstate')
        ELineConnection.sid = validated_data.data.get('sid')
        ELineConnection.type = 'Point_To_Point'

        uni1 = validated_data.data.get('uni1')
        uni2 = validated_data.data.get('uni2')

        uni1 = NetworkEdgePort.objects.get(pk=uni1['id'])
        uni2 = NetworkEdgePort.objects.get(pk=uni2['id'])

        ELineConnection.uni1 = uni1
        ELineConnection.uni2 = uni2
        ELineConnection.save()

        response_data = {}
        response_data['sid'] = ELineConnection.sid
        response_data['adminstate'] = ELineConnection.adminstate
        response_data['operstate'] = ELineConnection.operstate
        response_data['type'] = ELineConnection.type

        response_data['uni1'] = {}
        response_data['uni1']['id'] = uni1.id
        response_data['uni1']['pid'] = uni1.pid
        response_data['uni1']['bwpCfgCbs'] = uni1.bwpCfgCbs
        response_data['uni1']['bwpCfgEbs'] = uni1.bwpCfgEbs
        response_data['uni1']['bwpCfgCir'] = uni1.bwpCfgCir
        response_data['uni1']['bwpCfgEir'] = uni1.bwpCfgEir
        response_data['uni1']['name'] = uni1.name
        response_data['uni1']['location'] = uni1.location
        response_data['uni1']['latlng'] = uni1.latlng

        response_data['uni2'] = {}
        response_data['uni2']['id'] = uni2.id
        response_data['uni2']['pid'] = uni2.pid
        response_data['uni2']['bwpCfgCbs'] = uni2.bwpCfgCbs
        response_data['uni2']['bwpCfgEbs'] = uni2.bwpCfgEbs
        response_data['uni2']['bwpCfgCir'] = uni2.bwpCfgCir
        response_data['uni2']['bwpCfgEir'] = uni2.bwpCfgEir
        response_data['uni2']['name'] = uni1.name
        response_data['uni2']['location'] = uni1.location
        response_data['uni2']['latlng'] = uni1.latlng

        return Response(response_data)

class NetworkEdgeToMultipointConnectionSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    root = NetworkEdgePortSerializer(required=True, read_only=False)
    eps = NetworkEdgePortSerializer(required=True, read_only=False, many=True)

    class Meta:
        model = NetworkEdgeToMultipointConnection

        fields = ('humanReadableName',
                  'sid',
                  'id',
                  'type',
                  'root',
                  'eps',
                  'operstate',
                  'adminstate'
                  )

    def getHumanReadableName(self, obj):
        return obj.id

class NetworkEdgeToMultipointConnectionViewSet(XOSViewSet):
    base_name = "ETREE"
    method_name = "ETREE"
    method_kind = "viewset"
    queryset = NetworkEdgeToMultipointConnection.get_service_objects().all()
    serializer_class = NetworkEdgeToMultipointConnectionSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(NetworkEdgeToMultipointConnectionViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):

        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        ETreeConnectionToDelete = NetworkEdgeToMultipointConnection.objects.get(pk=pk)

        if (ETreeConnectionToDelete):
            ETreeConnectionToDelete.adminstate = 'deactivationrequested'
            ETreeConnectionToDelete.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def create(self, validated_data):

        ETreeConnection = NetworkEdgeToMultipointConnection()
        ETreeConnection.sid = validated_data.data.get('sid')
        ETreeConnection.adminstate = validated_data.data.get('adminstate')
        ETreeConnection.operstate = validated_data.data.get('operstate')
        ETreeConnection.sid = validated_data.data.get('sid')
        ETreeConnection.type = 'Root_Multipoint'

        root_id = validated_data.data.get('root')
        eps_list = validated_data.data.get('eps')

        root = NetworkEdgePort.objects.get(pk=root_id)
        ETreeConnection.root = root
        ETreeConnection.save()

        for ep in eps_list:
            port = NetworkEdgePort.objects.get(pk=ep['id'])
            ETreeConnection.eps.add(port)

        response_data = {}
        response_data['sid'] = ETreeConnection.sid
        response_data['adminstate'] = ETreeConnection.adminstate
        response_data['operstate'] = ETreeConnection.operstate
        response_data['type'] = ETreeConnection.type

        response_data['root'] = {}
        response_data['root']['id'] = root.id
        response_data['root']['pid'] = root.pid
        response_data['root']['bwpCfgCbs'] = root.bwpCfgCbs
        response_data['root']['bwpCfgEbs'] = root.bwpCfgEbs
        response_data['root']['bwpCfgCir'] = root.bwpCfgCir
        response_data['root']['bwpCfgEir'] = root.bwpCfgEir
        response_data['root']['name'] = root.name
        response_data['root']['location'] = root.location
        response_data['root']['latlng'] = root.latlng

        eps_data = []
        for ep in ETreeConnection.eps.all():
            port = {}
            port['id'] = ep.id
            port['pid'] = ep.pid
            port['bwpCfgCbs'] = ep.bwpCfgCbs
            port['bwpCfgEbs'] = ep.bwpCfgEbs
            port['bwpCfgCir'] = ep.bwpCfgCir
            port['bwpCfgEir'] = ep.bwpCfgEir
            port['name'] = ep.name
            port['location'] = ep.location
            port['latlng'] = ep.latlng
            eps_data.append(port)

        response_data['eps'] = eps_data

        return Response(response_data)

class NetworkMultipointToMultipointConnectionSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    eps = NetworkEdgePortSerializer(required=True, read_only=False, many=True)

    class Meta:
        model = NetworkMultipointToMultipointConnection

        fields = ('humanReadableName',
                  'sid',
                  'id',
                  'type',
                  'eps',
                  'operstate',
                  'adminstate'
                  )

    def getHumanReadableName(self, obj):
        return obj.id

class NetworkMultipointToMultipointConnectionViewSet(XOSViewSet):
    base_name = "ELAN"
    method_name = "ELAN"
    method_kind = "viewset"
    queryset = NetworkMultipointToMultipointConnection.get_service_objects().all()
    serializer_class = NetworkMultipointToMultipointConnectionSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(NetworkMultipointToMultipointConnectionViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):

        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        ETreeConnectionToDelete = NetworkMultipointToMultipointConnection.objects.get(pk=pk)

        if (ETreeConnectionToDelete):
            ETreeConnectionToDelete.adminstate = 'deactivationrequested'
            ETreeConnectionToDelete.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def create(self, validated_data):

        ELanConnection = NetworkMultipointToMultipointConnection()
        ELanConnection.sid = validated_data.data.get('sid')
        ELanConnection.adminstate = validated_data.data.get('adminstate')
        ELanConnection.operstate = validated_data.data.get('operstate')
        ELanConnection.sid = validated_data.data.get('sid')
        ELanConnection.type = 'Multipoint_To_Multipoint'

        eps_list = validated_data.data.get('eps')
        ELanConnection.save()

        for ep in eps_list:
            port = NetworkEdgePort.objects.get(pk=ep['id'])
            ELanConnection.eps.add(port)

        response_data = {}
        response_data['sid'] = ELanConnection.sid
        response_data['adminstate'] = ELanConnection.adminstate
        response_data['operstate'] = ELanConnection.operstate
        response_data['type'] = ELanConnection.type

        eps_data = []
        for ep in ELanConnection.eps.all():
            port = {}
            port['id'] = ep.id
            port['pid'] = ep.pid
            port['bwpCfgCbs'] = ep.bwpCfgCbs
            port['bwpCfgEbs'] = ep.bwpCfgEbs
            port['bwpCfgCir'] = ep.bwpCfgCir
            port['bwpCfgEir'] = ep.bwpCfgEir
            port['name'] = ep.name
            port['location'] = ep.location
            port['latlng'] = ep.latlng
            eps_data.append(port)

        response_data['eps'] = eps_data

        return Response(response_data)

############################

class BandwidthProfileSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")

    class Meta:
        model = BandwidthProfile

        fields = ('humanReadableName',
                  'id',
                  'bwpcfgcbs',
                  'bwpcfgebs',
                  'bwpcfgcir',
                  'bwpcfgeir',
                  'name'
                  )

    def getHumanReadableName(self, obj):
        return obj.name

class BandwidthProfileViewSet(XOSViewSet):
    base_name = "BANDWIDTH_PROFILE"
    method_name = "BANDWIDTH_PROFILE"
    method_kind = "viewset"
    queryset = BandwidthProfile.objects.all()
    serializer_class = BandwidthProfileSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(BandwidthProfileViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):

        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

    def create(self, validated_data):

        bandwidthProfile = BandwidthProfile()
        bandwidthProfile.name = validated_data.data.get('name')
        bandwidthProfile.bwpcfgcbs = validated_data.data.get('bwpcfgcbs')
        bandwidthProfile.bwpcfgebs = validated_data.data.get('bwpcfgebs')
        bandwidthProfile.bwpcfgcir = validated_data.data.get('bwpcfgcir')
        bandwidthProfile.bwpcfgeir = validated_data.data.get('bwpcfgeir')

        bandwidthProfile.save()

        response_data = {}
        response_data['name'] = bandwidthProfile.name
        response_data['bwpcfgcbs'] = bandwidthProfile.bwpcfgcbs
        response_data['bwpcfgebs'] = bandwidthProfile.bwpcfgebs
        response_data['bwpcfgcir'] = bandwidthProfile.bwpcfgeir
        response_data['bwpcfgcir'] = bandwidthProfile.bwpcfgcir
        response_data['id'] = bandwidthProfile.id

        return Response(response_data)

class VnodSiteSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")

    class Meta:
        model = Site

        fields = ('humanReadableName',
                  'site_url',
                  'enabled',
                  'longitude',
                  'latitude',
                  'name'
                  )

    def getHumanReadableName(self, obj):
        return obj.name

class RemotePortSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    edgeport = NetworkEdgePortSerializer(read_only=True)
    remoteportsite = VnodSiteSerializer(read_only=True)

    class Meta:
        model = RemotePort

        fields = ('humanReadableName',
                  'name',
                  'edgeport',
                  'id',
                  'remoteportsite'
                  )

    def getHumanReadableName(self, obj):
        return obj.name

class ServiceSpokeSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    vnodlocalsite = VnodSiteSerializer(read_only=True)
    vnodlocalport = RemotePortSerializer(read_only=True)

    class Meta:
        model = ServiceSpoke

        fields = ('humanReadableName',
                  'id',
                  'name',
                  'remotesubscriber',
                  'remotevnodid',
                  'autoattached',
                  'operstate',
                  'vnodlocalsite',
                  'vnodlocalport'
                  )

    def getHumanReadableName(self, obj):
        return obj.name

class VnodGlobalServiceSerializer(PlusModelSerializer):
    humanReadableName = serializers.SerializerMethodField("getHumanReadableName")
    metronetworkroottomultipoint = NetworkEdgeToMultipointConnectionSerializer(read_only=True)
    metronetworkmultipoint = NetworkMultipointToMultipointConnectionSerializer(read_only=True)
    metronetworkpointtopoint = NetworkEdgeToEdgePointConnectionSerializer(read_only=True)
    spokes = ServiceSpokeSerializer(read_only=True, many=True)
    bandwidthProfile = BandwidthProfileSerializer(read_only=True)

    class Meta:
        model = VnodGlobalService

        fields = ('humanReadableName',
                  'servicehandle',
                  'vlanid',
                  'id',
                  'type',
                  'operstate',
                  'adminstate',
                  'metronetworkroottomultipoint',
                  'metronetworkmultipoint',
                  'metronetworkpointtopoint',
                  'spokes',
                  'bandwidthProfile',
                  'name'
                  )

    def getHumanReadableName(self, obj):
        return obj.name

class VnodGlobalServiceViewSet(XOSViewSet):
    base_name = "VNOD_GLOBAL_SERVICE"
    method_name = "VNOD_GLOBAL_SERVICE"
    method_kind = "viewset"
    queryset = VnodGlobalService.get_service_objects().all()
    serializer_class = VnodGlobalServiceSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(VnodGlobalServiceViewSet, self).get_urlpatterns(api_path=api_path)

        return patterns

    def list(self, request):

        object_list = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(object_list, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        VnodGlobalServiceToDelete = VnodGlobalService.objects.get(pk=pk)

        if (VnodGlobalServiceToDelete):
            VnodGlobalServiceToDelete.adminstate = 'deactivationrequested'
            VnodGlobalServiceToDelete.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def create(self, validated_data):

        vnodGlobalService = VnodGlobalService()

        vnodGlobalService.name = validated_data.data.get('name')

        if VnodGlobalService.objects.filter(
                name=vnodGlobalService.name).exists():
            return HttpResponseBadRequest('Error: VnodGlobalService name \'' +  vnodGlobalService.name
                            + '\' already exists.')

        vnodGlobalService.servicehandle = validated_data.data.get('servicehandle')
        vnodGlobalService.adminstate = 'enabled'
        vnodGlobalService.operstate = 'inactive'
        vnodGlobalService.type = validated_data.data.get('type')

        vnodGlobalService.vlanid = self.getUniqueVlandId()

        bandwidth_profile = validated_data.data.get('bandwidthProfile')
        bandwidthprofile = BandwidthProfile.objects.get(pk=bandwidth_profile['id'])
        if (bandwidth_profile):
            vnodGlobalService.bandwidthProfile = bandwidthprofile

        vnodGlobalService.save()

        spokes_list = validated_data.data.get('spokes')
        if (spokes_list is None):
            vnodGlobalService.delete()
            return HttpResponseBadRequest('Error: No spokes found in request.')

        for spoke in spokes_list:
            vnodlocalsite = Site.objects.get(pk=spoke['vnodlocalsite']['id'])
            servicespoke = ServiceSpoke()
            servicespoke.vnodlocalsite = vnodlocalsite
            servicespoke.vnodlocalport = self.getRandomRemotePort(vnodlocalsite)
            servicespoke.name = spoke['name']
            if (spoke.get('autoattached')):
                servicespoke.autoattached = spoke['autoattached']
            servicespoke.operstate = 'inactive'
            servicespoke.adminstate = 'disabled'
            servicespoke.save()
            vnodGlobalService.spokes.add(servicespoke)

        serializer = self.get_serializer(vnodGlobalService)
        return Response(serializer.data)

    def getUniqueVlandId(self):
        unique = False
        while not unique:
            vlanid = randint(1, 4095)
            vnodglobalservice = VnodGlobalService.get_service_objects().filter(vlanid=vlanid)
            if (not vnodglobalservice):
                unique = True
        return vlanid

    def getRandomRemotePort(self, site):
        remotePort = RemotePort.objects.get(remoteportsite__name=site.name)
        if (remotePort):
            return remotePort
        return None

    @classmethod
    def calculateVnodGlobalOperState(self, servicehandle):
        vnodglobalservice = VnodGlobalService.get_service_objects().filter(servicehandle=servicehandle)
        if (not vnodglobalservice):
            HttpResponseBadRequest('Error: Could not find VnodGlobalObject with servicehandle=' + servicehandle)

        vnodglobalservice = vnodglobalservice[0]
        all_spokes_active_and_enabled = True

        for spoke in vnodglobalservice.spokes.all():
            if (spoke.operstate != 'active' or spoke.adminstate != 'enabled'):
                all_spokes_active_and_enabled = False
                break;

        if (all_spokes_active_and_enabled):
            vnodglobalservice.operstate = 'active'
        else:
            vnodglobalservice.operstate = 'inactive'

        vnodglobalservice.save()
        return all_spokes_active_and_enabled

    @classmethod
    def createService(self, servicehandle):
        vnodglobalservice = VnodGlobalService.get_service_objects().filter(servicehandle=servicehandle)
        if (not vnodglobalservice):
            HttpResponseBadRequest('Error: Could not find VnodGlobalObject with servicehandle=' + servicehandle)

        vnodglobalservice = vnodglobalservice[0]
        if (vnodglobalservice.type == 'eline'):

            spokes = vnodglobalservice.spokes.all()
            uni1 = spokes[0].vnodlocalport.edgeport
            uni2 = spokes[1].vnodlocalport.edgeport
            name = 'ELine-' + str(vnodglobalservice.id)
            type = 'Point_To_Point'
            operstate = 'active'
            adminstate = 'activationrequested'

            eline = NetworkEdgeToEdgePointConnection()
            eline.name = name
            eline.type = type
            eline.operstate = operstate
            eline.adminstate = adminstate
            eline.vlanid = vnodglobalservice.vlanid
            eline.sid = name
            eline.uni1 = NetworkEdgePort.objects.get(pid=uni1.pid)
            eline.uni2 = NetworkEdgePort.objects.get(pid=uni2.pid)

            eline.save()
            vnodglobalservice.metronetworkpointtopoint = eline
            vnodglobalservice.save()

        elif (vnodglobalservice.type == 'elan'):

            spokes = vnodglobalservice.spokes.all()

            name = 'ELAN-' + str(vnodglobalservice.id)
            type = 'Multipoint_To_Multipoint'
            operstate = 'active'
            adminstate = 'activationrequested'

            elan = NetworkMultipointToMultipointConnection()
            elan.name = name
            elan.type = type
            elan.operstate = 'inactive'
            elan.adminstate = 'disabled'
            elan.vlanid = vnodglobalservice.vlanid
            elan.save()

            for spoke in spokes:
                uni = NetworkEdgePort.objects.get(pid=spoke.vnodlocalport.edgeport.pid)
                elan.eps.add(uni)

            elan.operstate = operstate
            elan.adminstate = adminstate
            elan.save()

            vnodglobalservice.metronetworkmultipoint = elan
            vnodglobalservice.save()

        # TODO: elif (vnodglobalservice.type == 'etree'):

class VnodGlobalServiceAutoAttachmentView(APIView):
    method_kind = "list"
    method_name = "vnodglobal_api_autoattach"

    def get(self, request, format=None):
        params = request.query_params
        sitename = params.get('sitename')

        if ( sitename is None):
            HttpResponseBadRequest("Error: Request requires] 'sitename' as a query param.")

        vnodglobalservices = VnodGlobalService.get_service_objects().filter(spokes__autoattached=True,
                                                                            spokes__operstate='inactive',
                                                                            spokes__vnodlocalsite__name=sitename)

        if (not vnodglobalservices):
            HttpResponseBadRequest({"handles" : []})

        handles = []
        for vnodglobalservice in vnodglobalservices:
            if (vnodglobalservice.adminstate != 'disabled'):
                handles.append(vnodglobalservice.servicehandle)

        response_data = {'servicehandles' : handles}
        return Response(response_data)

class VnodGlobalServiceConfigurationView(APIView):
    method_kind = "list"
    method_name = "vnodglobal_api_configuration"

    def get(self, request, format=None):
        params = request.query_params
        servicehandle = params.get('servicehandle')
        sitename = params.get('sitename')

        if (servicehandle is None or sitename is None):
            HttpResponseBadRequest("Error: Request requires 'servicehandle' and 'sitename' as query params.")

        vnodglobalservice = VnodGlobalService.get_service_objects().filter(servicehandle=servicehandle)
        if (not vnodglobalservice):
            HttpResponseBadRequest('Error: Could not find VnodGlobalObject with servicehandle=' + servicehandle)

        vnodglobalservice = vnodglobalservice[0]
        response_data = {}
        response_data['vlanid'] = vnodglobalservice.vlanid

        for spoke in vnodglobalservice.spokes.all():
            if (spoke.vnodlocalsite.name == sitename and spoke.adminstate != 'configured'):
                response_data['port'] = {}
                response_data['port']['name'] = spoke.vnodlocalport.name
                break;

        return Response(response_data)

class VnodGlobalServiceActivationView(APIView):
    method_kind = "list"
    method_name = "vnodglobal_api_activation"

    def post(self, request, format=None):
        body_json = request.body
        body = json.loads(body_json)

        servicehandle=body['servicehandle']
        sitename=body['sitename']
        activate = body['activate']
        vnodlocalid = body['vnodlocalid']
        portid = body.get('portid')

        if (activate == 'true' or activate == 'True'):
            isActivate = True
        else:
            isActivate = False

        vnodglobalservice = VnodGlobalService.get_service_objects().filter(servicehandle=servicehandle)
        if (not vnodglobalservice):
            HttpResponseBadRequest('Error: Could not find VnodGlobalObject with servicehandle=' + servicehandle)

        vnodglobalservice = vnodglobalservice[0]

        for spoke in vnodglobalservice.spokes.all():
            if (spoke.vnodlocalsite.name == sitename and spoke.vnodlocalport.name == portid):
                spoke_id = spoke.id
                servicespoke = ServiceSpoke.objects.get(id=spoke_id)
                servicespoke.remotevnodid = vnodlocalid
                servicespoke.save()
                break;

        return Response()

class VnodGlobalServiceAdminOperationalStateView(APIView):
    method_kind = "list"
    method_name = "vnodglobal_api_status"

    def post(self, request, format=None):
        body_json = request.body
        body = json.loads(body_json)

        servicehandle = body['servicehandle']
        sitename = body['sitename']
        operstate = body.get('operstate')
        adminstate = body.get('adminstate')
        portid = body.get('portid')

        vnodglobalservice = VnodGlobalService.get_service_objects().filter(servicehandle=servicehandle)
        if (not vnodglobalservice):
            HttpResponseBadRequest('Error: Could not find VnodGlobalObject with servicehandle=' + servicehandle)

        vnodglobalservice = vnodglobalservice[0]

        for spoke in vnodglobalservice.spokes.all():
            if (spoke.vnodlocalsite.name == sitename and spoke.vnodlocalport.name == portid):
                spoke_id = spoke.id
                servicespoke = ServiceSpoke.objects.get(id=spoke_id)
                if (operstate):
                    servicespoke.operstate = operstate
                if (adminstate):
                    servicespoke.adminstate = adminstate
                servicespoke.save()
                break;

        isGlobalActive = VnodGlobalServiceViewSet.calculateVnodGlobalOperState(servicehandle=servicehandle)

        if (vnodglobalservice.metronetworkmultipoint is None and vnodglobalservice.metronetworkpointtopoint is None and
                    vnodglobalservice.metronetworkroottomultipoint is None and isGlobalActive):
            VnodGlobalServiceViewSet.createService(servicehandle=servicehandle)

        return Response()
