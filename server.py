from flask import Flask
from flask import request
from flask import render_template
import flask
import os
import server_helper
import cv2
import _thread

app = Flask(__name__)

cache_path = os.path.join(os.getcwd(), "cache")
model_path = os.path.join(os.getcwd(), "img", "face_recognition")



def save_cache(file):
    cache_file = os.path.join(cache_path, file.filename)
    file.save(cache_file)
    return cache_file


def save_model(frame, filename):
    cv2.imwrite(os.path.join(model_path, filename) + ".jpg", frame)

@app.route('/face_detection', methods=['POST'])
def compare_face():
    f = request.files['image']
    file_path = save_cache(f)
    static_filename=server_helper.compare_image(file_path)
    return flask.redirect(static_filename)


@app.route("/upload_model", methods=['POST'])
def upload_model():
    f = request.files['image']
    try:
        file_path = save_cache(f)
        frame = server_helper.corp_image(file_path)
        save_model(frame, f.filename)
        _thread.start_new_thread(server_helper.reload_model,())
    except:
        return "no"
    return "yes"


@app.route('/', methods=["GET"])
def index():
    return render_template('client.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8999,threaded=True)
