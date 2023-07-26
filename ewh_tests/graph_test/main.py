import importlib
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil

BINS = 31

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
    bounds = np.load('../proprietary/edh_boundaries.npy')
    transients = np.load('../proprietary/transients_interp.npy')
    t_set = np.array(
        [np.mean(arr) for arr in np.array_split(transients[set_num, :], BINS)]
    )
    max_time = np.max(bounds[set_num, :])
    b_set = np.arange(0, max_time, max_time // BINS)[1:] 
    return (t_set, b_set), (transients, bounds)

def single_hist_test(mod_name, set_num):
    """plots histogram, scatterplot, and regression equation against ground_truth data"""
    new_set, ori_set = load_dataset(set_num)
    t_set, b_set = new_set
    transients, bounds = ori_set
    transients_x = np.arange(0, len(transients[set_num, :]), 20)

    mod = load_model(mod_name) 
    if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
        b_set, t_set = mod.filter(b_set, t_set)
    predicted_vals = mod.regression_fit(b_set, t_set)

    # Plot histogram
    plt.hist(b_set, bins=BINS, weights=t_set, edgecolor='black', linewidth=1.2, color='g')
    plt.savefig(f'images/{mod_name}_histogram.png')
    plt.clf()

    # Plot scatterplot
    plt.scatter(transients_x, transients[set_num, ::20], c='r')
    plt.scatter(b_set, t_set, c='g')
    plt.savefig(f'images/{mod_name}_scatter.png')
    plt.clf()

    # Plot regression line
    plt.plot(transients[set_num, :], 'r')
    plt.plot(b_set, predicted_vals, 'g')
    plt.savefig(f'images/{mod_name}_regression_plot')
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
            new_set, ori_set = load_dataset(graph_list[i+j])
            t_set, b_set = new_set
            transients, bounds = ori_set
            if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
                b_set, t_set = mod.filter(b_set, t_set)
            predicted_vals = mod.regression_fit(b_set, t_set)
            axs[i,j].hist(b_set, bins=BINS, weights=t_set, edgecolor='black', linewidth=1.2)
            axs[i,j].plot(b_set, predicted_vals, 'r')
    plt.show()
    plt.savefig(f'images/{mod_name}_multi_plot.png')

def all_hist_test(mod_name):
    """plots histogram & regression for all transient datasets"""
    mod = load_model(mod_name)

    for i in range(29):
        new_set, ori_set = load_dataset(i)
        t_set, b_set = new_set
        transients, bounds = ori_set
        if hasattr(mod, 'filter') and callable(getattr(mod, 'filter', None)):
            b_set, t_set = mod.filter(b_set, t_set)
        predicted_vals = mod.regression_fit(b_set, t_set)
        plt.hist(b_set, bins=BINS, weights=t_set, edgecolor='black', linewidth=1.2)
        plt.plot(b_set, predicted_vals, 'r') 
        plt.savefig(f'images/{i}_{mod_name}_graph.png')
        plt.clf()

    shutil.make_archive(f'all_{mod_name}_graphs', 'zip', 'images')
