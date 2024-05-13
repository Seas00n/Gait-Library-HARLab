function [phase_vec,x_vec,y_vec] = calculate_phase_based_on_q_dq(thigh_angle)
    thigh_angle_d = zeros(101,1);
    thigh_angle_d(2:end) = -thigh_angle(2:101)+thigh_angle(1:101-1);
    max_d = max(thigh_angle_d);
    min_d = min(thigh_angle_d);
    max_q = max(thigh_angle);
    min_q = min(thigh_angle);
    x_y_ratio = (max_q-min_q)/(max_d-min_d);
    phase_vec = zeros(size(thigh_angle,1),1);
    x_vec = zeros(size(thigh_angle,1),1);
    y_vec = zeros(size(thigh_angle,1),1);
    thigh_angle_all=thigh_angle(1);
    for i=2:size(thigh_angle,1)
        x_vec(i) = thigh_angle(i);
        y_vec(i)=-thigh_angle(i)+thigh_angle(i-1);
        thigh_angle_all = [thigh_angle_all;thigh_angle(i)];
        val = 100*atan2( y_vec(i)*x_y_ratio, x_vec(i) )/2/pi ;
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

