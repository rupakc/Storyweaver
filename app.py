from flask import Flask, render_template, session, Response, request
from pymagnitude import *
from config import constants
from predict import generic_image_match, generic_object_detector
import json


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
model_full_path = constants.MODEL_FOLDER_PATH + constants.WORD_TO_VEC_MODEL_NAME
vectors = Magnitude(model_full_path)


@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.route("/", methods=['GET', 'POST'])
def root():
    return render_template('search.html')


@app.route("/dissect", methods=['GET', 'POST'])
def dissect():
    return render_template('dissect.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    search_term = 'A teacher teaching the class of students'
    if 'search_term' in request.args:
        search_term = str(request.args['search_term']).strip()
    response = dict({'imageList': generic_image_match.get_image_hash_names(search_term, vectors)})
    return Response(json.dumps(response), status=200, mimetype='application/json')


@app.route("/getobjects", methods=['GET', 'POST'])
def getobjects():
    search_term = 'girls are playing in the field with gods'
    if 'search_term' in request.args:
        search_term = str(request.args['search_term']).strip()
    detector_model_object = generic_object_detector.get_initialized_detector_model()
    r = generic_object_detector.object_extraction_pipeline(search_term, vectors, detector_model_object)
    response = dict({'imageObjectList': r})
    return Response(json.dumps(response), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
