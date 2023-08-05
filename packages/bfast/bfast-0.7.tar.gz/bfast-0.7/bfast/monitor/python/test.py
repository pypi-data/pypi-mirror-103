import multiprocessing as mp
from functools import partial

import numpy as np

def fit_single(y, X, n, mapped_indices):
    return y[0], y[1], y[2]



x = np.random.random((120, 10, 10))
print(x.shape)
x = np.transpose(x, (1, 2, 0)).reshape(10 * 10, 120)

X = np.array([[1,2,3],[4,5,6]])
n = 10
mapped_indices = np.array([1,2,3])

# my_fun = partial(fit_single, X=X, n=n, mapped_indices=mapped_indices)
def my_fun(y):
    return fit_single(y, X, n, mapped_indices)
pool = mp.Pool(mp.cpu_count())
rval = pool.map(my_fun, x)
rval = np.array(rval, dtype=object).reshape(10, 10, 3)

breaks = rval[:,:,0]
means = rval[:,:,1]
magnitudes = rval[:,:,2]
print(magnitudes)
