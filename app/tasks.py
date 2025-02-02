# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.decorators import task, periodic_task
from celery.canvas import subtask
from bank.models import KycDataSource, EcStatus, BankSetting
from app.models import Bank
from customer.models import CustomerProfile, CustomerVerificationScores
import requests
from datetime import timedelta
import json
from app.utils import do_ocr_ec_compare, match_faces
from django.conf import settings
from bank.caching import get_bank_settings, update_bank_settings                         
from django.core.mail import send_mail
from app.sms_helpers import send_sms, send_otp, send_tracking_number_sms
from app.email_helpers import send_otp_email, send_password_email, send_tracking_number_email, send_password_reset_email
from app.models import User, generate_otp, verify_otp, generate_otp_agent
from bank.verification_callback_helpers import verification_callback
from app.utils import allowed_file, image_as_base64, is_mobile_no_valid, image_as_secure_uri

@task
def check_ec_status_periodic():
    data_sources = KycDataSource.objects.all()
    for _d in data_sources:
        if _d.status is None:
            ec_status = EcStatus()
            ec_status.save()
            _d.status = ec_status
            _d.save()
        subtask('do_ec_status_check',args=(_d.bank.pk,_d.ip_bank,_d.ip_ec, _d.username, _d.password,_d.status.pk)).apply_async()

@task(name='do_ec_status_check')
def do_ec_status_check(bank_pk,ip_bank,ip_ec,username,password,status_pk):
    ec_status_model = EcStatus.objects.get(pk=status_pk)
    
    try:
        ec_status = requests.get('https://{}:4800/status'.format(ip_bank), verify=False, timeout=3, allow_redirects=False)
    except:
        ec_status_model.agent_status = 'unreachable'
        ec_status_model.save()
        return
    if ec_status.status_code == 200:
        _ec_status = ec_status.json()
        ec_status_model.average_ec_response = _ec_status['average_ec_response']
        ec_status_model.ec_server_status = _ec_status['ec_server_status']
        ec_status_model.is_set_ec_credentials = _ec_status['is_set_ec_credentials']
        ec_status_model.is_ec_logged_in = _ec_status['is_ec_logged_in']
        ec_status_model.is_ec_credentials_valid = _ec_status['is_ec_credentials_valid']
        ec_status_model.up_time = _ec_status['up_time']
        ec_status_model.nid_info_req_queue = _ec_status['nid_info_req_queue']
        ec_status_model.nid_info_upstream_queue = _ec_status['nid_info_upstream_queue']
        ec_status_model.upstream_status_queue = _ec_status['upstream_status_queue']
        ec_status_model.ec_job_running = _ec_status['ec_job_running']
        ec_status_model.upstream_job_running = _ec_status['upstream_job_running']
        ec_status_model.agent_status = 'stable'

        if _ec_status['is_set_ec_credentials'] == False:
            try:
                payload = {'username':username,'password':password, \
                         'ec_ip':ip_ec,'ec_port':'443'}
                res = requests.post('https://{}:4800/set-credentials'.format(ip_bank),allow_redirects=False, verify=False, \
                     timeout=3,data=json.dumps(payload),headers={'Content-Type': 'text/plain'})
                print(res.json())
                if res.json()['status'] == 'success':
                    ec_status_model.is_set_ec_credentials = True
            except:
                ec_status_model.agent_status = 'unreachable'
        ec_status_model.save()


@task
def request_ec_info_periodic():
    pending_ec_jobs = CustomerProfile.objects.filter(verification_status='pending')
    banks = dict()
    for _d in pending_ec_jobs:
        if _d.bank_id not in banks:
            if len(_d.nid_no) > 7 and len(_d.dob) > 7:
                banks[_d.bank_id] = [{'nid':_d.nid_no,'dob':_d.dob}]
        else:
            if len(_d.nid_no) > 7 and len(_d.dob) > 7:
                banks[_d.bank_id].append({'nid':_d.nid_no,'dob':_d.dob})

    for _bank_pk in banks:
        ec_jobs_payload = banks[_bank_pk]
        subtask('do_request_ec_info',args=(_bank_pk,ec_jobs_payload,)).apply_async()

