% clear all;clc;close all;
% init();def=defaults;
% subject = 'AB06';
% ambulationModes ='treadmill';
% trialfile ={'treadmill_01_01.mat',
%     'treadmill_02_01.mat',
%     'treadmill_03_01.mat',
%     'treadmill_04_01.mat',
%     'treadmill_05_01.mat',
%     'treadmill_06_01.mat',
%     'treadmill_07_01.mat',
%     'treadmill_08_01.mat'};
% sensors={'markers','gcLeft','gcRight','conditions','fp'};
% %% 加载subject信息，寻找对应的mass和height，用于标准化数据
% subjectLists = load(def.SUBJECT_INFO_FILE);subjectLists = subjectLists.data;
% subjectWeight = subjectLists.Weight(strcmp(subjectLists.Subject,subject));
% subjectHeight = subjectLists.Height(strcmp(subjectLists.Subject,subject));
% fprintf('Subject:%s\n Mass:%f kg\n Height:%f m\n',subject,subjectWeight,subjectHeight);
% %% 对数据进行分割
% fprintf('\t %s strides \n',ambulationModes);
% allfiles = f.fileList('Subject',subject, ...
%                       'Mode',ambulationModes, ...
%                       'Sensor',sensors, ...
%                       'Trial',trialfile);
% trials = f.EpicToolbox(allfiles);
% allstrides = [];
% for i =1:numel(trials)
%     trial = trials{i};
%     strides = segment_gc(trial,'GCtopic','gcRight','GCchannel','HeelStrike');
%     fprintf("\t %d gaits in treadmill_0%d \n",size(strides,1),i);
%     allstrides = [allstrides;strides];
% end
% fprintf('\t Totally %d gaits\n',size(allstrides,1));
% %% 归一化步态对应的时间为0-1，对应0-100%
% allstrides = Topics.normalize(allstrides,Topics.topics(allstrides),'Header');
% %% interpolate将根据Header的0-1对数据进行插值
% allstrides = Topics.interpolate(allstrides,0:0.01:1);
% %% 对于ID和JP的数据往往需要根据用户体重进行归一化
% allstrides = Topics.transform(@(x)(x/subjectWeight),allstrides,{'fp'});
% %% 根据每个stride的label对其行动进行划分
% alllabels = cell(size(allstrides));
% for i=1:numel(allstrides)
%     stride = allstrides{i};
%     stride_condition = stride.conditions;
%     if strcmp(ambulationModes,'treadmill')
%         if numel(unique(stride_condition.speed.Speed))>2
%             alllabels{i}='discard';%跑步机速度变化不稳定，无法分类
%         else
%             alllabels{i}='treadmill';
%         end
%         continue;
%     end
% end
% %% 
% [labels,~,label_idx] = unique(alllabels);%取出对应的strides
% for i=1:numel(labels)
%     label = labels{i};
%     if strcmp(label,'discard')
%         continue;
%     elseif strcmp(label,'treadmill')
%         strides = allstrides(label_idx==i);
%         fprintf("\t %d gaits is treadmill\n",numel(strides));
%         outfile=fstrides.genList('Subject',subject,'File',[label '.mat']);
%         outfile=outfile{1};% 文件将被存储在STRIDES/AB06/treadmill.mat中
%         mkdirfile(outfile);
%         save(outfile,'strides');
%     end
% end

clear all;clc;
close all;
strides = load("STRIDES\AB06\treadmill.mat").strides;
save_path = "I:\Open_Source_Data\gmm_data\";
save_count = 0;
for i=1:numel(strides)
    if mean(strides{i,1}.conditions.speed.Speed)>0.8
        time = strides{i,1}.fp.Header;
        fp_x = strides{i,1}.fp.Treadmill_R_vx;
        fp_y = strides{i,1}.fp.Treadmill_R_vy;
        fp_z = strides{i,1}.fp.Treadmill_R_vz;
        %plot(time,fp_x);
        %hold on
        idx_swing = find(abs(fp_y)<0.01);
        idx_swing_start = idx_swing(1);
        idx_swing_end = idx_swing(end);
        %scatter(time(idx_swing_start),fp_z(idx_swing_start));
        %scatter(time(idx_swing_end),fp_z(idx_swing_end));
        % x direction is small so doesn't use
        %fp_x_new = [fp_x(idx_swing_end-10:end);fp_x(1:idx_swing_end-11)];
        %fp_x_new = smoothdata(fp_x_new,'gaussian',10);
        fp_y_new = [fp_y(idx_swing_end-10:end);fp_y(1:idx_swing_end-11)];
        fp_y_new = smoothdata(fp_y_new,'gaussian',10);
        fp_z_new = [fp_z(idx_swing_end-10:end);fp_z(1:idx_swing_end-11)];
        fp_z_new = smoothdata(fp_z_new,'gaussian',10);
        idx_stance = find(abs(fp_y_new)>0.01);
        idx_stance_start = idx_stance(1);
        idx_stance_end = idx_stance(end);
        %plot(time, fp_y_new);
        %hold on
        %scatter(time(idx_stance_start),fp_y_new(idx_stance_start));
        %scatter(time(idx_stance_end),fp_y_new(idx_swing_end));
        x = idx_stance_start:idx_stance_end;
        fp_y_new = fp_y_new(idx_stance_start:idx_stance_end);
        fp_y_new(1)=0;fp_y_new(end)=0;
        fp_z_new = fp_z_new(idx_stance_start:idx_stance_end);
        fp_z_new(1)=0;fp_z_new(end)=0; 
        xx = linspace(idx_stance_start,idx_stance_end,100);
        time_interp = linspace(time(idx_stance_start),time(idx_stance_end),100);
        time_interp = time_interp-time_interp(1);
        fp_y_interp = interp1(x,fp_y_new,xx,"cubic");
        fp_z_interp = interp1(x,fp_z_new,xx,"cubic");
        conditions = ones(1,100)*mean(strides{i,1}.conditions.speed.Speed);
        %plot(time_interp, fp_y_interp,linewidth=2);
        %plot(time_interp,fp_z_interp,linewidth=2);
        save_data = [time_interp;conditions;fp_y_interp;fp_z_interp];
        writeNPY(save_data,save_path+string(save_count)+".npy");
        save_count = save_count+1;
    end
end
% data = readNPY(save_path+"100.npy");
% plot(data(1,:),data(3,:));
% hold on
% plot(data(1,:),data(4,:));
