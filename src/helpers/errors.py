#!usr/bin/env python3

import numpy as np

def mse(expected, predicted):
    return np.sum((expected-predicted)**2) / predicted.size

def rmse(expected, predicted):
    return np.sqrt(mse(expected, predicted))

def mae(expected, predicted):
    return np.sum(np.absolute(expected-predicted)) / predicted.size

def max_err(expected, predicted):
    return np.abs(np.max(expected) - np.max(predicted))

if __name__ == '__main__':
    pass
