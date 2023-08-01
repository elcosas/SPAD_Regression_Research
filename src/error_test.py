import csv
import numpy as np
import sklearn.metrics as met
from models import gaussian, lowess, kde
from sys import argv, exit

EW_BINS = 31
DEFAULT_TR = 0.0011

def main():
    if len(argv) != 2:
        print('SyntaxError: must provide 1 argument')
        exit(1)
    set_num = int(argv[1])

    b_set, t_set = load_data(set_num)
    true_vals = t_set
    x_pred = np.arange(0, len(true_vals))
    
    error_stats = compare_models(b_set, t_set, true_vals, x_pred, mode='ed')
    error_stats.insert(0, ['', 'gaussian', 'lowess', 'kde'])
    with open('edh_stats.csv', 'w') as file:
        csv.writer(file).writerows(error_stats)
    
    error_stats = compare_models(b_set, t_set, true_vals, x_pred, mode='ew')
    error_stats.insert(0, ['', 'gaussian', 'lowess'])
    with open('ewh_stats.csv', 'w') as file:
        csv.writer(file).writerows(error_stats)

def load_data(set_num):
    """Loads the dataset for the passed #"""
    b_set = np.load('../dataset/boundaries.npy')[set_num, :]
    t_set = np.load('../dataset/transients.npy')[set_num, :]
    return b_set, t_set

def compare_models(b_set, t_set, true_vals, x_preds, mode='ed'):
    """Runs regression error tests on predicted vals versus true vals"""
    pred_vals = []
    if mode == 'ed':
        b_set, t_set = convert_ed(b_set, t_set)
        pred_vals.append(gaussian.regression_fit(b_set, t_set, x_preds))
        pred_vals.append(lowess.regression_fit(b_set, t_set, x_preds))
        pred_vals.append(kde.regression_fit(b_set, t_set, x_preds))
    elif mode == 'ew':
        b_set, t_set = convert_ew(b_set, t_set)
        pred_vals.append(gaussian.regression_fit(b_set, t_set, x_preds))
        pred_vals.append(lowess.regression_fit(b_set, t_set, x_preds))
    else:
        print('SyntaxError: Invalid mode')
        exit(1)

    r2 = ['Coefficient of Determination (R2)']
    for val in pred_vals:
        r2.append(str(met.r2_score(true_vals, val)))

    mse = ['Mean Squared Error']
    for val in pred_vals:
        mse.append(str(met.mean_squared_error(true_vals, val)))

    max_err = ['Max Error']
    for val in pred_vals:
        max_err.append(str(met.max_error(true_vals, val)))

    pk_err = ['Peak Error']
    for val in pred_vals:
        pk_err.append(str(abs(np.max(true_vals) - np.max(val))))

    return [r2, mse, max_err, pk_err]

def convert_ed(b_set, t_set):
    """Generates x & y vals to fit EDH"""
    diffs = np.diff(b_set)
    b_set = b_set[:-1] + (diffs/2)
    t_set = np.array([DEFAULT_TR / (diffs[i] / diffs[0]) for i in range(len(b_set))])
    return b_set, t_set

def convert_ew(b_set, t_set):
    """Generates x & y vals to fit EWH"""
    t_set = np.array([np.mean(arr) for arr in np.array_split(t_set, EW_BINS)])
    max_time = np.max(b_set)
    b_set = np.arange(0, max_time, max_time // 31)[1:]
    return b_set, t_set

if __name__ == '__main__':
    main()
