clear all;clc;close all;
data = importdata('新建 Microsoft Excel 工作表.xlsx').data;
q = data(3:end, [1:3,5:7,9:11]);
for i=1:size(q,1)-3
    if isnan(q(i,1))
        q(i,:)=[];
    end
end
q_low = q(:,1:3);
q_median = q(:,4:6);
q_high = q(:,7:9);
plot(1:404,q_low)
q_thigh = q(:,1:3:end);
q_knee = q(:,2:3:end);
q_ankle = q(:,3:3:end);
save('Speedthigh_new.mat','q_thigh');
save('Speedknee_new.mat','q_knee');
save('Speedankle_new.mat','q_ankle');