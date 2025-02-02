from django.contrib.auth import authenticate
from django.contrib.auth import login as session_login
from django.contrib.auth import logout as session_logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from ..permissions import *
from rest_framework.response import Response
from django.db import IntegrityError
from ..models import User, Bank, OtpAuth, generate_otp, verify_otp
from ..serializers import UserSerializer
from ..sms_helpers import send_otp
from ..utils import is_mobile_no_valid


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    if user.is_active:
        session_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status':'success','token': token.key},
                        status=HTTP_200_OK)
    else:
        return Response({'status':'failed','message': 'sorry, your account is disabled.'}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def otp_request(request):
    mobile_no = request.data.get("mobile_no")
    user_type = request.data.get("user_type")

    if user_type is None or user_type not in User.USER_TYPES_MAP:
        return Response({'status':'failed','error': 'Please provide valid user type.'},
                        status=HTTP_400_BAD_REQUEST)

    if not is_mobile_no_valid(mobile_no):
        return Response({'status':'failed','error': 'Please provide a valid Bangladeshi mobile number without country code.'},
                        status=HTTP_400_BAD_REQUEST)
    user = User.objects.filter(mobile_no=mobile_no, user_type=user_type)
    if not user:
        return Response({'status':'failed','error': 'Invalid mobile number'},
                        status=HTTP_404_NOT_FOUND)
    user = user.first()
    status, otp = generate_otp(user)
    if status:
        try:
            send_otp(mobile_no, otp)
        except: 
            return Response({'status':'failed','detail': 'Could not send SMS.'},
                    status=HTTP_400_BAD_REQUEST) 
        return Response({'status':'success','detail': 'An OTP is sent to your mobile, validity will expire in 3 minutes.'},
                    status=HTTP_200_OK)
    else:
        return Response({'status':'failed','detail': 'Sorry could not generate OTP.'},
                    status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def otp_verify(request):
    mobile_no = request.data.get("mobile_no")
    otp = request.data.get("otp")

    if otp is None:
        return Response({'status':'failed','error': 'Please provide valid OTP.'},
                        status=HTTP_400_BAD_REQUEST)

    if not is_mobile_no_valid(mobile_no):
        return Response({'status':'failed','error': 'Please provide a valid Bangladeshi mobile number without country code.'},
                        status=HTTP_400_BAD_REQUEST)
    status, user = verify_otp(mobile_no=mobile_no,otp=otp)
    if not status:
        return Response({'status':'failed','error': 'Sorry could not verify.'},
                        status=HTTP_401_UNAUTHORIZED)

    if not user:
        return Response({'status':'failed','error': 'Sorry could not verify.'},
                        status=HTTP_404_NOT_FOUND)
    if user.is_active:
        print(user.id, user.mobile_no)
        session_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status':'success','token': token.key},
                    status=HTTP_200_OK)
    else:
        return Response({'status':'failed','message': 'sorry, your account is disabled.'}, status=HTTP_200_OK)



@csrf_exempt
@api_view(["GET"])
def logout(request):
    request.user.auth_token.delete()
    session_logout(request._request)
    return Response({'detail': 'User successfully logged out.'}, status=HTTP_200_OK)

class UserDetails(APIView):
    permission_classes = [Or(IsSuperAdmin, IsAdmin)]
    def post(self,request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        mobile_no = request.data.get('mobile_no')
        user_type = request.data.get('user_type')
        slug = request.data.get('bank')
        try:
            bank = Bank.objects.get(slug=slug)
        except Bank.DoesNotExist:
            bank = None
        branch = None

        if username is None or password is None or user_type is None:
            return Response({'error': 'Username or password or user type can not be null.'}, status=HTTP_400_BAD_REQUEST)      
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=HTTP_404_NOT_FOUND)
        if user_type not in User.USER_TYPES_MAP:
            return Response({'error': 'Wrong user type.'}, status=HTTP_404_NOT_FOUND)
        if (user_type != User.USER_TYPES_MAP['superadmin'] or user_type != User.USER_TYPES_MAP['admin']) and bank == None:
            return Response({'error': 'You must specify correct bank.'}, status=HTTP_404_NOT_FOUND)

        new_user = User(username=username,email=email,mobile_no=mobile_no,user_type=user_type, bank=bank, branch = branch)
        new_user.set_password(password)
        new_user.save()
        return Response({'username': new_user.username, 'user_type': new_user.user_type, 'bank': new_user.bank.name}, status=HTTP_200_OK)

    def get(self, request, format=None):
        users = User.objects.all()
        serialized_data = UserSerializer(users, many=True)
        return Response(serialized_data.data)


    def put(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Username or password can not be null.'}, status=HTTP_400_BAD_REQUEST)    
        user_object = User.objects.filter(username=username)
        if not user_object.exists():
            return Response({'error': 'Username does not exist.'}, status=HTTP_200_OK)

        _user = user_object.first()
        _user.set_password(password)
        _user.save()
        response = {'status':'success','message':'User password successfully updated','username': _user.username, 'user_type': _user.user_type}

        if _user.bank is not None:
            response['bank'] = _user.bank.name
        return Response(response, status=HTTP_200_OK)