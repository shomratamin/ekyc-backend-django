from ..models import Bank
from customer.models import CustomerProfile
from ..permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class VerificationQuotaAPI(APIView):
    permission_classes = [Or(IsSuperAdmin, IsAdmin)]

    def get(self, request, format=None):
        response = []
        banks = Bank.objects.all()
        for bank in banks:
            passed = 0
            failed = 0
            invalid = 0
            on_process = 0
            total = 0
            customer_profiles = CustomerProfile.objects.filter(bank=bank)
            for customer_profile in customer_profiles:
                if customer_profile.status == 'passed':
                    passed += 1
                elif customer_profile.status == 'failed':
                    failed += 1
                elif customer_profile.status == 'invalid':
                    invalid += 1
                else:
                    on_process += 1
                total += 1
            response.append({'Bank': bank.name, 'passed': passed, 'failed': failed, 'invalid': invalid, 'on_process': on_process, 'total': total})
        return Response(response)