import importlib
import numpy as np
#from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from sys import argv, exit

def main():
    """if len(argv) != 2:
        print('Syntax Error: Please provide 1 valid package name')
        exit()
     """   
    # Load dataset
    bucket_transients = np.load('../Prop_Notebooks/edh_boundaries.npy')

    # Load module w/ regression method
    """
    try:
        importlib.import_module(argv[1])
    except:
        print('Load Error: Invalid package name')
    """

    # set constants
    BINS = len(bucket_transients[1, :])

    #####################################################

    bt_set = bucket_transients[1, :]
    plt.hist(bt_set, bins=BINS)

    bt_hist = np.histogram(bt_set, bins=BINS)

    test_poly_eq = np.poly1d(np.polyfit(bt_set, bt_hist[0], 15))
    plt.plot(bt_set, test_poly_eq(bt_set), 'r')

    plt.show()

if __name__ == '__main__':
    main()
