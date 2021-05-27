# preparatory work
import utils
import pandas as pd
import numpy as np

# set up plotting
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter

# make plots pretty
sns.set_style('darkgrid')
sns.set_context('talk', font_scale=1.4)
sns.set_palette("Reds_r")


def pupil_analysis(datafile_path,
                   norm_pupil_path,
                   unnorm_pupil_path,
                   norm_pupil_fig_path,
                   on_off_path):
    """
    :param datafile_path:
    :param norm_pupil_path:
    :param unnorm_pupil_path:
    :param mean_pupil_path:
    :param norm_pupil_fig_path:
    :param mean_pupil_fig_path:
    :param on_off_path:
    :return:
    """
    df = pd.read_csv(datafile_path, sep='\t')  # load .tsv into dataframe
    df = utils.prepdata(df)  # run preparations

    # 'offtimes' are the times that the screen went off in sec
    # strings specify which columns to grab and convert
    df = utils.timestamp_to_seconds(df, 'ontime', 'ontimes')
    df = utils.timestamp_to_seconds(df, 'offtime', 'offtimes')

    # the screen went on at different times that we need to specify for plotting
    # These are the first, second, and third times, respectively (in seconds)
    first_ontime = df['ontimes'].to_list()[0]
    second_ontime = df['ontimes'].to_list()[1]
    third_ontime = df['ontimes'].to_list()[2]
    fourth_ontime = df['ontimes'].to_list()[3]

    # the screen went off at different times that we need to specify for plotting
    # These are the first, second, and third times, respectively (in seconds)
    first_offtime = df['offtimes'].to_list()[0]
    second_offtime = df['offtimes'].to_list()[1]
    third_offtime = df['offtimes'].to_list()[2]
    fourth_offtime = df['offtimes'].to_list()[3]

    # PARAMETERS
    tpre = -0.6
    tpost = 8

    chunklist, idx = utils.evtsplit(df, df['ontimes'], tpre, tpost)
    norm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[0]
    unnorm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[1]

    norm_pupil = norm_data[idx.get_loc('MeanPupil')]
    unnorm_pupil = unnorm_data[idx.get_loc('MeanPupil')]

    # Applies S-G (M=55, k=2) filter to the data from each normed trial
    # Adds new column with smoothed data for each normed trial
    norm_smoothed_trial0 = savgol_filter(norm_pupil.iloc[:, 0], 55, 2)
    norm_smoothed_trial1 = savgol_filter(norm_pupil.iloc[:, 1], 55, 2)
    norm_smoothed_trial2 = savgol_filter(norm_pupil.iloc[:, 2], 55, 2)
    norm_smoothed_trial3 = savgol_filter(norm_pupil.iloc[:, 3], 55, 2)
    norm_pupil['smoothed_trial0'] = norm_smoothed_trial0
    norm_pupil['smoothed_trial1'] = norm_smoothed_trial1
    norm_pupil['smoothed_trial2'] = norm_smoothed_trial2
    norm_pupil['smoothed_trial3'] = norm_smoothed_trial3

    # Finds mean and SD of smoothed data across all normed trials
    # Adds new columns for mean and SD for this participant's normed data
    norm_smoothed_all = norm_pupil.loc[:, 'smoothed_trial0':]
    norm_pupil['smoothed_avg'] = np.nanmean(norm_smoothed_all, 1)
    norm_pupil['smoothed_std'] = np.nanstd(norm_smoothed_all, 1)

    # Applies S-G (M=55, k=2) filter to the data from each unnormed trial
    # Adds new column with smoothed data for each unnormed trial
    unnorm_smoothed_trial0 = savgol_filter(unnorm_pupil.iloc[:, 0], 55, 2)
    unnorm_smoothed_trial1 = savgol_filter(unnorm_pupil.iloc[:, 1], 55, 2)
    unnorm_smoothed_trial2 = savgol_filter(unnorm_pupil.iloc[:, 2], 55, 2)
    unnorm_smoothed_trial3 = savgol_filter(unnorm_pupil.iloc[:, 3], 55, 2)
    unnorm_pupil['smoothed_trial0'] = unnorm_smoothed_trial0
    unnorm_pupil['smoothed_trial1'] = unnorm_smoothed_trial1
    unnorm_pupil['smoothed_trial2'] = unnorm_smoothed_trial2
    unnorm_pupil['smoothed_trial3'] = unnorm_smoothed_trial3

    # Finds mean and SD of smoothed data across all unnormed trials
    # Adds new columns for mean and SD for this participant's unnormed data
    unnorm_smoothed_all = unnorm_pupil.loc[:, 'smoothed_trial0':]
    unnorm_pupil['smoothed_avg'] = np.nanmean(unnorm_smoothed_all, 1)
    unnorm_pupil['smoothed_std'] = np.nanstd(unnorm_smoothed_all, 1)

    # Writes the event time data to a .csv
    on_off = pd.DataFrame({
        'onset_times': [first_ontime, second_ontime, third_ontime, fourth_ontime],
        'offset_times': [first_offtime, second_offtime, third_offtime, fourth_offtime]
    })
    on_off.to_csv(on_off_path, index=False)

    # Rename column headers for the normed data and write to a .csv
    norm_pupil = pd.DataFrame(norm_pupil).rename(columns={0: 'unsmoothed_trial0',
                                                          1: 'unsmoothed_trial1',
                                                          2: 'unsmoothed_trial2',
                                                          3: 'unsmoothed_trial3'})
    norm_pupil.to_csv(norm_pupil_path)

    # Rename column headers for the unnormed data and write to a .csv
    unnorm_pupil = pd.DataFrame(unnorm_pupil).rename(columns={0: 'unsmoothed_trial0',
                                                              1: 'unsmoothed_trial1',
                                                              2: 'unsmoothed_trial2',
                                                              3: 'unsmoothed_trial3'})
    unnorm_pupil.to_csv(unnorm_pupil_path)

    # Plotting data
    plt.figure(figsize=(10, 6))
    plt.plot(norm_pupil.index, norm_pupil.iloc[:, 4:8]);
    plt.xlim([tpre, tpost])
    plt.title('Pupillary Light Reflex');
    plt.ylabel('Normalized pupil size (arbitrary units)');
    plt.xlabel('Time from flash (s)');
    plt.legend(['1.00', '.75', '.50', '0.25'], title='Fraction full\nintensity',
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    plt.gca().get_legend().get_title().set_fontsize('14');
    plt.savefig(norm_pupil_fig_path, bbox_inches='tight');
    plt.cla()
    plt.close()


if __name__ == '__main__':

    # Participant 1: Trial 1 Usable
    pupil_analysis('data/CM0001/lighttest/lighttest11_30_15on04-06-2016.tsv',
                   'data/CM0001/lighttest/CM0001_lighttest_norm_pupil.csv',
                   'data/CM0001/lighttest/CM0001_lighttest_unnorm_pupil.csv',
                   'data/CM0001/lighttest/CM0001_lighttest_norm_pupil_fig.png',
                   'data/CM0001/lighttest/CM0001_on_off.csv')

    # Participant 3: Trials 0, 2, 3 Usable
    pupil_analysis('data/CM0003/lighttest/lighttest15_13_40on04-26-2016.tsv',
                   'data/CM0003/lighttest/CM0003_lighttest_norm_pupil.csv',
                   'data/CM0003/lighttest/CM0003_lighttest_unnorm_pupil.csv',
                   'data/CM0003/lighttest/CM0003_lighttest_norm_pupil_fig.png',
                   'data/CM0003/lighttest/CM0003_on_off.csv')

    # Participant 4: Great
    pupil_analysis('data/CM0004/lighttest/lighttest14_28_18on04-14-2016.tsv',
                   'data/CM0004/lighttest/CM0004_lighttest_norm_pupil.csv',
                   'data/CM0004/lighttest/CM0004_lighttest_unnorm_pupil.csv',
                   'data/CM0004/lighttest/CM0004_lighttest_norm_pupil_fig.png',
                   'data/CM0004/lighttest/CM0004_on_off.csv')

    # Participant 11: Great
    pupil_analysis('data/CM0011/lighttest/lighttest15_52_02on04-20-2016.tsv',
                   'data/CM0011/lighttest/CM0011_lighttest_norm_pupil.csv',
                   'data/CM0011/lighttest/CM0011_lighttest_unnorm_pupil.csv',
                   'data/CM0011/lighttest/CM0011_lighttest_norm_pupil_fig.png',
                   'data/CM0011/lighttest/CM0011_on_off.csv')

    # Participant 14: Great
    pupil_analysis('data/CM0014/lighttest/lighttest15_06_41on04-11-2016.tsv',
                   'data/CM0014/lighttest/CM0014_lighttest_norm_pupil.csv',
                   'data/CM0014/lighttest/CM0014_lighttest_unnorm_pupil.csv',
                   'data/CM0014/lighttest/CM0014_lighttest_norm_pupil_fig.png',
                   'data/CM0014/lighttest/CM0014_on_off.csv')

    # Participant 15: Good
    pupil_analysis('data/CM0015/lighttest/lighttest19_03_59on04-12-2016.tsv',
                   'data/CM0015/lighttest/CM0015_lighttest_norm_pupil.csv',
                   'data/CM0015/lighttest/CM0015_lighttest_unnorm_pupil.csv',
                   'data/CM0015/lighttest/CM0015_lighttest_norm_pupil_fig.png',
                   'data/CM0015/lighttest/CM0015_on_off.csv')

    # Participant 16: Great
    pupil_analysis('data/CM0016/lighttest/lighttest17_06_45on04-14-2016.tsv',
                   'data/CM0016/lighttest/CM0016_lighttest_norm_pupil.csv',
                   'data/CM0016/lighttest/CM0016_lighttest_unnorm_pupil.csv',
                   'data/CM0016/lighttest/CM0016_lighttest_norm_pupil_fig.png',
                   'data/CM0016/lighttest/CM0016_on_off.csv')

    # Participant 19: Great
    pupil_analysis('data/CM0019/lighttest/lighttest11_18_51on04-01-2016.tsv',
                   'data/CM0019/lighttest/CM0019_lighttest_norm_pupil.csv',
                   'data/CM0019/lighttest/CM0019_lighttest_unnorm_pupil.csv',
                   'data/CM0019/lighttest/CM0019_lighttest_norm_pupil_fig.png',
                   'data/CM0019/lighttest/CM0019_on_off.csv')

    # Participant 20: Great
    pupil_analysis('data/CM0020/lighttest/lighttest12_30_01on04-20-2016.tsv',
                   'data/CM0020/lighttest/CM0020_lighttest_norm_pupil.csv',
                   'data/CM0020/lighttest/CM0020_lighttest_unnorm_pupil.csv',
                   'data/CM0020/lighttest/CM0020_lighttest_norm_pupil_fig.png',
                   'data/CM0020/lighttest/CM0020_on_off.csv')

    # Participant 21: Great
    pupil_analysis('data/CM0021/lighttest/lighttest10_44_48on04-30-2016.tsv',
                   'data/CM0021/lighttest/CM0021_lighttest_norm_pupil.csv',
                   'data/CM0021/lighttest/CM0021_lighttest_unnorm_pupil.csv',
                   'data/CM0021/lighttest/CM0021_lighttest_norm_pupil_fig.png',
                   'data/CM0021/lighttest/CM0021_on_off.csv')

    # Participant 22: Usable
    pupil_analysis('data/CM0022/lighttest/lighttest14_52_03on04-19-2016.tsv',
                   'data/CM0022/lighttest/CM0022_lighttest_norm_pupil.csv',
                   'data/CM0022/lighttest/CM0022_lighttest_unnorm_pupil.csv',
                   'data/CM0022/lighttest/CM0022_lighttest_norm_pupil_fig.png',
                   'data/CM0022/lighttest/CM0022_on_off.csv')

    # Participant 24: Great
    pupil_analysis('data/CM0024/lighttest/lighttest13_17_23on04-13-2016.tsv',
                   'data/CM0024/lighttest/CM0024_lighttest_norm_pupil.csv',
                   'data/CM0024/lighttest/CM0024_lighttest_unnorm_pupil.csv',
                   'data/CM0024/lighttest/CM0024_lighttest_norm_pupil_fig.png',
                   'data/CM0024/lighttest/CM0024_on_off.csv')

    # Participant 25: Great
    pupil_analysis('data/CM0025/lighttest/lighttest13_59_45on04-04-2016.tsv',
                   'data/CM0025/lighttest/CM0025_lighttest_norm_pupil.csv',
                   'data/CM0025/lighttest/CM0025_lighttest_unnorm_pupil.csv',
                   'data/CM0025/lighttest/CM0025_lighttest_norm_pupil_fig.png',
                   'data/CM0025/lighttest/CM0025_on_off.csv')

    # Participant 26: Great
    pupil_analysis('data/CM0026/lighttest/lighttest14_02_44on04-01-2016.tsv',
                   'data/CM0026/lighttest/CM0026_lighttest_norm_pupil.csv',
                   'data/CM0026/lighttest/CM0026_lighttest_unnorm_pupil.csv',
                   'data/CM0026/lighttest/CM0026_lighttest_norm_pupil_fig.png',
                   'data/CM0026/lighttest/CM0026_on_off.csv')

    # Participant 29: Trials 2, 3 Usable
    pupil_analysis('data/CM0029/lighttest/lighttest13_53_37on04-22-2016.tsv',
                   'data/CM0029/lighttest/CM0029_lighttest_norm_pupil.csv',
                   'data/CM0029/lighttest/CM0029_lighttest_unnorm_pupil.csv',
                   'data/CM0029/lighttest/CM0029_lighttest_norm_pupil_fig.png',
                   'data/CM0029/lighttest/CM0029_on_off.csv')

    # # Participant 30: Unusable
    # pupil_analysis('data/CM0030/lighttest/lighttest13_59_13on04-29-2016.tsv',
    #                'data/CM0030/lighttest/CM0030_lighttest_norm_pupil.csv',
    #                'data/CM0030/lighttest/CM0030_lighttest_unnorm_pupil.csv',
    #                'data/CM0030/lighttest/CM0030_lighttest_norm_pupil_fig.png',
    #                'data/CM0030/lighttest/CM0030_on_off.csv')

    # Participant 31: Great
    pupil_analysis('data/CM0031/lighttest/lighttest13_35_33on04-21-2016.tsv',
                   'data/CM0031/lighttest/CM0031_lighttest_norm_pupil.csv',
                   'data/CM0031/lighttest/CM0031_lighttest_unnorm_pupil.csv',
                   'data/CM0031/lighttest/CM0031_lighttest_norm_pupil_fig.png',
                   'data/CM0031/lighttest/CM0031_on_off.csv')

    # # Participant 32: Unusable
    # pupil_analysis('data/CM0032/lighttest/lighttest11_57_43on04-12-2016.tsv',
    #                'data/CM0032/lighttest/CM0032_lighttest_norm_pupil.csv',
    #                'data/CM0032/lighttest/CM0032_lighttest_unnorm_pupil.csv',
    #                'data/CM0032/lighttest/CM0032_lighttest_norm_pupil_fig.png',
    #                'data/CM0032/lighttest/CM0032_on_off.csv')

    # Participant 33: Great
    pupil_analysis('data/CM0033/lighttest/lighttest10_32_06on04-29-2016.tsv',
                   'data/CM0033/lighttest/CM0033_lighttest_norm_pupil.csv',
                   'data/CM0033/lighttest/CM0033_lighttest_unnorm_pupil.csv',
                   'data/CM0033/lighttest/CM0033_lighttest_norm_pupil_fig.png',
                   'data/CM0033/lighttest/CM0033_on_off.csv')

    # Participant 34: Great
    pupil_analysis('data/CM0034/lighttest/lighttest10_26_41on04-13-2016.tsv',
                   'data/CM0034/lighttest/CM0034_lighttest_norm_pupil.csv',
                   'data/CM0034/lighttest/CM0034_lighttest_unnorm_pupil.csv',
                   'data/CM0034/lighttest/CM0034_lighttest_norm_pupil_fig.png',
                   'data/CM0034/lighttest/CM0034_on_off.csv')

    # Participant 35: Good
    pupil_analysis('data/CM0035/lighttest/lighttest11_15_41on04-19-2016.tsv',
                   'data/CM0035/lighttest/CM0035_lighttest_norm_pupil.csv',
                   'data/CM0035/lighttest/CM0035_lighttest_unnorm_pupil.csv',
                   'data/CM0035/lighttest/CM0035_lighttest_norm_pupil_fig.png',
                   'data/CM0035/lighttest/CM0035_on_off.csv')

    # Participant 36: Great
    pupil_analysis('data/CM0036/lighttest/lighttest15_40_21on04-13-2016.tsv',
                   'data/CM0036/lighttest/CM0036_lighttest_norm_pupil.csv',
                   'data/CM0036/lighttest/CM0036_lighttest_unnorm_pupil.csv',
                   'data/CM0036/lighttest/CM0036_lighttest_norm_pupil_fig.png',
                   'data/CM0036/lighttest/CM0036_on_off.csv')

    # Participant 40: Great
    pupil_analysis('data/CM0040/lighttest/lighttest12_42_31on04-24-2016.tsv',
                   'data/CM0040/lighttest/CM0040_lighttest_norm_pupil.csv',
                   'data/CM0040/lighttest/CM0040_lighttest_unnorm_pupil.csv',
                   'data/CM0040/lighttest/CM0040_lighttest_norm_pupil_fig.png',
                   'data/CM0040/lighttest/CM0040_on_off.csv')

    # Participant 41: Great
    pupil_analysis('data/CM0041/lighttest/lighttest16_51_31on04-28-2016.tsv',
                   'data/CM0041/lighttest/CM0041_lighttest_norm_pupil.csv',
                   'data/CM0041/lighttest/CM0041_lighttest_unnorm_pupil.csv',
                   'data/CM0041/lighttest/CM0041_lighttest_norm_pupil_fig.png',
                   'data/CM0041/lighttest/CM0041_on_off.csv')

    # Participant 42: Good
    pupil_analysis('data/CM0042/lighttest/lighttest15_28_25on04-29-2016.tsv',
                   'data/CM0042/lighttest/CM0042_lighttest_norm_pupil.csv',
                   'data/CM0042/lighttest/CM0042_lighttest_unnorm_pupil.csv',
                   'data/CM0042/lighttest/CM0042_lighttest_norm_pupil_fig.png',
                   'data/CM0042/lighttest/CM0042_on_off.csv')
