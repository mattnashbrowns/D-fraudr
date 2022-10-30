import pytest

import benford

import numpy as np
import pandas as pd

datafile = 'tests/census_2009b.csv'

census_df = pd.read_csv(datafile, sep='\t')

pop_data = census_df['7_2009'][census_df['7_2009'] > 0]

def test_data_check():
    assert len(pop_data) == 19507
    assert 'int' in str(pop_data.dtype)
    
def test_probability_distribution():
    probs = benford.get_probs(10)
    assert len(probs) == 9
    assert probs[0] == 0.3010299956639812
    
def test_digit_razor():
    digits = benford.first_digits(pop_data)
    