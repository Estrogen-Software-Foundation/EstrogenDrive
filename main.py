#!/bin/python3

import os
import uuid
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER']      = './database/' #Files stored in the database file 
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 #8 meg max file size


@app.errorhandler(413)
def request_entity_too_large(error): return "File Too Large", 413

@app.errorhandler(404)
def not_found(e): return render_template("404.html"), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No files")
            return redirect(request.url)

        file = request.files['file']


        if file.filename == '': 
            flash("No selected file")
            return redirect(request.url)

        

        if file:
            file_uuid = str(uuid.uuid4())
            file_extension = file.filename.split('.')

            filename = secure_filename(file_uuid + "." + file.filename.split(".",1)[1])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('download_file', name=filename))


    return render_template('index.html')

@app.route('/file/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)