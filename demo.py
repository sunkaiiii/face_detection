# coding: utf-8
import hashlib
import datetime 
import flask
from flask import render_template, url_for
import pymongo 
import bson.binary 
import bson.objectid 
import bson.errors 
from cStringIO import StringIO 
from PIL import Image 

app = flask.Flask(__name__) 
app.debug = True
app.secret_key = 'some string hard to guess'
db = pymongo.MongoClient('localhost', 27017).test 
allow_formats = ('jpeg', 'png', 'gif')


def save_file(f):
    if len(f.read()) > 2 * 1024 * 1024:
        flask.flash('不能上传大于15M的图片!')
        flask.redirect('/')
    content = StringIO(f.read()) 
    try: 
        mime = Image.open(content).format.lower() 
        if mime not in allow_formats: 
            raise IOError() 
    except IOError: 
        flask.abort(400) 

    sha1 = hashlib.sha1(content.getvalue()).hexdigest() 
    c = dict( 
        content=bson.binary.Binary(content.getvalue()), 
        mime=mime, 
        time=datetime.datetime.utcnow(), 
        sha1=sha1, 
    ) 
    try: 
        db.files.save(c) 
    except pymongo.errors.DuplicateKeyError: 
        pass 
    return sha1 


@app.route('/img/<sha1>')
def serve_file(sha1): 
    try: 
        f = db.files.find_one({'sha1': sha1}) 
        if f is None: 
            raise bson.errors.InvalidId() 
        if flask.request.headers.get('If-Modified-Since') == f['time'].ctime(): 
            return flask.Response(status=304) 
        resp = flask.Response(f['content'], mimetype='image/' + f['mime']) 
        resp.headers['Last-Modified'] = f['time'].ctime() 
        return resp 
    except bson.errors.InvalidId: 
        flask.abort(404) 


@app.route('/upload', methods=['POST']) 
def upload(): 
    f = flask.request.files['uploaded_file'] 
    sha1 = save_file(f) 
    return flask.redirect('/')


@app.route('/') 
def index():
    photos_cursor = db.files.find({}, {'content': 0})
    photos_list = []
    for p in photos_cursor:
        photos_list.append(p)
    return render_template('index.html', photos=photos_list)

if __name__ == '__main__': 
    app.run(port=7777)
