import scipy.io as scio
from utils import *

data_File = "./opensource_speed.mat"

speed_data = scio.loadmat(data_File)

thigh_speed_data = speed_data['thigh_speed']
knee_speed_data = speed_data['knee_speed']
ankle_speed_data = speed_data['ankle_speed']

thigh_speed_data = thigh_speed_data[0::2, 0::2]
phase = np.linspace(1, 100, np.shape(thigh_speed_data)[0])
v_vec = np.linspace(0.01, 1, np.shape(thigh_speed_data)[1])
num_c = 4  # the order of bernstein polynomial
num_popt = 4  # the order of polynomial including x**0=1 e.g. num_popt=4 x**0+x**1+x**2+x**3

c = cvx_phase_data_task_fit(thigh_speed_data,
                            phase,
                            v_vec,
                            num_c,
                            num_popt)

X, Y, Z = coefficient_to_surface(c,
                                 phase,
                                 v_vec,
                                 num_c,
                                 num_popt)
