clear all;clc;close all;
fig1 = figure(1);
flow_line(2,fig1,1);
for i=1:22
    fig = figure(i);
    flow_line(1,fig,i);
end
function flow_line(mode,fig,idx)
    if mode==1
        mode_n = 'low';
        v=0.55;
    elseif mode==2
        mode_n = 'median';
        v=0.85;
    else
        mode_n = 'high';
        v=1.2;
    end
    phase_predicted = readNPY(['q_',mode_n,'_speed_phase_desired.npy']);
    phase_actual = readNPY(['q_',mode_n,'_speed_phase_actual.npy']);
    load('../data/Speedthigh_new.mat')
    load('../data/Speedknee_new.mat')
    load('../data/Speedankle_new.mat')
    load ../Model_Fitting/opensource_speed.mat
    q_thigh = q_thigh(:,mode);
    step=2;
    q_knee = knee_speed(:,idx:step:idx+step*3);
    q_ankle = ankle_speed(:,idx:step:idx+step*3);
    [phase_qint,~,~] = calculate_phase_based_on_q_qint(q_thigh);
    [phase_dq,~,~] = calculate_phase_based_on_q_dq(q_thigh);
    for i=1:4
        phase_predicted_s(:,i) = phase_predicted((i-1)*101+1:i*101);
        phase_actual_s(:,i) = phase_actual((i-1)*101+1:i*101);
        phase_qint_s(:,i) = calculate_phase_based_on_q_qint(q_thigh((i-1)*101+1:i*101));
        phase_dq_s(:,i) =  calculate_phase_based_on_q_dq(q_thigh((i-1)*101+1:i*101));
        q_thigh_s(:,i) = q_thigh((i-1)*101+1:i*101);
        q_knee_s(:,i) = q_knee((i-1)*101+1:i*101);
        q_ankle_s(:,i) = q_ankle((i-1)*101+1:i*101);
    end
    mean_q_knee = mean(q_knee_s,2);
    mean_q_ankle = mean(q_ankle_s,2);
    for i=1:4
        %[q_knee_ours_s(:,i),q_ankle_ours_s(:,i)]=surface_fitting(phase_predicted_s(:,i),v);
        %[q_knee_qint_s(:,i),q_ankle_qint_s(:,i)]=surface_fitting(phase_qint_s(:,i),v);
        %[q_knee_dq_s(:,i),q_ankle_dq_s(:,i)]=surface_fitting(phase_dq_s(:,i),v);
        q_knee_ours_s(:,i) = spline(0:100,mean_q_knee,phase_actual_s(:,i));
        q_ankle_ours_s(:,i) = spline(0:100,mean_q_ankle,phase_actual_s(:,i));
        q_knee_qint_s(:,i) = spline(0:100,mean_q_knee,phase_qint_s(:,i));
        q_ankle_qint_s(:,i) = spline(0:100,mean_q_ankle,phase_qint_s(:,i));
        q_knee_dq_s(:,i) = spline(0:100,mean_q_knee,phase_dq_s(:,i));
        q_ankle_dq_s(:,i) = spline(0:100,mean_q_ankle,phase_dq_s(:,i));
    end
    %subplot(2,2,4*(mode-1)+1)
    subplot(2,2,1)
    shadedErrorBar(0:100,q_thigh_s',{@mean,@std},'lineProps',{'b','Linewidth',2});
    %subplot(2,2,4*(mode-1)+2)
    subplot(2,2,2)
    shadedErrorBar(0:100,phase_predicted_s',{@mean,@std},'lineProps',{'b','Linewidth',2});
    hold on
    shadedErrorBar(0:100,phase_actual_s',{@mean,@std},'lineProps',{'--r','Linewidth',2});
    %shadedErrorBar(0:100,phase_qint_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#FF7F00'});% orange
    %shadedErrorBar(0:100,phase_dq_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#77AC30'});% green
    %subplot(2,2,4*(mode-1)+3)
    subplot(2,2,3)
    shadedErrorBar(0:100,q_knee_s',{@mean,@std},'lineProps',{'b','Linewidth',2});
    hold on
    shadedErrorBar(0:100,q_knee_ours_s',{@mean,@std},'lineProps',{'--r','Linewidth',2});
    %shadedErrorBar(0:100,q_knee_qint_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#FF7F00'});
    %shadedErrorBar(0:100,q_knee_dq_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#77AC30'});
    %subplot(2,2,4*mode)
    subplot(2,2,4)
    shadedErrorBar(0:100,q_ankle_s',{@mean,@std},'lineProps',{'b','Linewidth',2});
    hold on
    shadedErrorBar(0:100,q_ankle_ours_s',{@mean,@std},'lineProps',{'--r','Linewidth',2});
    %shadedErrorBar(0:100,q_ankle_qint_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#FF7F00'});
    %shadedErrorBar(0:100,q_ankle_dq_s',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#77AC30'});
    
end