from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from ..serializers import AgentSerializer
from app.permissions import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from app.utils import allowed_file, image_as_base64

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAgent,))
def get_me(request):
    serialized_data = AgentSerializer(request.user, many=False)
    return Response({'me': serialized_data.data}, status=HTTP_200_OK)
