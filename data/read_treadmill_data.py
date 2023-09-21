import numpy as np
import os
data_path = "/media/yuxuan/SSD/DATASET/AB06/treadmill/"

# load file name
filelists = os.listdir(data_path+"ik")
num_file = len(filelists)

# load speed
speed_lists = []
for i in range(num_file):
    condition = np.load(data_path+"conditions/"+filelists[i])
    time = condition[:, 0]
    speeds = condition[:, 1]
    speed_lists.append(np.mean(speeds))

print("min speed:{}".format(min(speed_lists)))
print("max speed:{}".format(max(speed_lists)))

# divide speed bands
speed_bands = np.linspace(min(speed_lists), max(speed_lists), 20)
print("speed_bands:{}".format(speed_bands))

