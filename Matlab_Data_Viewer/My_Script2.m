clear all;clc;close all;
init();def=defaults;
subject = 'AB06';
ambulationModes ='treadmill';
trialfile ={'treadmill_01_01.mat',
            'treadmill_02_01.mat'};
sensors={'markers','gcLeft','gcRight','conditions','ik','id','emg','imu','gon','jp'};
%% 加载subject信息，寻找对应的mass和height，用于标准化数据
subjectLists = load(def.SUBJECT_INFO_FILE);subjectLists = subjectLists.data;
subjectWeight = subjectLists.Weight(strcmp(subjectLists.Subject,subject));
subjectHeight = subjectLists.Height(strcmp(subjectLists.Subject,subject));
fprintf('Subject:%s\n Mass:%f kg\n Height:%f m\n',subject,subjectWeight,subjectHeight);
%% 对数据进行分割
fprintf('\t %s strides \n',ambulationModes);
allfiles = f.fileList('Subject',subject, ...
                      'Mode',ambulationModes, ...
                      'Sensor',sensors, ...
                      'Trial',trialfile);
trials = f.EpicToolbox(allfiles);
allstrides = [];
for i =1:numel(trials)
    trial = trials{i};
    strides = segment_gc(trial,'GCtopic','gcRight','GCchannel','HeelStrike');
    fprintf("\t %d gaits in treadmill_0%d \n",size(strides,1),i);
    allstrides = [allstrides;strides];
end
fprintf('\t Totally %d gaits\n',size(allstrides,1));
%% 归一化步态对应的时间为0-1，对应0-100%
allstrides = Topics.normalize(allstrides,Topics.topics(allstrides),'Header');
%% interpolate将根据Header的0-1对数据进行插值
allstrides = Topics.interpolate(allstrides,0:0.01:1);
%% 对于ID和JP的数据往往需要根据用户体重进行归一化
allstrides = Topics.transform(@(x)(x/subjectWeight),allstrides,{'id','jp'});
%% 根据每个stride的label对其行动进行划分
alllabels = cell(size(allstrides));
for i=1:numel(allstrides)
    stride = allstrides{i};
    stride_condition = stride.conditions;
    if strcmp(ambulationModes,'treadmill')
        if numel(unique(stride_condition.speed.Speed))>2
            alllabels{i}='discard';%速度小，无法分类
        else
            alllabels{i}='treadmill';%速度>2在跑步机上运动
        end
        continue;
    end
end
%%
[labels,~,label_idx] = unique(alllabels);%自动进行分类
for i=1:numel(labels)
    label = labels{i};
    if strcmp(label,'discard')
        continue;
    elseif strcmp(label,'treadmill')
        strides = allstrides(label_idx==i);
        fprintf("\t %d gaits is treadmill\n",numel(strides));
        outfile=fstrides.genList('Subject',subject,'File',[label '.mat']); outfile=outfile{1};% 文件将被存储在STRIDES/AB06/treadmill.mat中
        mkdirfile(outfile);
        save(outfile,'strides');
    end
end