@task(name='do_request_ec_info')
def do_request_ec_info(bank_pk,payload):
    _bank = Bank.objects.get(slug=bank_pk)

    _data_source = KycDataSource.objects.filter(bank=_bank)
    if _data_source.exists():
        _data_source = _data_source.first()
        if _data_source.status is None:
            ec_status = EcStatus()
            ec_status.save()
            _data_source.status = ec_status
            _data_source.save()
        try:
            ip_bank = _data_source.ip_bank
            ec_info_req = requests.post('https://{}:4800/nid-info-request'.format(ip_bank),allow_redirects=False, verify=False, \
                timeout=3,data=json.dumps(payload),headers={'Content-Type': 'text/plain'})
            if ec_info_req.status_code == 200:
                if ec_info_req.json()['status'] == 'success':
                    ec_status_model = _data_source.status
                    ec_status_model.agent_status = 'stable'
                    ec_status_model.save()
                    for _payload in payload:
                        _customer = CustomerProfile.objects.filter(nid_no=_payload['nid'], dob=_payload['dob'], bank=_bank)
                        if _customer.exists():
                            _customer = _customer.first()
                            _customer.verification_status = 'ec_requested'
                            _customer.save()

        except:
            ec_status_model = _data_source.status
            ec_status_model.agent_status = 'unreachable'
            ec_status_model.save()

@task
def do_ec_ocr_face_verification(ec_id_image, ec_photo, nid_no):
    customer_profile = CustomerProfile.objects.filter(nid_no=nid_no)
    print('ocr verification running')
    print('count', customer_profile.count())
    if customer_profile.exists():
        customer_profile = customer_profile.first()

        customer_profile_nid_data = {'id_no_nid': str(customer_profile.nid_no), \
            'birth_nid': customer_profile.dob, 'name_b_nid' :customer_profile.customer_name_ben, \
            'name_e_nid': customer_profile.customer_name_eng, 'father_nid': customer_profile.father_name_ben, \
            'mother_nid': customer_profile.mother_name_ben, 'pres_addr_nid': customer_profile.pres_address_ben, \
            'spouse_nid':customer_profile.spouse_name_ben,'perm_addr_nid': customer_profile.perm_address_ben}
        
        ocr_comparison_result = None
        face_app_comparison_result = None
        face_nid_comparison_result = None

        for key in customer_profile_nid_data:
            value = customer_profile_nid_data[key]
            if value is None:
                customer_profile_nid_data[key] = ''
        try:
            print(customer_profile_nid_data)
            print('ec_images id : photo', ec_id_image, ec_photo)
            ocr_comparison_result = do_ocr_ec_compare(settings.EC_TEMP_DIR+ '/' + ec_id_image, customer_profile_nid_data)
            print('ocr comparison result', ocr_comparison_result)
        except:
            print('ocr service issue')
        try:
            face_app_comparison_result = match_faces(settings.EC_TEMP_DIR+ '/' + ec_photo, settings.NID_UPLOAD_DIR+ '/' + customer_profile.customer_photo_from_app_image)
            print('face app', face_app_comparison_result)
        except:
            print('face app issue')
        try:
            face_nid_comparison_result = match_faces(settings.EC_TEMP_DIR+ '/' + ec_photo, settings.NID_UPLOAD_DIR+ '/' + customer_profile.customer_photo_from_card_image)
            print('face nid', face_nid_comparison_result)
        except:
            print('face nid issue')

        scores = customer_profile.verification_scores
        if scores is None:
            scores = CustomerVerificationScores()
            scores.save()
            customer_profile.verification_scores = scores
            # customer_profile.save()

        if ocr_comparison_result is not None:
            scores.customer_name_eng_score = int(ocr_comparison_result['name_e_match'])
            scores.customer_name_ben_score = int(ocr_comparison_result['name_b_match'])
            scores.father_name_score = int(ocr_comparison_result['father_match'])
            scores.mother_name_score = int(ocr_comparison_result['mother_match'])
            scores.present_addrress_score = int(ocr_comparison_result['pres_addr_match'])
        else:
            scores.customer_name_eng_score = 0
            scores.customer_name_ben_score = 0
            scores.father_name_score = 0
            scores.mother_name_score = 0
            scores.present_addrress_score = 0
        
        if face_app_comparison_result is not None:  
            scores.customer_photo_app_score = int(face_app_comparison_result['score'])
        else:
            scores.customer_photo_app_score = 0
        
        if face_nid_comparison_result is not None:
            scores.customer_photo_card_score = int(face_nid_comparison_result['score'])
        else:
            scores.customer_photo_card_score = 0

        match_min_scores = BankSetting.objects.filter(bank=customer_profile.bank)
        # match_min_scores = get_bank_settings(customer_profile.bank)
        textual_pass = False
        face_app_pass = False
        face_app_other_pass = False
        face_card_pass = False
        if match_min_scores.exists():
            textual_pass = True
            face_app_pass = False
            face_card_pass = False
            for param in match_min_scores:
                _param = param.param
                _value = param.value
                if _param == 'customer_name_eng_thresh':
                    if scores.customer_name_eng_score < int(_value):
                        textual_pass = textual_pass and False
                        scores.customer_name_eng_status = 'failed'
                    else:
                        scores.customer_name_eng_status = 'passed'
                elif _param == 'customer_name_ben_thresh':
                    if scores.customer_name_ben_score < int(_value):
                        textual_pass = textual_pass and False
                        scores.customer_name_ben_status = 'failed'
                    else:
                        scores.customer_name_ben_status = 'passed'
                elif _param == 'father_name_thresh':
                    if scores.father_name_score < int(_value) and len(customer_profile_nid_data['spouse_nid']) < 2:
                        textual_pass = textual_pass and False
                        scores.father_name_status = 'failed'
                    else:
                        scores.father_name_status = 'passed'
                elif _param == 'mother_name_thresh':
                    if scores.mother_name_score < int(_value) and len(customer_profile_nid_data['spouse_nid']) < 2:
                        textual_pass = textual_pass and False
                        scores.mother_name_status = 'failed'
                    else:
                        scores.mother_name_status = 'passed'

            if scores.customer_photo_app_score >= 64:
                    face_app_pass = True
            if scores.customer_photo_card_score >= 64:
                    face_card_pass = True

            scores.customer_photo_card_status = 'passed' if face_card_pass else 'failed'
            scores.customer_photo_app_status = 'passed' if face_app_pass else 'failed'
            scores.textual_info_match_status = 'passed' if textual_pass else 'failed'

            if face_app_pass and face_card_pass and textual_pass:
                customer_profile.verification_status = 'passed'
            else:
                customer_profile.verification_status = 'failed'
            
            scores.save()
            customer_profile.save()

            verification_callback(customer_profile)



