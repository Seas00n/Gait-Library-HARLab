clear all;clc;close all;
init();def = defaults;
SUBJECT = 'AB06';
AMBULATION = 'treadmill';
DATE = "10_09_18";

subjectLists = load(def.SUBJECT_INFO_FILE);
subjectLists = subjectLists.data;
subjectWeight = subjectLists.Weight(strcmp(subjectLists.Subject,SUBJECT));
subjectHeight = subjectLists.Height(strcmp(subjectLists.Subject,SUBJECT));
subjectAge = subjectLists.Age(strcmp(subjectLists.Subject,SUBJECT));
subjectGender = subjectLists.Gender(strcmp(subjectLists.Subject,SUBJECT));
fprintf('Subject:%s\n Mass:%f kg\n Height:%f m\n',SUBJECT,subjectWeight,subjectHeight);
subjectInfo = [subjectAge,double(subjectGender=="M"),subjectWeight,subjectHeight];

f_dir = dir(fullfile("../"+"/"+SUBJECT+"/"+DATE+"/"+AMBULATION+"/conditions","*.mat"));
TRIAL = struct2table(f_dir).name;
allfiles = f.fileList("Subject",SUBJECT,"Mode",AMBULATION,"Trial",TRIAL);
trials = f.EpicToolbox(allfiles);
%%
save_path = "D:/DATASET/"+SUBJECT+"/"+AMBULATION+"/";
% if exist(save_path)==0
%     mkdir(save_path);
% end
% writeNPY(subjectInfo,save_path+"info.mat");
%%
clearvars -except trials save_path AMBULATION
fileID = fopen(save_path+'dataformat.txt','w');
namelist = fieldnames(trials{1,1});
for i=1:numel(namelist)
    fprintf(fileID, "@@@@@@@@@@@@@@@@@@@@@@@@@\n");
    fprintf(fileID, namelist{i}+"\n");
    fprintf(fileID, "$$$$$$$$\n");
    namelist_sub = fieldnames(trials{1,1}.(namelist{i}));
    for j =1:numel(namelist_sub)
        fprintf(fileID, namelist_sub{j}+"["+string(j-1)+"]"+"\n");
    end
end
fclose(fileID);

%%
% allstrides = [];
% for i =1:numel(trials)
%     trial = trials{i};
%     strides = segment_gc(trial,'GCtopic','gcRight','GCchannel','HeelStrike');
%     fprintf("\t %d gaits in treadmill_0%d \n",size(strides,1),i);
%     allstrides = [allstrides;strides];
% end
% %%
% clearvars -except allstrides save_path AMBULATION
% all_valid_strides = [];
% for i=1:numel(allstrides)
%     stride = allstrides{i};
%     stride_condition = stride.conditions;
%     if strcmp(AMBULATION,"treadmill")
%         if numel(unique(stride_condition.speed.Speed))>2
%             alllabels{i}='discard';%跑步机速度变化不稳定，无法分类
%         else
%             alllabels{i}='treadmill';
%             all_valid_strides = [all_valid_strides;stride];
%         end
%     elseif strcmp(AMBULATION,"stair")
%          all_valid_strides = [all_valid_strides;stride];
%     end
% end
% %%
% clearvars -except all_valid_strides save_path AMBULATION
% all_valid_strides_tables = struct2table(all_valid_strides);
% if strcmp(AMBULATION,"treadmill")
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% condition_tables = struct2table(all_valid_strides_tables.conditions).speed;
% save_path_ = save_path+"conditions/";
% save_data(condition_tables, save_path_);
% end
% if strcmp(AMBULATION,"stair")
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% condition_tables = struct2table(all_valid_strides_tables.conditions).labels;
% save_path_ = save_path+"conditions/";
% save_mode_data(condition_tables, save_path_);
% end
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.emg;
% save_path_ = save_path+"emg/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.fp;
% save_path_ = save_path+"fp/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.gcLeft;
% save_path_ = save_path+"gcLeft/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.gcRight;
% save_path_ = save_path+"gcRight/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.ik;
% save_path_ = save_path+"ik/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.id;
% save_path_ = save_path+"id/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.imu;
% save_path_ = save_path+"imu/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.gon;
% save_path_ = save_path+"gon/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.jp;
% save_path_ = save_path+"jp/";
% save_data(tables, save_path_);
% 
% clearvars -except all_valid_strides save_path all_valid_strides_tables
% tables = all_valid_strides_tables.markers;
% save_path_ = save_path+"markers/";
% save_data(tables, save_path_);
% 
% 
% 
% 




function save_data(tables,save_path)
if exist(save_path)==0
    mkdir(save_path);
end
for i=1:numel(tables)
    data = table2array(tables{i});
    writeNPY(data, save_path+string(i)+".npy")
end
end

function save_mode_data(tables, save_path)
if exist(save_path)==0
    mkdir(save_path);
end
for i=1:numel(tables)
    mode = [];
    for j =1:numel(tables{i})/2
        if tables{i}.Label{j} == "idle"
            mode = [mode;0];
        elseif tables{i}.Label{j} == "walk-stairascent"
            mode = [mode;1];
        elseif tables{i}.Label{j} == "walk-stairdescent"
            mode = [mode;2];
        end
    end
    writeNPY(mode, save_path+string(i)+".npy")
end
end