clear all;clc;close all;
figure(1)
thigh_55 = load("../data/VariableSpeed/thigh055.mat").yy24(:,1:23);
thigh_83 = load('../data/VariableSpeed/thigh083.mat').yy2(:,1:23);
thigh_110 = load('../data/VariableSpeed/thigh110.mat').yy3(:,1:23);
thigh_138 = load('../data/VariableSpeed/thigh138.mat').yy4(:,1:23);
knee_55 = load('../data/VariableSpeed/knee055.mat').yy1(:,1:23);
knee_83 = load('../data/VariableSpeed/knee083.mat').yy2(:,1:23);
knee_110 = load('../data/VariableSpeed/knee110.mat').yy3(:,1:23);
knee_138 = load('../data/VariableSpeed/knee138.mat').yy4(:,1:23);
ankle_55 = load('../data/VariableSpeed/ankle055.mat').yy1(:,1:23);
ankle_83 = load('../data/VariableSpeed/ankle083.mat').yy2(:,1:23);
ankle_110 = load('../data/VariableSpeed/ankle110.mat').yy3(:,1:23);
ankle_138 = load('../data/VariableSpeed/ankle138.mat').yy4(:,1:23);
q_thigh = [thigh_55,thigh_83,thigh_110,thigh_138];
q_knee = [knee_55,knee_83,knee_110,knee_138];
q_ankle = [ankle_55,ankle_83,ankle_110,ankle_138];
phase_desired = readNPY('./variable_actual/q_055_speed_phase_desired.npy');
phase_55 = readNPY('./variable_actual/q_055_speed_phase_actual.npy');
phase_83 = readNPY('./variable_actual/q_083_speed_phase_actual.npy');
phase_110 = readNPY('./variable_actual/q_110_speed_phase_actual.npy');
phase_138 = readNPY('./variable_actual/q_138_speed_phase_actual.npy');
phase_55_no_kf = readNPY('./variable_actual/q_055_speed_phase_actual_no_kf.npy');
phase_83_no_kf = readNPY('./variable_actual/q_083_speed_phase_actual_no_kf.npy');
phase_110_no_kf = readNPY('./variable_actual/q_110_speed_phase_actual_no_kf.npy');
phase_138_no_kf = readNPY('./variable_actual/q_138_speed_phase_actual_no_kf.npy');
thigh_55_mean = mean(thigh_55,2);
thigh_83_mean = mean(thigh_83,2);
thigh_110_mean = mean(thigh_110,2);
thigh_138_mean = mean(thigh_138,2);
q_thigh_mean = [thigh_55_mean,thigh_83_mean,thigh_110_mean,thigh_138_mean];
load ../Model_Fitting/thigh_speed_plot.mat
figure(1)
v_vec = 0.5:0.05:1.85;
area(linspace(0,50,10),30*ones(10,1),'linestyle','none','FaceColor','#F4E2D8','EdgeColor','none');
hold on
area(linspace(0,50,10),-30*ones(10,1),'linestyle','none','FaceColor','#F4E2D8','EdgeColor','none');
area(linspace(50,92,10),30*ones(10,1),'linestyle','none','FaceColor','#C4E0E5','EdgeColor','none');
area(linspace(50,92,10),-30*ones(10,1),'linestyle','none','FaceColor','#C4E0E5','EdgeColor','none')
area(linspace(92,100,10),30*ones(10,1),'linestyle','none','FaceColor','#ddd6f3','EdgeColor','none');
area(linspace(92,100,10),-30*ones(10,1),'linestyle','none','FaceColor','#ddd6f3','EdgeColor','none');
for i=1:6:size(thigh_speed,2)
    stance = 0:50;
    plot(stance,thigh_speed(stance+1,i),"Color",color_ruler(v_vec(i),'#e1eec3','#f05053'),'linewidth',2);
    swing = 50:92;
    plot(swing,thigh_speed(swing+1,i),"Color",color_ruler(v_vec(i),'#78ffd6','#007991'),'linewidth',2);
    refraction = 92:100;
    plot(refraction,thigh_speed(refraction+1,i),"Color",color_ruler(v_vec(i),'#ffc0cb','#800080'),'linewidth',2);
end

figure(2)
mean_phase_55 = phase_55(:,18);
mean_phase_55(1) = 0;
mean_phase_55_no_kf = mean(phase_55_no_kf(:,18),2);
mean_phase_55_no_kf(1)=0;
mean_phase_55_no_kf(end)=100;
windowSize = 3; 
b = (1/windowSize)*ones(1,windowSize);
a = 1;
mean_phase_55_no_kf=filter(b,a,mean_phase_55_no_kf);
hold on
plot(0:100,0:100,'linewidth',2,'Color','#f05053');
plot(0:100,mean_phase_55,'linewidth',2,'Color','#514A9D');
plot(0:100,mean_phase_55_no_kf,'linewidth',2,'Color','#24C6DC','LineStyle','--')



% hold on
% stance = 0:50;
% plot(stance,thigh_55_mean(stance+1),"Color",color_ruler(0.5,'#e1eec3','#f05053'),'linewidth',2);
% plot(stance,thigh_83_mean(stance+1),"Color",color_ruler(0.83,'#e1eec3','#f05053'),'linewidth',2);
% plot(stance,thigh_110_mean(stance+1),"Color",color_ruler(1.1,'#e1eec3','#f05053'),'linewidth',2);
% plot(stance,thigh_138_mean(stance+1),"Color",color_ruler(1.38,'#e1eec3','#f05053'),'linewidth',2);
% swing = 50:92;
% plot(swing,thigh_55_mean(swing+1),"Color",color_ruler(0.5,'#78ffd6','#007991'),'linewidth',2);
% plot(swing,thigh_83_mean(swing+1),"Color",color_ruler(0.83,'#78ffd6','#007991'),'linewidth',2);
% plot(swing,thigh_110_mean(swing+1),"Color",color_ruler(1.1,'#78ffd6','#007991'),'linewidth',2);
% plot(swing,thigh_138_mean(swing+1),"Color",color_ruler(1.38,'#78ffd6','#007991'),'linewidth',2);
% refraction = 92:100;
% plot(refraction,thigh_55_mean(refraction+1),"Color",color_ruler(0.5,'#ffc0cb','#800080'),'linewidth',2);
% plot(refraction,thigh_83_mean(refraction+1),"Color",color_ruler(0.83,'#ffc0cb','#800080'),'linewidth',2);
% plot(refraction,thigh_110_mean(refraction+1),"Color",color_ruler(1.1,'#ffc0cb','#800080'),'linewidth',2);
% plot(refraction,thigh_138_mean(refraction+1),"Color",color_ruler(1.38,'#ffc0cb','#800080'),'linewidth',2);
%test_color_ruler(1,'#e1eec3','#f05053')
function test_color_ruler(fig,s_c,e_c)
    v=0.5:0.01:1.4;
    figure(fig);
    for i=1:size(v,2)
        color_s = color_ruler(v(i),s_c,e_c);
        scatter(v(i),v(i),'filled','MarkerFaceColor',color_s)
        hold on
    end
end
function color_s=color_ruler(v,start_color,end_color)
    rgb0 = [hex2dec(start_color(2:3)),hex2dec(start_color(4:5)),hex2dec(start_color(6:7))];
    rgb1 = [hex2dec(end_color(2:3)),hex2dec(end_color(4:5)),hex2dec(end_color(6:7))];
    color = (1-abs(v-1.05)/1.35)*(rgb1-rgb0)+rgb0;
    color = floor(color);
    color_s = ['#',reshape(dec2hex(color)',[6,1])'];
end
