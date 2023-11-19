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
plt.plot(phase, DataOut[:, 0:1], c='r', lw=2, alpha=0.5)
plt.legend()
plt.show()

# save the beat result
if retrain_or_not == "Y":
    save_new_model_or_not = input("Save the new model? [Y/n]")
    if save_new_model_or_not == "Y":
        pickle.dump(gmm, open("fp_gmm", "wb"))
