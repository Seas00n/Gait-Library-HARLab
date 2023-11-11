import numpy as np
import os
import glob
from gmr import GMM, kmeansplusplus_initialization, covariance_initialization
from gmr.utils import check_random_state
import matplotlib.pyplot as plt
from sklearn.mixture import BayesianGaussianMixture

save_path = "I:/Open_Source_Data/gmm_data/"
fp_file_list = glob.glob(save_path + "*.npy")

train_data_list = []
for file in fp_file_list[0:40]:
    fp = np.load(file).T
    fp[:, 0] = np.linspace(0, 1, 100)
    train_data_list.append(fp[:, (0, 2, 3)])

train_data = np.array(train_data_list)
plt.plot(train_data[:, :, 0].T, train_data[:, :, 1].T, c='k', alpha=0.1)
plt.plot(train_data[:, :, 0].T, train_data[:, :, 2].T, c='k', alpha=0.1)

X_train = train_data.reshape(np.shape(train_data)[0] * np.shape(train_data)[1], np.shape(train_data)[2])
random_state = check_random_state(0)
n_components = 5
initial_means = kmeansplusplus_initialization(X_train, n_components, random_state)
initial_covs = covariance_initialization(X_train, n_components)

bgmm = BayesianGaussianMixture(n_components=n_components, max_iter=200).fit(X_train)
gmm = GMM(n_components=n_components,
          priors=bgmm.weights_,
          means=bgmm.means_,
          covariances=bgmm.covariances_,
          random_state=random_state)

phase = np.linspace(0, 1, 100)
TimeOut = []
DataOut = []
SigmaOut = []
for idx in range(100):
    conditional_gmm = gmm.condition([0], np.array([phase[idx]]))
    conditional_mvn = conditional_gmm.to_mvn()
    DataOut.append(conditional_mvn.mean)
    SigmaOut.append(conditional_mvn.covariance)
    TimeOut.append(phase[idx])
DataOut = np.array(DataOut)
SigmaOut = np.array(SigmaOut)
TimeOut = np.array(TimeOut)
plt.plot(TimeOut, DataOut, c='r', lw=2, alpha=0.5)

# KMP
test_data = train_data[10, :, :]
max_fz_0 = np.max(test_data[0:50, 1])
phase_max_fz_0 = np.argmax(test_data[0:50, 1])
max_fz_1 = np.max(test_data[50:, 1])
phase_max_fz_1 = np.argmax(test_data[50:, 1]) + 50
via_phase = [0, phase_max_fz_0, phase_max_fz_1, 0]
via_point = [0, max_fz_0, max_fz_1, 0]
via_var = np.diag((1e-6, 1e-6))

newDataOut = np.copy(DataOut)
newSigmaOut = np.copy(SigmaOut)
newTimeOut = np.copy(TimeOut)
for via_idx in range(len(via_point)):
    newTimeOut[via_idx] = via_phase[via_idx]
    newDataOut[via_idx, 1] = via_point[via_idx]
    newSigmaOut[via_idx, :] = via_var


def kmp_estimateMatrix_mean(Time, Sigma, kh=6, lamda=1):
    D = 2
    N = np.shape(Time)[0]
    kc = np.zeros((2 * N, 2 * N))
    for i in range(N):
        for j in range(N):
            kt_t = np.exp(-kh * (Time[i] - Time[j]) ** 2)
            kc[i * D:(i + 1) * D, j * D:(j + 1) * D] = np.diag((1, 1)) * kt_t
            if i == j:
                kc[i * D:(i + 1) * D, j * D:(j + 1) * D] += lamda * Sigma[i, :]
    Kinv = np.linalg.inv(kc)
    return Kinv


Kinv = kmp_estimateMatrix_mean(newTimeOut, newSigmaOut)


def kmp_pred_mean(t, Time, Data, Kinv, kh=6, lamda=1):
    D = 2
    N = np.shape(Time)[0]
    k = np.zeros((2, 2 * N))
    Y = np.zeros((2 * N, 1))
    for i in range(N):
        kt_t = np.exp(-kh * (t - Time[i]) ** 2)
        k[0:D, i * D:(i + 1) * D] = np.diag((1, 1)) * kt_t
        for h in range(D):
            Y[i * D + h] = Data[i, h]

    Mu = k @ Kinv @ Y
    return Mu


finalDataOut = []
for idx in range(100):
    mu = kmp_pred_mean(phase[idx],
                       newTimeOut,
                       newDataOut,
                       Kinv)
    finalDataOut.append(mu)

finalDataOut = np.array(finalDataOut).reshape((100, 2))
plt.plot(TimeOut, finalDataOut, c='c', lw=2)
plt.show()
