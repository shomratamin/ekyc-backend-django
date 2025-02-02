from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Branch
from ..serializers import CustomerSerializer, CustomerListSerializer, CustomerProfileSerializer, CustomerNomineeSerializer, \
    CustomerAccountSerializer, CustomerOtherInfoSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from app.permissions import *
import os
from app.utils import allowed_file, image_as_base64, is_mobile_no_valid, image_as_secure_uri
from django.conf import settings
from customer.models import CustomerProfile, CustomerVerificationScores
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from customer.models import CustomerAccount, CustomerProfile
from app.query import QueryBuilder

# class CustomerDetails(APIView):
#     permission_classes = [IsBank]

#     def get(self, request, format=None):
#         bank = request.user.bank
#         if bank is None:
#             return Response({'error':'Bank is null.'}, status=HTTP_400_BAD_REQUEST)
#         users = User.objects.filter(bank=bank, user_type=User.USER_TYPES_MAP['customer'])
#         serialized_data = CustomerSerializer(users, many=True)
#         return Response(serialized_data.data)


class CustomerVerificationStatus(APIView):
    permission_classes = [IsBank]

    def post(self, request, format=None):
        mobile_no = request.data.get('mobile_number')
        if not is_mobile_no_valid(mobile_no):
            return Response({ 'status':'error', 'message': 'Please provide a valid Bangladeshi mobile no without country code', }, status=HTTP_400_BAD_REQUEST)

        customer = CustomerProfile.objects.filter(mobile_number=mobile_no, bank=request.user.bank)
        if not customer.exists():
            return Response({ 'status':'failed', 'message': 'No applicant with this mobile number found', }, status=HTTP_400_BAD_REQUEST)
        customer_data = customer.first()
        if customer_data.verification_status == 'pending' or customer_data.verification_status == 'invalid':
            response_data =  {
                'mobile_number':customer_data.mobile_number,
                'applicant_name_eng': customer_data.customer_name_eng,
                'nid_no': customer_data.nid_no,
                'submitted_on': customer_data.submitted_on,
                'verification_status': customer_data.verification_status
                }
        else:
            response_data = {
                'status':customer_data.verification_status,
                'detail':{
                'nid_no': customer_data.nid_no,
                'dob':customer_data.dob,
                'applicant_name_eng': customer_data.customer_name_eng,
                'applicant_name_eng_score':customer_data.scores.customer_name_eng_score,
                'applicant_name_ben': customer_data.customer_name_ben,
                'applicant_name_ben_score':customer_data.scores.customer_name_ben_score,
                'father_name': customer_data.father_name,
                'father_name_score':customer_data.scores.father_name_score,
                'mother_name': customer_data.mother_name,
                'mother_name_score':customer_data.scores.mother_name_score,
                'pres_address': customer_data.pres_address,
                'pres_address_score': customer_data.scores.present_addrress_score,
                'textual_info_match': customer_data.scores.textual_info_match,
                'applicant_photo_from_card': image_as_base64(os.path.join(settings.NID_UPLOAD_DIR, customer_data.customer_photo_card)),
                'applicant_photo_card_ec_match': customer_data.scores.customer_photo_card_ec_match,
                'applicant_photo_from_app':image_as_base64(os.path.join(settings.NID_UPLOAD_DIR, customer_data.customer_photo_app)),
                'applicant_photo_app_ec_match': customer_data.scores.customer_photo_app_ec_match
                }
                }
        return Response({ 'status':'success', 'data': response_data, }, status=HTTP_200_OK)

