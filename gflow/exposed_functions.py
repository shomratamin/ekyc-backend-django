import os
from django.contrib.auth import authenticate
from django.contrib.auth import login as session_login
from django.contrib.auth import logout as session_logout
from app.models import User, verify_otp, verify_otp_joint
from bank.models import Bank, Branch
from app.tasks import send_email_task, send_sms_task, send_otp_task, send_otp_task_agent, send_email_otp_task_agent, \
    do_request_ec_info, send_tracking_number_email_task, send_tracking_number_sms_task, send_password_reset_email_task
from django.db.models import Q
from django.contrib.auth import logout as session_logout
import random
import string
from datetime import datetime, date
from django.utils import timezone, dateparse
from customer.models import CustomerProfile, CustomerAccount, CustomerNominee, CustomerOtherInfo, CustomerScreeningInfo, \
    CustomerVerificationScores, AdditionalServices, TransactionProfile, RiskGrading, RiskAssesment, BranchRelatedInfo, Introducer, \
    OtherBank, OtherBankCard, RiskGradingScore
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from bank.serializers import CustomerSerializer, CustomerListSerializer, CustomerProfileSerializer, CustomerNomineeSerializer, \
    CustomerAccountSerializer, AdditonalServiceSerializer, BranchSerializer, BankSettingsSerializer, \
    CustomerAccountWithProfileSerializer
from django.utils.timezone import make_aware
from app.utils import allowed_file, image_as_base64, is_mobile_no_valid, image_as_secure_uri
from django.conf import settings
from bank.models import BankSetting
from django.db.models import Q
import shutil
from django.core.files.storage import FileSystemStorage
from app.utils import *
from app.query import QueryBuilder
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from collections import OrderedDict
from .serializers import RiskAssesmentSerializer, RiskGradingSerializer, IntroducerSerializer, BranchRelatedInfoSerializer, OtherBankSerializer, \
     OtherBankCardSerializer, RiskGradingScoreSerializer, CustomerProfileReportSerializer, CustomerAccountReportSerializer, CustomerOtherInfoSerializer, TransactionProfileSerializer
from app.risk_grading_helpers import calculate_risk_grading, parse_and_save_risk_grading_scores
from django.contrib.auth.tokens import default_token_generator
from app.utils import generate_profile_pdf

def random_string(stringLength=20):
    """Generate a random string of fixed length """
    letters = ''.join([string.ascii_lowercase, string.ascii_uppercase])
    
    return ''.join(random.choice(letters) for i in range(stringLength))

def expose__generate_random_password():
    return random_string()


def expose__require(pre_condition):
    out = f'pre_condition::::{pre_condition}'
    return out

def expose__login_bank_admin(request, username, password):
    _user = User.objects.filter(Q(username=username) & Q(user_type = 'bank'))

    if _user is None:
        return 'non_existant_user'

    if _user.count() < 1:
        return 'non_existant_user'

    _user = _user.first()
    user = authenticate(username=_user.username, password=password)

    if not user:
        print('invalid credentials')
        print(_user.username)
        return 'invalid_credentials'

    if not user.is_active:
        return 'inactive'

    request.session.set_expiry(settings.BANK_LEAD_ONBOARDING_SESSION_TIMEOUT)
    session_login(request, user)
    print('login success')

    return 'success'

def expose__login(request, email, password):
    _user = User.objects.filter(Q(email=email) & (Q(user_type = 'agent') | Q(user_type = 'customer')))

    if _user is None:
        return 'non_existant_user'

    if _user.count() < 1:
        return 'non_existant_user'

    _user = _user.first()
    user = authenticate(username=_user.username, password=password)

    if not user:
        print('invalid credentials')
        print(_user.username)
        return 'invalid_credentials'

    if user.user_type != 'customer' and user.user_type != 'agent':
        return 'invalid_credentials'

    if not user.is_active:
        return 'inactive'

    request.session.set_expiry(settings.BANK_LEAD_ONBOARDING_SESSION_TIMEOUT)
    session_login(request, user)
    print('login success')

    return 'success'

def expose__login_otp(request,user_pk):
    _user = User.objects.filter(Q(pk=user_pk) & Q(user_type = 'customer'))

    if _user is None:
        return 'non_existant_user'

    if _user.count() < 1:
        return 'non_existant_user'

    _user = _user.first()
    user = authenticate(username=_user.username, password=password)

    if not user:
        print('invalid credentials')
        print(_user.username)
        return 'invalid_credentials'

    if user.user_type != 'customer' and user.user_type != 'agent':
        return 'invalid_credentials'

    if not user.is_active:
        return 'inactive'

    request.session.set_expiry(settings.BANK_LEAD_ONBOARDING_SESSION_TIMEOUT)
    session_login(request, user)
    print('login success')

    return 'success'


def expose__logout(request, app_route):
    session_logout(request._request)
    return f'redirect_to::::/{app_route}/'

def expose__get_customer_pk(mobile_no):
    bank = Bank.objects.filter(is_default=True)
    if bank is not None and bank.count() > 0:
        bank = bank.first()
    else:
        return -1
    user = User.objects.filter(mobile_no=mobile_no, user_type='customer')
    if user is not None and user.count() > 0:
        user = user.first()
        return user.id
    else:
        return -2

def expose__get_customers_report(request):
    page = request.query_params.get('page')
    per_page = request.query_params.get('per_page')

    if page is None:
        page = '1'
    if per_page is None:
        per_page = '20'

    if page.isnumeric():
        page = int(page)
    else:
        page = 1
    if per_page.isnumeric():
        per_page = int(per_page)
    else:
        per_page = 1

    bank = request.user.bank
    query_builder = QueryBuilder(CustomerProfile, request)
    query = query_builder.get_query()
    all_customers = CustomerProfile.objects.filter(query, bank=bank)
    total_customers = all_customers.count()
    paginator = Paginator(all_customers, per_page)

    try:
        customers = paginator.page(page)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    

    serialized_data = CustomerProfileReportSerializer(customers, many=True)
    return OrderedDict({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_customers,'data': serialized_data.data})


def expose__get_accounts_report(request):
    page = request.query_params.get('page')
    per_page = request.query_params.get('per_page')

    if page is None:
        page = '1'
    if per_page is None:
        per_page = '20'

    if page.isnumeric():
        page = int(page)
    else:
        page = 1
    if per_page.isnumeric():
        per_page = int(per_page)
    else:
        per_page = 1

    bank = request.user.bank
    query_builder = QueryBuilder(CustomerAccount, request)
    query = query_builder.get_query()
    all_accounts = CustomerAccount.objects.filter(query, Q(customer__bank=bank))
    total_accounts = all_accounts.count()
    paginator = Paginator(all_accounts, per_page)

    try:
        accounts = paginator.page(page)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)
    

    serialized_data = CustomerAccountReportSerializer(accounts, many=True)
    return OrderedDict({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_accounts,'data': serialized_data.data})


def expose__register_customer(mobile_no, email, password):
    username = random_string()
    bank = Bank.objects.filter(is_default=True)
    if bank is not None and bank.count() > 0:
        bank = bank.first()
    else:
        return -1
    user = User.objects.filter(mobile_no=mobile_no, user_type='customer')
    if user is not None and user.count() > 0:
        user = user.first()
        # if user.is_verified:
        #     return user.id
        # user.mobile_no = mobile_no
        # user.email = email
    else:
        user = User(username=username, email=email, mobile_no=mobile_no, user_type='customer', bank=bank, is_verified = False)
    user.set_password(password)
    user.save()
    return user.id


def expose__go_to_page(page):
    out = f'redirect_to::::{page}'
    return out

def expose__send_email_async(subject, body, to):
    send_email_task.delay(subject, body, to)
    return ' '

def expose__send_sms_async(to, message):
    send_sms_task.delay(to, message)
    return ' '

def expose__send_otp(request, user_pk, mobile_no):
    if request.user.is_anonymous:
        send_otp_task.delay(user_pk)
    else:
        send_otp_task_agent.delay(user_pk, mobile_no)

        print('otp mobile agent', mobile_no)

    return f'set_cookie::::cmb={mobile_no}=300'

def expose__resend_otp(request, user_pk, mobile_no):
    if request.user.is_anonymous:
        send_otp_task.delay(user_pk)
    else:
        send_otp_task_agent.delay(user_pk, mobile_no)

        print('otp mobile agent', mobile_no)

def expose__set_cookie(key, value, expire):
    return f'set_cookie::::{key}={value}={expire}'

