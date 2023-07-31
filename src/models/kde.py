from scipy.stats import gaussian_kde

def regression_fit(b_set, t_set, x_pred):
    bw = 0.05 # multipled by standard deviation of training set
    kde = gaussian_kde(b_set, bw_method=bw)
    return kde.evaluate(x_pred)*len(b_set)*10
