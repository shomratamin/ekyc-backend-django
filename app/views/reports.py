from ..serializers import BankSerializer, EcStatusSerializer
from ..permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from ..utils import get_file_creation_date
from customer.models import CustomerProfile
import os

class ReportsAPI(APIView):
    permission_classes = [Or(IsSuperAdmin, IsAdmin)]

    def get(self, request, format=None):
        all_customers = CustomerProfile.objects.all()
        all_customers_data = []
        counter = 0
        for i, data in enumerate(all_customers):
            if data.customer_photo_app is not None and data.customer_photo_card is not None:
                customer_photo_app = os.path.join(settings.NID_UPLOAD_DIR, data.customer_photo_app)
                customer_photo_app_time = get_file_creation_date(customer_photo_app)
                customer_photo_card = os.path.join(settings.NID_UPLOAD_DIR, data.customer_photo_card)
                customer_photo_card_time = get_file_creation_date(customer_photo_card)
                if customer_photo_app_time != -1 and customer_photo_card_time != -1:
                    time_taken = customer_photo_card_time - customer_photo_app_time
                    if time_taken > 0:
                        counter += 1
                        all_customers_data.append(','.join([str(counter), str(data.nid_no), data.bank.name, str(time_taken)]))
        all_customers_data_csv = '\n'.join(all_customers_data)
        return Response(all_customers_data_csv)