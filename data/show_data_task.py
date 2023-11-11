import matplotlib.pyplot as plt
import numpy as np
data_path = "/media/yuxuan/SSD/DATASET/Collect/"

info = np.load(data_path+"info.mat")
print(info)

fp_data = np.load(data_path+"fp_data.npy")
print()
