from .models import Bank, User
from rest_framework.serializers import ModelSerializer
from bank.models import  EcStatus, KycDataSource

class BankSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = Bank
        fields = ('name', 'slug', 'created_on', 'updated_on', 'test_quota', 'live_quota')

class UserSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('username', 'email', 'mobile_no', 'user_type', 'bank')

class EcStatusSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = KycDataSource
        fields = ('bank', 'status')

