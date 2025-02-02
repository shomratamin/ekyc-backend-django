from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .gflowengine import gflow_environment, gflow_loader, gflow_admin_environment
from app.permissions import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.permissions import BasePermission
from jinja2.exceptions import TemplateSyntaxError, UndefinedError, TemplateNotFound
from .models import GFlowPageUserStates
from .exposed_functions import load_customer_profile, save_customer_profile
from customer.models import AdditionalServices, CustomerNominee
from bank.serializers import AdditonalServiceSerializer, CustomerNomineeSerializer
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from collections import OrderedDict
import json
from django.conf import settings
import base64
import requests

def redirect_home(request):
    if settings.ACCESS_CHANNEL == 'bankled':
        return HttpResponseRedirect('/onboarding/')
    elif settings.ACCESS_CHANNEL == 'selfled':
        return HttpResponseRedirect('/aof/')
    
def has_permission(request):
    return True
    req_path = request.path

    if not req_path.startswith('/onboarding'):
        return False

    return True
    page = req_path.split('/')[2]
    if len(page) < 1:
        page = 'index'
    acl_permission = gflow_loader.get_access_permission(page)
    if not acl_permission:
        return False
    if not request.user.is_authenticated:
        if 'public' in acl_permission or 'publiconly' in acl_permission:
            return True
        else:
            return False
    if request.user.user_type in acl_permission or 'public' in acl_permission:
        return True
    else:
        return False


class GFlowIDEView(APIView):
    permission_classes = [IsSuperAdmin]
    def get(self, request, format=None):
        template = gflow_admin_environment.get_template('editor.html')
        data = dict()
        data['pages'] = gflow_loader.get_template_names()
        rendered = template.render(data)
        return HttpResponse(rendered)

global without_uuid
without_uuid = ['__index','__phone-number-verification','__email-verification', '__logout', '__test', '__customer-list', '__account-list', '__contact-information','__apply-for-new-account',\
    '__resend-otp','__resend-otp-email','__manage-nominee', '__forgot-password','__forgot-password-confirmation-email', '__forgot-password-reset']

