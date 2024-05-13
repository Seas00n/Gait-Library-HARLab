import numpy as np


def init_phase_filter():
    dt = 1
    R = np.array([[0.5, 0], [0, 5]])
    P = 0.1 * R
    Q = np.array([[0, 0], [0, 1e-6]])
    F = np.array([[1, dt], [0, 1]])
    H = np.array([[1, 0], [0, 1]])
    kf = KalmanFilter(P=P, Q=Q, R=R, F=F, H=H, x_0=np.array([0, 1]))
    return kf


class OnlinePhasePredictor(object):
    def __init__(self):
        self.hyper_parameter_popt = np.load('Model_Fitting/parameter_tuning.npy')
        self.hyper_parameters = np.zeros((2, 4))
        self.hyper_parameters[0, 1] = 25
        self.hyper_parameters[0, 2] = -0.1
        self.hyper_parameters[1, 1] = 71
        self.hyper_parameters[1, 2] = 0.17
        self.stance_end_threshold = -40
        self.stance_end_idx = 0
        self.swing_end_threshold = 0
        self.swing_end_idx = 92
        self.q_thigh_buffer = np.zeros(1)
        self.phase_buffer = np.zeros(1)
        self.time_buffer = np.zeros(1)
        self.acc_buffer = np.zeros(1)
        self.phase_vec = np.zeros(2)
        self.q_thigh_0 = 0
        self.gait_start = False
        self.state = 2
        self.acc_foot_threshold = 15
        self.kf = init_phase_filter()
        self.thresholds = np.array([self.stance_end_threshold, self.swing_end_threshold])
        self.v = 1

    def phase_predict(self, q_thigh, acc_z, dt=1, v_measured=1):
        self.acc_buffer = np.append(self.acc_buffer, acc_z)
        if not self.gait_start:
            self.q_thigh_buffer[-1] = q_thigh
        if self.state == 2 and (acc_z > self.acc_foot_threshold or acc_z < -self.acc_foot_threshold):
            self.gait_start = True
            self.update_each_gait_end(v_measured)
        if not self.gait_start:
            return None
        else:
            self.q_thigh_buffer = np.append(self.q_thigh_buffer, q_thigh)
            self.time_buffer = np.append(self.time_buffer, dt)
            if len(self.q_thigh_buffer) > 1:
                self.gait_state_estimation()
                phase = self.q_thigh_to_phase()
                self.phase_vec[:-1] = self.phase_vec[1:]
                self.phase_vec[-1] = phase
                F = np.array([[1, dt], [0, 1]])
                phase = self.kf.forward(np.array([phase, (self.phase_vec[1] - self.phase_vec[0]) / dt]), F)[0]
                phase = np.clip(phase, a_min=np.max(self.phase_buffer), a_max=100)
                self.phase_buffer = np.append(self.phase_buffer, phase)
            else:
                phase = 0
        return phase

    def update_each_gait_end(self, v_):
        if self.state == 1:
            all_clear = False
        elif self.state == 2:
            all_clear = True
        self.state = 0
        # 记录上一个步态周期最后的大腿角度
        self.q_thigh_0 = self.q_thigh_buffer[-1]
        # self.v = Forward_Kinematics_Estimate_V()
        # 清除数据缓存
        self.clear_data_buffer(all_clear)
        # 重新初始化滤波器
        self.kf = init_phase_filter()
        # 记录速度
        self.v = v_
        # 更新超参数
        self.hyper_parameters[0, 0] = self.hyper_parameter_popt[0, 0, 0] * self.v + self.hyper_parameter_popt[
            0, 0, 1]
        self.hyper_parameters[0, 3] = self.hyper_parameter_popt[0, 1, 0] * self.v + self.hyper_parameter_popt[
            0, 1, 1]
        self.hyper_parameters[1, 0] = self.hyper_parameter_popt[1, 0, 0] * self.v + self.hyper_parameter_popt[
            1, 0, 1]
        self.hyper_parameters[1, 3] = self.hyper_parameter_popt[1, 1, 0] * self.v + self.hyper_parameter_popt[
            1, 1, 1]

    def clear_data_buffer(self, all_clear=True):
        if all_clear:
            self.q_thigh_buffer = np.zeros(1)
        else:
            self.q_thigh_buffer = np.ones(1)*self.q_thigh_buffer[-1]
        self.phase_buffer = np.zeros(1)
        self.time_buffer = np.zeros(1)
        self.phase_vec = np.zeros(2)
        self.acc_buffer = np.zeros(1)

    def gait_state_estimation(self):
        q_thigh = self.q_thigh_buffer[-1] - self.q_thigh_0
        if self.state == 0:
            min_thigh_angle = np.min(self.q_thigh_buffer)-self.q_thigh_0
            self.stance_end_threshold = self.hyper_parameters[1, 3]
            #print('q_thigh', q_thigh,
            #      'min_q', min_thigh_angle,
            #      'stance_threshold', self.stance_end_threshold+5)
            if q_thigh < self.stance_end_threshold:
                self.state = 1
                self.stance_end_idx = len(self.q_thigh_buffer)
            if q_thigh > min_thigh_angle + 0.5 and min_thigh_angle < self.stance_end_threshold + 5:
                self.state = 1
                self.stance_end_idx = len(self.q_thigh_buffer)
                #print('Stance_end')
        elif self.state == 1:
            max_thigh_angle = np.max(self.q_thigh_buffer[self.stance_end_idx:])-self.q_thigh_0
            self.swing_end_threshold = 0
            #print('q_thigh', q_thigh,
            #      'max_q', max_thigh_angle,
            #      'swing_threshold', self.swing_end_threshold - 5)
            if q_thigh > self.swing_end_threshold:
                self.state = 2
                self.swing_end_idx = len(self.q_thigh_buffer)
            if q_thigh < max_thigh_angle - 0.2 and max_thigh_angle > self.swing_end_threshold - 5:
                self.state = 2
                self.swing_end_idx = len(self.q_thigh_buffer)
                #print('Swing_end')
            if max(self.acc_buffer) > self.acc_foot_threshold:
                #print('max', max(self.acc_buffer))
                self.state = 1
                self.update_each_gait_end(self.v)

    def q_thigh_to_phase(self):
        if self.state == 2:
            phase_d = self.phase_vec[-1] - self.phase_vec[1]
            phase = self.phase_vec[-1] + phase_d
            phase = np.clip(phase, 92, 100)
        else:
            if self.state == 0:
                x_low = 50
                x_high = 0
            elif self.state == 1:
                x_low = 50
                x_high = 92
            y_low = self.fun_x_to_y(x_low)
            y_high = self.fun_x_to_y(x_high)
            q_thigh = np.clip(self.q_thigh_buffer[-1]-self.q_thigh_0, y_low, y_high)
            phase = self.fun_y_to_x(q_thigh)
            phase = np.clip(phase, min(x_low, x_high), max(x_low, x_high))
        return phase

    def fun_x_to_y(self, x):
        h = self.hyper_parameters[self.state, 0]
        x0 = self.hyper_parameters[self.state, 1]
        k = self.hyper_parameters[self.state, 2]
        b = self.hyper_parameters[self.state, 3]
        y = h / (1 + np.exp(-k * (x - x0))) + b
        return y

    def fun_y_to_x(self, y):
        h = self.hyper_parameters[self.state, 0]
        x0 = self.hyper_parameters[self.state, 1]
        k = self.hyper_parameters[self.state, 2]
        b = self.hyper_parameters[self.state, 3]
        x = x0 - np.log(h / (y - b) - 1) / k
        return x


class KalmanFilter(object):
    """
        Simplified Kalman Filter only deals with the following dynamic model:
        x_k = F_k-1 x_k-1 + w_k
        y_k = H_k x_k + v_k
        """

    def __init__(self, P, Q, R, F, H, x_0):
        '''
        P: covariance matrix of the state, which indicates the uncertainty of the current estimation
        Q: covariance matrix of the process noises w
        R: covariance matrix of the measures noises v
        F: state transition matrix
        H: observation matrix
        '''
        self.P = P
        self.Q = Q
        self.R = R
        self.F = F
        self.H = H
        self.x = x_0

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q  # @ indicates matrix multiplication

    def update(self, y):
        K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
        self.x = self.x + K @ (y - self.H @ self.x)
        I = np.eye(len(self.x))
        self.P = (I - K @ self.H) @ self.P

    def forward(self, y, F):
        self.F = F
        self.predict()
        self.update(y)
        return self.x
