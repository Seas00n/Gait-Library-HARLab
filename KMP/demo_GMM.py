import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from GMM.utils import *
from KMP.utils import *
import pickle

# save_path = "I:/Open_Source_Data/gmm_data/"
save_path = "/media/yuxuan/My Passport/Open_Source_Data/gmm_data/"
fp_file_list = glob.glob(save_path + "*.npy")

train_data_list = []
condition_list = []
for file in fp_file_list:
    fp = np.load(file).T
    fp[:, 0] = np.linspace(0, 1, 100)
    condition = fp[0, 1]
    if 1.5 > condition > 1.4:
        train_data_list.append(fp[:, (0, 2, 3)])
        condition_list.append(condition)
condition_data = np.array(condition_list)
train_data = np.array(train_data_list)
plt.plot(train_data[:, :, 0].T, train_data[:, :, 1].T, c='k', alpha=0.1,label="Train Data")
plt.plot(train_data[:, :, 0].T, train_data[:, :, 2].T, c='k', alpha=0.1)

retrain_or_not = input("Train a new model or use current? [Y/n]")
if retrain_or_not == "Y":
    X_train = generate_X_train(train_data)
    gmm = train_GMM(X_train, n_components=5)
else:
    gmm = pickle.load(open('fp_gmm', "rb"))

phase = np.linspace(0, 1, 100)
DataOut, SigmaOut = gmm_Interp_with_phase(gmm, phase)
TimeOut = phase
plt.plot(phase, DataOut[:, 0:1], c='r', lw=2, alpha=0.5,label="GMR Reference")
plt.legend()
plt.show()

# save the beat result
if retrain_or_not == "Y":
    save_new_model_or_not = input("Save the new model? [Y/n]")
    if save_new_model_or_not == "Y":
        pickle.dump(gmm, open("fp_gmm", "wb"))

# # KMP
# test_data = train_data[10, :, :]
# plt.plot(phase, test_data[:, 1:], c='b', lw=2)
# idx_max_fz_0 = np.argmax(test_data[0:50, 1])
# max_fz_0 = test_data[idx_max_fz_0, 1]
# phase_max_fz_0 = phase[idx_max_fz_0]
# idx_max_fz_1 = np.argmax(test_data[50:, 1]) + 50
# max_fz_1 = test_data[idx_max_fz_1, 1]
# phase_max_fz_1 = phase[idx_max_fz_1]
# via_idx = [0, idx_max_fz_0, idx_max_fz_1, 99]
# via_phase = [0, phase_max_fz_0, phase_max_fz_1, 1]
# via_point = [0, max_fz_0, max_fz_1, 0]
# via_var = np.diag((1e-6, 1e-6))
# plt.scatter(via_phase, via_point)
#
# newDataOut = np.copy(DataOut)
# newSigmaOut = np.copy(SigmaOut)
# newTimeOut = np.copy(TimeOut)
# for i in range(len(via_idx)):
#     newTimeOut[via_idx[i]] = via_phase[i]
#     newDataOut[via_idx[i], 1] = via_point[i]
#     newSigmaOut[via_idx[i], :] = via_var
#
#
# def kmp_estimateMatrix_mean(Time, Sigma, kh=6, lamda=1):
#     D = 2
#     N = np.shape(Time)[0]
#     kc = np.zeros((2 * N, 2 * N))
#     for i in range(N):
#         for j in range(N):
#             kt_t = np.exp(-kh * (Time[i] - Time[j]) ** 2)
#             kc[i * D:(i + 1) * D, j * D:(j + 1) * D] = np.diag((1, 1)) * kt_t
#             if i == j:
#                 kc[i * D:(i + 1) * D, j * D:(j + 1) * D] += lamda * Sigma[i, :]
#     Kinv = np.linalg.inv(kc)
#     return Kinv
#
#
# Kinv = kmp_estimateMatrix_mean(newTimeOut, newSigmaOut)
#
#
# def kmp_pred_mean(t, Time, Data, Kinv, kh=6, lamda=1):
#     D = 2
#     N = np.shape(Time)[0]
#     k = np.zeros((2, 2 * N))
#     Y = np.zeros((2 * N, 1))
#     for i in range(N):
#         kt_t = np.exp(-kh * (t - Time[i]) ** 2)
#         k[0:D, i * D:(i + 1) * D] = np.diag((1, 1)) * kt_t
#         for h in range(D):
#             Y[i * D + h] = Data[i, h]
#
#     Mu = k @ Kinv @ Y
#     return Mu
#
#
# finalDataOut = []
# for idx in range(100):
#     mu = kmp_pred_mean(phase[idx],
#                        newTimeOut,
#                        newDataOut,
#                        Kinv)
#     finalDataOut.append(mu)
#
# finalDataOut = np.array(finalDataOut).reshape((100, 2))
# plt.plot(TimeOut, finalDataOut[:, 0], c='c', lw=2)
# plt.show()
