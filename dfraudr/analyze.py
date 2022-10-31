import os
from os.path import exists as file_exists
from flask import Flask, flash, request, redirect, url_for, send_from_directory, Blueprint, render_template, g
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
import benford
from dfraudr.db import get_db
import hashlib
import pandas as pd

app = Flask(__name__)
bp = Blueprint('analyze', __name__)
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

@bp.route('/analyze', methods=['GET', 'POST'])
def analyze_file(id):
    file_record = get_file(id)
    
    return render_template('analyze.html', )
    
# Retrieves the file's row from the DB and returns a DictRow object
def get_file(id):
    cursor = get_db()
    cursor.execute('SELECT * FROM df_datafiles WHERE id=%s', id)
    file = cursor.fetchone()
    return file
    
def load_file(filename, delimiter=','):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_df = pd.read_csv(filepath, sep = delimiter)
    
    columns = file_df.columns.array
        