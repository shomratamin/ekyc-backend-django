from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from ..serializers import AgentSerializer
from app.permissions import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from app.utils import *
from customer.models import CustomerProfile, CustomerVerificationScores
from django.db.models import Q
from app.tasks import do_request_ec_info
import shutil

class CustomerRegistration(APIView):
    permission_classes = [IsAgent]

    def post(self, request, format=None):
        step = request.query_params.get('step')
        # print('request from', request.user.username)
        if step == '1':
            try:
                id_front = request.FILES['id_front']
                id_back = request.FILES['id_back']
            except Exception as e:
                print(e)
                return Response({ 'status':'error', 'status_code': 5001, 'message': 'Please check your image fields', }, status=HTTP_400_BAD_REQUEST)

            if id_front and allowed_file(id_front.name):
                fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
                id_front_file_name = fs.save(filename_to_hash(id_front.name), id_front)
                __id_card_photo_file = id_front_file_name + '_crop_.jpg'
                # __ = fs.save(__id_card_photo_file, id_front)
                id_front_file_path = os.path.join(settings.NID_UPLOAD_DIR, id_front_file_name)
                __id_card_photo_file_path = os.path.join(settings.NID_UPLOAD_DIR, __id_card_photo_file)
                __ = crop_id(id_front_file_path,width=950)
                shutil.copy(id_front_file_path, __id_card_photo_file_path)
                face_region = face_detection_service(id_front_file_path)
                ocr_out_front = do_ocr_id_front_back(id_front_file_path, face_region=face_region)

            if id_back and allowed_file(id_back.name):
                fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
                id_back_file_name = fs.save(filename_to_hash(id_back.name), id_back)
                id_back_file_path = os.path.join(settings.NID_UPLOAD_DIR, id_back_file_name)
                __ = crop_id(id_back_file_path, width=1050)
                ocr_out_back = do_ocr_id_front_back(id_back_file_path, face_region=None)
                
                
            if ocr_out_front is None:                    
                return Response({ 'status':'failed', 'status_code': 6001, 'message': 'Nid or Date of Birth not found.', }, status=HTTP_200_OK)

            if ocr_out_front['id_no_nid'] == 'none' or ocr_out_front['birth_nid'] == 'none':
                return Response({ 'status':'failed', 'status_code': 6002, 'message': 'Nid and Date of Birth not found.', }, status=HTTP_200_OK)
            
            if ocr_out_back is not None:
                if 'addr' in ocr_out_back:
                    ocr_out_front['addr'] = ocr_out_back['addr']

            response_data = {
                'nid_no': ocr_out_front['id_no_nid'],
                'dob': ocr_out_front['birth_nid'],
                'applicant_name_ben': ocr_out_front['name_b_nid'],
                'applicant_name_eng': ocr_out_front['name_e_nid'],
                'father_name': ocr_out_front['father_nid'],
                'mother_name': ocr_out_front['mother_nid'] }
            if 'spouse_nid' in ocr_out_front:
                response_data['spouse_name'] = ocr_out_front['spouse_nid']
            response_data['address'] = ocr_out_front['addr']
            response_data['id_front_image'] = image_as_secure_uri(id_front_file_name)
            response_data['id_back_image'] = image_as_secure_uri(id_back_file_name)
            response_data['id_front_name'] = id_front_file_name
            response_data['id_back_name'] = id_back_file_name


            
            return Response({ 'status':'success', 'status_code': 4001, 'data': response_data, }, status=HTTP_200_OK)

        elif step == '2':
            nid_no = request.data.get('nid_no')
            dob = request.data.get('dob')
            applicant_name_ben = request.data.get('applicant_name_ben')
            applicant_name_eng = request.data.get('applicant_name_eng')
            father_name = request.data.get('father_name')
            mother_name = request.data.get('mother_name')
            pres_address = request.data.get('pres_address')
            perm_address = request.data.get('perm_address')
            id_front_name = request.data.get('id_front_name')
            id_back_name = request.data.get('id_back_name')
            gender = request.data.get('gender')
            profession = request.data.get('profession')
            nominee = request.data.get('nominee')
            nominee_relation = request.data.get('nominee_relation')
            mobile_number = request.data.get('mobile_number')
            applicant_photo = request.data.get('applicant_photo')
            applicant_photo_base64 = request.data.get('applicant_photo_base64')
            fields = [nid_no, dob, applicant_name_ben, applicant_name_eng, father_name, mother_name, pres_address, perm_address, \
                    id_front_name, id_back_name, gender, profession, nominee, nominee_relation, mobile_number]
            
            if None in fields or (applicant_photo is None and applicant_photo_base64 is None):
                return Response({ 'status':'error','status_code': 5002, 'message': 'All fields are mandatory', }, status=HTTP_400_BAD_REQUEST)
            if len(id_front_name) > 99 or len(id_back_name) > 99:
                return Response({ 'status':'error','status_code': 5003, 'message': 'id_front_name or id_back_name field can not be more than 100 characters', }, status=HTTP_400_BAD_REQUEST)
            # if not is_mobile_no_valid(mobile_number):
            #     return Response({ 'status':'error', 'status_code': 5004, 'message': 'Please provide a valid Bangladeshi mobile number without country code', }, status=HTTP_400_BAD_REQUEST)
            try:
                if applicant_photo_base64 is not None:
                    _applicant_photo = base64_to_image(applicant_photo_base64)
                else:
                    _applicant_photo = request.FILES['applicant_photo']
                if allowed_file(_applicant_photo.name):
                    fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
                    applicant_photo_name = fs.save(filename_to_hash(_applicant_photo.name), _applicant_photo)
                else:
                    return Response({ 'status':'error', 'status_code': 5005, 'message': 'Please upload a valid photo', }, status=HTTP_400_BAD_REQUEST)
            except:
                return Response({ 'status':'error', 'status_code': 5005, 'message': 'Please upload a valid photo', }, status=HTTP_400_BAD_REQUEST)                
            nid_no = nid_no.strip()
            dob = dob.strip()
            if not CustomerProfile.objects.filter((Q(nid_no=nid_no) & Q(mobile_number=mobile_number)) & Q(bank=request.user.bank)).exists():
                verification_scores = CustomerVerificationScores()
                verification_scores.save()
                customer_photo_from_card_name = id_front_name + '_crop_.jpg'
                new_customer = CustomerProfile(nid_no=nid_no,dob=dob,customer_name_ben=applicant_name_ben, \
                    customer_name_eng = applicant_name_eng, father_name_ben = father_name, mother_name_ben = mother_name, \
                    pres_address_ben = pres_address, perm_address_ben = perm_address, nid_front_image = id_front_name, \
                    nid_back_image = id_back_name, gender = gender, profession = profession, nominee = nominee, \
                    nominee_relation_profile = nominee_relation, mobile_number = mobile_number, customer_photo_from_app_image = applicant_photo_name, \
                    customer_photo_from_card_image = customer_photo_from_card_name, \
                    on_boarded_by = request.user.pk, bank = request.user.bank, verification_status = 'pending', verification_scores = verification_scores
                    )

                new_customer.save()
                bank_slug = request.user.bank.slug
                payload = [{'nid':nid_no,'dob':dob}]
                try:
                    do_request_ec_info.delay(bank_slug,payload)
                except:
                    pass
            else:
                existing_customer = CustomerProfile.objects.filter((Q(nid_no=nid_no) & Q(mobile_number=mobile_number)) & Q(bank=request.user.bank)).first()
                if existing_customer.verification_status == 'undecided':
                    return Response({ 'status':'failed', 'status_code': 6003, 'uuid': existing_customer.customer_uuid,  'message': 'Applicant with this NID or mobile number already exists.', }, status=HTTP_200_OK)
                else:
                    customer_photo_from_card_name = id_front_name + '_crop_.jpg'
                    existing_customer.nid_no=nid_no
                    existing_customer.dob=dob
                    existing_customer.customer_name_ben=applicant_name_ben
                    existing_customer.customer_name_eng = applicant_name_eng
                    existing_customer.father_name_ben = father_name
                    existing_customer.mother_name_ben = mother_name
                    existing_customer.pres_address_ben = pres_address
                    existing_customer.perm_address_ben = perm_address
                    existing_customer.nid_front_image = id_front_name
                    existing_customer.nid_back_image = id_back_name
                    existing_customer.gender = gender
                    existing_customer.profession = profession
                    existing_customer.nominee = nominee
                    existing_customer.nominee_relation_profile = nominee_relation
                    existing_customer.mobile_number = mobile_number
                    existing_customer.customer_photo_from_app_image = applicant_photo_name
                    existing_customer.customer_photo_from_card_image = customer_photo_from_card_name
                    existing_customer.on_boarded_by = request.user.pk
                    existing_customer.bank = request.user.bank
                    existing_customer.verification_status = 'pending'
                    existing_customer.verification_scores = existing_customer.verification_scores
                    existing_customer.save()

                    bank_slug = request.user.bank.slug
                    payload = [{'nid':nid_no,'dob':dob}]
                    try:
                        do_request_ec_info.delay(bank_slug,payload)
                    except:
                        pass

                    return Response({ 'status':'success', 'status_code': 4002,'uuid': existing_customer.customer_uuid, 'message': 'Customer is successfully re-enrolled, waiting verification.', }, status=HTTP_200_OK)
            return Response({ 'status':'success', 'status_code': 4003, 'uuid': existing_customer.customer_uuid, 'message': 'Customer is successfully enrolled, waiting verification.', }, status=HTTP_200_OK)



