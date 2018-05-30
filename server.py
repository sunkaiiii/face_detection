from flask import Flask
from flask import request
from flask import render_template
import flask
import os
import server_helper
import cv2
import _thread

app = Flask(__name__)

cache_path = os.path.join(os.getcwd(), "cache")  # 初始化临时文件的位置
model_path = os.path.join(os.getcwd(), "img", "face_recognition")  # 初始化脸部模型所在的位置


def save_cache(file):
    cache_file = os.path.join(cache_path, file.filename)
    file.save(cache_file)
    return cache_file


def save_model(frame, filename):
    cv2.imwrite(os.path.join(model_path, filename) + ".jpg", frame)


@app.route('/face_detection', methods=['POST'])
def compare_face():
    f = request.files['image']
    file_path = save_cache(f)  # 保存上传的图片到临时文件区
    static_filename = server_helper.compare_image(file_path)  # 检测人脸，并获取检测结果图片的网址
    return flask.redirect(static_filename)  # 客户端跳转


@app.route("/upload_model", methods=['POST'])
def upload_model():  # 上传模型图片
    f = request.files['image']
    try:
        file_path = save_cache(f)
        frame = server_helper.corp_image(file_path)  # 对上传的图片进行二次处理
        save_model(frame, f.filename)
        _thread.start_new_thread(server_helper.reload_model, ())  # 保存成功后，刷新脸部模型
    except:
        return "no"
    return "yes"


@app.route('/', methods=["GET"])
def index():
    return render_template('client.html')  # 主页，显示简单的文件上传功能


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8999, threaded=True)  # 启动服务器
