from app.models import User
from .models import CustomerProfile
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomerProfile, CustomerVerificationScores


class CustomerVerificationStatusSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'branch')


class CustomersVerificationLogSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'branch')