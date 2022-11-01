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
UPLOAD_LOCATION='instance/uploads'

bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        cur = get_db()
        file_desc = 'Untitled'
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
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

            file.save(fullpath)
            file_data = file.read()
            file_md5 = hashlib.md5(file_data).hexdigest()
            
            already_file = cur.execute('SELECT * FROM df_datafiles WHERE md5sum=?', (file_md5,)).fetchone()
            
            if already_file:
                flash('A file with checksum "%s" already exists, not inserting' % file_md5)
            else:
                file_type = file.content_type
                flash('Saved file "%s" (%s) with checksum "%s"' % (file.filename, file_type, file_md5) )
                cur.execute('INSERT INTO df_datafiles(filename, description, md5sum) VALUES (?,?,?)', 
                    (filename, file_desc, file_md5) )
                cur.commit()
        
            
            return redirect(url_for('upload.files'))
    return render_template('upload.html')

    
@bp.route('/files', methods=['GET','POST'])
def files():
  cursor = get_db()
  files = cursor.execute( 'SELECT id, filename, description, md5sum from df_datafiles' ).fetchall()
  
  if (files):
    return render_template('files.html', filelist=files)    
  else:
    return redirect(url_for('upload_file'))

  
@bp.route('/uploads/<name>')
def download_file(name):
  return send_from_directory(UPLOAD_LOCATION, name)
