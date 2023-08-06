## This is the second-step optimation, based on SSVDversion2. 
## Broadcasting are applied when selecting optimal lambda from a given grid. 
## Function get_tilde(), get_BIC(), and select_lam() are no longer necessary. 

import numpy as np 
import scipy.linalg as la

def update_uv(u_old, v_old, X, gamma1, gamma2, lam_grid):
    """Update u and v once given the current u and v.
    Input: 
        u_old: (n, 1)
        v_old: (d, 1)
        X: (n, d)
        Y: (nd, 1)
        Z: (nd, 1)
        gamma1, gamma2: scalar, tuning parameter
        lam_grid: ndarray, a grid of lambdas to be selected 
    Return:
        u_new: (n, 1)
        v_new: (d, 1)
        lambda_u, lambda_v: scalar, the optimal lambda under the current u and v
    """
    n, d = X.shape
    nd = n*d
    S = len(lam_grid)

    # initialize
    v_new = np.zeros(v_old.shape)
    u_new = np.zeros(u_old.shape)
    lambda_u = lambda_v = 0

    ## Update v using current u

    # ols for v, use current u
    v_tilde_hat = X.T @ u_old  # (d, 1), fixed ols estimate
    SSE_v = np.sum((X - np.outer(u_old, v_tilde_hat))**2)  # scalar, SSE_v = (Y-Y_hat).T @ (Y-Y_hat)
    sigma2_hat_v = SSE_v / (nd-d)  # scalar, fixed ols estimate

    # select lambda_v
    w2 = np.abs(v_tilde_hat)**(-gamma2)  # (d, 1)
    dfs_v = np.sum(np.abs(v_tilde_hat) > lam_grid*w2/2, axis=0)  # (S,), df for each lambda
    part2 = v_tilde_hat - lam_grid*w2/2; part2[part2<0] = 0
    part1 = np.sign(v_tilde_hat)
    v_tilde_br = part1 * part2  # (d, S), each column is v_tilde under each lambda
    outer_prods = np.outer(u_old, v_tilde_br.T)  # (n, d*S), each chunk of size (n, d) is the outer product mat under each lambda
    outer_prods = np.array(np.hsplit(outer_prods, S))  # (S, n, d)
    SSEs_v = ((X-outer_prods)**2).sum(axis = (1,2))  # (S,), ||X-uv_tilde^T||_F^2=||Y-Y_hat||^2 for each lambda
    BICs_v = SSEs_v/(nd*sigma2_hat_v) + np.log(nd)/nd*dfs_v  # (S,), BIC for each lambda
    lambda_v = lam_grid[np.argmin(BICs_v)]

    # update v
    part1 = np.sign(v_tilde_hat)
    part2 = np.abs(v_tilde_hat)-lambda_v*w2/2; part2[part2<0] = 0
    if not np.all(part2 == 0):  # not full shrinkage at v
        v_tilde = np.multiply(part1, part2)  # (d, 1)
        v_new = v_tilde / np.linalg.norm(v_tilde)
        
        ## Update u using current v

        # ols for u, use current v
        u_tilde_hat = X @ v_new  # (n, 1), fixed ols estimate
        SSE_u = np.sum((X.T - np.outer(v_new, u_tilde_hat))**2)
        sigma2_hat_u = SSE_u / (nd-n)  # scalar, fixed ols estimate

        # select lambda_u
        w1 = np.abs(u_tilde_hat)**(-gamma1)  # (n, 1)
        dfs_u = np.sum(np.abs(u_tilde_hat) > lam_grid*w1/2, axis=0)  # (S,), df for each lambda
        part2 = u_tilde_hat - lam_grid*w1/2; part2[part2<0] = 0
        part1 = np.sign(u_tilde_hat)
        u_tilde_br = part1 * part2  # (n, S), each column is u_tilde under each lambda
        outer_prods = np.outer(u_tilde_br.T, v_new)  # (n*S, d), each chunk of size (n, d) is the outer product mat under each lambda
        outer_prods = np.array(np.vsplit(outer_prods, S))  # (S, n, d)
        SSEs_u = ((X-outer_prods)**2).sum(axis = (1,2))  # (S,), ||X-u_tildev^T||_F^2=||Z-Z_hat||^2 for each lambda
        BICs_u = SSEs_u/(nd*sigma2_hat_u) + np.log(nd)/nd*dfs_u  # (S,), BIC for each lambda
        lambda_u = lam_grid[np.argmin(BICs_u)]

        # update u
        part1 = np.sign(u_tilde_hat)
        part2 = np.abs(u_tilde_hat)-lambda_u*w1/2; part2[part2<0] = 0
        if not np.all(part2 == 0):  # not full shrinkage at u
            u_tilde = np.multiply(part1, part2)  # (n, 1)
            u_new = u_tilde / np.linalg.norm(u_tilde)

    return u_new, v_new, lambda_u, lambda_v