class CustomerVerificationStatus(APIView):
    permission_classes = [IsAgent]

    def post(self, request, format=None):
        mobile_no = request.data.get('mobile_number')
        # uuid = request.data.get('uuid')
        # if not is_mobile_no_valid(mobile_no):
        #     return Response({ 'status':'error',  'status_code': 5004, 'message': 'Please provide a valid Bangladeshi mobile no without country code', }, status=HTTP_400_BAD_REQUEST)

        # customer = CustomerProfile.objects.filter(uuid=uuid, on_boarded_by = request.user.pk)
        customer = CustomerProfile.objects.filter(Q(mobile_number=mobile_no) & Q(bank=request.user.bank))
        if not customer.exists():
            return Response({ 'status':'failed',  'status_code': 6004, 'message': 'No applicant with this tracking number found', }, status=HTTP_200_OK)
        customer_data = customer.first()
        if customer_data.verification_status == 'pending' or customer_data.verification_status == 'invalid':
            response_data = {
                'status':customer_data.verification_status,
                'detail': {
                'mobile_number':customer_data.mobile_number,
                'uuid': customer_data.customer_uuid,
                'applicant_name_eng': customer_data.customer_name_eng,
                'nid_no': customer_data.nid_no,
                'submitted_on': customer_data.submitted_on,
                'status': customer_data.verification_status
                } }
        else:
            response_data = {
                'status': customer_data.verification_status,
                'textual_info_match': 'true' if customer_data.verification_scores.textual_info_match_status == 'passed' else 'false',
                'applicant_photo_card_ec_match': 'true' if customer_data.verification_scores.customer_photo_card_status == 'passed' else 'false',
                'applicant_photo_app_ec_match': 'true' if customer_data.verification_scores.customer_photo_app_status == 'passed' else 'false',
                'detail': {
                'nid_no': customer_data.nid_no,
                'mobile_number': customer_data.mobile_number,
                'dob': customer_data.dob,
                'gender': customer_data.gender,
                'profession': customer_data.profession,
                'nominee': customer_data.nominee,
                'nominee_relation': customer_data.nominee_relation_profile,
                'applicant_name_eng': customer_data.customer_name_eng,
                'applicant_name_eng_score': customer_data.verification_scores.customer_name_eng_score,
                'applicant_name_ben': customer_data.customer_name_ben,
                'applicant_name_ben_score': customer_data.verification_scores.customer_name_ben_score,
                'father_name': customer_data.father_name_ben,
                'father_name_score': customer_data.verification_scores.father_name_score,
                'mother_name': customer_data.mother_name_ben,
                'mother_name_score': customer_data.verification_scores.mother_name_score,
                "spouse_name":  customer_data.spouse_name_ben,
                "spouse_name_score": customer_data.verification_scores.spouse_name_score,
                'pres_address': customer_data.pres_address_ben,
                'pres_address_score': customer_data.verification_scores.present_addrress_score,
                'prem_address': customer_data.perm_address_ben,
                'applicant_photo' : image_as_base64(os.path.join(settings.NID_UPLOAD_DIR, customer_data.customer_photo_from_app_image)),
                'applicant_photo_score' : customer_data.verification_scores.customer_photo_app_score
                }}
        return Response({ 'status':'success',  'status_code': 4004,'data': response_data, }, status=HTTP_200_OK)

class CustomersVerificationLog(APIView):
    permission_classes = [IsAgent]

    def get(self, request, format=None):
        status = request.query_params.get('status')

        if status not in ['passed','failed','pending','invalid','all']:
            return Response({ 'status':'error',  'status_code': 5006, 'message': 'Please provide a valid status field' }, status=HTTP_400_BAD_REQUEST)
        if status == 'all':
            customers_data = CustomerProfile.objects.filter(on_boarded_by=request.user.pk)
        else:
            customers_data = CustomerProfile.objects.filter(verification_status=status, on_boarded_by=request.user.pk)

        response_data = []
        for customer_data in customers_data:
            _data = {
                'mobile_number':customer_data.mobile_number,
                'customer_name_eng': customer_data.customer_name_eng,
                'nid_no': customer_data.nid_no,
                'submitted_on': customer_data.submitted_on,
                'status': customer_data.verification_status
                }
            response_data.append(_data)
        if len(response_data) < 1:
            return Response({ 'status':'not_found',  'status_code': 6005, 'message': 'No applicants record found', }, status=HTTP_200_OK)

        return Response({ 'status':'success', 'status_code': 4005, 'data': response_data, }, status=HTTP_200_OK)




