from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.db import IntegrityError
from ..models import Bank
from ..serializers import BankSerializer
from bank.models import BankSetting, get_default_bank_settings
from ..permissions import *

class BankDetails(APIView):
    permission_classes = [Or(IsSuperAdmin, IsAdmin)]
    def post(self,request, format=None):
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'Please provide bank name.'},
                        status=HTTP_400_BAD_REQUEST)
        bank = Bank(name=name)
        try:
            bank.save()
        except IntegrityError:
            return Response({'error': "Bank name already exists."},
                        status=HTTP_400_BAD_REQUEST)
        all_default_kyc_params = get_default_bank_settings(bank)
        BankSetting.objects.bulk_create(all_default_kyc_params)
        return Response({'name': bank.name, 'slug': bank.slug, 'created_on': bank.created_on}, status=HTTP_200_OK)

    def get(self, request, format=None):
        banks = Bank.objects.all()
        serialized_data = BankSerializer(banks, many=True)
        return Response(serialized_data.data)

    def delete(self, request, format=None):
        slug = request.query_params.get('slug')
        if slug is None:
            return Response({'error': 'Please provide bank slug identifier.'},
                        status=HTTP_400_BAD_REQUEST)     
        bank = Bank.objects.filter(slug=slug)   
        bank.delete()
        return Response({'details': 'Bank deleted.'}, status=HTTP_200_OK)


    
