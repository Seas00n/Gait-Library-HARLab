import numpy as np
import os
import scipy.interpolate as scip
from load_data import *
from body_idx import *

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

fp_result = load_data(data_path=data_path + "fp/",
                      file_list=filelists,
                      idx_band_list=idx_band_list,
                      kind_id_list=list(range(19)))
np.save(save_path + "fp_data.npy", np.array(fp_result))

bd = BodyIdx()

Pelvis_id_list = [0] + bd.L_ASIS + bd.L_PSIS + bd.R_ASIS + bd.R_PSIS
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=Pelvis_id_list)
np.save(save_path + "pelvis_data.npy", np.array(result))

LThigh_id_list = [0] + bd.L_Thigh_Upper + bd.L_Thigh_Front + bd.L_Thigh_Rear + bd.L_Knee
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=LThigh_id_list)
np.save(save_path + "lthigh_data.npy", np.array(result))

RThigh_id_list = [0] + bd.R_Thigh_Upper + bd.R_Thigh_Front + bd.R_Thigh_Rear + bd.R_Knee
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=RThigh_id_list)
np.save(save_path + "rthigh_data.npy", np.array(result))

LShank_id_list = [0]+bd.L_Shank_Upper + bd.L_Shank_Front + bd.L_Shank_Rear + bd.L_Ankle
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=LShank_id_list)
np.save(save_path + "lshank_data.npy", np.array(result))

RShank_id_list = [0]+bd.R_Shank_Upper + bd.R_Shank_Front + bd.R_Shank_Rear + bd.R_Ankle
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=RShank_id_list)
np.save(save_path + "rshank_data.npy", np.array(result))

LFoot_id_list = [0]+bd.L_Toe_Lat+bd.L_Toe_Med+bd.L_Toe_Tip
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=LFoot_id_list)
np.save(save_path + "lfoot_data.npy", np.array(result))

RFoot_id_list = [0]+bd.R_Toe_Lat+bd.R_Toe_Med+bd.R_Toe_Tip
result = load_data(data_path=data_path + "markers/",
                   file_list=filelists,
                   idx_band_list=idx_band_list,
                   kind_id_list=RFoot_id_list)
np.save(save_path + "rfoot_data.npy", np.array(result))
