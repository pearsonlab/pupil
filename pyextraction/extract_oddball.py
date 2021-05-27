import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline


def pupil_extract(datafile_input_path, datafile_output_path):
    """
    :param datafile_input_path: The path to the data from which DVs will be extracted
    :param datafile_output_path: The path to the output .csv in which DVs will be written
    :return: a series of .csv files including all 4 DVs of interest
    """
    df = pd.read_csv(datafile_input_path)
    df.set_index('time')  # index based on time stamp

    # <!-- Initialize dictionary to which all DVs will be added before conversion to dataframe -->
    extracted_dvs = {}

    # <!-- Initialize x-value for applying cubic spline -->
    cs_x = np.array(df['time'])

    oddball_spl = pd.DataFrame(df['time'])
    oddball_spl.set_index('time')
    for colhead, colseries in df.iteritems():
        if str(colhead[-1]) == 'd':
            cs_y = np.array(df[colhead])
            spl = CubicSpline(cs_x, cs_y)
            oddball_spl[str(colhead) + '_spl'] = spl(cs_x)

    # ----------------------------------------------------------------- #
    # DV1: D_zero = AVERAGE BASELINE PUPIL DIAMETER (500MS < T-PRE < 0) #
    # ----------------------------------------------------------------- #
    # <!-- Set time range to be -0.5s <= t <= 0s -->
    D_zero_range = oddball_spl[
        (oddball_spl['time'] >= -.5) & (oddball_spl['time'] <= 0)]

    D_zero_alltrials = []
    for colhead, colseries in D_zero_range.iteritems():
        D_zero_alltrials.append(np.nanmean(D_zero_range[colhead]))
    extracted_dvs['baseline_pupil_diameter_avg'] = [np.nanmean(D_zero_alltrials)]
    extracted_dvs['baseline_pupil_diameter_stdev'] = [np.nanstd(D_zero_alltrials)]

    # ------------------------------------- #
    # DV2: D_m = MAXIMAL PUPILLARY DILATION #
    # ------------------------------------- #
    D_m_alltrials = []
    for colhead, colseries in oddball_spl.iteritems():
        D_m_alltrials.append(oddball_spl[colhead].max())
    extracted_dvs['maximal_pupillary_dilation_avg'] = [np.nanmean(D_m_alltrials)]
    extracted_dvs['maximal_pupillary_dilation_stdev'] = [np.nanstd(D_m_alltrials)]

    # --------------------------- #
    # DV3: A = DILATION AMPLITUDE #
    # --------------------------- #
    A_alltrials = []
    for idx in range(len(D_m_alltrials)):
        A_alltrials.append(D_m_alltrials[idx] - D_zero_alltrials[idx])
    extracted_dvs['dilation_amplitude_avg'] = [np.nanmean(A_alltrials)]
    extracted_dvs['dilation_amplitude_stdev'] = [np.nanstd(A_alltrials)]

    # ---------------------------- #
    # DV4: R_D = RELATIVE DILATION #
    # ---------------------------- #
    R_D_alltrials = []
    for idx in range(len(D_m_alltrials)):
        R_D_alltrials.append((D_m_alltrials[idx]**2 - D_zero_alltrials[idx]**2)/D_zero_alltrials[idx]**2)
    extracted_dvs['relative_dilation_avg'] = [np.nanmean(R_D_alltrials)]
    extracted_dvs['relative_dilation_stdev'] = [np.nanstd(R_D_alltrials)]

    pd.DataFrame(extracted_dvs).to_csv(datafile_output_path, index=False)


if __name__ == '__main__':
    # unusable_data = [16]
    # usable = [22, 29, 31, 32]
    # std_exceed_odd = [31, 33]
    good_data = [1, 3, 4, 11, 14, 15, 19, 20, 21, 22, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42]
    for p_num in good_data:
        p_num = str(p_num)
        if len(p_num) == 1:
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_pupil_std.csv',
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_std_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_pupil_std.csv',
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_std_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_pupil_odd.csv',
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_odd_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_pupil_odd.csv',
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_odd_dvs.csv')
        else:
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_pupil_std.csv',
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_std_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_pupil_std.csv',
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_std_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_pupil_odd.csv',
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_odd_dvs.csv')
            pupil_extract(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_pupil_odd.csv',
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_odd_dvs.csv')
