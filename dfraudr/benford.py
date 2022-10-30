#!/usr/bin/env python3
 
import pandas as pd
import numpy as np

class Benford:
    def __init__(self,base=10):
        self.base = base
        self.probabilities = _get_probs()

    # Takes a list of numbers as input, returns a list of the first digits
    def first_digits(numbers):
        firsts = [ str(x)[0] for x in numbers ]
        return firsts
    
    # get a list of Benford probabilities for the non-zero digits of an N-based number system
    # N defaults to 10
    def _get_probs(self):
        numbers = range(1, self.base)
        probabilities = [ np.log10(1 + (1/x)) for x in numbers ]
        return probabilities
        
    # Takes a list of numbers presumed to be naturally-occurring
    # Returns a list of counts for each digit from 1 to (base - 1)
    # containing the frequency of each one's occurrence in the list
    def get_freqs(numbers):
        all_digits = range(1,self.base)
        digits = first_digits(numbers)
        unique, counts = np.unique(digits, return_counts=True)
        missing = [ x for x in all_digits if x not in unique ]
        for x in missing:
            counts.insert(x - 1, 0)
        return counts

        