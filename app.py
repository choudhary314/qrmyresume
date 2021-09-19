# coding=utf-8
from datetime import time
from flask import Flask, render_template, request
from werkzeug.utils import redirect, secure_filename
import os
import re
import hashlib
from flask_qrcode import QRcode


app = Flask(__name__)
qrcode = QRcode(app)
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = re.escape(r'C:\Users\tarun\OneDrive\Documents\Projects\qrmyresume\uploads')
app.config['MAX_CONTENT_LENGTH'] = 40000000
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         hasher = hashlib.md5()
         buf = file.read()
         hasher.update(buf)
         filename = (hasher.hexdigest())
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         return redirect('/render')


@app.route('/render')
def render():
   url = "https://linkedin.com"
   return render_template("render.html", value = url )

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
