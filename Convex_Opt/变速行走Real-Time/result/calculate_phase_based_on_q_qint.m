function [phase_vec,x_vec,y_vec] = calculate_phase_based_on_q_qint(thigh_angle)
    thigh_angle_int = zeros(101,1);
    mean_angle = mean(thigh_angle(1:101));
    for i=2:101
        thigh_angle_int(i) = thigh_angle_int(i)+thigh_angle(i)-mean_angle;
        thigh_angle_int(i+1) = thigh_angle_int(i);
    end 
    thigh_angle_int(end) = thigh_angle_int(end-1)+thigh_angle(end);
    max_int = max(thigh_angle_int);
    min_int = min(thigh_angle_int);
    max_q = max(thigh_angle);
    min_q = min(thigh_angle);
    mean_x = 0.5*(max_q+min_q);
    mean_y = 0.5*(max_int+min_int);
    x_y_ratio = (max_q-min_q)/(max_int-min_int);
    phase_vec = zeros(size(thigh_angle,1),1);
    x_vec = zeros(size(thigh_angle,1),1);
    y_vec = zeros(size(thigh_angle,1),1);
    thigh_angle_all=thigh_angle(1);
    for i=2:size(thigh_angle,1)
        x_vec(i) = thigh_angle(i);
        y_vec(i)=thigh_angle(i)-mean_angle+y_vec(i-1);
        thigh_angle_all = [thigh_angle_all;thigh_angle(i)];
        val = 100*atan2( (y_vec(i)-mean_y)*x_y_ratio, (x_vec(i)-mean_x) )/2/pi ;
        period = 100;
        val_list = [val-period,val,val+period];
        dist_vec = abs(val_list-phase_vec(i-1));
        [~,min_dist_idx] = min(dist_vec);
        phase_vec(i) = val_list(min_dist_idx);
    end
    for i=1:size(thigh_angle,1)
        if phase_vec(i)>100
            phase_vec(i) = 100;
        elseif phase_vec(i)<0
            phase_vec(i) = 0;
        end
    end
end