def is_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def expose__send_otp_email(request, user_pk, email):
    if request.user.is_anonymous:
        send_email_otp_task.delay(user_pk)
    else:
        send_email_otp_task_agent.delay(user_pk, email)

        print('otp email agent', email)

    return f'set_cookie::::ceml={email}=300'

def expose__resend_otp_email(request, user_pk, email):
    if request.user.is_anonymous:
        send_email_otp_task.delay(user_pk)
    else:
        send_email_otp_task_agent.delay(user_pk, email)

        print('otp email agent', email)

def create_customer_profile(mobile_number, mobile_number_verified, nid_no, dob, bank):
    try:
        customer_profile = CustomerProfile.objects.get(mobile_number=mobile_number, bank=bank)
    except:
        customer_profile = CustomerProfile(mobile_number=mobile_number, mobile_number_verified = mobile_number_verified, nid_no=' ', dob=' ', bank=bank)
        customer_profile.save()
        
    return customer_profile

def expose__verify_otp(request, mobile_or_email, otp):
    status, user = verify_otp(mobile_or_email=mobile_or_email,otp=otp)
    customer_pk = -1
    if not status:
        return [None,None]
    if not user:
        return [None, None]
    bank = user.bank
    update_user_customer_flag = False
    if request.user.is_anonymous:
        update_user_customer_flag = False
        if not user.is_verified:
            user.is_verified = True
            update_user_customer_flag = True
            user.save()

    elif request.user.user_type == 'agent':
        bank = request.user.bank

    customer_profile = create_customer_profile(mobile_number=mobile_or_email, mobile_number_verified = True, nid_no=' ', dob=' ', bank=bank)
    customer_pk = customer_profile.id

    if user.user_type == 'customer' and not user.customer_profile:
        user.customer_profile = customer_profile
        user.save()
    if user.user_type == 'customer':
        session_login(request, user)
    print('customer pk', customer_pk)

    return [user, str(customer_pk)]

def expose__verify_otp_joint(request, user , otp, joint_applicant = 'second'):
    status, mobile_no = verify_otp_joint(user=user,otp=otp)
    customer_pk = -1
    if not status:
        return False

    bank = user.bank
    update_user_customer_flag = False
    customer_profile = None
    if request.user.is_anonymous:
        return False
    elif request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return False
        customer_profile = CustomerProfile.objects.filter(pk=tid, bank= bank)
        if customer_profile.count() < 1:
            return False
        else:
            customer_profile = customer_profile.first()
    elif request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile

    if mobile_no == customer_profile.mobile_number:
        return False

    uuid = request.GET.get('uuid')
    if not uuid:
        return False
    else:
        try:
            if request.user.user_type == 'agent':
                account = CustomerAccount.objects.get(uuid=uuid)
            elif request.user.user_type == 'customer':
                account = CustomerAccount.objects.get(Q(uuid=uuid) & (Q(customer=customer_profile) | Q(joint_second_applicant=customer_profile) | Q(joint_third_applicant=customer_profile)))
        except:
            return False

    if joint_applicant == 'second':
        print('second applicant')
        second_customer = create_customer_profile(mobile_number=mobile_no, mobile_number_verified = True, nid_no=' ', dob=' ', bank=bank)
        account.joint_second_applicant = second_customer
        account.save()
    
    if joint_applicant == 'third':
        third_customer = create_customer_profile(mobile_number=mobile_no, mobile_number_verified = True, nid_no=' ', dob=' ', bank=bank)
        account.joint_third_applicant = third_customer
        account.save()
    
    return True

def expose__verify_otp_email(request, email, otp, customer_pk = -1):
    status, user = verify_otp(mobile_or_email=email,otp=otp)
    if not status:
        return [None,None]
    if not user:
        return [None, None]
    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
        if customer_profile is not None:
            customer_profile.email = email
            customer_profile.email_verified = True
            customer_profile.save()
    elif request.user.user_type == 'agent':
        if customer_pk != -1:
            customer_profile = CustomerProfile.objects.filter(pk=customer_pk)
            if customer_profile.exists():
                customer_profile = customer_profile.first()
                customer_profile.email = email
                customer_profile.email_verified = True
                customer_profile.save()
    return [user, str(customer_pk)]

def expose__get_current_year():
    now = datetime.now()
    return now.year

def expose__length(anything):
    return len(anything)

def expose__len(anything):
    return len(anything)

def expose__to_json(input):
    return json.dumps(input)

def expose__to_dict(input):
    return json.loads(input)


def expose__generate_password_reset_token_and_send_email(request, reset_url, email):
    if not request.user.is_anonymous:
        return False, 'User is logged in.'

    user = User.objects.filter(email=email, user_type='agent')
    if user.count() < 1:
        return False, 'Sorry we could not find any associated user with the email.'
    
    user = user.first()

    token = default_token_generator.make_token(user)
    reset_link = f'{reset_url}?uid={user.id}&token={token}'
    print('reset link', reset_link)
    send_password_reset_email_task.delay(email, reset_link)
    return True, "success"

def expose__reset_password(request, new_password, new_password_confirm):
    if not request.user.is_anonymous:
        return False, 'User is logged in.'

    uid = request.GET.get('uid')
    token = request.GET.get('token')
    try:
        user = User.objects.get(pk=uid, user_type='agent')
    except:
        return False, 'User not found'

    is_valid = default_token_generator.check_token(user, token)

    if not is_valid:
        return False, 'Token is not valid'

    if new_password != new_password_confirm:
        return False, 'Passwords do not match'

    user.set_password(new_password)
    user.save()

    return True, 'Password was reset successfully'

    
    

def expose__format_date(_date):
    if _date is None:
        return ''
    try:
        _date = timezone.localtime(_date)
        date = _date.strftime('%b %d %Y %I:%M:%S %p')
        # date = make_aware(date)
        return date
    except:
        date = dateparse.parse_datetime(_date)
        date = date.strftime('%b %d %Y %I:%M:%S %p')
        return date

def expose__get_my_accounts(request):
    if request.user.is_anonymous:
        return False

    if request.user.user_type == 'agent':
        return False

    if request.user.user_type == 'customer':
        accounts = CustomerAccount.objects.filter(customer=request.user.customer_profile)
        if accounts.count() < 1:
            return False
        accounts_data = CustomerAccountWithProfileSerializer(accounts, many= True).data

        return accounts_data

def expose__get_customers(request, expose_all=False):
    print('expose all', expose_all)
    status = request.query_params.get('cstatus')
    page = request.query_params.get('page')
    per_page = request.query_params.get('per_page')
    search = request.POST.get('search')

    
    if status is None:
        status = 'all_tn'
    if page is None:
        page = '1'
    if per_page is None:
        per_page = '20'

    

    if page.isnumeric():
        page = int(page)
    else:
        page = 1
    if per_page.isnumeric():
        per_page = int(per_page)
    else:
        per_page = 1
    
    user_branch = request.user.branch
    branch_code = None
    if user_branch is not None:
        branch_code = user_branch.code

    if expose_all and branch_code is not None:
        if search is not None:
            search = search.upper()
            customers_data = CustomerAccount.objects.filter(Q(customer__bank=request.user.bank) & (Q(customer__nid_no__icontains=search) | \
                Q(tracking_number__icontains=search) | Q(customer__mobile_number__icontains=search))).order_by('-submitted_on')
        else:
            if status == 'all' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank).order_by('-submitted_on')
            elif status == 'all_tn' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, tracking_number__isnull = False).order_by('-submitted_on')
            elif status == 'submitted' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, tracking_number__isnull = False).order_by('-submitted_on')
            elif status == 'ongoing' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, tracking_number__isnull = True).order_by('-submitted_on')
            elif user_branch:
                customers_data = CustomerAccount.objects.filter(customer__verification_status=status, customer__bank=request.user.bank).order_by('-submitted_on')
            else:
                customers_data = CustomerAccount.objects.none()
    elif branch_code is not None:
        if search is not None:
            search = search.upper()
            customers_data = CustomerAccount.objects.filter(Q(customer__bank=request.user.bank) & (Q(customer__nid_no=search) | \
                Q(tracking_number=search) | Q(customer__mobile_number=search))).order_by('-submitted_on')
        else:
            if status == 'all' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, preferred_branch_code = branch_code).order_by('-submitted_on')
            elif status == 'all_tn' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, preferred_branch_code = branch_code, tracking_number__isnull = False).order_by('-submitted_on')
            elif status == 'submitted' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, preferred_branch_code = branch_code, tracking_number__isnull = False).order_by('-submitted_on')
            elif status == 'ongoing' and user_branch:
                customers_data = CustomerAccount.objects.filter(customer__bank=request.user.bank, preferred_branch_code = branch_code, tracking_number__isnull = True).order_by('-submitted_on')
            elif user_branch:
                customers_data = CustomerAccount.objects.filter(customer__verification_status=status, customer__bank=request.user.bank, preferred_branch_code= branch_code).order_by('-submitted_on')
            else:
                customers_data = CustomerAccount.objects.none()
    else:
        customers_data = CustomerAccount.objects.none()


    paginator = Paginator(customers_data, per_page)

    try:
        customers = paginator.page(page)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return [customers, paginator.num_pages, page]

