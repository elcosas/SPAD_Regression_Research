import numpy as np
from scipy.stats import gaussian_kde

def regression_fit(b_set, t_set, x_pred):
    bw = 0.05 #* np.std(t_set)
    kde = gaussian_kde(b_set, bw_method=bw)
    predicted = kde.evaluate(x_pred)
    return np.clip(predicted, 0, np.max(predicted))
