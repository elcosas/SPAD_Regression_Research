from scipy.stats import gaussian_kde

def regression_fit(b_set, t_set):
    kde = gaussian_kde(b_set, bw_method=0.05, weights=t_set)
    return kde.evaluate(b_set)*200