def generate_tracking_number(branch_code):
    tracking_number = random_string(4)
    if branch_code:
        tracking_number = ''.join([branch_code, tracking_number])
    tracking_number = tracking_number.upper()
    return tracking_number

def nid_exists(_nid_no):
    _nid = CustomerProfile.objects.filter(nid_no=_nid_no).exists()
    return _nid

def handle_nid_front(id_front, customer_profile, form_errors):
    if allowed_file(id_front.name):
        fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
        id_front_file_name = fs.save(filename_to_hash(id_front.name), id_front)
        __id_card_photo_file_name = id_front_file_name + '_crop_.jpg'
        # __ = fs.save(__id_card_photo_file, id_front)
        id_front_file_path = os.path.join(settings.NID_UPLOAD_DIR, id_front_file_name)
        __id_card_photo_file_path = os.path.join(settings.NID_UPLOAD_DIR, __id_card_photo_file_name)
        __ = crop_id(id_front_file_path,width=950)
        shutil.copy(id_front_file_path, __id_card_photo_file_path)
        try:
            face_region = face_detection_service(id_front_file_path)
            ocr_out_front = do_ocr_id_front_back(id_front_file_path, face_region=face_region)
            print('ocr front', ocr_out_front)

            if ocr_out_front['id_no_nid'] == 'none' or ocr_out_front['birth_nid'] == 'none':
                form_errors = 'Please upload a valid nid front side'
                return customer_profile, form_errors
            if(nid_exists(ocr_out_front['id_no_nid'])):
                form_errors = "Nid already exists"
                return customer_profile, form_errors

            setattr(customer_profile, 'nid_front_image' , id_front_file_name)
            setattr(customer_profile, 'customer_photo_from_card_image' , __id_card_photo_file_name)
            setattr(customer_profile, 'nid_no' , ocr_out_front['id_no_nid'] )
            setattr(customer_profile, 'dob' , ocr_out_front['birth_nid'] )
            if ocr_out_front['name_e_nid'] != 'none':
                setattr(customer_profile, 'customer_name_eng' , ocr_out_front['name_e_nid'])
            if ocr_out_front['name_b_nid'] != 'none':
                setattr(customer_profile, 'customer_name_ben' , ocr_out_front['name_b_nid'])
            if ocr_out_front['father_nid'] != 'none':
                setattr(customer_profile, 'father_name_ben' , ocr_out_front['father_nid'])
            if ocr_out_front['mother_nid'] != 'none':
                setattr(customer_profile, 'mother_name_ben' , ocr_out_front['mother_nid'])
            if ocr_out_front['spouse_nid'] != 'none':
                setattr(customer_profile, 'spouse_name_ben' , ocr_out_front['spouse_nid'])
        except:
            pass
    return customer_profile, form_errors

def handle_nid_back(id_back, customer_profile, form_errors):
    if allowed_file(id_back.name):
        fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
        id_back_file_name = fs.save(filename_to_hash(id_back.name), id_back)
        id_back_file_path = os.path.join(settings.NID_UPLOAD_DIR, id_back_file_name)
        __ = crop_id(id_back_file_path, width=1050)
        print(id_back_file_name)
        try:
            ocr_out_back = do_ocr_id_front_back(id_back_file_path, face_region=None)
            print('back out',ocr_out_back)
            if ocr_out_back and ocr_out_back['addr'] == 'none':
                form_errors = 'Please upload valid nid back side'
                return customer_profile, form_errors
            setattr(customer_profile, 'nid_back_image' ,id_back_file_name )
            setattr(customer_profile, 'perm_address_ben' , ocr_out_back['addr'] )
        except:
            pass
    return customer_profile, form_errors

def handle_photo(photo, customer_profile, field):
    if allowed_file(photo.name):
        fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
        photo_file_name = fs.save(filename_to_hash(photo.name), photo)
        # customer_photo_other_file_path = os.path.join(settings.NID_UPLOAD_DIR, customer_photo_other_file_name)
        setattr(customer_profile, field ,photo_file_name)
    return customer_profile

def handle_nominee_photo(photo, nominee, field):
    if allowed_file(photo.name):
        fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
        photo_file_name = fs.save(filename_to_hash(photo.name), photo)
        # customer_photo_other_file_path = os.path.join(settings.NID_UPLOAD_DIR, customer_photo_other_file_name)
        setattr(nominee, field ,photo_file_name )
    return nominee

def handle_image(handle_object, field, value, form_errors):
    if field == 'nid_front_image':
        handle_object , form_errors = handle_nid_front(value, handle_object, form_errors)
    elif field == 'nid_back_image':
        handle_object , form_errors = handle_nid_back(value, handle_object, form_errors)
    else:
        try:
            fs = FileSystemStorage(location=settings.NID_UPLOAD_DIR)
            file_name = fs.save(filename_to_hash(value.name), value)
            setattr(handle_object , field , file_name)
        except:
            pass
    return handle_object, form_errors

def handle_image_base64(handle_object, field, value, form_errors):
    image = base64_to_image(value)
    if image is None:
        return handle_object, form_errors

    field = '_'.join(field.split('_')[:-1])
    handle_object, form_errors = handle_image(handle_object, field, image, form_errors)
    return handle_object, form_errors

def handle_fields(handle_object, prefix, values, form_errors):
    for key in values:
        if key == 'id':
            continue

        value = values[key]
        print(prefix, key, ':')

        if key.endswith('_base64'):
            handle_object, form_errors = handle_image_base64(handle_object, key, value, form_errors)
        elif key.endswith('_image'):
            handle_object, form_errors = handle_image(handle_object, key, value, form_errors)
        else:
            setattr(handle_object, key, value)

    handle_object.save()
    if prefix == 'risk_grading':
        try:
            risk_scores = calculate_risk_grading(handle_object)
            if risk_scores:
                risk_scores_model = RiskGradingScore.objects.filter(customer=handle_object.customer)
                if risk_scores_model.count() < 1:
                    risk_scores_model = RiskGradingScore(customer=handle_object.customer)
                else:
                    risk_scores_model = risk_scores_model.first()

                status = parse_and_save_risk_grading_scores(risk_scores_model, risk_scores)
            else:
                return form_errors
        except Exception as e:
            print('aml exception',e)
    return form_errors

def create_customer_account(request, customer_pk=None):
    if not request.user.is_authenticated:
        return False

    if request.user.user_type == 'agent':
        if not customer_pk:
            tid = request.GET.get('tid')
            if not tid:
                return False
        else:
            tid = customer_pk

    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
    else:
        try:
            customer_profile = CustomerProfile.objects.get(pk=tid, bank=request.user.bank)
        except:
            return False

    account = CustomerAccount(customer=customer_profile)
    account.save()

    nominee = CustomerNominee(nominee_index=0, bank_account=account)
    nominee.save()

    customer_profile.editing_account_uuid = account.uuid
    customer_profile.save()

    return account.uuid

def expose__create_customer_account(request, customer_pk=None):
    return create_customer_account(request, customer_pk)

