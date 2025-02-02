from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import BankSetting, Branch, KycDataSource, DEFAULT_BANK_SETTINGS, EcStatus
from ..serializers import BankSettingsSerializer, BranchSerializer, KycDataSourceSerializer, BankAdminSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import api_view, permission_classes
from app.permissions import *
import json
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.query import QueryBuilder


@api_view(['GET'])
@permission_classes((IsBank,))
def get_me(request):
    serialized_data = BankAdminSerializer(request.user, many=False)
    return Response({'me': serialized_data.data}, status=HTTP_200_OK)


class BankSettings(APIView):
    permission_classes = [IsBank,]
    def get(self, request, format=None):
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        param = request.query_params.get('param')
        filter_endswith = request.query_params.get('filter_endswith')

        if filter_endswith is not None:
            params = BankSetting.objects.filter(bank=bank, param__endswith=filter_endswith)
        elif param is None:
            params = BankSetting.objects.filter(bank=bank)
        else:
            params = BankSetting.objects.filter(bank=bank, param=param)

        serialized_data = BankSettingsSerializer(params, many=True)
        return Response(serialized_data.data, status=HTTP_200_OK)

    def post(self, request, format=None):
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'}, status=HTTP_404_NOT_FOUND)
        bulk = request.query_params.get('bulk')
        bulk_list = request.query_params.get('bulk_list')
        if bulk_list == 'true':
            json_payload = request.data.get('payload_json')
            print(json_payload)
            try:
                json_data = json.loads(json_payload)
            except ValueError:
                return Response({'error':'Invalid Json data.'}, status=HTTP_400_BAD_REQUEST )

            for data in json_data:
                param = data['param']
                value = data['value']
                if not BankSetting.objects.filter(param=param, bank=bank).exists():
                    new_param = BankSetting(param=param,value=value,bank=bank)
                    new_param.save()
                else:
                    BankSetting.objects.filter(param=param, bank=bank).update(value=value)

            
            return Response({'detail': 'Values updated successfully', 'data': json_data}, status=HTTP_200_OK )         
            
        elif bulk == 'true':
            json_payload = request.data.get('payload_json')
            try:
                json_data = json.loads(json_payload)
            except ValueError:
                return Response({'error':'Invalid Json data.'}, status=HTTP_400_BAD_REQUEST )

            for param in json_data:
                value = json_data[param]
                if not BankSetting.objects.filter(param=param, bank=bank).exists():
                    new_param = BankSetting(param=param,value=value,bank=bank)
                    new_param.save()
                else:
                    BankSetting.objects.filter(param=param, bank=bank).update(value=value)

            
            return Response({'detail': 'Values updated successfully', 'data': json_data}, status=HTTP_200_OK )
        else:
            param = request.data.get('param')
            value = request.data.get('value')
            if param is None or value is None:
                return Response({'error': 'Please provide both param and value.'}, status=HTTP_400_BAD_REQUEST)

            if param.endswith('_options'):
                try:
                    json_data = json.loads(value)
                except ValueError:
                    return Response({'error':'Invalid Json data.'}, status=HTTP_400_BAD_REQUEST )

                if not BankSetting.objects.filter(param=param, bank=bank).exists():
                    json_data['id'] = 1
                    value_out = [json_data]
                    value_out = json.dumps(value_out)
                    new_param = BankSetting(param=param,value=value_out,bank=bank)
                    new_param.save()
                else:
                    setting_data = BankSetting.objects.filter(param=param, bank=bank).first()
                    _setting_data = BankSettingsSerializer(setting_data).data
                    max_id = 1
                    _settings_value = _setting_data['value']
                    _settings_value = json.loads(_settings_value)
                    append = True
                    for i, data in enumerate(_settings_value):
                        if 'id' in json_data:
                            if json_data['id'] == int(data['id']):
                                _settings_value[i]= json_data
                                append = False
                        elif int(data['id']) > max_id:
                            max_id = int(data['id'])

                        if json_data['name'] == data['name']:
                            json_data['id'] = data['id']
                            _settings_value[i]= json_data
                            append = False
                        
                    if append:
                        max_id += 1
                        json_data['id'] = max_id
                        _settings_value.append(json_data)
                    value_out = json.dumps(_settings_value)
                    BankSetting.objects.filter(param=param, bank=bank).update(value=value_out)

            else:              
                if not BankSetting.objects.filter(param=param, bank=bank).exists():
                    new_param = BankSetting(param=param,value=value,bank=bank)
                    new_param.save()
                else:
                    BankSetting.objects.filter(param=param, bank=bank).update(value=value)
            return Response({'param': param, 'value': value}, status=HTTP_200_OK )

    def delete(self, request, format=None):
        param = request.query_params.get('param')
        value = request.query_params.get('value')

        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        if param is None:
            return Response({'error': 'Please provide param.'})
        complete_delete = True
        if value is not None and param.endswith('_options'):
            try:
                json_data = json.loads(value)
            except ValueError:
                return Response({'error':'Invalid Json data.'}, status=HTTP_400_BAD_REQUEST )

            settings = BankSetting.objects.filter(param=param, bank=bank)
            if settings.exists():
                setting_data = BankSetting.objects.filter(param=param, bank=bank).first()
                _setting_data = BankSettingsSerializer(setting_data).data
                _settings_value = _setting_data['value']
                _settings_value = json.loads(_settings_value)
                new_settings_value = []
                for i, data in enumerate(_settings_value):
                    if json_data['id'] is not None:
                        if json_data['id'] != int(data['id']):
                            new_settings_value.append(data)
                        complete_delete = False
                value_out = json.dumps(new_settings_value)
                BankSetting.objects.filter(param=param, bank=bank).update(value=value_out)

        elif param in DEFAULT_BANK_SETTINGS and complete_delete == True:
            return Response({'error': 'This parameter is not deletable'}, status=HTTP_400_BAD_REQUEST )
        if complete_delete:
            BankSetting.objects.filter(param=param, bank=bank).delete()
        return Response({'param': param}, status=HTTP_200_OK )