class CustomersVerificationLog(APIView):
    permission_classes = [IsBank]

    def get(self, request, format=None):
        status = request.query_params.get('status')
        page = request.query_params.get('page')
        per_page = request.query_params.get('per_page')
        if page is None:
            page = 1
        if per_page is None:
            per_page = 20
        
        if status not in ['passed','failed','pending','invalid','all']:
            return Response({ 'status':'error', 'message': 'Please provide a valid status field' }, status=HTTP_400_BAD_REQUEST)
        if status == 'all':
            customers_data = CustomerProfile.objects.filter(bank=request.user.bank)
        else:
            customers_data = CustomerProfile.objects.filter(verification_status=status, bank=request.user.bank)

        total_customers = customers_data.count()
        paginator = Paginator(customers_data, per_page)

        try:
            customers = paginator.page(page)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)
        
        customers_page = list(map(lambda customer: customer.as_dict(), list(customers)))
        return Response({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_customers,'data': customers_page}, status=HTTP_200_OK)

        # response_data = []
        # for customer_data in customers_data:
        #     _data = {
        #         'mobile_number':customer_data.mobile_number,
        #         'applicant_name_eng': customer_data.customer_name_eng,
        #         'nid_no': customer_data.nid_no,
        #         'submitted_on': customer_data.submitted_on,
        #         'verification_status': customer_data.status
        #         }
        #     response_data.append(_data)
        # if len(response_data) < 1:
        #     return Response({ 'status':'not_found', 'message': 'No applicants record found', }, status=HTTP_200_OK)

        # return Response({ 'status':'success', 'data': response_data, }, status=HTTP_200_OK)

class CustomersVerificationRetry(APIView):
    permission_classes = [IsBank]

    def post(self, request, format=None):
        from_status = 'ec_requested'
        to_status = 'pending'
        customers_data = CustomerProfile.objects.filter(verification_status=from_status, bank=request.user.bank)
        for customer_data in customers_data:
            customer_data.verification_status = to_status
            customer_data.save()

        return Response({ 'status':'success', 'total': customers_data.count(), }, status=HTTP_200_OK)


class CustomerList(APIView):
    permission_classes = [IsBank]

    def get(self, request, format=None):
        status = request.query_params.get('status')
        page = request.query_params.get('page')
        per_page = request.query_params.get('per_page')
        search = request.query_params.get('search')
        count_only = request.query_params.get('count_only')
        csv = request.query_params.get('csv')

        if status is None:
            status = 'all'
        if page is None:
            page = '1'
        if per_page is None:
            per_page = '20'
        if search is None:
            search = 'all'
        if csv is None:
            csv = False

        if not page.isnumeric() or not per_page.isnumeric():
            return Response({'status': 'error', 'message':'Bad formatted request.'}, status=HTTP_400_BAD_REQUEST)

        status_types = ['passed','failed','pending','invalid','ec_requested','all']
        if status not in status_types:
            return Response({ 'status':'error', 'message': 'Please provide a valid status field' }, status=HTTP_400_BAD_REQUEST)

        if count_only:
            if status != 'all':
                customers_count = CustomerProfile.objects.filter(verification_status=status, bank=request.user.bank).count()
                return Response({status:customers_count}, status=HTTP_200_OK)
            else:
                results = dict()
                for s_type in status_types[:-1]:
                    _count = CustomerProfile.objects.filter(verification_status=s_type, bank=request.user.bank).count()
                    results[s_type] = _count

                return Response(results, status=HTTP_200_OK)



        if status == 'all':
            if search != 'all':  
                customers_data = CustomerProfile.objects.filter(Q(bank=request.user.bank) & (Q(nid_no__startswith=search) | \
                    Q(tracking_number__startswith=search))).order_by('-submitted_on')
            else:
                customers_data = CustomerProfile.objects.filter(bank=request.user.bank)
        else:
            if search != 'all':  
                customers_data = CustomerProfile.objects.filter(Q(bank=request.user.bank) & Q(verification_status=status) & \
                    (Q(nid_no__startswith=search) | Q(tracking_number__startswith=search))).order_by('-submitted_on')
            else:
                customers_data = CustomerProfile.objects.filter(verification_status=status, bank=request.user.bank).order_by('-submitted_on')

        

        total_customers = customers_data.count()

        paginator = Paginator(customers_data, per_page)

        try:
            customers = paginator.page(page)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)

        if csv:
            csv_fields = ['tracking_number', 'branch_code', 'nid_no', 'dob', 'customer_name_eng', \
                'father_name_eng', 'mother_name_eng', 'spouse_name_eng', 'pres_address_eng', 'perm_address_eng', \
                    'mobile_number', 'email', 'tin_number', 'submitted_on' 'account_type', 'branch_code']
            out_csv_lines = []
            for _customer in customers:
                csv_line = ','.join(_customer.as_list())
                out_csv_lines.append(csv_line)
            out_csv = '\n'.join(out_csv_lines)
            return HttpResponse(out_csv,content_type = 'text/csv')


        customers_page = CustomerListSerializer(customers, many=True)



        return Response({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_customers,'data': customers_page.data}, status=HTTP_200_OK)

