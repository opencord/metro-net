from rest_framework.response import Response
from rest_framework import serializers, filters, status
from api.xosapi_helpers import PlusModelSerializer, XOSViewSet, ReadOnlyField
from services.metronetwork.models import MetroNetworkService, NetworkEdgePort, NetworkEdgeToEdgePointConnection
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers as jsonserializer

class MetroNetworkServiceSerializer(PlusModelSerializer):
        id = ReadOnlyField()
        humanReadableName = serializers.SerializerMethodField("getHumanReadableName")

        class Meta:
            model = MetroNetworkService
            fields = ('humanReadableName',
                      'id',
                      'restUrl',
                      'administrativeState',
                      'operationalState')

        def getHumanReadableName(self, obj):
            return obj.__unicode__()

class MetroNetworkServiceViewSet(XOSViewSet):
    base_name = "metronetworkservice"
    method_name = "metronetwork"
    method_kind = "viewset"
    queryset = MetroNetworkService.get_service_objects().all()
    serializer_class = MetroNetworkServiceSerializer

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = super(MetroNetworkServiceViewSet, self).get_urlpatterns(api_path=api_path)

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
    base_name = "SCA_ETH_FPP_UNI_N"
    method_name = "SCA_ETH_FPP_UNI_N"
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
    base_name = "SCA_ETH_FDFr_EC"
    method_name = "SCA_ETH_FDFr_EC"
    method_kind = "viewset"
    queryset = NetworkEdgeToEdgePointConnection.objects.all()
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