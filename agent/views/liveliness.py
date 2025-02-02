from django.conf import settings
from app.permissions import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from app.utils import *
from django.core.files.storage import FileSystemStorage
import os
from app.utils import detect_liveliness

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAgent,))
def liveliness_check(request):
    video_file = request.data.get('lvid')
    rotate = request.data.get('rotate')
    if rotate is None:
        rotate = 0

    if rotate is None and not rotate.isnumeric():
        rotate = 0

    if video_file is None:
        return Response({'status':'failed','message': 'Please upload a video'}, status=HTTP_200_OK)
    fs = FileSystemStorage(location=settings.LIVELINESS_UPLOAD_DIR)
    _video_file_name = fs.save(filename_to_hash(video_file.name), video_file)
    _video_file_path = os.path.join(settings.LIVELINESS_UPLOAD_DIR, _video_file_name)
    face_image_file_name = _video_file_name + '_face.jpg'
    _face_image_file_path = os.path.join(settings.LIVELINESS_UPLOAD_DIR, face_image_file_name)

    result = detect_liveliness(_video_file_path,_face_image_file_path, rotate)
    print(result['liveliness_status'], result['live_ratio'])
    if result is None:
        return Response({'status':'failed','message': 'Invalid video'}, status=HTTP_200_OK)

    if result['liveliness_status'] == 'fake':
        return Response({'status':'success','liveliness_status':'fake'}, status=HTTP_200_OK)

    if result['liveliness_status'] == 'live':
        output_image = result['output_image']
        output_image = ''.join(['data:image/jpeg;base64,',output_image])
        return Response({'status':'success','liveliness_status':'live','face_image_name':face_image_file_name,'face_image_base64':output_image}, status=HTTP_200_OK)