def save_customer_profile(request, pk=-1):
    reject_list = ('id','uuid','user','tracking_number','account_status','on_boarded_by','screening_status', 'screening_info', 'verification_status',\
        'verification_scores', 'email_verified', 'mobile_number_verified', 'editing_account_type',\
        'bank', 'created_on', 'submitted_on', 'updated_on','customeraccount', 'nominees', \
        'branch_related_info','customer', 'additional_services', 'bank_account', 'first_applicant', 'joint_second_appicant',\
        'joint_third_appicant', 'joint_fourth_appicant', 'joint_fifth_appicant', 'transaction_profile', 'risk_grading', 'risk_assessment', 'branch_related_info', \
         'introducer', 'other_bank', 'other_bank_card', 'otherinfo')

    if not request:
        return False, False

    if request.user.is_anonymous:
        return False, False

    if request.user.user_type == 'agent':
        if not pk:
            return False, False

    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
    else:
        try:
            customer_profile = CustomerProfile.objects.get(pk=pk, bank=request.user.bank)
        except:
            return False, False

    uuid = request.GET.get('uuid')
    if not uuid:
        return False, False
    else:
        try:
            if request.user.user_type == 'agent':
                bank_account = CustomerAccount.objects.get(uuid=uuid)
            elif request.user.user_type == 'customer':
                bank_account = CustomerAccount.objects.get(Q(uuid=uuid) & (Q(customer=customer_profile) | Q(joint_second_applicant=customer_profile) | Q(joint_third_applicant=customer_profile)))
        except:
            return False, False
    
    if bank_account.uuid != customer_profile.editing_account_uuid:
        customer_profile.editing_account_uuid = bank_account.uuid
        customer_profile.save()

    if bank_account.account_operation_type == 'joint':
        customer_profile = bank_account.customer
        joint_second_profile = bank_account.joint_second_applicant
        joint_third_profile = bank_account.joint_third_applicant

    customer_profile_fields = set([f.name for f in CustomerProfile._meta.get_fields()]) # joint
    additional_services_fields = set([f.name for f in AdditionalServices._meta.get_fields()]) # account related
    customer_account_fields = set([f.name for f in CustomerAccount._meta.get_fields()]) # account
    transaction_profile_fields = set([f.name for f in TransactionProfile._meta.get_fields()]) # account related fixed multi dimentional
    risk_grading_fields = set([f.name for f in RiskGrading._meta.get_fields()]) # customer related
    risk_assessment_fields = set([f.name for f in RiskAssesment._meta.get_fields()]) # customer related
    branch_related_fields = set([f.name for f in BranchRelatedInfo._meta.get_fields()]) # account related
    introducer_fields = set([f.name for f in Introducer._meta.get_fields()]) # customer related
    other_bank_fields = set([f.name for f in OtherBank._meta.get_fields()]) # multi dimentional
    other_bank_card_fields = set([f.name for f in OtherBankCard._meta.get_fields()]) # multi dimentional
    account_nominees_fields = set([f.name for f in CustomerNominee._meta.get_fields()]) # multi dimentional

    # field_list = []
    # field_list.extend(['customer_profile.' + f.name for f in CustomerProfile._meta.get_fields()])
    # field_list.extend(['additional_services.' + f.name for f in AdditionalServices._meta.get_fields()])
    # field_list.extend(['bank_account.' + f.name for f in CustomerAccount._meta.get_fields()])
    # field_list.extend(['transaction_profile.' + f.name for f in TransactionProfile._meta.get_fields()])
    # field_list.extend(['risk_grading.' + f.name for f in RiskGrading._meta.get_fields()])
    # field_list.extend(['risk_assessment.' + f.name for f in RiskAssesment._meta.get_fields()])
    # field_list.extend(['branch_related_info.' + f.name for f in BranchRelatedInfo._meta.get_fields()])
    # field_list.extend(['introducer.' + f.name for f in Introducer._meta.get_fields()])
    # field_list.extend(['other_banks.' + f.name for f in OtherBank._meta.get_fields()])
    # field_list.extend(['other_bank_cards.' + f.name for f in OtherBankCard._meta.get_fields()])
    # field_list.extend(['nominees.' + f.name for f in CustomerNominee._meta.get_fields()])

    # for f in field_list:
    #     print(f"'{f}':[],")

    applicant_group = []
    applicant_group.append(OrderedDict())
    applicant_group.append(OrderedDict())
    applicant_group.append(OrderedDict())

    for key in request.POST:
        dbkey = key
        applicant_index = 0
        key_index = 0
        value = request.POST.get(key)

        if key.count(']') == 2 and key.endswith(']'):
            dbkey = key[:-6]
            key_index = key[-2]
            applicant_index = key[-5]
            try:
                key_index = int(key_index)
                applicant_index = int(applicant_index)
            except:
                continue
        elif key.count(']') == 1 and key.endswith(']'):
            dbkey = key[:-3]
            key_index = 0
            applicant_index = key[-2]
            try:
                applicant_index = int(applicant_index)
            except:
                continue



        if applicant_index > 3:
            continue

        if key_index > 9:
            continue

        data_group = applicant_group[applicant_index]
        _db_key = dbkey

        if _db_key.endswith('_base64'):
            _db_key = '_'.join(dbkey.split('_')[:-1])
            print(_db_key)

        if _db_key in reject_list:
            continue

        if _db_key in customer_profile_fields:
            if not 'customer_profile' in data_group:
                data_group['customer_profile'] = OrderedDict()
            data_group['customer_profile'][dbkey] = value

        elif _db_key in additional_services_fields:
            if not 'additional_services' in data_group:
                data_group['additional_services'] = OrderedDict()
            data_group['additional_services'][dbkey] = value

        elif _db_key in customer_account_fields:
            if not 'bank_account' in data_group:
                data_group['bank_account'] = OrderedDict()
            data_group['bank_account'][dbkey] = value

        elif _db_key in risk_grading_fields:
            if not 'risk_grading' in data_group:
                data_group['risk_grading'] = OrderedDict()
            data_group['risk_grading'][dbkey] = value

        elif _db_key in risk_assessment_fields:
            if not 'risk_assessment' in data_group:
                data_group['risk_assessment'] = OrderedDict()
            data_group['risk_assessment'][dbkey] = value

        elif _db_key in branch_related_fields:
            if not 'branch_related' in data_group:
                data_group['branch_related'] = OrderedDict()
            data_group['branch_related'][dbkey] = value

        elif _db_key in introducer_fields:
            if not 'introducer' in data_group:
                data_group['introducer'] = OrderedDict()
            data_group['introducer'][dbkey] = value

        # multi dimentional handling
        elif _db_key in transaction_profile_fields:
            if not 'transaction_profile' in data_group:
                data_group['transaction_profile'] = [OrderedDict()]
            if len(data_group['transaction_profile']) < key_index + 1:
                upto = key_index + 1 - len(data_group['transaction_profile'])
                for _i in range(upto):
                    data_group['transaction_profile'].append(OrderedDict())
            try:
                data_group['transaction_profile'][key_index][dbkey] = int(value)
            except:
                if dbkey == 'transaction_channel':
                    data_group['transaction_profile'][key_index][dbkey] = value
                else:
                    data_group['transaction_profile'][key_index][dbkey] = 0
        

        # multi dimentional handling 
        elif _db_key in other_bank_fields:
            if not 'other_banks' in data_group:
                data_group['other_banks'] = [OrderedDict()]
            if len(data_group['other_banks']) < key_index + 1:
                upto = key_index + 1 - len(data_group['other_banks'])
                for _i in range(upto):
                    data_group['other_banks'].append(OrderedDict())
            data_group['other_banks'][key_index][dbkey] = value

        # multi dimentional handling
        elif _db_key in other_bank_card_fields:
            if not 'other_bank_cards' in data_group:
                data_group['other_bank_cards'] = [OrderedDict()]
            if len(data_group['other_bank_cards']) < key_index + 1:
                upto = key_index + 1 - len(data_group['other_bank_cards'])
                for _i in range(upto):
                    data_group['other_bank_cards'].append(OrderedDict())
            data_group['other_bank_cards'][key_index][dbkey] = value

        # multi dimentional handling
        elif _db_key in account_nominees_fields:
            if not 'nominees' in data_group:
                data_group['nominees'] = [OrderedDict()]
            if len(data_group['nominees']) < key_index + 1:
                upto = key_index + 1 - len(data_group['nominees'])
                for _i in range(upto):
                    data_group['nominees'].append(OrderedDict())
            data_group['nominees'][key_index][dbkey] = value
        
        applicant_group[applicant_index] = data_group

    form_errors = None

    for i, data_group in enumerate(applicant_group):
        for prefix in data_group:
            if i == 0:
                if prefix == 'customer_profile':
                    form_errors = handle_fields(customer_profile, prefix, data_group[prefix], form_errors)

                elif prefix == 'additional_services':
                    if not bank_account.additional_services:
                        additional_services = AdditionalServices()
                        additional_services.save()
                        bank_account.additional_services = additional_services
                        bank_account.save()
                    else:
                        additional_services = bank_account.additional_services
                    form_errors = handle_fields(additional_services, prefix, data_group[prefix], form_errors)

                elif prefix == 'bank_account':
                    form_errors = handle_fields(bank_account, prefix, data_group[prefix], form_errors)
                elif prefix == 'transaction_profile':
                    for j , tp in enumerate(data_group[prefix]):
                        tp_profile =  TransactionProfile.objects.filter(customer=customer_profile, transaction_channel_index = j)
                        if tp_profile.count() < 1:
                            tp_profile = TransactionProfile(customer=customer_profile, transaction_channel_index = j)
                        else:
                            tp_profile = tp_profile.first()
                        form_errors = handle_fields(tp_profile, prefix, tp, form_errors)

                elif prefix == 'risk_grading':
                    risk_grading = RiskGrading.objects.filter(customer=customer_profile)
                    if risk_grading.count() < 1:
                        risk_grading = RiskGrading(customer=customer_profile)
                    else:
                        risk_grading = risk_grading.first()

                    form_errors = handle_fields(risk_grading, prefix, data_group[prefix], form_errors)

                elif prefix == 'risk_assessment':
                    risk_assessment = RiskAssesment.objects.filter(customer=customer_profile)
                    if risk_assessment.count() < 1:
                        risk_assessment = RiskAssesment(customer=customer_profile)
                    else:
                        risk_assessment = risk_assessment.first()

                    form_errors = handle_fields(risk_assessment, prefix, data_group[prefix], form_errors)
                
                elif prefix == 'branch_related':
                    branch_related_info = BranchRelatedInfo.objects.filter(customer=customer_profile)
                    if branch_related_info.count() < 1:
                        branch_related_info = BranchRelatedInfo(customer=customer_profile)
                    else:
                        branch_related_info = branch_related_info.first()

                    form_errors = handle_fields(branch_related_info, prefix, data_group[prefix], form_errors)

                elif prefix == 'introducer':
                    introducer_info = Introducer.objects.filter(customer=customer_profile)
                    if introducer_info.count() < 1:
                        introducer_info = Introducer(customer=customer_profile)
                    else:
                        introducer_info = introducer_info.first()

                    form_errors = handle_fields(introducer_info, prefix, data_group[prefix], form_errors)

                elif prefix == 'other_banks':
                    for j , ob in enumerate(data_group[prefix]):
                        other_bank =  OtherBank.objects.filter(customer=customer_profile, otherbank_index = j)
                        if other_bank.count() < 1:
                            other_bank = OtherBank(customer=customer_profile, otherbank_index = j)
                        else:
                            other_bank = other_bank.first()
                        form_errors = handle_fields(other_bank, prefix, ob, form_errors)

                elif prefix == 'other_bank_cards':
                    for j , obc in enumerate(data_group[prefix]):
                        other_bank_card =  OtherBankCard.objects.filter(customer=customer_profile, otherbankcard_index = j)
                        if other_bank_card.count() < 1:
                            other_bank_card = OtherBankCard(customer=customer_profile, otherbankcard_index = j)
                        else:
                            other_bank_card = other_bank_card.first()
                        form_errors = handle_fields(other_bank_card, prefix, obc, form_errors)

                elif prefix == 'nominees':
                    for j , nomi in enumerate(data_group[prefix]):
                        nominee =  CustomerNominee.objects.filter(bank_account=bank_account, nominee_index = j)
                        if nominee.count() < 1:
                            nominee = CustomerNominee(bank_account=bank_account, nominee_index = j)
                        else:
                            nominee = nominee.first()
                        form_errors = handle_fields(nominee, prefix, nomi, form_errors)
            
            elif i == 1 and bank_account.account_operation_type == 'joint':
                if joint_second_profile is None:
                    continue

                if prefix == 'customer_profile':
                    form_errors = handle_fields(joint_second_profile, prefix, data_group[prefix], form_errors)

                elif prefix == 'other_banks':
                    for j , ob in enumerate(data_group[prefix]):
                        other_bank =  OtherBank.objects.filter(customer=joint_second_profile, otherbank_index = j)
                        if other_bank.count() < 1:
                            other_bank = OtherBank(customer=joint_second_profile, otherbank_index = j)
                        else:
                            other_bank = other_bank.first()
                        form_errors = handle_fields(other_bank, prefix, ob, form_errors)

                elif prefix == 'other_bank_cards':
                    for j , obc in enumerate(data_group[prefix]):
                        other_bank_card =  OtherBankCard.objects.filter(customer=joint_second_profile, otherbankcard_index = j)
                        if other_bank_card.count() < 1:
                            other_bank_card = OtherBankCard(customer=joint_second_profile, otherbankcard_index = j)
                        else:
                            other_bank_card = other_bank_card.first()
                        form_errors = handle_fields(other_bank_card, prefix, obc, form_errors)

            elif i == 2 and bank_account.account_operation_type == 'joint':
                if joint_third_profile is None:
                    continue
                if prefix == 'customer_profile':
                    form_errors = handle_fields(joint_third_profile, prefix, data_group[prefix], form_errors)

                elif prefix == 'other_banks':
                    for j , ob in enumerate(data_group[prefix]):
                        other_bank =  OtherBank.objects.filter(customer=joint_third_profile, otherbank_index = j)
                        if other_bank.count() < 1:
                            other_bank = OtherBank(customer=joint_third_profile, otherbank_index = j)
                        else:
                            other_bank = other_bank.first()
                        form_errors = handle_fields(other_bank, prefix, ob, form_errors)

                elif prefix == 'other_bank_cards':
                    for j , obc in enumerate(data_group[prefix]):
                        other_bank_card =  OtherBankCard.objects.filter(customer=joint_third_profile, otherbankcard_index = j)
                        if other_bank_card.count() < 1:
                            other_bank_card = OtherBankCard(customer=joint_third_profile, otherbankcard_index = j)
                        else:
                            other_bank_card = other_bank_card.first()
                        form_errors = handle_fields(other_bank_card, prefix, obc, form_errors)

    for key in request.POST:
        if key.startswith('otherinfo_'):
            _keys = key.split('_')
            _key = '_'.join(_keys[1:])
            f_value = request.POST.get(key)
            _otherinfo = CustomerOtherInfo.objects.filter(customer=customer_profile, info_key=_key)

            if _otherinfo.count() < 1:
                _otherinfo = CustomerOtherInfo(customer=customer_profile, info_key=_key, info_value=f_value)
            else:
                _otherinfo = _otherinfo.first()
                _otherinfo.info_value = f_value
            _otherinfo.save()

    for key in request.POST:
        if key == 'generate_tracking_number':
            tracking_number = generate_tracking_number(bank_account.preferred_branch_code)
            print('tracking_number',tracking_number)
            if not bank_account.tracking_number:
                bank_account.tracking_number = tracking_number
                bank_account.save()
            bank_slug = request.user.bank.slug
            payload = [{'nid':customer_profile.nid_no,'dob':customer_profile.dob}]
            try:
                do_request_ec_info.delay(bank_slug,payload)
            except:
                pass

    customer_profile_data = CustomerProfileSerializer(customer_profile).data

    for key in customer_profile_data:
        if key.endswith('_image'):
            if customer_profile_data[key] is not None:
                customer_profile_data[key] = image_as_secure_uri(customer_profile_data[key])

    if bank_account.account_operation_type == 'joint':
        customer_profiles = []
        # print('number of applicant',bank_account.joint_number_of_applicants)
        profile_data = []
        if bank_account.joint_number_of_applicants == 2:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data
            # print(profile_data,'profile data')

        if bank_account.joint_number_of_applicants == 3:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            if joint_third_profile:
                customer_profiles.append(joint_third_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data

        joint_profiles = []

        for profile in profile_data:
            for key in profile:
                if key.endswith('_image'):
                    if profile[key] is not None:
                        profile[key] = image_as_secure_uri(profile[key])
                        
            joint_profiles.append(profile)

        customer_profile_data['customer_profiles'] = joint_profiles

    

    if not bank_account.additional_services:
        additional_services = AdditionalServices()
        additional_services.save()
        bank_account.additional_services = additional_services
        bank_account.save()
    else:
        additional_services = bank_account.additional_services

    customer_nominees = CustomerNominee.objects.filter(bank_account=bank_account)
    if customer_nominees.count() < 1:
        _nominee = CustomerNominee(bank_account=bank_account,nominee_index=0)
        _nominee.save()
        customer_nominees = CustomerNominee.objects.filter(bank_account=bank_account)

    customer_profile_data['bank_account'] = CustomerAccountWithProfileSerializer(bank_account, many= False).data
    customer_other_info = customer_profile.otherinfo.all()
    otherinfos = OrderedDict()
    if customer_other_info.count() > 0:
        for _info in customer_other_info:
            otherinfos[_info.info_key] = _info.info_value
    customer_nominess_data = CustomerNomineeSerializer(customer_nominees, many=True).data
    customer_profile_data['bank'] = request.user.bank.slug
    customer_profile_data['account_nominees'] = customer_nominess_data
    customer_profile_data['otherinfo'] = otherinfos
    customer_profile_data['additional_services'] = AdditonalServiceSerializer(additional_services).data
    customer_profile_data['customer_nominees'] = customer_nominess_data
    customer_profile_data['uuid'] = bank_account.uuid

    return customer_profile_data, form_errors
    
def load_customer_profile(request, pk=-1):
    if not request:
        return False

    if request.user.is_anonymous:
        return False

    if not request.GET.get('uuid') and request.user.user_type == 'customer':
        return False

    if request.user.user_type == 'agent':
        if not pk:
            return False
    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
    else:
        try:
            customer_profile = CustomerProfile.objects.get(pk=pk, bank= request.user.bank)
        except:
            return False

    uuid = request.GET.get('uuid')
    if not uuid:
        return False
    else:
        try:
            if request.user.user_type == 'agent':
                bank_account = CustomerAccount.objects.get(uuid=uuid)
            elif request.user.user_type == 'customer':
                bank_account = CustomerAccount.objects.get(Q(uuid=uuid) & (Q(customer=customer_profile) | Q(joint_second_applicant=customer_profile) | Q(joint_third_applicant=customer_profile)))
        except:
            return False

    if bank_account.account_operation_type == 'joint':
        customer_profile = bank_account.customer
        joint_second_profile = bank_account.joint_second_applicant
        joint_third_profile = bank_account.joint_third_applicant

    customer_profile.updated_on = timezone.localtime(customer_profile.updated_on)
    customer_nominess = bank_account.account_nominees.all()
    customer_other_info = customer_profile.otherinfo.all()
    customer_profile_data = CustomerProfileSerializer(customer_profile).data
    customer_nominess_data = CustomerNomineeSerializer(customer_nominess, many=True).data

    if bank_account.account_operation_type == 'joint':
        customer_profiles = []
        profile_data = []
        if bank_account.joint_number_of_applicants == 2:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data

        if bank_account.joint_number_of_applicants == 3:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            if joint_third_profile:
                customer_profiles.append(joint_third_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data

        joint_profiles = []
        for profile in profile_data:
            for key in profile:
                if key.endswith('_image'):
                    if profile[key] is not None:
                        profile[key] = image_as_secure_uri(profile[key])
                        
            joint_profiles.append(profile)

        customer_profile_data['customer_profiles'] = joint_profiles

    for key in customer_profile_data:
        if key.endswith('_image'):
            if customer_profile_data[key] is not None:
                customer_profile_data[key] = image_as_secure_uri(customer_profile_data[key])

    for nominee in customer_nominess_data:
        for key in nominee:
            if key.endswith('_image'):
                if nominee[key] is not None:
                    nominee[key] = image_as_secure_uri(nominee[key])

    # print(customer_profile_data)
    # customer_profile_data['bank'] = customer_profile_data['bank']['slug']
    # print('bank', request.user.bank)
    # customer_account = CustomerAccount.objects.filter(customer=customer_profile)
    # if customer_account.count() < 1:
    #     customer_account = CustomerAccount(customer=customer_profile)
    #     customer_account.save()
    # else:
    #     customer_account = customer_account.first()

    # additional_services_changed = False
    # if not bank_account.additional_services:
    #     additional_services = AdditionalServices()
    #     additional_services.save()
    #     bank_account.additional_services = additional_services
    #     bank_account.save()
    #     customer_profile_changed = True
    # else:
    #     additional_services = bank_account.additional_services

    print(bank_account)
    customer_profile_data['bank_account'] = CustomerAccountWithProfileSerializer(bank_account, many= False).data
    customer_profile_data['bank'] = request.user.bank.slug
    customer_profile_data['customer_nominees'] = customer_nominess_data
    customer_profile_data['account_nominees'] = customer_nominess_data
    otherinfos = OrderedDict()
    if customer_other_info.count() > 0:
        for _info in customer_other_info:
            otherinfos[_info.info_key] = _info.info_value

    customer_profile_data['otherinfo'] = otherinfos

    if bank_account.id:
        customer_profile_data['uuid'] = bank_account.uuid

    return customer_profile_data

def expose__get_transaction_profile(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return OrderedDict()

        transaction_profile = TransactionProfile.objects.filter(customer_id=tid)
        if transaction_profile.count() < 1:
            return OrderedDict()
        

        transaction_profile_data = OrderedDict()
        for tp_data in transaction_profile:
            key = 'transaction_channel_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_channel
            key = 'transaction_deposit_number_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_deposit_number
            key = 'transaction_deposit_amount_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_deposit_amount
            key = 'transaction_deposit_amount_per_max_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_deposit_amount_per_max
            key = 'transaction_withdraw_number_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_withdraw_number
            key = 'transaction_withdraw_amount_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_withdraw_amount
            key = 'transaction_withdraw_amount_per_max_' + str(tp_data.transaction_channel_index)
            transaction_profile_data[key] = tp_data.transaction_withdraw_amount_per_max

        return transaction_profile_data
    else:
        return OrderedDict()

def expose__get_risk_grading(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return RiskGradingSerializer(RiskGrading()).data

        risk_grading = RiskGrading.objects.filter(customer_id=tid)
        if risk_grading.count() < 1:
            return RiskGradingSerializer(RiskGrading()).data

        risk_grading = risk_grading.first()
        risk_grading_data = RiskGradingSerializer(risk_grading).data

        return risk_grading_data
    else:
        return RiskGradingSerializer(RiskGrading()).data

def expose__get_risk_grading_score(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return RiskGradingScoreSerializer(RiskGradingScore()).data

        risk_grading_score = RiskGradingScore.objects.filter(customer_id=tid)
        if risk_grading_score.count() < 1:
            return RiskGradingScoreSerializer(RiskGradingScore()).data

        risk_grading_score = risk_grading_score.first()
        risk_grading_score_data = RiskGradingScoreSerializer(risk_grading_score).data

        return risk_grading_score_data
    else:
        return RiskGradingScoreSerializer(RiskGradingScore()).data


def expose__get_risk_assessment(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return RiskAssesmentSerializer(RiskAssesment()).data

        risk_assessment = RiskAssesment.objects.filter(customer_id=tid)
        if risk_assessment.count() < 1:
            return RiskAssesmentSerializer(RiskAssesment()).data

        risk_assessment = risk_assessment.first()
        risk_assessment_data = RiskAssesmentSerializer(risk_assessment).data

        return risk_assessment_data
    else:
        return RiskAssesmentSerializer(RiskAssesment()).data

def expose__get_introducer(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return IntroducerSerializer(Introducer()).data

        introducer = Introducer.objects.filter(customer_id=tid)
        if introducer.count() < 1:
            return IntroducerSerializer(Introducer()).data

        introducer = introducer.first()
        introducer_data = IntroducerSerializer(introducer).data

        return introducer_data
    elif request.user.user_type == 'customer':
        introducer = Introducer.objects.filter(customer=request.user.customer_profile)
        if introducer.count() < 1:
            return IntroducerSerializer(Introducer()).data

        introducer = introducer.first()
        introducer_data = IntroducerSerializer(introducer).data

        return introducer_data

def expose__get_branch_related_info(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return BranchRelatedInfoSerializer(BranchRelatedInfo()).data

        bank_related_info = BranchRelatedInfo.objects.filter(customer_id=tid)
        if bank_related_info.count() < 1:
            return BranchRelatedInfoSerializer(BranchRelatedInfo()).data

        bank_related_info = bank_related_info.first()
        bank_related_info_data = BranchRelatedInfoSerializer(bank_related_info).data

        return bank_related_info_data
    else:
        return BranchRelatedInfoSerializer(BranchRelatedInfo()).data

def expose__get_other_banks(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank = OtherBank.objects.filter(customer_id=tid)
        if otherbank.count() < 1:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank_data = OtherBankSerializer(otherbank, many=True).data

        return otherbank_data
    elif request.user.user_type == 'customer':
        otherbank = OtherBank.objects.filter(customer=request.user.customer_profile)
        if otherbank.count() < 1:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank_data = OtherBankSerializer(otherbank, many=True).data

        return otherbank_data

def expose__get_other_bank_cards(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard = OtherBankCard.objects.filter(customer_id=tid)
        if otherbankcard.count() < 1:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard_data = OtherBankCardSerializer(otherbankcard, many=True).data

        return otherbankcard_data
    elif request.user.user_type == 'customer':
        otherbankcard = OtherBankCard.objects.filter(customer=request.user.customer_profile)
        if otherbankcard.count() < 1:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard_data = OtherBankCardSerializer(otherbankcard, many=True).data

        return otherbankcard_data

def expose__get_other_banks_joint(request):
    if request.user.is_anonymous:
        return None


    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank = OtherBank.objects.filter(customer_id=tid)
        if otherbank.count() < 1:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank_data = OtherBankSerializer(otherbank, many=True).data

        return otherbank_data
    elif request.user.user_type == 'customer':
        otherbank = OtherBank.objects.filter(customer=request.user.customer_profile)
        if otherbank.count() < 1:
            return OtherBankSerializer([OtherBank()], many=True).data

        otherbank_data = OtherBankSerializer(otherbank, many=True).data

        return otherbank_data

def expose__get_other_bank_cards_joint(request):
    if request.user.is_anonymous:
        return None

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if tid is None:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard = OtherBankCard.objects.filter(customer_id=tid)
        if otherbankcard.count() < 1:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard_data = OtherBankCardSerializer(otherbankcard, many=True).data

        return otherbankcard_data
    elif request.user.user_type == 'customer':
        otherbankcard = OtherBankCard.objects.filter(customer=request.user.customer_profile)
        if otherbankcard.count() < 1:
            return OtherBankCardSerializer([OtherBankCard()], many=True).data

        otherbankcard_data = OtherBankCardSerializer(otherbankcard, many=True).data

        return otherbankcard_data

def expose__load_customer_profile(request, pk=-1):
    return load_customer_profile(request, pk)

def expose__contains_in(keyword, value):
    value = value.lower()
    keyword = keyword.lower()
    if keyword in value:
        return True
    else:
        return False

def expose__generate_pdf_profile(request):
    if not request:
        return False

    if request.user.is_anonymous:
        return False

    if not request.GET.get('uuid') and request.user.user_type == 'customer':
        return False

    if request.user.user_type == 'agent':
        tid = request.GET.get('tid')
        if not tid:
            return False
    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
    else:
        try:
            customer_profile = CustomerProfile.objects.get(pk=tid, bank= request.user.bank)
        except:
            return False

    uuid = request.GET.get('uuid')
    if not uuid:
        return False
    else:
        try:
            if request.user.user_type == 'agent':
                bank_account = CustomerAccount.objects.get(uuid=uuid, customer = customer_profile)
            elif request.user.user_type == 'customer':
                bank_account = CustomerAccount.objects.get(Q(uuid=uuid) & (Q(customer=customer_profile) | Q(joint_second_applicant=customer_profile) | Q(joint_third_applicant=customer_profile)))
        except:
            return False

    if bank_account.account_operation_type == 'joint':
        customer_profile = bank_account.customer
        joint_second_profile = bank_account.joint_second_applicant
        joint_third_profile = bank_account.joint_third_applicant

    customer_profile.updated_on = timezone.localtime(customer_profile.updated_on)
    customer_nominess = bank_account.account_nominees.all()
    customer_other_info = customer_profile.otherinfo.all()
    customer_other_info_data = CustomerOtherInfoSerializer(customer_other_info, many=True).data
    customer_profile_data = CustomerProfileSerializer(customer_profile).data
    customer_nominess_data = CustomerNomineeSerializer(customer_nominess, many=True).data

    if bank_account.account_operation_type == 'joint':
        customer_profiles = []
        profile_data = []
        if bank_account.joint_number_of_applicants == 2:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data

        if bank_account.joint_number_of_applicants == 3:
            customer_profiles.append(customer_profile)
            if joint_second_profile:
                customer_profiles.append(joint_second_profile)
            if joint_third_profile:
                customer_profiles.append(joint_third_profile)
            profile_data = CustomerProfileSerializer(customer_profiles, many=True).data

        joint_profiles = []
        for profile in profile_data:
            for key in profile:
                if key.endswith('_image'):
                    if profile[key] is not None:
                        profile[key] = image_as_base64(profile[key])
                        
            joint_profiles.append(profile)

        customer_profile_data['customer_profiles'] = joint_profiles

    for key in customer_profile_data:
        if key.endswith('_image'):
            if customer_profile_data[key] is not None:
                _name = os.path.join(settings.NID_UPLOAD_DIR, customer_profile_data[key])
                customer_profile_data[key] = image_as_base64(_name)

    for nominee in customer_nominess_data:
        for key in nominee:
            if key.endswith('_image'):
                if nominee[key] is not None:
                    _name = os.path.join(settings.NID_UPLOAD_DIR, nominee[key])
                    nominee[key] = image_as_base64(_name)

    otherbank = OtherBank.objects.filter(customer=customer_profile)
    otherbank_data = OtherBankSerializer(otherbank, many=True).data
    otherbank_card = OtherBankCard.objects.filter(customer=customer_profile)
    otherbank_card_data = OtherBankCardSerializer(otherbank_card, many=True).data
    additional_services = bank_account.additional_services
    branch_related_info = BranchRelatedInfo.objects.filter(customer=customer_profile)
    if branch_related_info.count() < 1:
        branch_related_info = BranchRelatedInfo(customer=customer_profile)
    else:
        branch_related_info = branch_related_info.first()
    introducer = Introducer.objects.filter(customer=customer_profile)
    if introducer.count() < 1:
        introducer = Introducer(customer=customer_profile)
    else:
        introducer = introducer.first()

    transaction_profile = TransactionProfile.objects.filter(customer=customer_profile)
    if transaction_profile.count() < 1:
        transaction_profile = OrderedDict()
        
    transaction_profile_data = OrderedDict()
    transaction_profile_data['transaction_summary'] = OrderedDict()
    transaction_profile_data['transaction_individual'] = TransactionProfileSerializer(transaction_profile, many=True).data
    for _otherinfo_data in customer_other_info_data:
        print(_otherinfo_data)
        if _otherinfo_data['info_key'] == 'sum_of_number_of_deposits':
            transaction_profile_data['transaction_summary']['transaction_deposit_number'] = _otherinfo_data['info_value']
        elif _otherinfo_data['info_key'] == 'sum_of_amount_of_deposits':
            transaction_profile_data['transaction_summary']['transaction_deposit_amount'] = _otherinfo_data['info_value']
        elif _otherinfo_data['info_key']  == 'sum_of_number_of_withdraws':
            transaction_profile_data['transaction_summary']['transaction_withdraw_number'] = _otherinfo_data['info_value']
        elif _otherinfo_data['info_key']  == 'sum_of_amount_of_withdraws':
            transaction_profile_data['transaction_summary']['transaction_withdraw_amount'] = _otherinfo_data['info_value']

    transaction_profile_data['transaction_summary']['transaction_channel'] = ''
    transaction_profile_data['transaction_summary']['transaction_deposit_amount_per_max'] = ''
    transaction_profile_data['transaction_summary']['transaction_withdraw_amount_per_max'] = ''

    print(transaction_profile_data)

    risk_grading = RiskGrading.objects.filter(customer=customer_profile)
    if risk_grading.count() < 1:
        risk_grading = RiskGrading(customer=customer_profile)
    else:
        risk_grading = risk_grading.first()

    risk_grading_score = RiskGradingScore.objects.filter(customer=customer_profile)
    if risk_grading_score.count() < 1:
        risk_grading_score = RiskGradingScore(customer=customer_profile)
    else:
        risk_grading_score = risk_grading_score.first()

    risk_assessment = RiskAssesment.objects.filter(customer=customer_profile)
    if risk_assessment.count() < 1:
        risk_assessment = RiskAssesment(customer=customer_profile)
    else:
        risk_assessment = risk_assessment.first()


    account_data = CustomerAccountSerializer(bank_account, many= False).data
    account_data['preferred_branch_name'] = convert_branch_code_to_name(request,account_data['preferred_branch_code'])
    print(account_data)
    rg_iter = RiskGradingSerializer(risk_grading, many=False).data
    rg_score = RiskGradingScoreSerializer(risk_grading_score, many=False).data
    risk_grading_data = OrderedDict()
    risk_grading_data['rg_item'] = rg_iter
    risk_grading_data['rg_score'] = rg_score
    customer_profile_data['other_banks'] = otherbank_data
    customer_profile_data['other_bank_cards'] = otherbank_card_data
    customer_profile_data['transaction_profile'] = transaction_profile_data
    customer_profile_data['additional_services'] = AdditonalServiceSerializer(additional_services, many=False).data
    customer_profile_data['risk_grading'] = risk_grading_data
    customer_profile_data['risk_assessment'] = RiskAssesmentSerializer(risk_assessment, many=False).data
    customer_profile_data['introducer'] = IntroducerSerializer(introducer, many=False).data
    customer_profile_data['branch_related_info'] = BranchRelatedInfoSerializer(branch_related_info, many=False).data
    customer_profile_data['nominess'] = customer_nominess_data
    customer_profile_data['accounts'] = [account_data]
    customer_profile_data['bank'] = request.user.bank.slug
    customer_profile_data['otherinfo'] = customer_other_info_data


    if bank_account.id:
        customer_profile_data['uuid'] = bank_account.uuid
    final_data = OrderedDict()
    final_data['BusinessData'] = OrderedDict()
    if bank_account.account_profile_type == 'simplified':
        final_data['BusinessData']['onboardingType'] = 'Simplified'
    else:
        final_data['BusinessData']['onboardingType'] = 'Regular'
    final_data['BusinessData']['data'] = customer_profile_data

    # print(final_data)
    
    try:
        result = generate_profile_pdf(final_data)
        if result['responseStatus'] == True:
            data = result['responseBusinessData']
            return True, data, uuid
        else:
            return False, False, False
    except:
        return False, False, False

def expose__download_as_pdf(data, filename):
    filename = filename + '.pdf'
    output = ''.join(['download_pdf::::',data,'::::', filename])
    return output

def load_bank_settings(request):
    setting_data = BankSetting.objects.filter(bank=request.user.bank)
    setting_data = BankSettingsSerializer(setting_data,many=True).data

    
    processed_settings_data = dict()
    for _settings_data in setting_data:
        if _settings_data['param'].endswith('_options'):
            processed_settings_data[_settings_data['param']] = json.loads(_settings_data['value'])
        else:
            processed_settings_data[_settings_data['param']] = _settings_data['value']


    return processed_settings_data

def expose__load_bank_settings(request):
    return load_bank_settings(request)


def expose__get_bank_branches(request):
    if not request.user.is_authenticated:
        return []

    branches = Branch.objects.filter(bank=request.user.bank, visible_in_form=True)
    if branches.count() < 1:
        return []

    return branches

def expose__branch_code_to_name(request, branch_code):
    branch = Branch.objects.filter(bank=request.user.bank, code = branch_code)
    if branch.count() < 1:
        return ''
    branch = branch.first()
    return branch.name

def convert_branch_code_to_name(request, branch_code):
    branch = Branch.objects.filter(bank=request.user.bank, code = branch_code)
    if branch.count() < 1:
        return ''
    branch = branch.first()
    return branch.name

def expose__send_tracking_number_sms(to, tracking_number):
    send_tracking_number_sms_task.delay(to, tracking_number)

def expose__send_tracking_number_email(to, tracking_number):
    send_tracking_number_email_task.delay(to, tracking_number)

def expose__remove_nominee(request,tid,nominee_index):
    if not request:
        return False

    if request.user.is_anonymous:
        return False

    uuid = request.GET.get('uuid')
    if not uuid:
        return False

    if nominee_index == 0:
        return False

    if request.user.user_type == 'agent':
        if not tid:
            return False
    if request.user.user_type == 'customer':
        customer_profile = request.user.customer_profile
    else:
        customer_profile = CustomerProfile.objects.filter(pk=tid, bank= request.user.bank)
        if customer_profile.count() < 1:
            return False
        customer_profile = customer_profile.first()

    bank_account = CustomerAccount.objects.filter(uuid=uuid)
    if bank_account.count() < 1:
        return

    bank_account = bank_account.first()
    customer_nominess = CustomerNominee.objects.filter(bank_account=bank_account, nominee_index= nominee_index)

    if customer_nominess.count() < 1:
        return False

    if bank_account.customer.id != customer_profile.id:
        return False
    
    customer_nominess = customer_nominess.first()
    print(customer_nominess)
    customer_nominess.delete()
    print(customer_nominess)

    return 'success'





def expose__find_ref(ref_data, key, value):
    ref = ''
    reference_array = ref_data[key]['Reference']
    value_array = ref_data[key]['Value']

    matched_index = None
    if value in value_array:
        matched_index = value_array.index(value)

    if matched_index != None:
        ref = reference_array[matched_index]

    return ref


def expose__get_title(gender, spouse):
    if (gender.lower() == "male"):
        return 'Mr'
    elif (gender.lower() == "female"):
        if spouse and len(spouse) > 0:
            return 'Mrs'
        else:
            return 'Ms'
    else:
        return 'Mr'


def expose__get_short_name(full_name):
    if len(full_name) > 15:
        return full_name[0:15]
    else:
        return full_name


def expose__get_last_name(full_name):
    return full_name.split(' ')[-1]


def expose__get_middle_name(full_name):
    name_words_array = full_name.split(' ')
    if len(name_words_array) > 2:
        return name_words_array[-2]
    else:
        return name_words_array[-1]


def expose__get_first_name(full_name):
    firstname = ''
    lastname = full_name.split(' ')[-1]
    if(len(full_name) - len(lastname)) < 15:
        firstname = full_name.replace(lastname, '')
    else:
        firstname = full_name.split(' ')[0]

    firstname = firstname.strip()
    return firstname



def expose__get_id_type(id_type, nid_no):
    if id_type.lower() == 'NID/Smart Card'.lower():
        if len(nid_no) != 10:
            return 'National ID'
        else:
            return 'Smart NID'

    elif id_type.lower() == 'Passport'.lower():
        return 'Passport'

    elif id_type.lower() == 'Birth Certificate'.lower():
        return 'Birth Certificate'

    elif id_type.lower() == 'Driving License'.lower():
        return 'Driving License'

    else:
        return ''


def expose__get_is_tax_payer(e_tin):
    if e_tin:
        return True
    else:
        return False


def expose__get_tax_reference(e_tin):
    if e_tin:
        return 'TX'
    else:
        return 'TY'


def expose__get_isd(mobile_number):
    if len(mobile_number) == 14 or "+880" in mobile_number:
        return mobile_number[0:4]

    else:
        return ''


def expose__get_contact_number(mobile_number):

    if len(mobile_number) == 14 or "+880" in mobile_number:
        return mobile_number[4:]

    else:
        return ''


def expose__get_ordinal_date(date):
    sdtdate = str(date)
    if '/' in date:
        sdtdate = datetime.strptime(date, '%Y/%m/%d').date()
    elif '-' in date:
        sdtdate = datetime.strptime(date, '%Y-%m-%d').date()
    elif '.' in date:
        sdtdate = datetime.strptime(date, '%Y.%m.%d').date()

    ordinal_date = sdtdate.toordinal()
    return ordinal_date

def expose__get_today():
    sdtdate = ''
    today = date.today()
    str_date = str(today)
    if '/' in str_date:
        print("/")
        sdtdate = datetime.strptime(str_date, '%Y/%m/%d').date()
    elif '-' in str_date:
        print("-")
        sdtdate = datetime.strptime(str_date, '%Y-%m-%d').date()
    elif '.' in str_date:
        print(".")
        sdtdate = datetime.strptime(str_date, '%Y.%m.%d').date()

    ordinal_date = sdtdate.toordinal()
    return ordinal_date


def expose__get_address_type(addr_type):
    if 'present' in addr_type.lower():
        return 'Present Address'
    elif 'professional' in addr_type.lower():
        return 'Professional Address'
    elif 'permanent' in addr_type.lower():
        return 'Permanent Address'
    else:
        return ''


def expose__get_address(data, addr_type):
    if 'present' in addr_type.lower():
        return data['pres_address_eng']
    elif 'professional' in addr_type.lower():
        return data['prof_address_eng']
    elif 'permanent' in addr_type.lower():
        return data['perm_address_eng']
    else:
        return ''

def expose__get_today():
    today = date.today()
    str_date = str(today)
    return str_date

def expose__get_random_number(x):
    return random.randint(10*(x-1), 10*x-1)