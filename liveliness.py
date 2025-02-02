from flask import Flask, jsonify, request
import os
import json
from services.liveliness.live import analyze_liveliness
app = Flask(__name__)
    
@app.route('/check_liveliness')
def check_liveliness():
    video_file = request.args.get('video_file')
    image_to_save = request.args.get('image_file')
    rotate = request.args.get('rotate')
    if video_file is None:
        return jsonify({'status':'error', 'message':'Please specify a video file'})

    status, real_ratio, image_bas64, time_taken = analyze_liveliness(video_file,image_to_save, rotate)
    if real_ratio > 70.0:
        return jsonify({'status':'success', 'liveliness_status':'live', 'live_ratio': real_ratio, 'output_image': image_bas64, 'time_taken':time_taken})
    else:
        return jsonify({'status':'success', 'liveliness_status':'fake','live_ratio': real_ratio, 'time_taken':time_taken})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=False)