class BranchDetails(APIView):
    permission_classes = [IsBank]

    def get(self, request, format=None):
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})

        page = request.query_params.get('page')
        per_page = request.query_params.get('per_page')
        if page is None:
            page = 1
        if per_page is None:
            per_page = 20

        query_builder = QueryBuilder(Branch, request)
        query = query_builder.get_query()
        branches = Branch.objects.filter(query,bank=bank)

        total_branches = branches.count()
        paginator = Paginator(branches, per_page)

        try:
            branches = paginator.page(page)
        except EmptyPage:
            branches = paginator.page(paginator.num_pages)
        serialized_data = BranchSerializer(branches, many=True)
        return Response({'total_pages': paginator.num_pages,'current_page': page,'total_count': total_branches,'data': serialized_data.data}, status=HTTP_200_OK)

    def post(self, request, format=None):
        name = request.data.get('name')
        address = request.data.get('address')
        branch_code = request.data.get('code')

        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'}, status=HTTP_404_NOT_FOUND)
        if name is None:
            return Response({'error': 'Please provide a branch name.'}, status=HTTP_400_BAD_REQUEST)
        if branch_code is None:
            return Response({'error': 'Please provide a unique branch code.'}, status=HTTP_400_BAD_REQUEST)

        if not Branch.objects.filter(code=branch_code, bank=bank).exists():
            new_branch = Branch(name=name,address=address,bank=bank, code=branch_code)
            new_branch.save()
        else:
            Branch.objects.filter(code=branch_code, bank=bank).update(address=address)
        return Response({'name': name, 'address': address}, status=HTTP_200_OK )

    def delete(self, request, format=None):
        pk = request.query_params.get('pk')
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        if pk is None:
            return Response({'error': 'Please provide branch primary key.'})
        Branch.objects.filter(pk=pk, bank=bank).delete()
        return Response({'details': 'Branch deleted.'}, status=HTTP_200_OK )

class KycDataSourceDetails(APIView):
    permission_classes = [IsBank]

    def get(self, request, format=None):
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        sources = KycDataSource.objects.filter(bank=bank)
        serialized_data = KycDataSourceSerializer(sources, many=True)
        return Response(serialized_data.data, status=HTTP_200_OK)

    def post(self, request, format=None):
        ip_bank = request.data.get('ip_bank')
        ip_ec = request.data.get('ip_ec')
        username = request.data.get('username')
        password = request.data.get('password')
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'}, status=HTTP_404_NOT_FOUND)
        if ip_ec is None or username is None or password is None:
            return Response({'error': 'Please provide ip, username and password.'}, status=HTTP_400_BAD_REQUEST)

        # kyc_data_source = KycDataSource.objects.filter(bank=bank)
        # if not kyc_data_source.exists():
        ec_status = EcStatus()
        ec_status.save()
        new_source = KycDataSource(ip_bank=ip_bank,ip_ec=ip_ec, username=username, password=password, bank=bank, status=ec_status)
        new_source.save()
        # else:
        #     if kyc_data_source.count() > 1:
        #         kyc_data_source.delete()
        #         ec_status = EcStatus()
        #         ec_status.save()
        #         new_source = KycDataSource(ip_bank=ip_bank,ip_ec=ip_ec, username=username, password=password, bank=bank, status=ec_status)
        #         new_source.save()
        #     elif kyc_data_source.count() == 1:
        #         kyc_data_source = kyc_data_source.first()
        #         kyc_data_source.ip_bank = ip_bank
        #         kyc_data_source.ip_ec = ip_ec
        #         kyc_data_source.username = username
        #         kyc_data_source.password = password
        #         kyc_data_source.bank = bank
        #         if kyc_data_source.status is None:
        #             ec_status = EcStatus()
        #             ec_status.save()
        #             kyc_data_source.status = ec_status
        #         kyc_data_source.save()

        return Response({'status': 'success', 'message':'Successfully added ec data source'}, status=HTTP_200_OK )

    def delete(self, request, format=None):
        pk = request.query_params.get('pk')
        bank = request.user.bank
        if bank is None:
            return Response({'error':'Bank is null.'})
        if pk is None:
            return Response({'error': 'Please provide branch primary key.'})
        KycDataSource.objects.filter(pk=pk, bank=bank).delete()
        return Response({'details': 'Kyc data source deleted.'}, status=HTTP_200_OK )