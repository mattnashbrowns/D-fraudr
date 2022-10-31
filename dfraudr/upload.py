import os
from os.path import exists as file_exists
from flask import (Flask, flash, request, redirect, url_for, 
    send_from_directory, Blueprint, render_template, g, current_app)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
import benford
from dfraudr.db import get_db
import hashlib

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv'}


bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    UPLOAD_LOCATION = current_app.config['UPLOAD_LOCATION']
    if request.method == 'POST':
        cur = get_db()
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
            fullpath = os.path.join(UPLOAD_LOCATION, filename)
            
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
  cursor = get_db()
  cursor.execute( 'SELECT id, filename, description, md5sum from df_datafiles' )
  files = cursor.fetchall()
  
  if (files):
    return render_template('files.html', filelist=files)    
  else:
    return redirect(url_for('upload_file'))

  
@bp.route('/uploads/<name>')
def download_file(name):
  return send_from_directory(UPLOAD_LOCATION, name)