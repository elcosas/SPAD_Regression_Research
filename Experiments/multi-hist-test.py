import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    # Load data
    bucket_transients = np.load('../Prop_Notebooks/edh_boundaries.npy')

    # set constants
    GRAPH_COUNT = 9
    BINS = len(bucket_transients[1, :])

    #####################################################

    sects = int(math.sqrt(GRAPH_COUNT))
    graph_list = np.random.choice(range(29), GRAPH_COUNT, replace=False)
    fig, axs = plt.subplots(sects, sects)
    for i in range(sects):
        for j in range(sects):
            axs[i, j].hist(bucket_transients[graph_list[i+j], :], bins=BINS) 
    plt.show()

if __name__ == '__main__':
    main()
