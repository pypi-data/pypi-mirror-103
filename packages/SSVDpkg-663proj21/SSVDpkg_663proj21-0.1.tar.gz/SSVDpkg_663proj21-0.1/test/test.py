## This is an illustration of simulation.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
from SSVD.functions import SSVD_layer
from SSVD.functions import SSVD

def clusterheatmap(us, ss, vs, label):
    """Plot the clustered heatmap"""
    X_sparse = ss*us@vs.T
    levels = np.unique(label)
    row_index = np.empty(0, dtype = 'int')
    
    for i in range(len(levels)):
        index, = np.where(label == levels[i])
        index_sort = index[np.argsort(us.reshape(-1)[index])]
        row_index = np.concatenate((row_index, index_sort))
        
    v_reshape = vs.reshape(-1)
    col_sort = np.argsort(np.abs(v_reshape))
    X_sparse_sort = X_sparse[:,col_sort]
    col_index = np.argsort(v_reshape[col_sort])
    
    trans = (row_index.reshape(-1,1),col_index.reshape(1,-1))
    plot = sns.heatmap(X_sparse_sort[trans], vmin=-1, vmax=1, cmap = 'bwr')
    return plot


u_tilde = [list(range(10, 2, -1)), list(np.repeat(2, 17)), list(np.repeat(0, 75))]
u_tilde = np.array(reduce(lambda x, y: x+y, u_tilde))
v_tilde = [[10, -10, 8, -8, 5, -5], list(np.repeat(3, 5)), list(np.repeat(-3, 5)), list(np.repeat(0, 34))]
v_tilde = np.array(reduce(lambda x, y: x+y, v_tilde))

u_true = u_tilde / np.linalg.norm(u_tilde)  # (100,)
v_true = v_tilde / np.linalg.norm(v_tilde)  # (50,)
s_true = 50
Xstar = s_true * np.outer(u_true, v_true)  # (100, 50)

label_true = np.concatenate((np.ones(11-3), np.ones(17)*2, np.ones(75)*3))

plt.figure()
clusterheatmap(u_true[:,None], s_true, v_true[:,None], label_true)
plt.title("True SSVD first layer plot")
plt.show()

X = Xstar + np.random.normal(0, 1, Xstar.shape)
lam_grid = np.linspace(0, 8, 81)
gamma1 = gamma2 = 2
n_iters, us, vs, ss, lambda_us, lambda_vs = SSVD(X, 1, lam_grid, gamma1, gamma2)

plt.figure()
clusterheatmap(us, ss, vs, label_true)
plt.title("SSVD first layer plot by the codes")
plt.show()
