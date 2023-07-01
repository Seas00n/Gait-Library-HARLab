# Gait-Library-HARLab
 
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