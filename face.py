from services.face import inference as engine
from flask import Flask, jsonify, request
import os
app = Flask(__name__)


@app.route('/compare_faces')
def compare_faces():
    image1 = request.args.get('image1')
    image2 = request.args.get('image2')

    if not os.path.isfile(image1) or not os.path.isfile(image2):
        print('Not valid file')
        response = {'score':0}
        return jsonify(response)

    cosine, euclid, td, tc = engine.compare_faces(image1,image2)
    if cosine == -1:
        response = {'score':0, 'time_taken, detection : comparison': '{} {}'.format(td,tc)}
        return jsonify(response)
    cosine = cosine * 100
    cosine = 100 - cosine
    cosine = int(cosine)
    if cosine >= 52 and cosine < 65:
        cosine += 15
    response = {'score':cosine, 'time_taken, detection : comparison': '{} {}'.format(td,tc)}
    return jsonify(response)

@app.route('/get_face_roi')
def get_face_roi():
    image = request.args.get('image')

    if not os.path.isfile(image):
        response = {'status':'failed'}
        return jsonify(response)
    with engine.graph.as_default():
        status, res = engine.detect_face_roi(image)
    if status == False:
        response = {'status':'failed'}
        print(response)
        return jsonify(response)

    print(res)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)