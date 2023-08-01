import numpy as np
import matplotlib.pyplot as plt
from models import gaussian, lowess, kde
from sys import argv, exit

DEFAULT_TR = 0.0011

def main():
    if len(argv) != 2:
        print('SyntaxError: must provide set number as argument')
        exit(1)
    b_set, transients = load_dataset(int(argv[1]))

    b_set, t_set = gen_vals(b_set)
    x = np.arange(0, len(transients))
    gauss_vals = gaussian.regression_fit(b_set, t_set, x)
    lowess_vals = lowess.regression_fit(b_set, t_set, x)
    kde_vals = kde.regression_fit(b_set, t_set, x)

    # Plot graph
    ax = plt.gca()
    ax.set_ylim([0, np.max(transients)])
    bins = np.append(b_set, np.max(b_set)+1)
    plt.hist(b_set, bins=bins, edgecolor='black', linewidth=0.5, alpha=0.2)
    plt.plot(x, transients, 'k', label='Ground truth')
    plt.plot(x, gauss_vals, 'b', linestyle='--', label='gaussian regression')
    plt.plot(x, lowess_vals, 'g', linestyle='--', label='lowess regression')
    plt.plot(x, kde_vals, 'r', linestyle='--', label='kde regression')
    plt.legend() 
    plt.title(f'Modeling SPAD Data With Regression')
    plt.show()
    plt.savefig(f'example.png')

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

if __name__ == '__main__':
    main()
