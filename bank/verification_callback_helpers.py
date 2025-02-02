import json
from django.db.models import Q
from .models import BankSetting
from .serializers import BankSettingsSerializer
from app.utils import allowed_file, image_as_base64, is_mobile_no_valid, image_as_secure_uri
import requests
import os
from django.conf import settings


def verification_callback(customer_profile):
    customer_data = {
    'status':customer_profile.verification_status,
    'textual_info_match': 'true' if customer_profile.verification_scores.textual_info_match_status == 'passed' else 'false',
    'applicant_photo_card_ec_match': 'true' if customer_profile.verification_scores.customer_photo_card_status == 'passed' else 'false',
    'applicant_photo_app_ec_match': 'true' if customer_profile.verification_scores.customer_photo_app_status == 'passed' else 'false',
    'detail': {
    'nid_no': customer_profile.nid_no,
    'mobile_number': customer_profile.mobile_number,
    'dob':customer_profile.dob,
    'gender': customer_profile.gender,
    'profession': customer_profile.profession,
    'nominee': customer_profile.nominee,
    'nominee_relation': customer_profile.nominee_relation_profile,
    'applicant_name_eng': customer_profile.customer_name_eng,
    'applicant_name_eng_score':customer_profile.verification_scores.customer_name_eng_score,
    'applicant_name_ben': customer_profile.customer_name_ben,
    'applicant_name_ben_score':customer_profile.verification_scores.customer_name_ben_score,
    'father_name': customer_profile.father_name_ben,
    'father_name_score':customer_profile.verification_scores.father_name_score,
    'mother_name': customer_profile.mother_name_ben,
    'mother_name_score':customer_profile.verification_scores.mother_name_score,
    "spouse_name" :customer_profile.spouse_name_ben,
    "spouse_name_score":customer_profile.verification_scores.spouse_name_score,
    'pres_address': customer_profile.pres_address_ben,
    'pres_address_score': customer_profile.verification_scores.present_addrress_score,
    'prem_address': customer_profile.perm_address_ben,
    'applicant_photo' : image_as_base64(os.path.join(settings.NID_UPLOAD_DIR, customer_data.customer_photo_from_app_image)),
    'applicant_photo_score' : customer_profile.verification_scores.customer_photo_app_score
    }
    }
    url = 'https://api.bdkepler.com/api_middleware-0.0.1-TESTING/ekyc_notification'
    req_headers = {'Content-Type':'application/json; charset=utf-8', 'Connection':'keep-alive','USER-TOKEN':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'}
    try:
        response = requests.post(url, json=customer_data, headers=req_headers, timeout=30)
        print('response',response.status_code)
        print('response data', response.content)
    except Exception as e:
        print('Exception', e)
