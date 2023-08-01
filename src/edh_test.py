import importlib
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil
import os
from sys import argv, exit

DEFAULT_TR = 0.0011

def main():
    if len(argv) != 4:
        print('SyntaxError: Must provide 4 valid arguments')
        print('Usage: python3 hist_test_run {mod_name} {method_name} {set #}')
        exit(1)

    if argv[2] == 'single':
        single_hist_test(argv[1], int(argv[3]))
        exit(0)
    if argv[2] == 'all':
        all_hist_test(argv[1])
        exit(0)

    print('SyntaxError: Invalid method name')
    exit(1)

def load_model(mod_name):
    """loads model name passed""" 
    try:
        mod = importlib.import_module(f'models.{mod_name}')
    except ImportError:
        print(f'LoadError: "{mod_name}" not found')
        exit(1)
    return mod

def load_dataset(set_num):
    """loads dataset # passed"""
    transients = np.load('../dataset/transients.npy')
    bounds = np.load('../dataset/boundaries.npy')
    return bounds[set_num, :], transients[set_num, :]

def gen_vals(b_set):
    """generates x & y values from ED buckets"""
    diffs = np.diff(b_set)
    b_set = b_set[:-1] + (diffs/2)
    t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])
    return b_set, t_set

def single_hist_test(mod_name, set_num):
    """plots histogram, scatterplot, and regression equation against ground_truth data"""
    b_set, transients = load_dataset(set_num)
    mod = load_model(mod_name) 

    b_set, t_set = gen_vals(b_set)
    x = np.arange(0, len(transients))
    predicted_vals = mod.regression_fit(b_set, t_set, x)

    # Plot graph
    ax = plt.gca()
    ax.set_ylim([0, np.max(transients)])
    bins = np.append(b_set, np.max(b_set)+1)
    plt.hist(b_set, bins=bins, edgecolor='black', linewidth=0.5, alpha=0.2)
    plt.plot(x, transients, 'k', label='Ground truth')
    plt.plot(b_set, t_set, 'g', label='Estimated curve')
    plt.plot(x, predicted_vals, 'r', label=f'{mod_name} regression')
    plt.legend() 
    plt.title(f'{mod_name} regression')
    plt.savefig(f'{mod_name}_graph.png')

def all_hist_test(mod_name):
    """plots histogram & regression for all transient datasets"""
    mod = load_model(mod_name)
    os.makedirs('images', exist_ok=True)

    for i in range(29):
        b_set, transients = load_dataset(i)
        b_set, t_set = gen_vals(b_set)
        x = np.arange(0, len(transients))
        predicted_vals = mod.regression_fit(b_set, t_set, x)

        # Plot graph
        ax = plt.gca()
        ax.set_ylim([0, np.max(transients)])
        bins = np.append(b_set, np.max(b_set)+1)
        plt.hist(b_set, bins=bins, edgecolor='black', linewidth=0.5, alpha=0.2)
        plt.plot(x, transients, 'k', label='Ground truth')
        plt.plot(b_set, t_set, 'g', label='Estimated curve')
        plt.plot(x, predicted_vals, 'r', label=f'{mod_name} regression')
        plt.legend() 
        plt.title(f'{mod_name} regression')
        plt.savefig(f'images/{i}_{mod_name}_graph.png')
        plt.clf()

    shutil.make_archive(f'all_{mod_name}_graphs', 'zip', 'images')

if __name__ == '__main__':
    main()
