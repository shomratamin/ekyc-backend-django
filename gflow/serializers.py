from app.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from customer.models import CustomerProfile, RiskGrading, RiskAssesment, Introducer, BranchRelatedInfo, OtherBank, OtherBankCard, RiskGradingScore, CustomerAccount, CustomerOtherInfo, TransactionProfile


class RiskGradingSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = RiskGrading
        fields = '__all__'

class RiskGradingScoreSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = RiskGradingScore
        fields = '__all__'


class RiskAssesmentSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = RiskAssesment
        fields = '__all__'

class IntroducerSerializer(ModelSerializer):
    is_empty = SerializerMethodField()

    def get_is_empty(self, instance):
        return instance.is_empty()

    class Meta:
        depth = 0
        model = Introducer
        fields = ([f.name for f in Introducer._meta.get_fields()]+['is_empty'])

class BranchRelatedInfoSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = BranchRelatedInfo
        fields = '__all__'

class OtherBankSerializer(ModelSerializer):
    is_empty = SerializerMethodField()

    def get_is_empty(self, instance):
        return instance.is_empty()

    class Meta:
        depth = 0
        model = OtherBank
        fields = ([f.name for f in OtherBank._meta.get_fields()]+['is_empty'])

class OtherBankCardSerializer(ModelSerializer):
    is_empty = SerializerMethodField()

    def get_is_empty(self, instance):
        return instance.is_empty()

    class Meta:
        depth = 0
        model = OtherBankCard
        fields = ([f.name for f in OtherBankCard._meta.get_fields()]+['is_empty'])


class CustomerProfileReportSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CustomerProfile
        fields = '__all__'


class CustomerAccountReportSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CustomerAccount
        fields = '__all__'

class CustomerOtherInfoSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = CustomerOtherInfo
        fields = '__all__'

class TransactionProfileSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = TransactionProfile
        fields = '__all__'