class GFlowRenderView(APIView):
    global without_uuid
    permission_classes = [AllowAnyGflow]
    def get(self, request, app = None, format=None):
        permission = has_permission(request)
        print('is ajax', request.is_ajax())

        page = 'index'

        # if request.user.is_anonymous and page != 'index':
        #     return HttpResponseRedirect('/onboarding/')

        # if not permission:
        #     return HttpResponseRedirect('/onboarding/not-found/')

        app_route = ''
        if settings.ACCESS_CHANNEL == 'bankled':
            app_route = 'onboarding'
        elif settings.ACCESS_CHANNEL == 'selfled':
            app_route = 'aof'
        # elif settings.ACCESS_CHANNEL == 'all':
        #     app_route = 'aof'

        if not app is None:
            _uri = app.split('/')
            if len(_uri) < 2:
                if settings.ACCESS_CHANNEL == 'all' or settings.ACCESS_CHANNEL == 'bankled':
                    app_route = _uri[0]
                page = app_route + '__index'
            else:
                if settings.ACCESS_CHANNEL == 'all' or settings.ACCESS_CHANNEL == 'bankled':
                    app_route = _uri[0]
                page = app_route + '__' + _uri[1]
        else:
            page = app_route + '__index'

        print('access page', page)
        allowed_without_uuid = set([app_route + p for p in without_uuid])

        if request.user.is_anonymous:
            if page not in allowed_without_uuid:
                print(page, "not logged in")
                return HttpResponseRedirect(f'/{app_route}/')
        else:
            if not request.GET.get('uuid') and page not in allowed_without_uuid and not request.GET.get('tid'):
                print(page, "not uuid")
                return HttpResponseRedirect(f'/{app_route}/')

        data = dict()

        data['access_channel'] = settings.ACCESS_CHANNEL

        data['app_route'] = app_route
        data['request'] = request
        data['cbs'] = requests
        try:
            template = gflow_environment.get_template(page)
            data['url_append'] = ''
            for key in request.GET:
                data[key] = request.GET.get(key)
            for key in request.COOKIES:
                data[key] = request.COOKIES.get(key)

            data['additional_services'] = AdditonalServiceSerializer(AdditionalServices()).data
            dummy = OrderedDict()
            dummy['account_operation_type'] = 'simplified'
            data['bank_account'] = dummy
            data['customer_profile'] = {'id':None}
            if not request.user.is_anonymous and request.user.user_type == 'agent':
                if 'tid' in request.GET:
                    _tid = request.GET.get('tid')
                    data['url_append'] = ''.join(['?tid=', _tid])
                    customer_profile = load_customer_profile(request, _tid)
                    if customer_profile and 'uuid' in customer_profile:
                        data['url_append'] = data['url_append'] + '&uuid=' + customer_profile['uuid']
                    data['customer_profile'] = customer_profile
                    if customer_profile != False:
                        for _key in customer_profile:
                            if customer_profile[_key] is None:
                                data[_key] = ''
                            else:
                                if _key == 'id':                
                                    data['customer_id'] = customer_profile[_key]
                                else:
                                    data[_key] = customer_profile[_key]
                    else:
                        if page not in allowed_without_uuid:
                            return HttpResponseRedirect(f'/{app_route}/')

            elif not request.user.is_anonymous and request.user.user_type == 'customer':

                data['url_append'] = ''
                customer_profile = load_customer_profile(request)
                if customer_profile and 'uuid' in customer_profile:
                    data['url_append'] = data['url_append'] + '?uuid=' + customer_profile['uuid']
                data['customer_profile'] = customer_profile
                if customer_profile:
                    for _key in customer_profile:
                        if customer_profile[_key] is None:
                            data[_key] = ''
                        else:
                            if _key == 'id':                
                                data['customer_id'] = customer_profile[_key]
                            else:
                                data[_key] = customer_profile[_key]                
                else:
                    if page not in allowed_without_uuid:
                        return HttpResponseRedirect(f'/{app_route}/')
            chunks = []
            cookies = []
            redirect_to = None
            allow_public = False
            for gen in template.generate(data):
                gen = gen.strip()
                if gen.startswith('redirect_to::::'):
                    redirect_to = gen.split('::::')[-1]
                    break
                elif gen.startswith('set_cookie::::'):
                    cookie = gen.split('::::')[-1]
                    cookie = cookie.split('=')
                    cookies.append(cookie)
                elif gen.startswith('pre_condition::::'):
                    pre_condition = gen.split('::::')[-1]
                    # if pre_condition == 'public_access':
                    #     allow_public = True

                    # if pre_condition == 'tid':
                    #     if not 'tid' in request.GET or not 'tid' in request.POST:
                    #         return HttpResponseRedirect(f'/{app_route}/')
                    #         break  
                elif gen.startswith('download_pdf::::'):
                    info = gen.split('::::')
                    data = info[1]
                    filename = info[-1]
                    data = base64.b64decode(data, validate=True)
                    response =  HttpResponse(data,content_type='application/pdf')
                    response['Content-Disposition'] = f"attachment; filename={filename}"
                    return response
                else:
                    chunks.append(gen)

            
            print('page is', page)
            rendered = ''.join(chunks)
            if redirect_to is None:
                response = HttpResponse(rendered)
            else:
                response = HttpResponseRedirect(redirect_to)

            for cookie in cookies:
                response.set_cookie(cookie[0], cookie[1],float(cookie[2]))
            return response
        except TemplateSyntaxError as e:
            print(e)
            return HttpResponseNotFound(f'{e}')
        except TemplateNotFound as e:
            template = gflow_environment.get_template(f'aof__not-found')
            return HttpResponseNotFound(template.render(data))

        except Exception as e:
            print(e)
            return HttpResponseNotFound(f'{e}')

    def post(self, request, app = None, format=None):
        page = 'index'
        app_route = ''
        if settings.ACCESS_CHANNEL == 'bankled':
            app_route = 'onboarding'
        elif settings.ACCESS_CHANNEL == 'selfled':
            app_route = 'aof'
        if not app is None:
            _uri = app.split('/')
            if len(_uri) < 2:
                if settings.ACCESS_CHANNEL == 'all' or settings.ACCESS_CHANNEL == 'bankled':
                    app_route = _uri[0]
                page = app_route + '__index'
            else:
                if settings.ACCESS_CHANNEL == 'all' or settings.ACCESS_CHANNEL == 'bankled':
                    app_route = _uri[0]
                page = app_route + '__' + _uri[1]
        else:
            page = app_route + '__index'

        print('access page', page)
        allowed_without_uuid = set([app_route + p for p in without_uuid])

        if request.user.is_anonymous:
            if page not in allowed_without_uuid:
                print(page, "not logged in")
                return HttpResponseRedirect(f'/{app_route}/')
        else:
            if not request.GET.get('uuid') and page not in allowed_without_uuid and not request.GET.get('tid'):
                print(page, "not uuid")
                return HttpResponseRedirect(f'/{app_route}/')

        data = dict()

        data['access_channel'] = settings.ACCESS_CHANNEL

        data['app_route'] = app_route
        data['cbs'] = requests
        try:
            template = gflow_environment.get_template(page)
            data['app_route'] = app_route
            data['url_append'] = ''
            data['request'] = request
            for key in request.POST:
                data[key] = request.POST.get(key)
            for key in request.GET:
                data[key] = request.GET.get(key)
            for key in request.COOKIES:
                data[key] = request.COOKIES.get(key)
            form_errors = True
            if not request.user.is_anonymous and request.user.user_type == 'agent':
                if 'tid' in request.GET:
                    __tid = request.GET.get('tid')              
                    data['customer_id'] = __tid

                data['additional_services'] = AdditonalServiceSerializer(AdditionalServices()).data
                dummy = OrderedDict()
                dummy['account_operation_type'] = 'simplified'
                data['bank_account'] = dummy
                data['customer_profile'] = json.dumps({'id':None})
                form_errors = True
                if 'tid' in request.GET:
                    _tid = request.GET.get('tid')
                    data['url_append'] = ''.join(['?tid=', _tid])
                    customer_profile, form_errors = save_customer_profile(request, _tid)

                    if customer_profile and 'uuid' in customer_profile:
                        data['url_append'] = data['url_append'] + '&uuid=' + customer_profile['uuid']

                    data['customer_profile'] = customer_profile
                    print('form errors', form_errors)
                    if customer_profile != False:
                        for _key in customer_profile:
                            if customer_profile[_key] is None:
                                data[_key] = ''
                            else:
                                if key == 'id':                        
                                    data['customer_id'] = customer_profile[_key]
                                else:
                                    data[_key] = customer_profile[_key]
                    else:
                        if page not in allowed_without_uuid:
                            return HttpResponseRedirect(f'/{app_route}/')

            elif not request.user.is_anonymous and request.user.user_type == 'customer':
                print('customer')
                data['url_append'] = ''
                customer_profile, form_errors = save_customer_profile(request)
                if customer_profile and 'uuid' in customer_profile:
                    data['url_append'] = data['url_append'] + '?uuid=' + customer_profile['uuid']
                data['customer_profile'] = customer_profile
                # print('form errors indivi', customer_profile)
                # print(customer_profile)
                if customer_profile != False:
                    for _key in customer_profile:
                        if customer_profile[_key] is None:
                            data[_key] = ''
                        else:
                            if key == 'id':                        
                                data['customer_id'] = customer_profile[_key]
                            else:
                                data[_key] = customer_profile[_key]
                else:
                    if page not in allowed_without_uuid:
                        return HttpResponseRedirect(f'/{app_route}/')
            elif request.user.is_anonymous:
                data['additional_services'] = AdditonalServiceSerializer(AdditionalServices()).data
                dummy = OrderedDict()
                dummy['account_operation_type'] = 'simplified'
                data['bank_account'] = dummy
                data['customer_profile'] = json.dumps({'id':None})

            data['form_errors'] = form_errors
            chunks = []
            cookies = []
            redirect_to = None
            for gen in template.generate(data):
                gen = gen.strip()
                # print('gen:',gen)
                if gen.startswith('redirect_to::::'):
                    redirect_to = gen.split('::::')[-1]
                    break
                elif gen.startswith('set_cookie::::'):
                    cookie = gen.split('::::')[-1]
                    cookie = cookie.split('=')
                    cookies.append(cookie)
                else:
                    chunks.append(gen)
            rendered = ''.join(chunks)

            if redirect_to is None:
                response = HttpResponse(rendered)
            else:
                response = HttpResponseRedirect(redirect_to)

            for cookie in cookies:
                response.set_cookie(cookie[0], cookie[1], float(cookie[2]))
            return response
        except TemplateSyntaxError as e:
            print(e)
            return HttpResponseNotFound(f'{e}')
        except TemplateNotFound as e:
            template = gflow_environment.get_template(f'aof__not-found')
            data = dict()
            data['request'] = request
            return HttpResponseNotFound(template.render(data))

        except Exception as e:
            print(e)
            return HttpResponseNotFound(f'{e}')


class GFlowPageEditView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, format=None):
        page = request.GET.get('page')
        name = request.GET.get('name')
        if name is not None:
            if name == '__all__':
                templates = gflow_loader.get_collections()
                print(templates)
                templates = json.dumps(templates)
                return HttpResponse(templates)

            template = gflow_loader.get_template_ide(name)
            if template != False:
                return HttpResponse(template)
            elif page is not None and template == False:
                content = '<html><body></body></html>'
                try:
                    with open(f'gflow/templates/predefined/{page}.html', mode='r', encoding='utf-8') as f:
                        content = f.read()
                        gflow_loader.create_or_update_template(name=name, content= content)
                        return HttpResponse(content)
                except:
                    gflow_loader.create_or_update_template(name=name, content= content)
                    return HttpResponse(content)
            else:
                return HttpResponse('error')

        return HttpResponse('error')

    def post(self, request, format=None):
        name = request.POST.get('name')
        content = request.POST.get('content')
        if name is not None and content is not None:
            gflow_loader.create_or_update_template(name, content)
            return Response({'status':'success'}, status=HTTP_200_OK)
        else:
            return Response({'status':'failed'}, status=HTTP_400_BAD_REQUEST)