class CustomerProfileView(APIView):
    permission_classes = [IsBank]

    def get(self, request, format=None):
        primary_key = request.query_params.get('pk')
        csv = request.query_params.get('csv')

        if csv is None:
            csv = False


        if primary_key is None:
            return Response({'status': 'error', 'message':'Bad formatted request.'}, status=HTTP_400_BAD_REQUEST)

        if not primary_key.isnumeric():
            return Response({'status': 'error', 'message':'Bad formatted request.'}, status=HTTP_400_BAD_REQUEST)

        customer_profile = CustomerProfile.objects.filter(pk=primary_key)

        if customer_profile.count() < 1:
            return Response({'status': 'not_found', 'message':'Customer profile is not found.'}, status=HTTP_200_OK)

        customer_profile = customer_profile.first()
        customer_nominess = customer_profile.nominees.all()
        customer_accounts = customer_profile.first_applicant.all()
        customer_other_info = customer_profile.otherinfo.all()
        customer_profile_data = CustomerProfileSerializer(customer_profile).data

        if csv:
            out_csv = ','.join(customer_profile.as_list())
            return HttpResponse(out_csv, content_type = 'text/csv')

        for key in customer_profile_data:
            if key.endswith('_image'):
                if customer_profile_data[key] is not None:
                    customer_profile_data[key] = image_as_secure_uri(customer_profile_data[key])
                else:
                    customer_profile_data[key] = ''

        nominee_data = CustomerNomineeSerializer(customer_nominess, many=True).data

        for nominee in nominee_data:
            for key in nominee:
                if key.endswith('_image'):
                    if nominee[key] is not None:
                        nominee[key] = image_as_secure_uri(nominee[key])
                    else:
                        nominee[key] = ''

        customer_profile_data['bank'] = customer_profile_data['bank']['slug']
        customer_profile_data['nominess'] = nominee_data
        customer_profile_data['accounts'] = CustomerAccountSerializer(customer_accounts, many=True).data
        customer_profile_data['otherinfo'] = CustomerOtherInfoSerializer(customer_other_info, many=True).data

        

        return Response({'status': 'success', 'data': customer_profile_data}, status=HTTP_200_OK)


class CustomerBankAccount(APIView):
    permission_classes = [IsBank]

    def post(self, request, format=None):
        account_number = request.POST.get('account_number')
        unique_account_number = request.POST.get('unique_account_number')
        remarks = request.POST.get('remarks')
        customer_pk = request.POST.get('pk')
        if customer_pk is None:
            return Response({'status': 'error', 'message':'Please send a customer valid id.'}, status=HTTP_400_BAD_REQUEST)
        customer = CustomerProfile.objects.filter(pk=customer_pk)
        if customer.exists():
            customer = customer.first()
            customer_account = CustomerAccount.objects.filter(customer=customer)
            if customer_account.exists():
                customer_account = customer_account.first()
                customer_account.account_number = account_number
                customer_account.unique_account_number = unique_account_number
                customer_account.account_remarks = remarks
                customer_account.save()
                return Response({'status': 'success'}, status=HTTP_200_OK)
            else:
                customer_account = CustomerAccount(customer=customer, account_name=customer.customer_name_eng, \
                    account_number= account_number, unique_account_number= unique_account_number, \
                        account_remarks = remarks)
                customer_account.save()
                return Response({'status': 'success'}, status=HTTP_200_OK)

        return Response({'status': 'error', 'message':'Customer Profile Not Found.'}, status=HTTP_200_OK)

