import numpy as np
import scipy.interpolate as scip


def load_data(data_path, file_list, idx_band_list, kind_id_list, interp_kind='cubic'):
    result_list = []
    num_chosen = 100
    for i in range(len(idx_band_list)):
        if num_chosen >= len(idx_band_list[i]):
            num_chosen = len(idx_band_list[i])
    print("load data in {} and get mean of pre {}".format(data_path, num_chosen))
    for i in range(len(idx_band_list)):
        print("load band {}".format(i))
        idx_in_band_i = idx_band_list[i]
        data_in_band_i_list = np.zeros((1, 100, len(kind_id_list)))
        for j in idx_in_band_i:
            data_in_file_j = np.load(data_path + file_list[j])
            interp_x = np.arange(np.shape(data_in_file_j)[0])
            interp_x = (interp_x - 0) / (interp_x[-1] - 0)
            interp_xx = np.linspace(0, 1, 100)
            data_in_file_j_of_chosen_kinds_collection = []
            for k in kind_id_list:
                data_of_kind_k = data_in_file_j[:, k]
                if k == 0:  # time
                    data_of_kind_k = data_of_kind_k - data_of_kind_k[0]
                else:
                    data_of_kind_k[-1] = data_of_kind_k[0]
                f_k = scip.interp1d(interp_x, data_of_kind_k, kind=interp_kind)
                data_of_kind_k_yy = f_k(interp_xx)
                data_in_file_j_of_chosen_kinds_collection.append(data_of_kind_k_yy)
        data_in_band_i_list = np.vstack([data_in_band_i_list,
                                         (np.array(data_in_file_j_of_chosen_kinds_collection).T).reshape((1, 100, -1))])
        data_in_band_i_list = data_in_band_i_list[1:, :]
        timeend_median = np.median(data_in_band_i_list[:, -1, 0])
        data0_median = np.median(data_in_band_i_list[:, 0, 1:], axis=0)
        mean_of_band_i = np.zeros((100, len(kind_id_list)))
        mean_of_band_i[:, 0] = np.linspace(0, timeend_median, 100)
        mean_of_band_i[:, 1:] = np.mean(
            data_in_band_i_list[0:num_chosen, :, 1:] -
            data_in_band_i_list[0:num_chosen, 0, 1:].reshape((-1, 1, len(kind_id_list)-1)),
            axis=0
        ) + data0_median
        result_list.append(mean_of_band_i)
    result_list = np.array(result_list)
    return result_list
