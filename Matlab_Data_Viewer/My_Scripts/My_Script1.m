clear all;clc;
init();def = defaults;%类似于头文件，初始化文件管理器
SUBJECT = 'AB06';%选择受试者
AMBULATION = 'treadmill';%选择地形
TRIAL = {'treadmill_02_01.mat','treadmill_01_01.mat'};%选择实验对应文件名称
%获取所有同名实验不同类型数据的路径
allfiles = f.fileList("Subject",SUBJECT,"Mode",AMBULATION,"Trial",TRIAL);
%每个实验对应的数据被封装在一个trial结构体内部
trials = f.EpicToolbox(allfiles);
%选择第一次实验
trial = trials{1};
%% 绘制数据
% Plot Walking speed from the trial conditions
subplot(4,1,1);
plot(trial.conditions.speed.Header,trial.conditions.speed.Speed);
xlabel('Time(s)'); ylabel('Speed (m/s)');
% Plot Gastrocnemius medialis from the EMG data
subplot(4,1,2);
plot(trial.emg.Header,trial.emg.gastrocmed);
xlabel('Time(s)'); ylabel('EMG');
% Plot the hip flexion from the inverse kinematics
subplot(4,1,3);
plot(trial.ik.Header,trial.ik.hip_flexion_r);
xlabel('Time(s)'); ylabel('Hip angle (deg)');
% Plot the hip flexion moment from the inverse dynamics
subplot(4,1,4);
plot(trial.id.Header,trial.id.hip_flexion_r_moment);
xlabel('Time(s)'); ylabel('Hip moment (N/m)');
%% 画指定的channel
sensor = 'fp';
channel = 'Treadmill_R_vy';
if(isfield(trial, sensor))
    if(any(strcmp(trial.(sensor).Properties.VariableNames, channel)))
        figure();
        plot(trial.(sensor).Header,trial.(sensor).(channel));
        xlabel('Time(s)');
        title(['Sensor: ', sensor, '; Channel: ', channel], 'Interpreter', 'none');
    else
        warning('Available Channels:');
        trial.(sensor).Properties.VariableNames'
        error('Channel not found... please make sure the channel name is correct');    
    end
else
    warning('Available Sensors:');
    fieldnames(trial)'
    error('Sensor not found... please make sure the sensor name is correct');
end