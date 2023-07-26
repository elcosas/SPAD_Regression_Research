from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def regression_fit(b_set, t_set):
    kernel = RBF(length_scale=1.0, length_scale_bounds="fixed")
    gaussian_reg = GaussianProcessRegressor(kernel=kernel).fit(b_set.reshape(-1, 1), t_set)
    return gaussian_reg.predict(b_set.reshape(-1, 1))

