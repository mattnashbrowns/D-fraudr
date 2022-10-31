import os
from os.path import exists as file_exists
from flask import (Flask, flash, request, redirect, url_for, 
    send_from_directory, Blueprint, render_template, g, current_app)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
import benford
from dfraudr.db import get_db
from dfraudr import create_app
import hashlib
import pandas as pd

app = Flask(__name__)

bp = Blueprint('analyze', __name__)



# Show the columns available in the file and choose one to evaluate
@bp.route('/analyze/<int:id>', methods=['GET', 'POST'])
def analyze_file(id, delimiter=None):
    file_record = get_file(id)
    filepath = os.path.join(current_app.config['UPLOAD_LOCATION'], file_record['filename'])
    
    # Read the file into a pandas dataframe
    file_df = pd.read_csv(filepath, sep = delimiter)
    stats = file_df.describe()
    
    # numbercols is a list of Series objects, 
    # each of which is a numeric column in this file
    numbercols = [ df[x] for x in stats.columns.array ]
    
    return render_template('analyze.html', columns=numbercols, stats=stats)
    
# Retrieves the file's row from the DB and returns a DictRow object
def get_file(id):
    cursor = get_db()
    cursor.execute('SELECT * FROM df_datafiles WHERE id=%s', (id,))
    file = cursor.fetchone()
    return file



    
        
    