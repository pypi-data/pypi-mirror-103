## This is the first-step optimization, based on SSVDversion1.
## Based on linear algebra, 
## computation about about Y, Z, and the Kronecker product are replaced.

import numpy as np 
import scipy.linalg as la

def get_tilde(lam, tilde_hat, w):
    """Get the tilde vector given the lambda, tilde_hat_vector, and w."""
    part1 = np.sign(tilde_hat)
    part2 = np.abs(tilde_hat)-lam*w/2
    part2[part2<np.zeros(part2.shape)] = 0
    tilde = np.multiply(part1, part2)
    return tilde
def get_BIC(lam, w, tilde_hat, fixed_vec, sigma2_hat, nd, X, fixed_name):
    """ Compute BIC given the lambda.
    lam: scalar
    For v:
        w = w2: (d, 1)
        tilde_hat = v_tilde_hat: (d, 1)
        fixed_vec = u_old: (n, 1)
        response = Y: (nd, 1)
        sigma2_hat = sigma2_hat_v: scalar
        nd: scalar, =n*d
    For u:
        w = w1: (n, 1)
        tilde_hat = u_tilde_hat: (n, 1)
        fixed_vec = v_new: (d, 1)
        response = Z: (nd, 1)
        sigma2_hat = sigma2_hat_u: scalar
        nd: scalar, =n*d
    Return: BIC, scalar
    """
    df = np.sum(np.abs(tilde_hat) > lam*w/2)
    tilde = get_tilde(lam, tilde_hat, w)
    SSE = np.sum((X - np.outer(fixed_vec, tilde))**2) if fixed_name == "u" else\
        np.sum((X - np.outer(tilde, fixed_vec))**2)
    BIC = SSE/(nd*sigma2_hat)+np.log(nd)/nd*df
    return BIC
def select_lam(lam_grid, w, tilde_hat, fixed_vec, sigma2_hat, nd, X, fixed_name):
    """ Select lambda given a lambda grid based on BIC.
    lam_grid: (S,)
    For v:
        w = w2: (d, 1)
        tilde_hat = v_tilde_hat: (d, 1)
        fixed_vec = u_old: (n, 1)
        response = Y: (nd, 1)
        sigma2_hat = sigma2_hat_v: scalar
        nd: scalar, =n*d
    For u:
        w = w1: (n, 1)
        tilde_hat = u_tilde_hat: (n, 1)
        fixed_vec = v_new: (d, 1)
        response = Z: (nd, 1)
        sigma2_hat = sigma2_hat_u: scalar
        nd: scalar, =n*d
    Return: scalar, the optimal lambda
    """
    BICs = list(map(lambda lam: get_BIC(lam, w, tilde_hat, fixed_vec, sigma2_hat, nd, X, fixed_name), lam_grid))
    return lam_grid[np.argmin(BICs)]

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

    ## Update v using current u

    # ols for v, use current u
    v_tilde_hat = X.T @ u_old  # (d, 1), fixed ols estimate
    SSE_v = np.sum((X - np.outer(u_old, v_tilde_hat))**2)  # scalar, SSE_v = (Y-Y_hat).T @ (Y-Y_hat)
    sigma2_hat_v = SSE_v / (nd-d)  # scalar, fixed ols estimate

    # select lambda_v
    w2 = np.abs(v_tilde_hat)**(-gamma2)  # (d, 1)
    lambda_v = select_lam(lam_grid, w2, v_tilde_hat, u_old, sigma2_hat_v, nd, X, "u")

    # update v
    v_tilde = get_tilde(lambda_v, v_tilde_hat, w2)  # (d, 1)

    if np.all(v_tilde == 0):  # full shrinkage at v
        v_new = np.zeros(v_old.shape)
        u_new = np.zeros(u_old.shape)
        lambda_u = 0
    else:
        v_new = v_tilde / np.linalg.norm(v_tilde)
        
        ## Update u using current v

        # ols for u, use current v
        u_tilde_hat = X @ v_new  # (n, 1), fixed ols estimate
        SSE_u = np.sum((X.T - np.outer(v_new, u_tilde_hat))**2)
        sigma2_hat_u = SSE_u / (nd-n)  # scalar, fixed ols estimate

        # select lambda_u
        w1 = np.abs(u_tilde_hat)**(-gamma1)
        lambda_u = select_lam(lam_grid, w1, u_tilde_hat, v_new, sigma2_hat_u, nd, X, "v")

        # update u
        u_tilde = get_tilde(lambda_u, u_tilde_hat, w1)  # (n, 1)
        u_new = u_tilde / np.linalg.norm(u_tilde) if np.linalg.norm(u_tilde) != 0 else u_tilde

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

     