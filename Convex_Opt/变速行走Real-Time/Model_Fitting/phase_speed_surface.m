clear all;clc;close all
load opensource_speed.mat
%% plot thigh
% 如果优化速度慢可以降低网格采样率
thigh_speed = thigh_speed-thigh_speed(1,:);
thigh_speed = downsample(thigh_speed,2);
angle = downsample(thigh_speed',2)';
phase = 0:100;
phase = downsample(phase,2);
v_vec = linspace(0.5,1.85,size(angle,2));
% ck(v) 伯恩斯D坦多项式的个数
num_c = 4;
% 使用几次多项式拟合bk(s) 
num_popt = 7;
[x,angle_pre]=angle_map(angle,phase,v_vec,num_c,num_popt,'parula',1,1);
plot_thigh_ridge(angle_pre,phase,v_vec)
writeNPY(x,'thigh_beta.npy');
%% plot knee
knee_speed = downsample(knee_speed,2);
angle = downsample(knee_speed',2)';
[x,~]=angle_map(angle,phase,v_vec,num_c,num_popt,'parula',2,2);
writeNPY(x,'knee_beta.npy')
%% plot ankle
ankle_speed = downsample(ankle_speed,2);
angle = downsample(ankle_speed',2)';
[x,~]=angle_map(angle,phase,v_vec,num_c,num_popt,'parula',3,3);
writeNPY(x,'ankle_beta.npy')

function [x,angle_pre] = angle_map(angle,phase,v_vec,num_c,num_popt,color,fig1,fig2)
    A=0;f=0;
    for i=1:size(angle,1)
        for j=1:size(v_vec,2)
            Aij = cal_delta_mat(phase(i),v_vec(j),num_c,num_popt); 
            A=A+Aij'*Aij;
            f = f-2*angle(i,j)*Aij;
        end
    end
    A = 2*A;
    rank(A)
    opt = optimset('MaxIter',5000);
    f = f';
    lb=-1000*ones(size(f,1),1);
    ub=1000*ones(size(f,1),1);
    x = quadprog(A,f,[],[],[],[],[],[],[],opt);
    figure(1)
    subplot(3,1,fig1)
    [X,Y]=meshgrid(v_vec,phase);
    s1=surf(X,Y,angle);
    s1.EdgeColor='none';
    s1.FaceAlpha=0.5;
    colormap("autumn")
    grid off
    colormap('cool')
    angle_pre = zeros(size(X,1),size(X,2));
    for i=1:size(X,1)
        for j=1:size(X,2)
            Aij = cal_delta_mat(phase(i),v_vec(j),num_c,num_popt);
            angle_pre(i,j) = Aij*x;
        end
    end
    figure(2)
    subplot(3,1,fig2)
    s2=surf(X,Y,angle_pre);
    grid off
    colormap(color)
    s2.EdgeColor='none';
    s2.FaceAlpha=0.5;
    angle_pre = angle_pre';
end
function delta_mat = cal_delta_mat(si,vj,num_c,num_popt)
    c_vec = zeros(1,num_c);
    c_vec(1)=1;
    for i=2:num_c
        n=num_c-2;
        k=i-2;
        c_vec(i) = nchoosek(n,k)*vj^(k)*(1-vj)^(n-k);
    end
    b_vec = zeros(num_c,num_c*num_popt);
    for i=1:num_c
        b_vec(i,num_popt*(i-1)+1:num_popt*i) = si.^(num_popt-1:-1:0);
    end
    delta_mat = c_vec*b_vec;
end
function plot_thigh_ridge(angle_pre,phase,v_vec)
    angle_pre=angle_pre';
    x_vec = zeros(1,size(angle_pre,2));
    y_vec = zeros(1,size(angle_pre,2));
    z_vec = zeros(2,size(angle_pre,2));
    for i=1:size(angle_pre,2)
        angle_center = angle_pre(:,i);
        [stance_end_threshold,stance_end_idx]= min(angle_center);
        [swing_end_threshold,swing_end_idx]=max(angle_center(stance_end_idx:end-5));
        x_vec(i) = v_vec(i);
        y_vec(1,i) = phase(stance_end_idx);
        y_vec(2,i) = phase(swing_end_idx+stance_end_idx-1);
        z_vec(1,i) = stance_end_threshold;
        z_vec(2,i) = swing_end_threshold;
    end
    figure(2)
    subplot(3,1,1)
    hold on
    x=1:size(angle_pre,2);
    xx=linspace(1,size(angle_pre,2),1000);
    popt = polyfit(x,x_vec,5);
    new_x = polyval(popt,x);
    popt = polyfit(x,y_vec(1,:),5);
    new_y = polyval(popt,x);
    popt = polyfit(x,z_vec(1,:),5);
    new_z = polyval(popt,x);
    plot3(new_x,new_y,new_z,'LineWidth',2,'Color','#D95319')
    popt = polyfit(x,y_vec(2,:),5);
    new_y = polyval(popt,x);
    popt = polyfit(x,z_vec(2,:),5);
    new_z = polyval(popt,x);
    plot3(new_x,new_y,new_z,'LineWidth',2,'Color','#D95319')
end