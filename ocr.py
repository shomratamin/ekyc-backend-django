from services.ocr.detect_nid_fileds import detect_nid_fields_front_back_ocr, ec_ocr_compare_nid
from services.ocr.id_card_detection import detect_id_card_and_save
from flask import Flask, jsonify, request
import os
import json
app = Flask(__name__)

@app.route('/do_ocr_id_front_back')
def do_ocr_id():
    image = request.args.get('image')
    _fr = request.args.get('face_region')
    face_region = None
    if _fr is not None:
        face_region = json.loads(_fr)
        if 'is_null' in face_region:
            face_region = None
    if not os.path.isfile(image):
        print('Not valid file')
        return jsonify({'status':'error'})
    ocr_out = detect_nid_fields_front_back_ocr(image, face_region)
    return jsonify(ocr_out)

@app.route('/do_ocr_ec_compare')
def do_ocr_ec_compare():
    image = request.args.get('image')
    nid_data = json.loads(request.args.get('nid_data'))

    if not os.path.isfile(image):
        print('Not valid file')
        return jsonify({'status':'error'})
    print(nid_data)
    scores_out = ec_ocr_compare_nid(image, nid_data)
    return jsonify(scores_out)
    
@app.route('/detect_id')
def detect_id():
    image = request.args.get('image')
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))
    if not os.path.isfile(image):
        print('Not valid file')
        return jsonify({'status':'error'})
    res, _t = detect_id_card_and_save(image, width, height)
    print(res, 'time', _t)
    if res:
        return jsonify({'status':'success', 'time_taken':_t})
    else:
        return jsonify({'status':'failed', 'time_taken':_t})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=False)