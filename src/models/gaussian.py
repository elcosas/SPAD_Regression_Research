import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RationalQuadratic

def regression_fit(b_set, t_set, x_pred):
    diffs = np.diff(b_set)
    lc = np.mean(diffs)
    a = np.min(diffs) / np.max(diffs)
    kernel = RationalQuadratic(
        length_scale=lc, 
        alpha=a, 
        length_scale_bounds='fixed', 
        alpha_bounds='fixed'
    )
    gaussian_reg = GaussianProcessRegressor(kernel=kernel).fit(b_set.reshape(-1, 1), t_set)
    return gaussian_reg.predict(x_pred.reshape(-1, 1))

