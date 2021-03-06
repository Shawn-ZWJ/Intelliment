import os
from frames import frame_capture
from aws import build_dataset
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from intelliment import generate_graphs

ALLOWED_EXTENSIONS = set(['mp4'])

UPLOAD_FOLDER = './static/upload'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            file_path = './static/upload/' + filename
            frame_capture(file_path)
            build_dataset()
            generate_graphs()
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
