function [q_knee,q_ankle] = surface_fitting(phase,v)
    num_c = 4;
    num_popt = 7;
    x_knee = readNPY('..\Model_Fitting\knee_beta.npy');
    x_ankle = readNPY('..\Model_Fitting\ankle_beta.npy');
    q_knee = zeros(101,1);
    q_ankle = zeros(101,1);
    for j=1:101
        vj = v;
        si = phase(j);
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
        q_knee(j) = delta_mat*x_knee;
        q_ankle(j) = delta_mat*x_ankle;
    end
end
