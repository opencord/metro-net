from rest_framework.response import Response
from rest_framework import serializers, filters, status
from api.xosapi_helpers import PlusModelSerializer, XOSViewSet, ReadOnlyField
from services.metronetwork.models import *
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
            return obj.__unicode__()

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
        ELineConnection.type = validated_data.data.get('type')

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
        ETreeConnection.type = validated_data.data.get('type')

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
        ELanConnection.type = validated_data.data.get('type')

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
