import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.interpolate as scip
data_path = "/media/yuxuan/SSD/DATASET/AB06/treadmill/"

info = np.load(data_path+"info.mat")[0]
print("Age:{} Gender:{} Mass:{} Height:{}".format(info[0],info[1],info[2],info[3]))

filelists = os.listdir(data_path + "fp")
num_file = len(filelists)
print("Totally {} Gait was record".format(num_file))

speed_lists = []
for i in range(num_file):
    condition = np.load(data_path + "conditions/" + filelists[i])
    time = condition[:, 0]
    speeds = condition[:, 1]
    speed_lists.append(np.mean(speeds))
print("min speed:{}".format(min(speed_lists)))
print("max speed:{}".format(max(speed_lists)))

speed_bands = np.linspace(min(speed_lists), max(speed_lists), 20)
speed_bands[0] -= 1e-8
speed_bands[-1] += 1e-8
print("speed_bands:{}".format(speed_bands))
speeds = np.array(speed_lists)
idx_band_list = []
num_band_list = []
for i in range(np.shape(speed_bands)[0] - 1):
    idx_band = np.where(np.logical_and(speeds > speed_bands[i], speeds <= speed_bands[i + 1]))[0]
    idx_band_list.append(idx_band)

gait_chosen = idx_band_list[10]
print("Chosen fp data:{}".format(gait_chosen))

raw_data_list = []
for gait_i in gait_chosen:
    gait_i_fp = np.load(data_path+"fp/{}.npy".format(gait_i))
    interp_x = np.arange(np.shape(gait_i_fp)[0])
    interp_x = (interp_x-0)/(interp_x[-1]-0)
    interp_xx = np.linspace(0,1,1000)
    num_attribute = np.shape(gait_i_fp)[1]
    gait_i_fp_interp = []
    for attr_j in range(num_attribute):
        attr_j_data = gait_i_fp[:,attr_j]
        if attr_j == 0:
            attr_j_data = attr_j_data-attr_j_data[0] # time
        interp_fun = scip.interp1d(interp_x,attr_j_data,kind='cubic')
        attr_j_data_interp = interp_fun(interp_xx)
        gait_i_fp_interp.append(attr_j_data_interp)
    raw_data_list.append(gait_i_fp_interp)
np.save("./scripts/raw_data.npy",np.array(raw_data_list))

raw_data = np.load("./scripts/raw_data.npy")
mass = 74.84 #kg
chosen_attribute_i = 3
for i in range(np.shape(raw_data)[0]):
    gait_i_data = raw_data[i,:,:].reshape((1000,-1))
    phase = np.linspace(0,1,1000)
    plt.plot(phase, gait_i_data[:,chosen_attribute_i])
plt.show()