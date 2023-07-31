import numpy as np
from statistics import mode
from moepy import lowess

def regression_fit(b_set, t_set, x_pred):
    lowess_mod = lowess.Lowess()
    lowess_mod.fit(b_set, t_set, frac=0.1, robust_iters=0)
    return lowess_mod.predict(x_pred)