@task
def send_email_task(subject, body, to):
    send_mail(
    subject,
    body,
    settings.EMAIL_HOST_USER,
    [to],
    fail_silently=False,)

@task
def send_sms_task(to, message):
    send_sms(to, message)

@task
def send_otp_task(user_pk):
    user = User.objects.get(pk=user_pk)
    status, otp = generate_otp(user)
    mobile_no = user.mobile_no
    if status and mobile_no is not None:
        try:
            send_otp(mobile_no, otp)
        except:
            pass

@task
def send_otp_task_agent(user_pk, mobile_no):
    user = User.objects.get(pk=user_pk)
    status, otp = generate_otp_agent(user, mobile_no)
    if status and mobile_no is not None:
        try:
            send_otp(mobile_no, otp)
        except:
            pass
@task
def send_email_otp_task(user_pk):
    user = User.objects.get(pk=user_pk)
    status, otp = generate_otp(user)
    mobile_no = user.mobile_no
    if status and mobile_no is not None:
        try:
            send_otp(mobile_no, otp)
        except:
            pass

@task
def send_email_otp_task_agent(user_pk, email):
    user = User.objects.get(pk=user_pk)
    status, otp = generate_otp_agent(user, email)
    if status and email is not None:
        try:
            send_otp_email(email, otp)
        except:
            pass

@task
def send_password_email_task(email, password):
    try:
        send_password_email(email, password)
    except:
        pass
@task
def send_password_reset_email_task(email, link):
    try:
        send_password_reset_email(email, link)
    except:
        pass

@task
def send_tracking_number_email_task(email, tracking_number):
    try:
        send_tracking_number_email(email,tracking_number)
    except:
        pass

@task
def send_tracking_number_sms_task(recipient, tracking_number):
    try:
        send_tracking_number_sms(recipient, tracking_number)
    except:
        pass