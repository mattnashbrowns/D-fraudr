import pandas as pd
import numpy as np


# Takes a list of numbers as input, returns a list of the first digits
def first_digits(numbers):
    firsts = [ int(str(x)[0]) for x in numbers ]
    return firsts

# get a list of Benford probabilities for the non-zero digits of an N-based number system
# N defaults to 10
def get_probs(base=10):
    numbers = range(1, base)
    probabilities = [ np.log10(1 + (1/x)) for x in numbers ]
    return probabilities
    
# Takes a list of numbers presumed to be naturally-occurring
# Returns a list of counts for each digit from 1 to (base - 1)
# containing the frequency of each one's occurrence in the list
def get_freqs(numbers,base=10):
    all_digits = range(1,base)
    
    digits = first_digits(numbers)
    unique, counts = np.unique(digits, return_counts=True)
    counts_dict = dict(zip(unique,counts))
    
    # Check for missing digits
    for x in all_digits:
        if x not in counts_dict:
            counts_dict[x] = 0
            
    return counts_dict
        
    

        