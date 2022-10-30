import os
from os.path import exists as file_exists
from flask import Flask, flash, request, redirect, url_for, send_from_directory, Blueprint, render_template, g
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
import benford
from dfraudr.db import get_db
import hashlib

UPLOAD_FOLDER = 'instance/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        file_desc = 'Untitled'
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file_data = file.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        file_type = file.content_type
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if file_exists(fullpath):
                flash('File "%s" already exists!' % fullpath)
            else:
                file.save(fullpath)
                flash('Saved file "%s" (%s) with checksum "%s"' % (file.filename, file_type, file_md5) )
            
            cur.execute('INSERT INTO df_datafiles(filename, description) VALUES (%s,%s)', 
                (filename, file_desc) )
            
            return redirect(url_for('upload.files'))
    return render_template('upload.html')

    
@bp.route('/files', methods=['GET','POST'])
def files():
  return render_template('files.html')
  
@bp.route('/uploads/<name>')
def download_file(name):
  return send_from_directory(app.config["UPLOAD_FOLDER"], name)