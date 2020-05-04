from flask import Flask, jsonify, request, redirect, make_response
import logging, sys, time
import cv2
import numpy as np
import os, re
from werkzeug.datastructures import ImmutableMultiDict
import face_recognition

# Intializion code. Also reduces cold start time 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


# This functions checks for image file extensions 
# curl -XPOST -F "file=@.jpeg "  -F url='https://' http://localhost:5000/upload

def allowed_file(filename):
    """
    params:
        - filename: Name of the image to be checked for extension 
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    This path takes two inputs in multiform/data.
    Name of paramaters:
    file: Image of the user
    url: This should be in json . Ex: {'url':'http://..'}

    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return make_response(jsonify("Msg: Upload an image"),415)

        url= dict(request.form)
        test_url = re.search("^http|https|rstp", url['url'])
        if test_url:
            file = request.files['file']

            if file.filename == '':
                return make_response(jsonify("Msg: Upload an image"),415)

            if file and allowed_file(file.filename):
                found = detect_faces(file,url)
                if found:
                    return make_response(jsonify("Msg: Person Found"),200)
                else:
                    return make_response(jsonify("Msg: Person not found"),417)
        else:
            return make_response(jsonify("Msg: Invalid url"), 415)




# Detects a face, returns boolean
def detect_faces(file_stream, url):

    """
    params:
    - file_stream: Image served as binary stream
    - url: Url for video source
    """
    logger.debug("Into detect faces function")
    start_time = time.perf_counter()
    logger.info(url['url'])
    for i in range(5):
        try: 
            video_capture = cv2.VideoCapture(url['url']) 
        except:
            if i > 5:
                return False
            else:
                logger.debug("retrying to fetch the video")
              



    try:
        logger.debug("Loading image file")
        person_tobe_found = face_recognition.load_image_file(file_stream)
        person_tbf_encoding = face_recognition.face_encodings(person_tobe_found)[0]

        known_face_encodings = [
            person_tbf_encoding
        ]
        known_face_names = [
            "Person"
        ]

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
    except:
        e = sys.exc_info()
        logger.exception(e)
        return False


    while True:
        try:
            logger.debug("Read the video feed")
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame,None, fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                logger.debug("Processing a frame")
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance= 0.5)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]                   
                    
                    face_names.append(name)
                    logger.debug(face_names)
                    if 'Person' in face_names:
                        logger.info("Actually found the person")
                        return True
        except:
            e = sys.exc_info()
            logger.exception(e)
        process_this_frame = not process_this_frame

        end_time = time.perf_counter()
        run_time = end_time - start_time
        
        if run_time > 20: # No. of seconds we look for that person 
            return False

    video_capture.release()
    cv2.destroyAllWindows()