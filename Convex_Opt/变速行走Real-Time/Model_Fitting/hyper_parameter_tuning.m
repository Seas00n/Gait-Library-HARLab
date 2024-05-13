clear all;clc;close all;
load opensource_speed.mat
thigh_speed = thigh_speed-thigh_speed(1,:);
plot(1:101,thigh_speed,'linewidth',2,'color','#7E2F8E');
grid off
popt_list = readNPY('popt_list.npy');
popt_list_all = zeros(28,2,4);
hold on
for i=1:28
    thigh_speed(:,i) = change_range(thigh_speed(:,i)',50,92)';
end
stance_end_threshold_vec = zeros(1,28);
swing_end_threshold_vec = zeros(1,28);
for i=1:28
    angle_center = thigh_speed(:,i);
    [stance_end_threshold,stance_end_idx]= min(angle_center(1:70));
    stance_end_threshold_vec(i) = stance_end_threshold;
    [swing_end_threshold,swing_end_idx]=max(angle_center(stance_end_idx:90));
    swing_end_threshold_vec(i) = swing_end_threshold;
    popt_list = readNPY('popt_list.npy');
    phase_vec = zeros(1,101);
    idx_list = [1,stance_end_idx,swing_end_idx+stance_end_idx-1,101];
    popt_list_new = zeros(2,4);
    for j =1:2
            x=idx_list(j):idx_list(j+1)-1;
            [popt_list_new(j,:),phase_vec(x)] = fit_phase_of_monotonous_vec(x',angle_center(x),popt_list(j,:));
    end
    popt_list_all(i,:,:) = popt_list_new;
end
figure(2)
v_vec = 0.5:0.05:1.85;
subplot(211)
plot(v_vec,stance_end_threshold_vec);
popt = polyfit(v_vec,stance_end_threshold_vec,1);
hold on
s_vec_new = polyval(popt,v_vec);
plot(v_vec,s_vec_new);
subplot(212)
plot(v_vec,swing_end_threshold_vec);
popt = polyfit(v_vec,swing_end_threshold_vec,1);
hold on
s_vec_new = polyval(popt,v_vec);
plot(v_vec,s_vec_new);

h_vec = zeros(3,28);
for i=1:28
    h_vec(1,i) = popt_list_all(i,1,1);
    h_vec(2,i) = popt_list_all(i,2,1);
end
s0_vec = zeros(3,28);
for i=1:28
    s0_vec(1,i) = popt_list_all(i,1,2);
    s0_vec(2,i) = popt_list_all(i,2,2);
end
k_vec = zeros(3,28);
for i=1:28
    k_vec(1,i) = popt_list_all(i,1,3);
    k_vec(2,i) = popt_list_all(i,2,3);
end
b_vec = zeros(3,28);
for i=1:28
    b_vec(1,i) = popt_list_all(i,1,4);
    b_vec(2,i) = popt_list_all(i,2,4);
end

parameter_changed = zeros(2,2,2); 
% stance|h stance|b
% swing|h swing|b
figure(3)
subplot(221)
plot(v_vec,h_vec(1,:),'linewidth',2,'LineStyle','-.');
title('Change of parameter h for stance')
xlabel('Speed')
ylabel('h')
popt = polyfit(v_vec, h_vec(1,:),1);
parameter_changed(1,1,:)=popt;
h_vec_new = polyval(popt,v_vec);
hold on
plot(v_vec, h_vec_new,'linewidth',2,'LineStyle','-')

subplot(222)
plot(v_vec,b_vec(1,:),'linewidth',2,'LineStyle','-.');
title('Change of parameter b for stance')
xlabel('Speed')
ylabel('h')
popt = polyfit(v_vec, b_vec(1,:),1);
parameter_changed(1,2,:)=popt;
b_vec_new = polyval(popt,v_vec);
hold on
plot(v_vec, b_vec_new,'linewidth',2,'LineStyle','-')

subplot(223)
plot(v_vec,h_vec(2,:),'linewidth',2,'LineStyle','-.');
title('Change of parameter h for swing')
xlabel('Speed')
ylabel('h')
popt = polyfit(v_vec, h_vec(2,:),1);
parameter_changed(2,1,:)=popt;
h_vec_new = polyval(popt,v_vec);
hold on
plot(v_vec, h_vec_new,'linewidth',2,'LineStyle','-')

subplot(224)
plot(v_vec, b_vec(2,:),'linewidth',2,'LineStyle','-.');
title('Change of parameter b for swing')
xlabel('Speed')
ylabel('h')
popt = polyfit(v_vec, b_vec(2,:),1);
parameter_changed(2,2,:)=popt;
b_vec_new = polyval(popt,v_vec);
hold on
plot(v_vec, b_vec_new,'linewidth',2,'LineStyle','-')
writeNPY(parameter_changed,'parameter_tuning.npy')



function [popt,phase] = fit_phase_of_monotonous_vec(x,y,beta0)
    sig = @(popt,x)popt(1)./(1+exp(-popt(3)*(x-popt(2))))+popt(4);
    sig_inv=@(popt,y)popt(2)-log(popt(1)./(y-popt(4))-1)/popt(3);
    %plot(x-1,sig(beta0,x-1),'blue','linewidth',1,'LineStyle','-')
    hold on
    %plot(x-1,y,'red','linewidth',1,'LineStyle','-');
    opt=statset('MaxIter',1000,'TolX',1e-12);
    popt = nlinfit(x-1,y,sig,beta0,opt);
    [popt,~]=fmincon(@(beta)new_target_fun(beta,y,x-1),popt);
    plot(x-1,sig(popt,x-1),'--','color','c','LineWidth',0.5);
    xlabel('Phase (%)')
    ylabel('Thigh Angle (deg)')
    xlim([0,100])
    phase = abs(sig_inv(popt,y));
    phase(phase>100) = 100;
    grid on
end
function error=new_target_fun(popt,y,x)
    phase = popt(2)-log(popt(1)./(y-popt(4))-1)/popt(3);
    for i=2:size(phase,1)
        if phase(i)<phase(i-1)
            phase(i) = phase(i-1);
        end
    end
    delta = abs(phase-x);
    delta_max = max(delta);
    error = 0.01*sum(delta'*delta)+1*delta_max/(x(end)-x(1));
    error = abs(error);
end
function angle = change_range(angle,new_stance_idx,new_swing_idx)
    [~,stance_end_idx]= min(angle(1,:));
    [~,swing_end_idx] = max(angle(1,stance_end_idx+1:99));
    xx=linspace(1,stance_end_idx,new_stance_idx);
    angle1 = spline(1:stance_end_idx,angle(:,1:stance_end_idx),xx);
    xx=linspace(stance_end_idx,swing_end_idx+stance_end_idx,new_swing_idx-new_stance_idx+1);
    angle2 = spline(stance_end_idx:swing_end_idx+stance_end_idx,angle(:,stance_end_idx:swing_end_idx+stance_end_idx),xx);
    xx=linspace(swing_end_idx+stance_end_idx,101,101-size(angle1,2)-size(angle2,2));
    angle3 = spline(swing_end_idx+stance_end_idx:101,angle(:,stance_end_idx+swing_end_idx:101),xx);
    angle=[angle1,angle2,angle3];
end