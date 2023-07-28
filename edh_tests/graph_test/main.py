import importlib
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil

DEFAULT_TR = 0.0011

def load_model(mod_name):
    """loads model name passed""" 
    try:
        mod = importlib.import_module(mod_name)
    except ImportError:
        print(f'Load Error: "{mod_name}" not found')
        return None
    return mod

def load_dataset(set_num):
    """loads dataset # passed"""
    transients = np.load('../proprietary/transients_interp.npy')
    bounds = np.load('../proprietary/edh_boundaries.npy')
    return bounds[set_num, :], transients[set_num, :]

def single_hist_test(mod_name, set_num):
    """plots histogram, scatterplot, and regression equation against ground_truth data"""
    b_set, transients = load_dataset(set_num)

    # Generate x|y values
    diffs = np.diff(b_set)
    b_set = b_set[:-1] + (diffs/2)
    t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])

    mod = load_model(mod_name) 
    if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
        b_set, t_set = mod.filter(b_set, t_set)
    predicted_vals = mod.regression_fit(b_set, t_set)

    # Plot histogram
    plt.hist(b_set, bins=np.append(b_set, np.max(b_set)+1), edgecolor='black', linewidth=0.5)
    plt.savefig(f'images/{mod_name}_histogram.png')
    plt.clf()

    # Plot regressiom
    plt.plot(transients)
    plt.plot(b_set, predicted_vals, 'r')
    plt.savefig(f'images/{mod_name}_regression.png')
    plt.clf()

def multi_hist_test(mod_name, count_num):
    """plots histogram and regression equation from set # of random datasets"""
    mod = load_model(mod_name)

    # Plot dataset
    sects = int(math.sqrt(count_num))
    graph_list = np.random.choice(range(29), count_num, replace=False)
    fig, axs = plt.subplots(sects, sects)
    for i in range(sects):
        for j in range(sects):
            b_set, transients = load_dataset(graph_list[i+j])
            
            # Generate x|y values
            diffs = np.diff(b_set, t_set)
            b_set = b_set[:-1] + (diffs/2)
            t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])

            if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
                b_set, t_set = mod.filter(b_set, t_set)
            predicted_vals = mod.regression_fit(b_set)
            axs[i,j].hist(
                b_set, 
                bins=np.append(b_set, np.max(b_set)+1), 
                edgecolor='black', 
                linewidth=1.2
            )
            axs[i,j].plot(b_set, predicted_vals, 'r')
    plt.show()
    plt.savefig(f'images/{mod_name}_multi_plot.png')

def all_hist_test(mod_name):
    """plots histogram & regression for all transient datasets"""
    mod = load_model(mod_name)

    for i in range(29):
        b_set, transients = load_dataset(i)
        
        # Generate x|y values
        diffs = np.diff(b_set)
        b_set = b_set[:-1] + (diffs/2)
        t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])


        if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
            b_set, t_set = mod.filter(b_set, t_set)
        predicted_vals = mod.regression_fit(b_set, t_set)
        plt.hist(b_set, bins=np.append(b_set, np.max(b_set)+1), edgecolor='black', linewidth=1.2)
        plt.plot(b_set, predicted_vals, 'r') 
        plt.savefig(f'images/{i}_{mod_name}_graph.png')
        plt.clf()

    shutil.make_archive(f'all_{mod_name}_graphs', 'zip', 'images')
