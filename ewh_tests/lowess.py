import numpy as np
from statistics import mode
from moepy import lowess

def regression_fit(b_set, t_set):
    """fits lowess regression to dataset, returns predicted values"""
    lowess_mod = lowess.Lowess()
    lowess_mod.fit(b_set, t_set, frac=0.1)
    return lowess_mod.predict(b_set)

def filter(b_set, t_set):
    """filter ambient light"""
    amb_light = mode(t_set)
    filters = [not val == amb_light for val in t_set]
    return b_set[filters], t_set[filters]

