import numpy as np
import os
import pickle
import glob
import matplotlib.pyplot as plt
from GMM.utils import *
from KMP.utils import *

# save_path = "I:/Open_Source_Data/gmm_data/"
save_path = "/media/yuxuan/My Passport/Open_Source_Data/gmm_data/"
fp_file_list = glob.glob(save_path + "*.npy")

train_data_list = []
for file in fp_file_list[0:40]:
    fp = np.load(file).T
    fp[:, 0] = np.linspace(0, 1, 100)
    train_data_list.append(fp[:, (0, 2, 3)])

train_data = np.array(train_data_list)
plt.plot(train_data[:, :, 0].T, train_data[:, :, 1].T, c='k', alpha=0.1)
plt.plot(train_data[:, :, 0].T, train_data[:, :, 2].T, c='k', alpha=0.1)

gmm = pickle.load(open("fp_gmm", "rb"))
phase_ref = np.linspace(0, 1, 100)
Data_ref, Sigma_ref = gmm_Interp_with_phase(gmm, phase_ref)
Ref_Old = plt.plot(phase_ref, Data_ref[:, 0], c='r', lw=2, alpha=0.5)
plt.plot(phase_ref, Data_ref[:, 1], c='r', lw=2, alpha=0.5)
plt.legend(Ref_Old, "Ref Old")
plt.show()

# choose a gait as test data
test_phase = train_data[10, :, 0]  # test_phase may be longer than phase
test_data = train_data[10, :, 1:]  # n_sample*n_dim
test_data_d = np.zeros_like(test_data)
for i in range(np.shape(test_data)[1]):
    test_data_d[:, i] = np.gradient(test_data[:, i]) / (test_phase[1] - test_phase[0])

test_plot = plt.plot(test_phase, test_data, c='b', lw=2)

# choose via point
idx_max_fz_0 = np.argmax(test_data[0:50, 0])
idx_mid = 50
idx_max_fz_1 = np.argmax(test_data[50:, 0]) + 50

via_idx = [0, idx_max_fz_0, idx_mid, idx_max_fz_1, 99]
via_phase = test_phase[via_idx]
via_point = np.zeros((len(via_idx), 4))
via_point[:, 0:2] = test_data[via_idx, :]  # n_sample*n_dim
via_point[:, 2:] = test_data_d[via_idx, :]  # n_sample*n_dim
via_var = np.eye(4) * 1e-6
plt.scatter(via_phase, via_point[:, 0], linewidths=5)
plt.scatter(via_phase, via_point[:, 1], linewidths=5)

newPhase, newData, newSigma = insert_via_point(phase=phase_ref, data=Data_ref, sigma=Sigma_ref,
                                               via_phase=via_phase, via_point=via_point, via_sigma=via_var,
                                               via_flag=np.ones((len(via_idx),)))
test_data_with_via_point_plot = plt.plot(newPhase, newData[:, 0:2], 'r--', lw=2)

kh = 10
Kinv = kmp_estimateMatrix_mean(phase=newPhase,
                               data=newData,
                               sigma=newSigma,
                               kh=kh,
                               lamda=1)

finalPhase = np.linspace(0, 1, 100)
finalTraj = kmp_interp_with_phase(phase_new=finalPhase,
                                  phase_ref=newPhase,
                                  data_ref=newData,
                                  kh=kh,
                                  Kinv=Kinv)
kmp_plot = plt.plot(finalPhase, finalTraj[:, 0:2], 'm')
plt.show()
