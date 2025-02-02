from django.conf import settings
import requests
import os
import base64
from time import time
import hashlib
from django.core.files.base import ContentFile
import json
import platform
import string 
import random 

def get_file_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        try:
            _time = os.path.getctime(path_to_file)
            return _time
        except:
            return -1
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_UPLOAD_EXTENSIONS

def is_mobile_no_valid(mobile_no):
    if mobile_no is None or not mobile_no.startswith('01') or len(mobile_no) != 11:
        return False
    else:
        return True

def image_as_base64(image_file, format='png'):
    if image_file is None:
        return None
    if not os.path.isfile(image_file):
        return None
    
    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
        encoded_string = encoded_string.decode('utf-8')
    return 'data:image/%s;base64,%s' % (format, encoded_string)

def image_as_secure_uri(image_file):
    if not image_file:
        return ''
    image_secure_uri = ''.join(['/securefile/', image_file])
    return image_secure_uri

def do_ocr_id_front_back(file_path, face_region={}):
    try:
        if face_region is None:
            face_region = {'is_null':True}
        url = '{}/do_ocr_id_front_back'.format(settings.OCR_SERVICE_BASE_URL)
        req = requests.get(url, {'image':file_path, 'face_region': json.dumps(face_region)},timeout=30)
        return req.json()
    except:
        return None

def face_detection_service(image_path):
    try:
        url = '{}/get_face_roi'.format(settings.FACE_SERVICE_BASE_URL)
        req = requests.get(url, {'image':image_path},timeout=30)
        return req.json()
    except:
        return None
        
def do_ocr_ec_compare(ec_file_path, nid_data):
    try:
        url = '{}/do_ocr_ec_compare'.format(settings.OCR_SERVICE_BASE_URL)
        req = requests.get(url, {'image':ec_file_path, 'nid_data': json.dumps(nid_data)},timeout=30)
        return req.json()
    except Exception as e:
        print(e)
        return None

def crop_id(file_path, width=900, height = 600):
    try:
        url = '{}/detect_id'.format(settings.OCR_SERVICE_BASE_URL)
        req = requests.get(url, {'image':file_path, 'width': width, 'height': height},timeout=30)
        return req.json()
    except:
        return None

def match_faces(face1_path, face2_path):
    try:
        url = '{}/compare_faces'.format(settings.FACE_SERVICE_BASE_URL)
        req = requests.get(url, {'image1':face1_path, 'image2': face2_path},timeout=30)
        return req.json()
    except:
        return None

def detect_liveliness(video_file, output_image=None, rotate=0):
    try:
        url = '{}/check_liveliness'.format(settings.LIVELINESS_BASE_URL)
        req = requests.get(url, {'video_file':video_file, 'video_file': video_file, 'rotate':rotate},timeout=60)
        return req.json()
    except:
        return None

def generate_profile_pdf(data):
    try:
        req_headers = {'Content-Type':'application/json; charset=utf-8', 'Connection':'keep-alive'}
        req = requests.post(settings.PDF_SERVICE_BASE_URL, json=data, headers=req_headers, timeout=30)
        return req.json()
    except:
        return None
def filename_to_hash(file_name):
    ext = file_name.split('.')[-1]
    file_name = file_name + str(time())
    encoded_name = hashlib.sha256(file_name.encode()).hexdigest()
    encoded_name = encoded_name + '.' + ext
    return encoded_name



def base64_to_image(data):
    if len(data) > 100:
        _format, imgstr = data.split(';base64,') 
        ext = _format.split('/')[-1] 
        rand_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 32))
        data = ContentFile(base64.b64decode(imgstr), name=f'{rand_name}.' + ext)

        return data
    else:
        return None