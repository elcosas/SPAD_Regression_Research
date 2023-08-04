#!/usr/bin/env python3

import importlib
import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit

DEFAULT_TR = 0.0011

def main():
    if len(argv) != 3:
        print('SyntaxError: Must provide filename and regression model name as arguments')
        exit(1)
    data_set, model = load_args(argv[1], argv[2])

    new_set = []
    for row in data_set:
        new_row = []
        for col in row:
            b_set, t_set = gen_vals(col)
            pred_vals = model.regression_fit(b_set, t_set, np.arange(0, 1000))
            max_point = np.max(pred_vals)
            new_row.append(max_point)
        new_set.append(np.array(new_row))
    new_set = np.array(new_set)

    plt.imshow(new_set)
    plt.savefig(f'{argv[2]}_depthmap.png')

def load_args(file_name, mod_name):
    """Loads filename and regression module"""
    try:
        bounds = np.load(file_name)
    except:
        print(f'LoadError: {file_name} not found') 
        exit(1)

    try:
        module = importlib.import_module(f'models.{mod_name}')
    except ImportError:
        print(f'LoadError: {mod_name} not found') 
        exit(1)

    return bounds, module

def gen_vals(b_set):
    """Generates x & y values from ED bins"""
    diffs = np.diff(b_set)
    b_set = b_set[:-1] + (diffs/2)
    t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])
    return b_set, t_set

if __name__ == '__main__':
    main()
