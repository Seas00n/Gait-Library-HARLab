% 此文档演示如何绘制分割后的步态数据
clear all;clc;close all;
init();def=defaults;
subject={'AB06','AB09'};
ambulationModes = 'treadmill';
sensor='ik';channel='hip_flexion_r';
%% subject对应的strides文件绝对路径
allfiles = fstrides.fileList('Subject',subject,'File',[ambulationModes,'.mat']);
% data被以struct结构加载，所有strides都混在同一个struct中
data = multiload(allfiles);
% 通过该函数使得每个患者的数据被单独包含在一个cell中，组成一个cell数组
data=cellfun(@(x)(x.strides),data,'Uni',0);
%% x为速度，y为数据
x = cell(size(data));
y = cell(size(data));
for i =1:numel(subject)
    channel_data = GetChannelFromStrides(data{i},sensor,channel);
    % 对于treadmill选择condition为速度
    condition = GetConditionFromStrides(data{i});
    x{i} = condition(~isnan(condition));
    y{i} = channel_data(:,~isnan(condition));
end
%% 在每个subplot中画出一个stride
h = figure(1);
h.Name = '不同速度下的平均大腿角度';
unique_x = unique([x{1};x{2}]);%该函数可以挑选出x中不重复的元素，从而得到速度的所有选择
cmap = parula(numel(unique_x));%颜色
subplot(1,2,1);
yy = y{1};
xx = x{1};
for i=1:numel(unique_x)
    plot(nanmean(yy(:,xx==unique_x(i)),2),'Color',cmap(i,:),'linewidth',4);
    hold on
end
grid on
title(sprintf('%s',subject{1}));
xlabel('Gait cycle (%)');
ylabel(yLabelSelector(sensor, channel));
colorbar;
clim([min(unique_x),max(unique_x)]);
subplot(1,2,2);
yy = y{2};
xx = x{2};
for i=1:numel(unique_x)
    plot(nanmean(yy(:,xx==unique_x(i)),2),'Color',cmap(i,:),'LineWidth',4);
    hold on
end
grid on
title(sprintf('%s',subject{2}));
xlabel('Gait cycle (%)');
ylabel(yLabelSelector(sensor, channel));
colorbar;
clim([min(unique_x),max(unique_x)]);