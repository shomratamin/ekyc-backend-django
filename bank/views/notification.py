from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Branch, KycDataSource, DEFAULT_BANK_SETTINGS
from ..serializers import BankSettingsSerializer, BranchSerializer, KycDataSourceSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from app.utils import allowed_file
from app.tasks import do_ec_ocr_face_verification
from customer.models import CustomerProfile


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def ec_notification(request):
    secret = request.data.get("secret")
    if secret is None:
        return Response({'status': 'failed'},status=HTTP_400_BAD_REQUEST)
    if secret != settings.NOTIFICATION_SECRET:
        return Response({'status': 'failed'}, status=HTTP_400_BAD_REQUEST)

    info = request.data.get('info')
    nid_no = request.data.get('nid_no')
    # print(info, nid_no)
    _nid_image = request.data.get('nid_image')
    _nid_photo = request.data.get('nid_photo')
    if _nid_image is not None and _nid_photo is not None:
        nid_image = request.FILES['nid_image']
        nid_photo = request.FILES['nid_photo']
        if allowed_file(nid_image.name) and allowed_file(nid_photo.name):
            fs = FileSystemStorage(location=settings.EC_TEMP_DIR)
            nid_image = fs.save(nid_image.name, nid_image)
            nid_photo = fs.save(nid_photo.name, nid_photo)
            do_ec_ocr_face_verification.delay(nid_image,nid_photo, nid_no)
            print(nid_image,nid_photo, nid_no)

    if info is not None:
        info_parsed = json.loads(info)
        for _info in info_parsed:
            info_nid = _info['nid']
            # info_dob = _info['dob']
            customer_profile = CustomerProfile.objects.filter(verification_status='ec_requested', nid_no=info_nid)
            customer_profile.update(verification_status='invalid')
            if customer_profile.exists():
                for c_profile in customer_profile:
                    c_profile.save()

    return Response({'status': 'success'},
                    status=HTTP_200_OK)