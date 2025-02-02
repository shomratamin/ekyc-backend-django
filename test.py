from time import time
import requests
# from services.ocr.detect_nid_fileds import detect_nid_fields_front_back_ocr
# from services.ocr import page as engine
import cv2

def face_test():
       from services import face
       image1 = 'C:/Users/User/Desktop/EKYC Demo/6405477941_voterPhoto.jpg'
       image2 = 'C:/Users/User/Desktop/EKYC Demo/2690243804553_voterPhoto.jpg'

       consine, euclid, t1, t2 = face.engine.compare_faces(image1,image2)
       consine, euclid, t1, t2 = face.engine.compare_faces(image1,image2)
       print('consine', consine)
       print('euclid', euclid)
       print('detector comparator', t1, t2)

def ocr_nid_test():
       image = 'C:/Users/User/Desktop/EKYC Demo/6405477941 (2).jpg'
       results = engine.do_ocr_field(image)
       results = engine.do_ocr_field(image)
       print(results)

def ocr_nid_back_test():
       from services import ocr
       image = 'C:/Users/User/Desktop/EKYC Demo/2690243804553_voterInfo.jpg'
       t1 = time()
       result = ocr.engine.do_ocr_nid_back(image)
       t2 = time()
       print(result)
       print('time taken', t2-t1)

def ocr_ec_test():
       image = 'C:/Users/User/Desktop/EKYC Demo/1923464083_voterInfo_m2HeWnZ.jpg'
       result = engine.do_ocr_ec_compare(image,None)
       print(result)

def ocr_id_service():
       ocr_req = requests.get('http://localhost:4000/do_ocr_id_front',{'image':'uploads/6405477941 (2).jpg'})
       print(ocr_req.json())

def face_compare_service():
       face_req = requests.get('http://127.0.0.1:5000/compare_faces',{'image1':r'E:\Projects\ekyc\darknet\build\nid_data_illum\1923464083_voterPhoto_chZZTYS.jpg','image2':r'E:\Projects\ekyc\darknet\build\nid_data_illum\ac559917b11d7cdaf1f4d9130eeff44743ab12171ba0817539b88a7257ec73db.jpg'})
       print('face match score', face_req.json())

def id_card_service():
       id_req = requests.get('http://localhost:4000/detect_id',{'image':r'uploads/0d58b554f9a5dfb2698c395e89371c1a27db24264b8fd1de8663d5e6edc18626.jpg'})
       print('id response', id_req.json())
def ec_ocr_service():
       import json
       customer_profile_nid_data = {'id_no_nid':'customer_profile.nid_no', \
            'birth_nid': 'customer_profile.dob', 'name_b_nid' :'সরকার জহির আহমেদ', \
            'name_e_nid': 'SARKAR ZAHIR AHAMED', 'father_nid': 'customer_profile.father_name', \
            'mother_nid': 'customer_profile.mother_name', 'pres_addr_nid': 'customer_profile.pres_address', \
            'perm_addr_nid': 'customer_profile.perm_address'}
       id_req = requests.get('http://localhost:4000/do_ocr_ec_compare',{'image':r'C:\Users\User\Desktop\nid\1515322453920_voterInfo.jpg', 'nid_data':json.dumps(customer_profile_nid_data)})
       print('id response', id_req.text)


def face_detection_service(image_path):
       face_req = requests.get('http://127.0.0.1:5000/get_face_roi',{'image':'{}'.format(image_path)})
       return face_req.json()

if __name__ == "__main__":
       # face_test()
       # ocr_nid_test()
       # ocr_ec_test()
       # ocr_nid_back_test()
       # ocr_id_service()
       import sys
       t1 = time()
       # face_compare_service()
       ec_ocr_service()
       # image_file = 'E:\\Projects\\ekyc\\darknet\\build\\nid_data_illum\{}.jpg'.format(sys.argv[1])
       # face_region = face_detection_service(image_file)
       # detect_nid_fields_front_back_ocr(image_file, face_region)
       t2 = time() - t1
       print(t2)
       # id_card_service()