def SSVD_layer(X, lam_grid, gamma1, gamma2, max_iter=5000, tol=1e-6):
    """Get the sparse SVD layer given the data matrix X at a SVD layer and the tuning parameters grid.
    Input: 
        X: (n, d), can be the original data matrix or the residual matrix
        lam_grid: ndarray, a grid of lambdas to be selected 
        gamma1, gamma2: scalar, tuning parameter
        max_iter: integer, the maximum iteration times
        tol: float, tolerance to stop the iteration
    Return: n_iter, u, v, s, lambda_u, lambda_v
        n_iter: number of iterations
        u: (n, 1), the final u at convergence 
        v: (d, 1), the final v at convergence 
        s: scalar, the singular value at convergence
        lambda_u, lambda_v: the optimal tuning parameter at convergence
    """
    # SVD
    U, _, VT = la.svd(X)

    # initial value
    u_old = U[:,0][:,None]
    v_old = VT[0][:,None]

    for i in range(max_iter):
        u_new, v_new, lambda_u, lambda_v = update_uv(u_old, v_old, X, gamma1, gamma2, lam_grid)
        if np.linalg.norm(u_new-u_old) < tol and np.linalg.norm(v_new-v_old) < tol:  # achieve the tolerance
            break 
        if np.all(u_new == 0) or np.all(u_new == 0):  # full shrinkage (i.e., all zeros in the vector)
            print("Warning: Full shrinkage has been achieved. Iterations stops. No further decomposition. The desired number of layers may not be achieved. ")
            break
        u_old, v_old = u_new, v_new
    n_iter = i+1  # number of iterations
    u, v = u_new, v_new  # the final u and v at convergence 
    s = (u_new.T @ X @ v_new)[0][0]
    if n_iter == max_iter:
        print("Warning: The maximum iteration has been achieved. Please consider increasing `max_iter`.")
    return n_iter, u, v, s, lambda_u, lambda_v

def SSVD(X, num_layer, lam_grid, gamma1, gamma2, max_iter=5000, tol=1e-6):
    """Get the SSVD given the data matrix X and the desired number of SSVD layers.
    Input: 
        X: (n, d), the original data matrix
        num_layer: desired number of SSVD layers
        lam_grid: ndarray, a grid of lambdas to be selected 
        gamma1, gamma2: scalar, tuning parameter
        max_iter: integer, the maximum iteration times
        tol: float, tolerance to stop the iteration
    Return: n_iters, us, vs, ss, lambda_us, lambda_vs
        n_iters: (num_layer,), number of iterations for each layer
        us: (n, num_layer), the final u at convergence for each layer
        vs: (d, num_layer), the final v at convergence for each layer
        ss: (num_layer,), the singular value at convergence for each layer
        lambda_us, lambda_vs: (num_layer,), the optimal tuning parameter at convergence for each layer
    """
    n, d = X.shape
    n_iters = np.zeros(num_layer, dtype = int)
    ss = np.zeros(num_layer)
    lambda_us = np.zeros(num_layer)
    lambda_vs = np.zeros(num_layer)
    us = np.zeros((n, num_layer))
    vs = np.zeros((d, num_layer))
    # initial value
    u = np.zeros((n, 1)); v = np.zeros((d, 1)); resi_mat = X; s = 0
    for i in range(num_layer):
        resi_mat = resi_mat - s*u@v.T
        n_iter, u, v, s, lambda_u, lambda_v = SSVD_layer(resi_mat, lam_grid, gamma1, gamma2, max_iter, tol)
        n_iters[i] = n_iter
        ss[i] = s
        lambda_us[i] = lambda_u
        lambda_vs[i] = lambda_v 
        us[:,i] = u[:,0]
        vs[:,i] = v[:,0]
        if np.all(u == 0) or np.all(v == 0):  # full shrinkage (i.e., all zeros in the vector)
            break
    return n_iters, us, vs, ss, lambda_us, lambda_vs
