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
    :return: a series of .csv files including all 7 DVs of interest
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
    cs_trial2 = np.array(df['smoothed_trial2'])
    cs_trial3 = np.array(df['smoothed_trial3'])

    # <!-- Applying cubic spline -->
    spl_trial2 = CubicSpline(cs_x, cs_trial2)
    spl_trial3 = CubicSpline(cs_x, cs_trial3)

    # <!-- 2nd derivative of cubic spline -->
    spl_d2_trial2 = spl_trial2.derivative(nu=2)
    spl_d2_trial3 = spl_trial3.derivative(nu=2)

    # <!-- Create dataframe out of the output cubic spline fits -->
    spline_df = pd.DataFrame({'time': cs_x,
                              'trial2_spline': spl_trial2(cs_x),
                              'trial3_spline': spl_trial3(cs_x),
                              'trial2_spline_2d': spl_d2_trial2(cs_x),
                              'trial3_spline_2d': spl_d2_trial3(cs_x)})

    # ----------------------------------------------------------------- #
    # DV1: D_zero = AVERAGE BASELINE PUPIL DIAMETER (500MS < T-PRE < 0) #
    # ----------------------------------------------------------------- #
    # <!-- Set time range to be -0.5s <= t <= 0s -->
    D_zero_range = spline_df[
        (spline_df['time'] >= -.5) & (spline_df['time'] <= 0)]

    # <!-- Calculate average pupil diameter during the 500ms interval preceding the event -->
    D_zero_trial2 = np.nanmean(D_zero_range['trial2_spline'])
    D_zero_trial3 = np.nanmean(D_zero_range['trial3_spline'])

    extracted_dvs['baseline_pupil_diameter'] = [D_zero_trial2, D_zero_trial3]
    extracted_dvs_avg['baseline_pupil_diameter_avg'] = [np.nanmean([D_zero_trial2, D_zero_trial3])]
    extracted_dvs_avg['baseline_pupil_diameter_std'] = [np.nanstd([D_zero_trial2, D_zero_trial3])]

    # ----------------------------------------- #
    # DV2: D_m = MAXIMAL PUPILLARY CONSTRICTION #
    # ----------------------------------------- #
    # <!-- Set time range to be 0s <= t <= 3s -->
    D_m_range = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= 3)]

    # <!-- Find minimum dilation diameter -->
    D_m_trial2 = D_m_range['trial2_spline'].min()
    D_m_trial3 = D_m_range['trial3_spline'].min()

    extracted_dvs['maximal_pupillary_constriction'] = [D_m_trial2, D_m_trial3]
    extracted_dvs_avg['maximal_pupillary_constriction_avg'] = [np.nanmean([D_m_trial2, D_m_trial3])]
    extracted_dvs_avg['maximal_pupillary_constriction_std'] = [np.nanstd([D_m_trial2, D_m_trial3])]

    # <!-- Find the time at which maximum pupillary constriction occurred -->
    local_min_trial2_x_idx = np.argmin(D_m_range['trial2_spline'])
    local_min_trial2_x = D_m_range['time'].iloc[[local_min_trial2_x_idx]].values[0]

    local_min_trial3_x_idx = np.argmin(D_m_range['trial3_spline'])
    local_min_trial3_x = D_m_range['time'].iloc[[local_min_trial3_x_idx]].values[0]

    # ------------------------------- #
    # DV3: A = CONSTRICTION AMPLITUDE #
    # ------------------------------- #
    # <!-- Initial diameter - minimum diameter -->
    A_trial2 = D_zero_trial2 - D_m_trial2
    A_trial3 = D_zero_trial3 - D_m_trial3

    extracted_dvs['constriction_amplitude'] = [A_trial2, A_trial3]
    extracted_dvs_avg['constriction_amplitude_avg'] = [np.nanmean([A_trial2, A_trial3])]
    extracted_dvs_avg['constriction_amplitude_std'] = [np.nanstd([A_trial2, A_trial3])]

    # ---------------------- #
    # DV4: t_L = PLR LATENCY #
    # ---------------------- #
    # <!-- Set time range to be between 0s and the point of maximum pupillary constriction -->
    t_L_range_trial2 = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= local_min_trial2_x)]
    t_L_range_trial3 = spline_df[(spline_df['time'] >= 0) & (spline_df['time'] <= local_min_trial3_x)]

    # <!-- Find the corresponding time for the highest acceleration in the negative direction (PLR latency) -->
    local_min_d2_trial2 = np.argmin(t_L_range_trial2['trial2_spline_2d'])
    t_L_trial2 = t_L_range_trial2['time'].iloc[[local_min_d2_trial2]].values[0]

    local_min_d2_trial3 = np.argmin(t_L_range_trial3['trial3_spline_2d'])
    t_L_trial3 = t_L_range_trial3['time'].iloc[[local_min_d2_trial3]].values[0]

    extracted_dvs['plr_latency'] = [t_L_trial2, t_L_trial3]
    extracted_dvs_avg['plr_latency_avg'] = [np.nanmean([t_L_trial2, t_L_trial3])]
    extracted_dvs_avg['plr_latency_std'] = [np.nanstd([t_L_trial2, t_L_trial3])]

    # ---------------------------- #
    # DV5: t_C = CONSTRICTION TIME #
    # ---------------------------- #
    # <!-- Time at which max constriction occurred minus latency time -->
    t_C_trial2 = local_min_trial2_x - t_L_trial2
    t_C_trial3 = local_min_trial3_x - t_L_trial3

    extracted_dvs['constriction_time'] = [t_C_trial2, t_C_trial3]
    extracted_dvs_avg['constriction_time_avg'] = [np.nanmean([t_C_trial2, t_C_trial3])]
    extracted_dvs_avg['constriction_time_std'] = [np.nanstd([t_C_trial2, t_C_trial3])]

    # ------------------------ #
    # DV6: t_R = RECOVERY TIME #
    # ------------------------ #
    # <!-- Limit to time range between peak pupil diameter and roughly where it tops out -->
    t_R_range_trial2 = spline_df[(spline_df['time'] >= local_min_trial2_x) & (spline_df['time'] <= 8)]
    t_R_range_trial3 = spline_df[(spline_df['time'] >= local_min_trial3_x) & (spline_df['time'] <= 8)]

    # <!-- Calculate theoretical half maximum pupil constriction diameter -->
    t_R_t2_trial2_y = D_m_trial2 + A_trial2/2
    t_R_t2_trial3_y = D_m_trial3 + A_trial3/2

    # <!-- Get closest recorded overestimate of the constriction when just over half constriction amplitude -->
    t_R_t2_trial2_y_approx = list(
        filter(lambda timestamp: timestamp > t_R_t2_trial2_y, t_R_range_trial2['trial2_spline']))[0]
    t_R_t2_trial3_y_approx = list(
        filter(lambda timestamp: timestamp > t_R_t2_trial3_y, t_R_range_trial3['trial3_spline']))[0]

    # <!-- Get index of closest overestimate of the time when dilation is half constriction amplitude -->
    t_R_t2_trial2_x_idx = t_R_range_trial2['trial2_spline'].tolist().index(t_R_t2_trial2_y_approx)
    t_R_t2_trial3_x_idx = t_R_range_trial3['trial3_spline'].tolist().index(t_R_t2_trial3_y_approx)

    # <!-- Plug in the discovered index to find the time at the corresponding list index -->
    t_R_t2_trial2 = t_R_range_trial2['time'].iloc[[t_R_t2_trial2_x_idx]].values[0]
    t_R_t2_trial3 = t_R_range_trial3['time'].iloc[[t_R_t2_trial3_x_idx]].values[0]

    # <!-- Find the time difference between the time at which the pupil dilates at half peak constriction (t2)
    # and when it reaches full constriction (t1) -->
    t_R_trial2 = t_R_t2_trial2 - local_min_trial2_x
    t_R_trial3 = t_R_t2_trial3 - local_min_trial3_x

    extracted_dvs['recovery_time'] = [t_R_trial2, t_R_trial3]
    extracted_dvs_avg['recovery_time_avg'] = [np.nanmean([t_R_trial2, t_R_trial3])]
    extracted_dvs_avg['recovery_time_std'] = [np.nanstd([t_R_trial2, t_R_trial3])]

    # -------------------------------- #
    # DV7: R_C = RELATIVE CONSTRICTION #
    # -------------------------------- #
    # <!-- (Initial^2 - Maximum Constriction^2) / Initial^2 -->
    R_C_trial2 = (D_zero_trial2**2 - D_m_trial2**2)/D_zero_trial2**2
    R_C_trial3 = (D_zero_trial3**2 - D_m_trial3**2)/D_zero_trial3**2

    extracted_dvs['relative_constriction'] = [R_C_trial2, R_C_trial3]
    extracted_dvs_avg['relative_constriction_avg'] = [np.nanmean([R_C_trial2, R_C_trial3])]
    extracted_dvs_avg['relative_constriction_std'] = [np.nanstd([R_C_trial2, R_C_trial3])]

    pd.DataFrame(extracted_dvs).to_csv(datafile_output_path, index=False)
    pd.DataFrame(extracted_dvs_avg).to_csv(datafile_output_path_avg, index=False)


if __name__ == '__main__':
    # bad_data = [1, 3, 29] -> 1 (trial 1 is is only good one), 3 (trial 1 is bad), 29 (trial 2, 3 are good enough)
    pupil_extract(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_norm_pupil.csv',
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_norm_dvs.csv',
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_norm_dvs_avg.csv')
    pupil_extract(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_unnorm_pupil.csv',
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_unnorm_dvs.csv',
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_unnorm_dvs_avg.csv')
