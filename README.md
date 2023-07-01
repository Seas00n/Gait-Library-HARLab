# Gait-Library-HARLab

# 使用说明
### 环境搭建
下载数据集，下载Opensim，注意Opensim使用默认路径，不要自定义安装

解压fcgm3chfff-1，解压scripts，解压AB06数据集，文件路径如下
```angular2html
fcgm3chfff-1
-AB06
    --10_09_18
        ---levelground
        ---ramp
        ---stair
        ---treadmill
-scripts
    --EpicToolbox
    --lib
    --MoCapTools
    --*.m
```
运行EpicToobox文件夹下的`install.m`文件
```angular2html
Installing EPICTOOLBOX...
Scripts added to path...
Path saved
```
运行MoCapTools文件架下的`install.m`文件
```angular2html
Scripts added to path...
Path saved...
If you are new to using this repo, please see +Osim/examples/example.m for information on how to use OpenSim
via MATLAB, or +Vicon/examples/example.m for information on automated iterative gap-filling via MATLAB.
Please restart MATLAB.
```


## 关于数据集
### conditions
Experiment description, locomotion mode labels,terrain condition (walking speed, ramp incline, or stair height).Sampled at 1000Hz.
### emg
Electromyography from 11 muscles. Sampled at 1000Hz, bandpass filtered (20-400Hz).
### fp
Ground reaction force data of all force plates used in a trial.Sampled at 1000Hz.
### gcLeft/gcRight 
Gait cycle segmented by heel strike or toe off of left/right foot. Sampled at 200Hz
### id
Inverse dynamics calculated by OpenSim using ground reaction force
            and motion capture kinematic data. Sampled at 200Hz.
### ik
Inverse kinematics calculated by OpenSim using motion capture data.
            Sampled at 200Hz.
### imu
Inertial Measurement Unit data from trunk, thigh, shank, and 
            foot segments. Sampled at 200Hz.
### jp
Estimation of instantaneous joint power using joint moment and
            angular velocity. Sampled at 200Hz.
### markers
Marker trajectories from motion capture. Sampled at 200Hz.

## Matlab脚本基本使用方法
参考Matlab_Data_Viewer/MyScript*.m

