import matplotlib.pyplot as plt
import numpy as np
import scipy.io as scio
import Phase_Algo_Velocity_Change


def main():
    Speedthigh = np.load('data/VariableSpeed/SpeedThigh.npy')
    mode = 0
    if mode == 0:
        title = 'q_055_speed'
        v = 0.6
    elif mode == 1:
        title = 'q_083_speed'
        v = 0.83
    elif mode == 2:
        title = 'q_110_speed'
        v = 1.1
    elif mode == 3:
        title = 'q_138_speed'
        v = 1.3
    q_thigh_vec = Speedthigh[:, mode*22:(mode+1)*22+1]
    q_thigh_vec = q_thigh_vec-q_thigh_vec[0, :]
    time_step_num = len(q_thigh_vec)
    gait_step_num = len(q_thigh_vec[0])
    phase_vec = np.zeros((time_step_num, gait_step_num))
    phase_desired_vec = np.zeros((time_step_num, gait_step_num))
    time_vec = np.zeros((time_step_num, gait_step_num))
    final_state_vec = np.zeros((gait_step_num,))
    for i in range(gait_step_num):
        phase_predictor = Phase_Algo_Velocity_Change.OnlinePhasePredictor()
        for j in range(time_step_num):
            acc_z = 20 if j % 101 == 0 else 0
            q_thigh = q_thigh_vec[j, i]
            dt = 0.2
            phase = phase_predictor.phase_predict(q_thigh, acc_z, dt, v)
            phase_desired = j % 101
            phase_vec[j, i] = phase
            phase_desired_vec[j, i] = phase_desired
            time_vec[j, i] = dt * j
        final_state_vec[i] = phase_predictor.state
        if phase_predictor.state != 2:
            print('i', phase_predictor.state)
            if phase_predictor.state == 0:
                print('Bad')
        else:
            print('OK')
    for i in range(gait_step_num):
        if final_state_vec[i] == 0:
            n = 3
            phase_vec[:, i] = phase_vec[:, n+i]
            print(i)

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
    np.save('result/variable_actual/{}_phase_desired.npy'.format(title), phase_desired_vec)
    np.save('result/variable_actual/{}_phase_actual.npy'.format(title), phase_vec)


def fifo_mat(data_mat, data_vec):
    data_mat[:-1] = data_mat[1:]
    data_mat[-1] = data_vec
    return data_mat


if __name__ == '__main__':
    main()
