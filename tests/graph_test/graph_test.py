import importlib
import numpy as np
import matplotlib.pyplot as plt

from . import settings

def load_dataset(mod_name, set_num):
    """Loads dataset # and module name passed"""
    try:
        mod = importlib.import_module(mod_name)
    except ImportError:
        print(f'Load Error: "{mod_name}" not found')
        return

    # Load dataset
    bounds = np.load('../proprietary/edh_boundaries.npy')
    transients = np.load('../proprietary/transients_interp.npy')
    t_set = np.array(
        [np.mean(arr) for arr in np.array_split(transients[set_num, :], settings.bins)]
    )
    max_time = np.max(bounds[set_num, :])
    b_set = np.arange(0, max_time, max_time // settings.bins)[1:] 
    return (t_set, b_set), (transients, bounds)

def single_hist_test(mod_name, set_num):
    """plots histogram, scatterplot, and regression equation against ground_truth data"""
    new_set, ori_set = load_dataset(mod_name, set_num)
    t_set, b_set = new_set
    transients, bounds = ori_set

    predicted_vals = mod.regression_fit(b_set, t_set)

    # Plot histogram
    plt.hist(b_set, bins=settings.bins, weights=t_set, edgecolor='black', linewidth=1.2)
    plt.savefig(f'{mod_name}_histogram.png')
    plt.clf()

    # Plot scatterplot
    plt.scatter(b_set, t_set)
    plt.savefig(f'{mod_name}_scatter.png')
    plt.clf()

    # Plot regression line
    plt.plot(b_set, predicted_vals)
    plt.savefig(f'{mod_name}_regression_plot')
    plt.clf()

def multi_hist_test(mod_name, count_num):
    """plots histogram and regression equation from set # of random datasets"""

    # Plot dataset
    sects = int(math.sqrt(count_num))
    graph_list = np.random.choice(range(29), GRAPH_COUNT, replace=False)
    fig, axs = plt.subplots(sects, sects)
    for i in range(sects):
        for j in range(sects):
            new_set, ori_set = load_dataset(mod_name, num)
            t_set, b_set = new_set
            transients, bounds = ori_set
            axs[i+j].hist(
                transients[graph_list[i+j], :], 
                bins=settings.bins, 
                edgecolor='black', 
                linewidth=1.2
            )
    plt.savefig(f'{mod_name}_multi_plot.png')

def main():
    single_hist_test(gaussian,0)

if __name__ == '__main__':
    main()
