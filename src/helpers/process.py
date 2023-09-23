#!/usr/bin/env python3
import numpy as np

def convert_ew(b_set, t_set, res):
    """Generates x & y vals to fit EWH"""
    bins = len(b_set)+1
    step = res / bins
    b_set = np.arange(0, res+step, step)
    b_set = b_set[:-1] + (np.diff(b_set)/2)
    t_set = np.array([np.mean(arr) for arr in np.array_split(t_set, bins)])
    return b_set, t_set

def convert_ed(b_set, t_set, res, ambient):
    """Generates x & y vals to fit EDH"""
    b_set = np.concatenate([[0], b_set, [res]], axis=None)
    diffs = np.diff(b_set)
    b_set = b_set[:-1] + (diffs/2)
    t_set = np.array([ambient / (diffs[i] / diffs[0]) for i in range(len(b_set))])
    return b_set, t_set