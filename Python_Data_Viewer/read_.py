import scipy.io as scio

data_path = "E:/Open_Source_Data/Data1/AB06/AB06/10_09_18"
env_ = "levelground"


def load_conditions(data_path, env_):
    file_path = data_path + "/" + env_ + "/conditions/levelground_ccw_fast_01_01.mat"
    conditions = scio.loadmat(file_path)
    print("")


load_conditions(data_path, env_)
