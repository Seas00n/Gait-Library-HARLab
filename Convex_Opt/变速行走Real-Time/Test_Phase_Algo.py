import matplotlib.pyplot as plt
import numpy as np
import scipy.io as scio
import Phase_Algo_Velocity_Change

def main():
    Speedthigh = scio.loadmat('data/Speedthigh_new.mat')
    mode = 2
    if mode == 0:
        title = 'q_low_speed'
        v = 0.55
    elif mode == 1:
        title = 'q_median_speed'
        v = 0.85
    else:
        title = 'q_high_speed'
        v = 1.3
    q_thigh_vec = Speedthigh['q_thigh'][:, mode]
    # 0.8
    # 1.14
    # 1.45
    # q_thigh_vec = q_thigh_vec-q_thigh_vec[0]
    phase_predictor = Phase_Algo_Velocity_Change.OnlinePhasePredictor()
    repeats = 1
    q_thigh_vec = np.tile(q_thigh_vec, repeats)
    time_step_num = np.size(q_thigh_vec)
    phase_vec = np.zeros((time_step_num,))
    phase_desired_vec = np.zeros((time_step_num,))
    time_vec = np.zeros((time_step_num, ))
    acc_z = 1
    for i in range(time_step_num):
        if i % 100 != 0:
            acc_z = 0
        if i % 101 == 0:
            acc_z = 20
        print('acc_z:', acc_z)
        q_thigh = q_thigh_vec[i]
        dt = 0.2
        print(i)
        phase = phase_predictor.phase_predict(q_thigh, acc_z, dt, v)
        print(phase)
        phase_desired = i % 101
        fifo_mat(phase_vec, phase)
        fifo_mat(phase_desired_vec, phase_desired)
        fifo_mat(time_vec, dt*i)
    plt.figure()
    plt.subplot(211)
    plt.plot(time_vec, q_thigh_vec)
    plt.xlabel('Time')
    plt.ylabel('Thigh_Angle')
    plt.subplot(212)
    plt.plot(time_vec, phase_vec)
    plt.plot(time_vec, phase_desired_vec)
    plt.xlabel('Time')
    plt.ylabel('Phase')
    plt.show()
    np.save('result/{}_phase_desired.npy'.format(title), phase_desired_vec)
    np.save('result/{}_phase_actual.npy'.format(title), phase_vec)


def fifo_mat(data_mat, data_vec):
    data_mat[:-1] = data_mat[1:]
    data_mat[-1] = data_vec
    return data_mat

if __name__=='__main__':
    main()