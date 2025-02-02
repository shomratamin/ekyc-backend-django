from app.models import User
from .models import BankSetting, Branch, KycDataSource
from customer.models import CustomerProfile, CustomerAccount, CustomerNominee, CustomerOtherInfo, AdditionalServices
from rest_framework.serializers import ModelSerializer

class BankSettingsSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = BankSetting
        fields = ('name','param', 'value', 'deletable')

class BankAdminSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'bank')

class BranchSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = Branch
        fields = ('pk','name', 'address', 'code')

class AgentSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type','cbs_id','cbs_username','cbs_password','branch')

class CustomerSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'branch')

class CustomerListSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = CustomerProfile
        fields = ('pk','account_status','tracking_number','customer_name_eng', 'nid_no', 'dob', 'mobile_number', 'verification_status', 'submitted_on', 'created_on', 'preferred_branch')

class KycDataSourceSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = KycDataSource
        fields = ('pk', 'ip_bank', 'ip_ec', 'username', 'password')

class CustomerProfileSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CustomerProfile
        fields = '__all__'

class AdditonalServiceSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = AdditionalServices
        fields = '__all__'



class CustomerAccountSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = CustomerAccount
        fields = '__all__'

class CustomerAccountWithProfileSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CustomerAccount
        fields = '__all__'

class CustomerNomineeSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = CustomerNominee
        fields = '__all__'

class CustomerOtherInfoSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = CustomerOtherInfo
        fields = '__all__'