import numpy as np
import os
import scipy.interpolate as scip
from load_data import *

data_path = "/media/yuxuan/SSD/DATASET/AB06/treadmill/"
save_path = "/media/yuxuan/SSD/DATASET/Collect/"

# load file name
filelists = os.listdir(data_path + "ik")
num_file = len(filelists)

# load speed
speed_lists = []
for i in range(num_file):
    condition = np.load(data_path + "conditions/" + filelists[i])
    time = condition[:, 0]
    speeds = condition[:, 1]
    speed_lists.append(np.mean(speeds))

print("min speed:{}".format(min(speed_lists)))
print("max speed:{}".format(max(speed_lists)))

# divide speed bands
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

angle_result = load_data(data_path=data_path + "gon/",
                         file_list=filelists,
                         idx_band_list=idx_band_list,
                         kind_id_list=[0, 4, 3, 1])
np.save(save_path+"speeds.npy", speeds)
np.save(save_path+"angle_data.npy", np.array(angle_result))

ik_result = load_data(data_path=data_path + "ik/",
                    file_list=filelists,
                    idx_band_list=idx_band_list,
                    kind_id_list=[0, 7, 10, 11])
np.save(save_path+"ik_angle_data.npy", np.array(ik_result))


id_result = load_data(data_path=data_path + "id/",
                    file_list=filelists,
                    idx_band_list=idx_band_list,
                    kind_id_list=[0, 7, 16, 18])
np.save(save_path+"id_angle_data.npy", np.array(id_result))

