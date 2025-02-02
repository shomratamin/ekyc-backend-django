from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Branch
from app.models import User
from ..serializers import AgentSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.permissions import *
from app.tasks import send_password_email_task
from rest_framework.decorators import api_view, permission_classes
import random
import string
from app.query import QueryBuilder

def get_random_alpha_numeric_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def generate_password_by_policy(length=8):
    upper_case = string.ascii_uppercase
    lower_case = string.ascii_lowercase
    special = '!#$%&():;<=>?@[]^{|}~'
    number = string.digits
    password = []
    password.extend([random.choice(upper_case) for i in range(2)])
    password.extend([random.choice(lower_case) for i in range(2)])
    password.extend([random.choice(special) for i in range(2)])
    password.extend([random.choice(number) for i in range(2)])

    random.shuffle(password)
    password = ''.join(password)
    return password


@api_view(['POST'])
@permission_classes((IsBank,))
def reset_password_and_send_in_email(request):
    user_pk = request.data.get('user_pk')
    try:
        user = User.objects.get(pk=user_pk,user_type='agent')
    except:
        return Response({'status': 'failed','message':'User not found.'}, status=HTTP_200_OK)
    
    new_password = generate_password_by_policy()
    user.set_password(new_password)
    user.save()
    send_password_email_task.delay(user.email, new_password)
    user_data = AgentSerializer(user)
    return Response({'status': 'success', 'message':'User password is reset and email is sent','user_data':user_data.data}, status=HTTP_200_OK)

class AgentDetails(APIView):
    permission_classes = [IsBank]
    def post(self,request, format=None):
        pk = request.data.get('pk')
        print('pk',pk)
        bank = request.user.bank
        if pk is None:
            name = request.data.get('name')
            email = request.data.get('email')
            mobile_no = request.data.get('mobile_no')
            branch_code = request.data.get('branch_code')
            cbs_id = request.data.get('cbs_id')
            cbs_username = request.data.get('cbs_username')
            cbs_password = request.data.get('cbs_password')
            user_type = request.data.get('user_type')
            if user_type is None:
                user_type = 'agent'

            if mobile_no is None or not mobile_no.startswith('01') or len(mobile_no) != 11:
                return Response({'status':'failed','error':'You need to provide a valid Bangladeshi mobile number without country code.'}, status=HTTP_400_BAD_REQUEST)

            if User.objects.filter(mobile_no=mobile_no, user_type=User.USER_TYPES_MAP[user_type]).exists():
                return Response({'status':'failed','error': 'Mobile number already exists.'}, status=HTTP_404_NOT_FOUND)

            if bank is None:
                return Response({'status':'failed','error':'Bank is null.'}, status=HTTP_400_BAD_REQUEST)

            try:
                branch = Branch.objects.get(code=branch_code, bank=bank)
            except Branch.DoesNotExist:
                return Response({'status':'failed','error':'Your specified branch does not exist.'}, status=HTTP_400_BAD_REQUEST)

            username = bank.slug + '_agent_' + mobile_no
            password = generate_password_by_policy()
    
            if User.objects.filter(username=username).exists():
                return Response({'status':'failed','error': 'Agent already exists.'}, status=HTTP_404_NOT_FOUND)

            new_user = User(name=name,username=username, email=email,mobile_no=mobile_no,user_type=User.USER_TYPES_MAP[user_type], bank=bank, branch=branch)
            new_user.set_password(password)
            if cbs_id is not None:
                new_user.cbs_id = cbs_id
            if cbs_username is not None:
                new_user.cbs_username = cbs_username
            if cbs_password is not None:
                new_user.cbs_password = cbs_password
            new_user.save()
            send_password_email_task.delay(email, password)
            return Response({'mobile_no': new_user.mobile_no, 'user_type': new_user.user_type, 'branch': new_user.branch.name}, status=HTTP_200_OK)
        else:
            branch_code = request.data.get('branch_code')
            name = request.data.get('name')
            email = request.data.get('email')
            mobile_no = request.data.get('mobile_no')
            cbs_id = request.data.get('cbs_id')
            cbs_username = request.data.get('cbs_username')
            cbs_password = request.data.get('cbs_password')

            try:
                user = User.objects.get(pk=pk)
                if branch_code is not None:
                    try:
                        branch = Branch.objects.get(code=branch_code, bank=bank)
                        user.branch = branch
                        if name is not None:
                            user.name = name
                        if email is not None:
                            user.email = email
                        if mobile_no is not None:
                            user.mobile_no = mobile_no
                        if cbs_id is not None:
                            user.cbs_id = cbs_id
                        if cbs_username is not None:
                            user.cbs_username = cbs_username
                        if cbs_password is not None:
                            user.cbs_password = cbs_password

                        user.save()
                        user_data = AgentSerializer(user)
                        return Response({'status':'success', 'message':'Information successfully updated.','user_data':user_data.data}, status=HTTP_200_OK)
                    except Branch.DoesNotExist:
                        return Response({'status':'failed','error':'Your specified branch does not exist.'}, status=HTTP_200_OK)

                    
            except:
                return Response({'status':'failed', 'message':'Bank Officer not found.'}, status=HTTP_200_OK)

    def get(self, request, format=None):
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'}, status=HTTP_400_BAD_REQUEST)
        pk = request.GET.get('pk')
        print('pk',pk)
        if pk is None:
            page = request.query_params.get('page')
            per_page = request.query_params.get('per_page')
            if page is None:
                page = 1
            if per_page is None:
                per_page = 20

            query_builder = QueryBuilder(User, request)
            query = query_builder.get_query()
            all_agents = User.objects.filter(query, user_type=User.USER_TYPES_MAP['agent'],bank=bank)
            total_agents = all_agents.count()
            paginator = Paginator(all_agents, per_page)

            try:
                agents = paginator.page(page)
            except EmptyPage:
                agents = paginator.page(paginator.num_pages)
            
            # customers_page = list(map(lambda customer: customer.as_dict(), list(customers)))

            serialized_data = AgentSerializer(agents, many=True)
            return Response({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_agents,'data': serialized_data.data}, status=HTTP_200_OK)
        else:
            try:
                agent = User.objects.get(pk=pk)
                serialized_data = AgentSerializer(agent, many=False)
                return Response({'status': 'success','data': serialized_data.data}, status=HTTP_200_OK)
            except:
                return Response({'status':'failed', 'message':'Bank Officer not found.'}, status=HTTP_200_OK)
        # return Response(serialized_data.data)

    def delete(self, request, format=None):
        pk = request.query_params.get('pk')
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        if pk is None:
            return Response({'error': 'Please provide agent primary key.'})
        User.objects.filter(pk=pk, bank=bank, user_type=User.USER_TYPES_MAP['agent']).delete()
        return Response({'details': 'Agent deleted.'}, status=HTTP_200_OK )