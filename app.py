# coding=utf-8
from datetime import time
from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect, secure_filename, send_from_directory
import os, json
import hashlib
import qrcode

key = os.urandom(12).hex()

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 40000000
app.config['SECRET_KEY'] = key
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
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + '.pdf'))
         (qrcode.make("http://localhost:5000/{0}".format(filename))).save("./static/qr_render/{0}".format(str(filename) + '.jpg'))
         session['filename'] = filename + '.jpg'
         return redirect(url_for('render', filename = filename))


@app.route('/render')
def render():
   filename = request.args['filename']
   filename = session['filename']
   return render_template("render.html", filename=('static/qr_render/' + filename))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/<variable>', methods=['GET'])
def send_pdf(variable):
   return send_from_directory(app.config['UPLOAD_FOLDER'], variable + '.pdf', environ=request.environ)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
