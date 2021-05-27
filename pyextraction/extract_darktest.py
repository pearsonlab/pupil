import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline


def pupil_extract(datafile_input_path,
                  datafile_output_path,
                  datafile_output_path_avg):
    """
    :param datafile_input_path: The path to the data from which DVs will be extracted
    :param datafile_output_path: The path to the output .csv in which DVs will be written
    :param datafile_output_path_avg: The path to the output .csv in which DVs averaged across subjects will be written
    :return: a series of .csv files including all DVs of interest
    """
    df = pd.read_csv(datafile_input_path)
    df.set_index('time')  # index based on time stamp

    # <!-- Initialize dictionary to which all DVs will be added before conversion to dataframe -->
    extracted_dvs = {}

    # <!-- Initialize dictionary to which all averaged DVs will be added before conversion to df -->
    extracted_dvs_avg = {}

    # <!-- Initialize x-value for applying cubic spline -->
    cs_x = np.array(df['time'])

    # <!-- Initialize y-values for applying cubic spline -->
    cs_trial0 = np.array(df['smoothed_trial0'])
    cs_trial1 = np.array(df['smoothed_trial1'])
    cs_trial2 = np.array(df['smoothed_trial2'])

    # <!-- Applying cubic spline -->
    spl_trial0 = CubicSpline(cs_x, cs_trial0)
    spl_trial1 = CubicSpline(cs_x, cs_trial1)
    spl_trial2 = CubicSpline(cs_x, cs_trial2)

    # <!-- 2nd derivative of cubic spline -->
    spl_d2_trial0 = spl_trial0.derivative(nu=2)
    spl_d2_trial1 = spl_trial1.derivative(nu=2)
    spl_d2_trial2 = spl_trial2.derivative(nu=2)

    # <!-- Create dataframe out of the output cubic spline fits -->
    spline_df = pd.DataFrame({'time': cs_x,
                              'trial0_spline': spl_trial0(cs_x),
                              'trial1_spline': spl_trial1(cs_x),
                              'trial2_spline': spl_trial2(cs_x),
                              'trial0_spline_2d': spl_d2_trial0(cs_x),
                              'trial1_spline_2d': spl_d2_trial1(cs_x),
                              'trial2_spline_2d': spl_d2_trial2(cs_x)})

    # ----------------------------------------------------------------- #
    # DV1: D_zero = AVERAGE BASELINE PUPIL DIAMETER (500MS < T-PRE < 0) #
    # ----------------------------------------------------------------- #
    # <!-- Set time range to be -0.5s < t < 0s -->
    D_zero_range = spline_df[
        (spline_df['time'] >= -.5) & (spline_df['time'] <= 0)]  # limit to window of only -.5 <= t <= 0

    # <!-- Calculate average pupil diameter during the 500ms interval preceding the event -->
    D_zero_trial0 = np.nanmean(D_zero_range['trial0_spline'])
    D_zero_trial1 = np.nanmean(D_zero_range['trial1_spline'])
    D_zero_trial2 = np.nanmean(D_zero_range['trial2_spline'])

    extracted_dvs['baseline_pupil_diameter'] = [D_zero_trial0, D_zero_trial1, D_zero_trial2]
    extracted_dvs_avg['baseline_pupil_diameter_avg'] = [np.nanmean([D_zero_trial0, D_zero_trial1, D_zero_trial2])]
    extracted_dvs_avg['baseline_pupil_diameter_std'] = [np.nanstd([D_zero_trial0, D_zero_trial1, D_zero_trial2])]

    # ------------------------------------- #
    # DV2: D_m = MAXIMAL PUPILLARY DILATION #
    # ------------------------------------- #
    # <!-- Set time range to be 0s <= t <= 3s -->
    D_m_range = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= 3)]

    # <!-- Find maximum dilation diameter -->
    D_m_trial0 = D_m_range['trial0_spline'].max()
    D_m_trial1 = D_m_range['trial1_spline'].max()
    D_m_trial2 = D_m_range['trial2_spline'].max()

    extracted_dvs['maximal_pupillary_dilation'] = [D_m_trial0, D_m_trial1, D_m_trial2]
    extracted_dvs_avg['maximal_pupillary_dilation_avg'] = [np.nanmean([D_m_trial0, D_m_trial1, D_m_trial2])]
    extracted_dvs_avg['maximal_pupillary_dilation_std'] = [np.nanstd([D_m_trial0, D_m_trial1, D_m_trial2])]

    # <!-- Find the time at which maximum pupillary dilation occurred -->
    local_max_trial0_x_idx = np.argmax(D_m_range['trial0_spline'])
    local_max_trial0_x = D_m_range['time'].iloc[[local_max_trial0_x_idx]].values[0]
    local_max_trial1_x_idx = np.argmax(D_m_range['trial1_spline'])
    local_max_trial1_x = D_m_range['time'].iloc[[local_max_trial1_x_idx]].values[0]
    local_max_trial2_x_idx = np.argmax(D_m_range['trial2_spline'])
    local_max_trial2_x = D_m_range['time'].iloc[[local_max_trial2_x_idx]].values[0]

    # --------------------------- #
    # DV3: A = DILATION AMPLITUDE #
    # --------------------------- #
    # <!-- Maximum diameter - initial diameter -->
    A_trial0 = D_m_trial0 - D_zero_trial0
    A_trial1 = D_m_trial1 - D_zero_trial1
    A_trial2 = D_m_trial2 - D_zero_trial2

    extracted_dvs['dilation_amplitude'] = [A_trial0, A_trial1, A_trial2]
    extracted_dvs_avg['dilation_amplitude_avg'] = [np.nanmean([A_trial0, A_trial1, A_trial2])]
    extracted_dvs_avg['dilation_amplitude_std'] = [np.nanstd([A_trial0, A_trial1, A_trial2])]

    # ---------------------- #
    # DV4: t_L = PLR LATENCY #
    # ---------------------- #
    # <!-- Set time range to be between 0s and the point of maximum pupillary dilation -->
    t_L_range_trial0 = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= local_max_trial0_x)]
    t_L_range_trial1 = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= local_max_trial1_x)]
    t_L_range_trial2 = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= local_max_trial2_x)]

    # <!-- Find the corresponding time for the highest acceleration in the positive direction (PLR latency) -->
    local_max_d2_trial0_x_idx = np.argmax(t_L_range_trial0['trial0_spline_2d'])
    t_L_trial0 = t_L_range_trial0['time'].iloc[[local_max_d2_trial0_x_idx]].values[0]
    local_max_d2_trial1_x_idx = np.argmax(t_L_range_trial1['trial1_spline_2d'])
    t_L_trial1 = t_L_range_trial1['time'].iloc[[local_max_d2_trial1_x_idx]].values[0]
    local_max_d2_trial2_x_idx = np.argmax(t_L_range_trial2['trial2_spline_2d'])
    t_L_trial2 = t_L_range_trial2['time'].iloc[[local_max_d2_trial2_x_idx]].values[0]

    extracted_dvs['plr_latency'] = [t_L_trial0, t_L_trial1, t_L_trial2]
    extracted_dvs_avg['plr_latency_avg'] = [np.nanmean([t_L_trial0, t_L_trial1, t_L_trial2])]
    extracted_dvs_avg['plr_latency_std'] = [np.nanstd([t_L_trial0, t_L_trial1, t_L_trial2])]

    # ------------------------ #
    # DV5: t_D = DILATION TIME #
    # ------------------------ #
    # <!-- Time at which max dilation occurred minus latency time -->
    t_D_trial0 = local_max_trial0_x - t_L_trial0
    t_D_trial1 = local_max_trial1_x - t_L_trial1
    t_D_trial2 = local_max_trial2_x - t_L_trial2

    extracted_dvs['dilation_time'] = [t_D_trial0, t_D_trial1, t_D_trial2]
    extracted_dvs_avg['dilation_time_avg'] = [np.nanmean([t_D_trial0, t_D_trial1, t_D_trial2])]
    extracted_dvs_avg['dilation_time_std'] = [np.nanstd([t_D_trial0, t_D_trial1, t_D_trial2])]

    # ------------------------ #
    # DV6: t_R = RECOVERY TIME #
    # ------------------------ #
    # <!-- Limit to time range between peak pupil diameter and roughly where it bottoms out -->
    t_R_range_trial0 = spline_df[(spline_df['time'] >= local_max_trial0_x) & (spline_df['time'] <= 3)]
    t_R_range_trial1 = spline_df[(spline_df['time'] >= local_max_trial1_x) & (spline_df['time'] <= 3)]
    t_R_range_trial2 = spline_df[(spline_df['time'] >= local_max_trial2_x) & (spline_df['time'] <= 3)]

    # <!-- Calculate theoretical half maximum pupil dilation diameter -->
    t_R_t2_trial0_y = D_m_trial0 - A_trial0/2
    t_R_t2_trial1_y = D_m_trial1 - A_trial1/2
    t_R_t2_trial2_y = D_m_trial2 - A_trial2/2

    # <!-- Get closest recorded overestimate of the dilation when just under half dilation amplitude -->
    t_R_t2_trial0_y_approx = list(
        filter(lambda timestamp: timestamp < t_R_t2_trial0_y, t_R_range_trial0['trial0_spline']))[0]
    t_R_t2_trial1_y_approx = list(
        filter(lambda timestamp: timestamp < t_R_t2_trial1_y, t_R_range_trial1['trial1_spline']))[0]
    t_R_t2_trial2_y_approx = list(
        filter(lambda timestamp: timestamp < t_R_t2_trial2_y, t_R_range_trial2['trial2_spline']))[0]

    # <!-- Get index of closest overestimate of the time when dilation is half dilation amplitude -->
    t_R_t2_trial0_x_idx = t_R_range_trial0['trial0_spline'].tolist().index(t_R_t2_trial0_y_approx)
    t_R_t2_trial1_x_idx = t_R_range_trial1['trial1_spline'].tolist().index(t_R_t2_trial1_y_approx)
    t_R_t2_trial2_x_idx = t_R_range_trial2['trial2_spline'].tolist().index(t_R_t2_trial2_y_approx)

    # <!-- Plug in the discovered index to find the time at the corresponding list index -->
    t_R_t2_trial0 = t_R_range_trial0['time'].iloc[[t_R_t2_trial0_x_idx]].values[0]
    t_R_t2_trial1 = t_R_range_trial1['time'].iloc[[t_R_t2_trial1_x_idx]].values[0]
    t_R_t2_trial2 = t_R_range_trial2['time'].iloc[[t_R_t2_trial2_x_idx]].values[0]

    # <!-- Find the time difference between the time at which the pupil dilates at half peak dilation (t2)
    # and when it reaches full dilation (t1) -->
    t_R_trial0 = t_R_t2_trial0 - local_max_trial0_x
    t_R_trial1 = t_R_t2_trial1 - local_max_trial1_x
    t_R_trial2 = t_R_t2_trial2 - local_max_trial2_x

    extracted_dvs['recovery_time'] = [t_R_trial0, t_R_trial1, t_R_trial2]
    extracted_dvs_avg['recovery_time_avg'] = [np.nanmean([t_R_trial0, t_R_trial1, t_R_trial2])]
    extracted_dvs_avg['recovery_time_std'] = [np.nanstd([t_R_trial0, t_R_trial1, t_R_trial2])]

    # ---------------------------- #
    # DV7: R_D = RELATIVE DILATION #
    # ---------------------------- #
    # <!-- (Maximum Dilation^2 - Initial^2) / Initial^2 -->
    R_D_trial0 = (D_m_trial0**2 - D_zero_trial0**2)/D_zero_trial0**2
    R_D_trial1 = (D_m_trial1**2 - D_zero_trial1**2)/D_zero_trial1**2
    R_D_trial2 = (D_m_trial2**2 - D_zero_trial2**2)/D_zero_trial2**2

    extracted_dvs['relative_dilation'] = [R_D_trial0, R_D_trial1, R_D_trial2]
    extracted_dvs_avg['relative_dilation_avg'] = [np.nanmean([R_D_trial0, R_D_trial1, R_D_trial2])]
    extracted_dvs_avg['relative_dilation_std'] = [np.nanstd([R_D_trial0, R_D_trial1, R_D_trial2])]

    pd.DataFrame(extracted_dvs).to_csv(datafile_output_path, index=False)
    pd.DataFrame(extracted_dvs_avg).to_csv(datafile_output_path_avg, index=False)


if __name__ == '__main__':
    # bad_data = [3]
    good_data = [1, 4, 11, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42]
    for p_num in good_data:
        p_num = str(p_num)
        if len(p_num) == 1:
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_norm_pupil.csv',
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_norm_dvs.csv',
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_norm_dvs_avg.csv')
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_unnorm_pupil.csv',
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_unnorm_dvs.csv',
                '../pyanalysis/data/CM000' + p_num + '/darktest/CM000' + p_num + '_darktest_unnorm_dvs_avg.csv')
        else:
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_norm_pupil.csv',
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_norm_dvs.csv',
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_norm_dvs_avg.csv')
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_unnorm_pupil.csv',
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_unnorm_dvs.csv',
                '../pyanalysis/data/CM00' + p_num + '/darktest/CM00' + p_num + '_darktest_unnorm_dvs_avg.csv')
