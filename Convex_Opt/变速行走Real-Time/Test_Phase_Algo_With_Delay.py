import matplotlib.pyplot as plt
import numpy as np
import scipy.io as scio
import Phase_Algo_Velocity_Change


def main():
    mode = 2
    if mode == 0:
        title = 'q_055_speed'
        v = 0.6
    elif mode == 1:
        title = 'q_083_speed'
        v = 0.83
    elif mode == 2:
        title = 'q_110_speed'
        v = 0.8
    elif mode == 3:
        title = 'q_138_speed'
        v = 1.3
    Speedthigh = scio.loadmat('data/Speedthigh_new.mat')
    q_thigh_vec = Speedthigh['q_thigh'][:, mode]
    Speedthigh = np.load('data/VariableSpeed/SpeedThigh.npy')
    q_thigh_vec = Speedthigh[:, mode * 22:(mode + 1) * 22 + 1]
    # q_thigh_vec = q_thigh_vec-q_thigh_vec[0, :]
    q_thigh_vec = np.reshape(q_thigh_vec.T, (len(q_thigh_vec) * len(q_thigh_vec[0]),))
    time_step_num = len(q_thigh_vec)
    acc_vec = np.zeros((time_step_num,))
    phase_desired_vec = np.zeros((time_step_num,))
    for i in range(time_step_num):
        if i % 100 != 0:
            acc_vec[i] = 0
        if i % 101 == 0:
            acc_vec[i] = 20
        phase_desired_vec[i] = i % 101

    start = 260
    length = 100
    q_thigh_vec, time_step_num = add_Delay(q_thigh_vec, time_step_num, start, length)
    acc_vec, time_step_num = add_Delay(acc_vec, time_step_num, start, length)
    phase_desired_vec, time_step_num = add_Delay(phase_desired_vec, time_step_num, start, length)
    phase_vec = np.zeros((time_step_num,))
    time_vec = np.zeros((time_step_num,))
    phase_predictor = Phase_Algo_Velocity_Change.OnlinePhasePredictor()
    state_vec = np.zeros((time_step_num,))
    for i in range(time_step_num):
        print('acc_z:', acc_vec[i])
        acc_z = acc_vec[i]
        q_thigh = q_thigh_vec[i]
        dt = 0.2
        #print(i)
        phase = phase_predictor.phase_predict(q_thigh, acc_z, 10*dt, v)
        #print(phase)
        fifo_mat(phase_vec, phase)
        fifo_mat(time_vec, dt * i)
        print(phase_predictor.state)
        state_vec[i] = phase_predictor.state
    plt.figure()
    plt.subplot(211)
    plt.plot(time_vec, q_thigh_vec)
    plt.plot(time_vec, state_vec*20)
    plt.xlabel('Time')
    plt.ylabel('Thigh_Angle')
    plt.subplot(212)
    plt.plot(time_vec, phase_vec)
    plt.plot(time_vec, phase_desired_vec)
    plt.xlabel('Time')
    plt.ylabel('Phase')
    plt.show()
    np.save('result/variable_actual/{}_phase_desired_delay.npy'.format(title), phase_desired_vec)
    np.save('result/variable_actual/{}_phase_actual_delay.npy'.format(title), phase_vec)


def fifo_mat(data_mat, data_vec):
    data_mat[:-1] = data_mat[1:]
    data_mat[-1] = data_vec
    return data_mat


def add_Delay(thigh_vec, time_step_num, start, length):
    add_thigh = thigh_vec[start] * np.ones((length,))
    thigh_vec_pre = np.append(thigh_vec[0:start], add_thigh)
    thigh_vec = np.append(thigh_vec_pre, thigh_vec[start+1:])
    time_step_num = len(thigh_vec)
    return thigh_vec, time_step_num


if __name__ == '__main__':
    main()
