from ..models import Bank
from ..serializers import BankSerializer, EcStatusSerializer
from bank.models import EcStatus, KycDataSource
from ..permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class EcStatusAPI(APIView):
    permission_classes = [Or(IsSuperAdmin, IsAdmin)]

    def get(self, request, format=None):
        ec_stat = KycDataSource.objects.all()
        serialized_data = EcStatusSerializer(ec_stat, many=True)
        return Response(serialized_data.data)