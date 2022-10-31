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
import benford as bf

app = Flask(__name__)

bp = Blueprint('analyze', __name__)



# Show the columns available in the file and choose one to evaluate
@bp.route('/analyze_file/<int:id>', methods=['GET', 'POST'])
def analyze_file(id, delimiter='\t'):
    file_record = get_file(id)
    filename = file_record['filename']
    
    file_df = get_file_dataframe(filename)
    
    stats = file_df.describe()
    
    # numbercols is a list of Series objects, 
    # each of which is a numeric column in this file
    numbercols = [ file_df[x] for x in stats.columns.array ]
    
    return render_template('analyze_file.html', file_record=file_record, columns=numbercols, stats=stats)

    
# Analyze a column for its adherence to Benford's Law
@bp.route('/analyze_column/<int:file_id>/<column_name>')
def analyze_column(file_id, column_name):
    file_record = get_file(file_id)
    
    # Future: base this on the number-base
    all_digits = range(1,10)
    
    # Get a pandas dataframe representing the file
    df = get_file_dataframe(file_record['filename'])

    # Extract a pandas Series representing all of the positive values in the Series
    column = df[column_name][df[column_name] > 0]
    pop_size = len(column)
    
    # Get a list of the probability of each digit occurring 
    # according to Benford's Law
    probs = bf.get_probs()
    
    # Get a list of the expected counts of each digit
    expected = [ int(x * pop_size) for x in probs ]
    
    # Get a list of all the first digits in the Series
    digits = bf.first_digits(column)
    
    # Get a dict listing the frequency of each digit
    freqs = bf.get_freqs(digits)
    
    # Get a list of the actual counts of each digit
    actual = [ freqs[x] for x in all_digits ]
    
    return render_template('analyze_column.html', 
        actual=actual, 
        expected=expected, 
        column_name=column_name,
        )
    
# Retrieves the file's row from the DB and returns a DictRow object
def get_file(id):
    cursor = get_db()
    cursor.execute('SELECT * FROM df_datafiles WHERE id=%s', (id,))
    file = cursor.fetchone()
    return file
    
def get_file_dataframe(filename, delimiter=None):
    # Build the path to the uploaded file
    filepath = os.path.join(current_app.config['UPLOAD_LOCATION'], filename )
    # Read the file into a pandas dataframe
    file_df = pd.read_csv(filepath, sep = delimiter)
    
    return file_df



    
        
    