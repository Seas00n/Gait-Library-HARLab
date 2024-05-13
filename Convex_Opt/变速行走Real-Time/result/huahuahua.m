clear all;clc;close all;
figure(1)
thigh_55 = load("../data/VariableSpeed/thigh055.mat").yy24(:,20:23);
thigh_83 = load('../data/VariableSpeed/thigh083.mat').yy2(:,20:23);
thigh_110 = load('../data/VariableSpeed/thigh110.mat').yy3(:,20:23);
thigh_138 = load('../data/VariableSpeed/thigh138.mat').yy4(:,20:23);
knee_55 = load('../data/VariableSpeed/knee055.mat').yy1(:,20:23);
knee_83 = load('../data/VariableSpeed/knee083.mat').yy2(:,20:23);
knee_110 = load('../data/VariableSpeed/knee110.mat').yy3(:,20:23);
knee_138 = load('../data/VariableSpeed/knee138.mat').yy4(:,20:23);
ankle_55 = load('../data/VariableSpeed/ankle055.mat').yy1(:,20:23);
ankle_83 = load('../data/VariableSpeed/ankle083.mat').yy2(:,20:23);
ankle_110 = load('../data/VariableSpeed/ankle110.mat').yy3(:,20:23);
ankle_138 = load('../data/VariableSpeed/ankle138.mat').yy4(:,20:23);
q_thigh = [thigh_55,thigh_83,thigh_110,thigh_138];
q_knee = [knee_55,knee_83,knee_110,knee_138];
q_ankle = [ankle_55,ankle_83,ankle_110,ankle_138];
phase_desired = readNPY('./variable_actual/q_055_speed_phase_desired.npy');
phase_55 = readNPY('./variable_actual/q_055_speed_phase_actual.npy');
phase_83 = readNPY('./variable_actual/q_083_speed_phase_actual.npy');
phase_110 = readNPY('./variable_actual/q_110_speed_phase_actual.npy');
phase_138 = readNPY('./variable_actual/q_138_speed_phase_actual.npy');
for i=1:size(thigh_55,2)
    phase_55_qint(:,i) = calculate_phase_based_on_q_qint(thigh_55(:,i));
    phase_83_qint(:,i) = calculate_phase_based_on_q_qint(thigh_83(:,i));
    phase_110_qint(:,i) = calculate_phase_based_on_q_qint(thigh_110(:,i));
    phase_138_qint(:,i) = calculate_phase_based_on_q_qint(thigh_138(:,i));
    phase_55_dq(:,i) = calculate_phase_based_on_q_dq(thigh_55(:,i));
    phase_83_dq(:,i) = calculate_phase_based_on_q_dq(thigh_83(:,i));
    phase_110_dq(:,i) = calculate_phase_based_on_q_dq(thigh_110(:,i));
    phase_138_dq(:,i) = calculate_phase_based_on_q_dq(thigh_138(:,i));
end
knee_55_mean = mean(knee_55,2);
knee_83_mean = mean(knee_83,2);
knee_110_mean = mean(knee_110,2);
knee_138_mean = mean(knee_138,2);
ankle_55_mean = mean(ankle_55,2);
ankle_83_mean = mean(ankle_83,2);
ankle_110_mean = mean(ankle_110,2);
ankle_138_mean = mean(ankle_138,2);
pipeline(thigh_55,knee_55,ankle_55,phase_desired,phase_55,phase_55_qint,phase_55_dq,1,0.6);
pipeline(thigh_83,knee_83,ankle_83,phase_desired,phase_83,phase_83_qint,phase_83_dq,2,0.83);
pipeline(thigh_110,knee_110,ankle_110,phase_desired,phase_110,phase_110_qint,phase_110_dq,3,1.1);
pipeline(thigh_138,knee_138,ankle_138,phase_desired,phase_138,phase_138_qint,phase_138_dq,4,1.4);

function pipeline(q_thigh,q_knee,q_ankle,phase_desired,phase_actual,phase_qint,phase_dq,mode,v)
    q_knee_mean = mean(q_knee,2);
    q_ankle_mean = mean(q_ankle,2);
    
    subplot(4,4,4*(mode-1)+1)
    shadedErrorBar(0:100,q_thigh',{@mean,@std},'lineProps',{'Linewidth',2,'Color','#008F7A'});
    hold on
    plot(0:100,q_thigh,'--','linewidth',0.2,'Color','#00896F')

    subplot(4,4,4*(mode-1)+2)
    shadedErrorBar(0:100,phase_desired',{@mean,@std},'lineProps',{'Linewidth',2,'Color','#0089BA'});
    hold on
    shadedErrorBar(0:100,phase_actual',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#C34A36'});
    %shadedErrorBar(0:100,phase_qint',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#FF7F00'});% orange
    %shadedErrorBar(0:100,phase_dq',{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#77AC30'});% green
    
    for i = 1:size(q_thigh,2)
%         q_knee_ours(:,i) = spline(0:100,q_knee_mean,phase_actual(:,i));
%         q_ankle_ours(:,i) = spline(0:100,q_ankle_mean,phase_actual(:,i));
%         q_knee_qint(:,i) = spline(0:100,q_knee_mean,phase_qint(:,i));
%         q_ankle_qint(:,i) = spline(0:100,q_ankle_mean,phase_qint(:,i));
%         q_knee_dq(:,i) = spline(0:100,q_knee_mean,phase_dq(:,i));
%         q_ankle_dq(:,i) = spline(0:100,q_ankle_mean,phase_dq(:,i));
        [q_knee_ours(:,i),q_ankle_ours(:,i)] = surface_fitting(phase_actual(:,i),v);
        [q_knee_qint(:,i),q_ankle_qint(:,i)] = surface_fitting(phase_qint(:,i),v);
        [q_knee_dq(:,i),q_ankle_dq(:,i)] = surface_fitting(phase_dq(:,i),v);
    end
    subplot(4,4,4*(mode-1)+3)
    hold on
    %shadedErrorBar(0:100,q_knee_ours',{@mean,@std},'lineProps',{'--r','Linewidth',2});
    shadedErrorBarImproved(0:100,q_knee',1,{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#845EC2'});% orange
    shadedErrorBarImproved(0:100,q_knee_ours',2,{@mean,@std},'lineProps',{'Linewidth',2,'Color','#4B4453'});% green
    
    subplot(4,4,4*(mode-1)+4)
    hold on
    %shadedErrorBar(0:100,q_ankle_ours',{@mean,@std},'lineProps',{'--r','Linewidth',2});
    shadedErrorBarImproved(0:100,q_ankle_dq',1,{@mean,@std},'lineProps',{'--','Linewidth',2,'Color','#845EC2'});% orange
    shadedErrorBarImproved(0:100,q_ankle_ours',2,{@mean,@std},'lineProps',{'Linewidth',2,'Color','#4B4453'});% green
end
