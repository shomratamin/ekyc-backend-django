from app.models import User
from rest_framework.serializers import ModelSerializer

class AgentSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'branch', 'bank')

class CustomerSerializer(ModelSerializer):
    class Meta:
        depth = 0
        model = User
        fields = ('pk','username', 'email', 'mobile_no', 'user_type', 'branch', 'bank')