import numpy as np
from scipy.special import comb
from scipy.linalg import eigh
import cvxpy as cp


def cvx_phase_data_task_fit(data, phase, v_vec, num_c, num_popt):
    A = 0
    f = 0
    for i in range(np.shape(phase)[0]):
        for j in range(np.shape(v_vec)[0]):
            Aij = cal_delta_mat(phase[i], v_vec[j], num_c, num_popt)
            AijTAij = Aij.T @ Aij
            uptri_AijTAij = np.triu(AijTAij)
            sym_AijTAij = uptri_AijTAij + uptri_AijTAij.T - np.diag(uptri_AijTAij.diagonal())
            A = A + sym_AijTAij
            f = f - 2 * data[i, j] * Aij

    A = 2 * (A + A.T / 2)
    n_x = np.shape(A)[0]
    f = f.reshape((n_x,))
    x = cp.Variable(n_x)
    con = [x >= -1000, x <= 1000]
    w, _ = eigh(A)
    assert np.all(w >= 0)
    prog = cp.Problem(objective=cp.Minimize((1 / 2) * cp.quad_form(x, A) + f.T @ x),
                      constraints=con)
    prog.solve()
    coefficient = x.value

    return coefficient


def cal_delta_mat(si, vj, num_c, num_popt):
    c_vec = np.zeros((num_c,))
    c_vec[0] = 1
    for i in range(1, num_c):
        n = num_c - 2
        k = i - 1
        # print("n{}k{}".format(n, k))
        c_vec[i] = comb(n, k) * (vj ** k) * ((1 - vj) ** (n - k))
    b_vec = np.zeros((num_c, num_c * num_popt))
    for i in range(0, num_c):
        b_vec[i, num_popt * i:num_popt * (i + 1)] = si ** np.arange(0, num_popt)
    delta_mat = np.dot(c_vec.reshape((1, -1)), b_vec)
    return delta_mat


def coefficient_to_surface(c, phase, v_vec, num_c, num_popt):
    [X, Y] = np.meshgrid(v_vec, phase)
    Z = np.zeros(np.shape(X))
    for i in range(np.shape(X)[0]):
        for j in range(np.shape(X)[1]):
            Aij = cal_delta_mat(phase[i], v_vec[j], num_c, num_popt)
            Z[i, j] = Aij @ c
    return X, Y, Z
