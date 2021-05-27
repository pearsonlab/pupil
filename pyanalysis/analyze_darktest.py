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
sns.set_palette("Set2")


def pupil_analysis(datafile_path,
                   norm_pupil_path,
                   unnorm_pupil_path,
                   mean_pupil_path,
                   norm_pupil_fig_path,
                   mean_pupil_fig_path,
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

    # the screen went off at different times that we need to specify for plotting
    # These are the first, second, and third times, respectively (in seconds)
    first_offtime = df['offtimes'].to_list()[0]
    second_offtime = df['offtimes'].to_list()[1]
    third_offtime = df['offtimes'].to_list()[2]

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
    norm_pupil['smoothed_trial0'] = norm_smoothed_trial0
    norm_pupil['smoothed_trial1'] = norm_smoothed_trial1
    norm_pupil['smoothed_trial2'] = norm_smoothed_trial2

    # Finds mean and SD of smoothed data across all normed trials
    # Adds new columns for mean and SD for this participant's normed data
    norm_smoothed_all = norm_pupil.loc[:, 'smoothed_trial0':]
    norm_pupil['smoothed_avg'] = np.nanmean(norm_smoothed_all, 1)
    norm_pupil['smoothed_std'] = np.nanstd(norm_smoothed_all, 1)

    # Applies S-G filter to the data from each unnormed trial
    # Adds new column with smoothed data for each unnormed trial
    unnorm_smoothed_trial0 = savgol_filter(unnorm_pupil.iloc[:, 0], 55, 2)
    unnorm_smoothed_trial1 = savgol_filter(unnorm_pupil.iloc[:, 1], 55, 2)
    unnorm_smoothed_trial2 = savgol_filter(unnorm_pupil.iloc[:, 2], 55, 2)
    unnorm_pupil['smoothed_trial0'] = unnorm_smoothed_trial0
    unnorm_pupil['smoothed_trial1'] = unnorm_smoothed_trial1
    unnorm_pupil['smoothed_trial2'] = unnorm_smoothed_trial2

    # Finds mean and SD of smoothed data across all unnormed trials
    # Adds new columns for mean and SD for this participant's unnormed data
    unnorm_smoothed_all = unnorm_pupil.loc[:, 'smoothed_trial0':]
    unnorm_pupil['smoothed_avg'] = np.nanmean(unnorm_smoothed_all, 1)
    unnorm_pupil['smoothed_std'] = np.nanstd(unnorm_smoothed_all, 1)

    # Writes the event time data to a .csv
    on_off = pd.DataFrame({
        'onset_times': [first_ontime, second_ontime, third_ontime],
        'offset_times': [first_offtime, second_offtime, third_offtime]
    })
    on_off.to_csv(on_off_path, index=False)  # Write stimulus onset/offset time to .csv

    # Rename column headers for the normed data and write to a .csv
    norm_pupil = pd.DataFrame(norm_pupil).rename(columns={0: 'unsmoothed_trial0',
                                                          1: 'unsmoothed_trial1',
                                                          2: 'unsmoothed_trial2'})
    norm_pupil.to_csv(norm_pupil_path)

    # Rename column headers for the unnormed data and write to a .csv
    unnorm_pupil = pd.DataFrame(unnorm_pupil).rename(columns={0: 'unsmoothed_trial0',
                                                              1: 'unsmoothed_trial1',
                                                              2: 'unsmoothed_trial2'})
    unnorm_pupil.to_csv(unnorm_pupil_path)

    # Write mean pupil data to .csv
    pd.DataFrame(df['MeanPupil']).to_csv(mean_pupil_path)

    # Plotting data
    plt.figure(figsize=(10, 6))
    plt.plot(norm_pupil.index, norm_pupil.loc[:, 'smoothed_trial0':'smoothed_trial2']);
    plt.xlim([tpre, tpost])
    plt.title('Pupillary Dark Reflex');
    plt.ylabel('Normalized pupil size (arbitrary units)');
    plt.xlabel('Time from blank (s)');
    plt.savefig(norm_pupil_fig_path, bbox_inches='tight');
    plt.close("all")

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['MeanPupil']);
    plt.ylim([0, 5])
    plt.plot((first_ontime, first_ontime), (0, 5), 'darkgreen', zorder=1, alpha=0.25)
    plt.plot((second_ontime, second_ontime), (0, 5), 'darkgreen', zorder=1, alpha=0.25)
    plt.plot((third_ontime, third_ontime), (0, 5), 'darkgreen', zorder=1, alpha=0.25)
    plt.plot((first_offtime, first_offtime), (0, 5), 'darkred', zorder=1, alpha=0.25)
    plt.plot((second_offtime, second_offtime), (0, 5), 'darkred', zorder=1, alpha=0.25)
    plt.plot((third_offtime, third_offtime), (0, 5), 'darkred', zorder=1, alpha=0.25)
    plt.title('Full Trial with Events Marked');
    plt.ylabel('Pupil size (mm)');
    plt.xlabel('Trial time (s)');
    plt.savefig(mean_pupil_fig_path, bbox_inches='tight');
    plt.close("all")


if __name__ == '__main__':

    # Participant 1: Great
    pupil_analysis('data/CM0001/darktest/darktest11_29_17on04-06-2016.tsv',
                   'data/CM0001/darktest/CM0001_darktest_norm_pupil.csv',
                   'data/CM0001/darktest/CM0001_darktest_unnorm_pupil.csv',
                   'data/CM0001/darktest/CM0001_darktest_mean_pupil.csv',
                   'data/CM0001/darktest/CM0001_darktest_norm_pupil_fig.png',
                   'data/CM0001/darktest/CM0001_darktest_mean_pupil_fig.png',
                   'data/CM0001/darktest/CM0001_on_off.csv')

    # Participant 3: Unusable
    pupil_analysis('data/CM0003/darktest/darktest15_12_40on04-26-2016.tsv',
                   'data/CM0003/darktest/CM0003_darktest_norm_pupil.csv',
                   'data/CM0003/darktest/CM0003_darktest_unnorm_pupil.csv',
                   'data/CM0003/darktest/CM0003_darktest_mean_pupil.csv',
                   'data/CM0003/darktest/CM0003_darktest_norm_pupil_fig.png',
                   'data/CM0003/darktest/CM0003_darktest_mean_pupil_fig.png',
                   'data/CM0003/darktest/CM0003_on_off.csv')

    # Participant 4: Great
    pupil_analysis('data/CM0004/darktest/darktest14_27_24on04-14-2016.tsv',
                   'data/CM0004/darktest/CM0004_darktest_norm_pupil.csv',
                   'data/CM0004/darktest/CM0004_darktest_unnorm_pupil.csv',
                   'data/CM0004/darktest/CM0004_darktest_mean_pupil.csv',
                   'data/CM0004/darktest/CM0004_darktest_norm_pupil_fig.png',
                   'data/CM0004/darktest/CM0004_darktest_mean_pupil_fig.png',
                   'data/CM0004/darktest/CM0004_on_off.csv')

    # Participant 11: Great
    pupil_analysis('data/CM0011/darktest/darktest15_50_24on04-20-2016.tsv',
                   'data/CM0011/darktest/CM0011_darktest_norm_pupil.csv',
                   'data/CM0011/darktest/CM0011_darktest_unnorm_pupil.csv',
                   'data/CM0011/darktest/CM0011_darktest_mean_pupil.csv',
                   'data/CM0011/darktest/CM0011_darktest_norm_pupil_fig.png',
                   'data/CM0011/darktest/CM0011_darktest_mean_pupil_fig.png',
                   'data/CM0011/darktest/CM0011_on_off.csv')

    # Participant 14: Great
    pupil_analysis('data/CM0014/darktest/darktest15_05_45on04-11-2016.tsv',
                   'data/CM0014/darktest/CM0014_darktest_norm_pupil.csv',
                   'data/CM0014/darktest/CM0014_darktest_unnorm_pupil.csv',
                   'data/CM0014/darktest/CM0014_darktest_mean_pupil.csv',
                   'data/CM0014/darktest/CM0014_darktest_norm_pupil_fig.png',
                   'data/CM0014/darktest/CM0014_darktest_mean_pupil_fig.png',
                   'data/CM0014/darktest/CM0014_on_off.csv')

    # Participant 15: Great
    pupil_analysis('data/CM0015/darktest/darktest19_03_06on04-12-2016.tsv',
                   'data/CM0015/darktest/CM0015_darktest_norm_pupil.csv',
                   'data/CM0015/darktest/CM0015_darktest_unnorm_pupil.csv',
                   'data/CM0015/darktest/CM0015_darktest_mean_pupil.csv',
                   'data/CM0015/darktest/CM0015_darktest_norm_pupil_fig.png',
                   'data/CM0015/darktest/CM0015_darktest_mean_pupil_fig.png',
                   'data/CM0015/darktest/CM0015_on_off.csv')

    # Participant 16: Good
    pupil_analysis('data/CM0016/darktest/darktest17_05_51on04-14-2016.tsv',
                   'data/CM0016/darktest/CM0016_darktest_norm_pupil.csv',
                   'data/CM0016/darktest/CM0016_darktest_unnorm_pupil.csv',
                   'data/CM0016/darktest/CM0016_darktest_mean_pupil.csv',
                   'data/CM0016/darktest/CM0016_darktest_norm_pupil_fig.png',
                   'data/CM0016/darktest/CM0016_darktest_mean_pupil_fig.png',
                   'data/CM0016/darktest/CM0016_on_off.csv')

    # Participant 19: Great
    pupil_analysis('data/CM0019/darktest/darktest11_17_57on04-01-2016.tsv',
                   'data/CM0019/darktest/CM0019_darktest_norm_pupil.csv',
                   'data/CM0019/darktest/CM0019_darktest_unnorm_pupil.csv',
                   'data/CM0019/darktest/CM0019_darktest_mean_pupil.csv',
                   'data/CM0019/darktest/CM0019_darktest_norm_pupil_fig.png',
                   'data/CM0019/darktest/CM0019_darktest_mean_pupil_fig.png',
                   'data/CM0019/darktest/CM0019_on_off.csv')

    # Participant 20: Good
    pupil_analysis('data/CM0020/darktest/darktest12_29_06on04-20-2016.tsv',
                   'data/CM0020/darktest/CM0020_darktest_norm_pupil.csv',
                   'data/CM0020/darktest/CM0020_darktest_unnorm_pupil.csv',
                   'data/CM0020/darktest/CM0020_darktest_mean_pupil.csv',
                   'data/CM0020/darktest/CM0020_darktest_norm_pupil_fig.png',
                   'data/CM0020/darktest/CM0020_darktest_mean_pupil_fig.png',
                   'data/CM0020/darktest/CM0020_on_off.csv')

    # Participant 21: Great
    pupil_analysis('data/CM0021/darktest/darktest10_43_54on04-30-2016.tsv',
                   'data/CM0021/darktest/CM0021_darktest_norm_pupil.csv',
                   'data/CM0021/darktest/CM0021_darktest_unnorm_pupil.csv',
                   'data/CM0021/darktest/CM0021_darktest_mean_pupil.csv',
                   'data/CM0021/darktest/CM0021_darktest_norm_pupil_fig.png',
                   'data/CM0021/darktest/CM0021_darktest_mean_pupil_fig.png',
                   'data/CM0021/darktest/CM0021_on_off.csv')

    # Participant 22: Good; 0 < t < 4
    pupil_analysis('data/CM0022/darktest/darktest14_51_03on04-19-2016.tsv',
                   'data/CM0022/darktest/CM0022_darktest_norm_pupil.csv',
                   'data/CM0022/darktest/CM0022_darktest_unnorm_pupil.csv',
                   'data/CM0022/darktest/CM0022_darktest_mean_pupil.csv',
                   'data/CM0022/darktest/CM0022_darktest_norm_pupil_fig.png',
                   'data/CM0022/darktest/CM0022_darktest_mean_pupil_fig.png',
                   'data/CM0022/darktest/CM0022_on_off.csv')

    # Participant 24: Good
    pupil_analysis('data/CM0024/darktest/darktest13_16_26on04-13-2016.tsv',
                   'data/CM0024/darktest/CM0024_darktest_norm_pupil.csv',
                   'data/CM0024/darktest/CM0024_darktest_unnorm_pupil.csv',
                   'data/CM0024/darktest/CM0024_darktest_mean_pupil.csv',
                   'data/CM0024/darktest/CM0024_darktest_norm_pupil_fig.png',
                   'data/CM0024/darktest/CM0024_darktest_mean_pupil_fig.png',
                   'data/CM0024/darktest/CM0024_on_off.csv')

    # Participant 25: Good
    pupil_analysis('data/CM0025/darktest/darktest13_58_39on04-04-2016.tsv',
                   'data/CM0025/darktest/CM0025_darktest_norm_pupil.csv',
                   'data/CM0025/darktest/CM0025_darktest_unnorm_pupil.csv',
                   'data/CM0025/darktest/CM0025_darktest_mean_pupil.csv',
                   'data/CM0025/darktest/CM0025_darktest_norm_pupil_fig.png',
                   'data/CM0025/darktest/CM0025_darktest_mean_pupil_fig.png',
                   'data/CM0025/darktest/CM0025_on_off.csv')

    # Participant 26: Great
    pupil_analysis('data/CM0026/darktest/darktest14_01_50on04-01-2016.tsv',
                   'data/CM0026/darktest/CM0026_darktest_norm_pupil.csv',
                   'data/CM0026/darktest/CM0026_darktest_unnorm_pupil.csv',
                   'data/CM0026/darktest/CM0026_darktest_mean_pupil.csv',
                   'data/CM0026/darktest/CM0026_darktest_norm_pupil_fig.png',
                   'data/CM0026/darktest/CM0026_darktest_mean_pupil_fig.png',
                   'data/CM0026/darktest/CM0026_on_off.csv')

    # Participant 29: Good; 0 < t < 4
    pupil_analysis('data/CM0029/darktest/darktest13_52_34on04-22-2016.tsv',
                   'data/CM0029/darktest/CM0029_darktest_norm_pupil.csv',
                   'data/CM0029/darktest/CM0029_darktest_unnorm_pupil.csv',
                   'data/CM0029/darktest/CM0029_darktest_mean_pupil.csv',
                   'data/CM0029/darktest/CM0029_darktest_norm_pupil_fig.png',
                   'data/CM0029/darktest/CM0029_darktest_mean_pupil_fig.png',
                   'data/CM0029/darktest/CM0029_on_off.csv')

    # Participant 30: Great
    pupil_analysis('data/CM0030/darktest/darktest13_58_17on04-29-2016.tsv',
                   'data/CM0030/darktest/CM0030_darktest_norm_pupil.csv',
                   'data/CM0030/darktest/CM0030_darktest_unnorm_pupil.csv',
                   'data/CM0030/darktest/CM0030_darktest_mean_pupil.csv',
                   'data/CM0030/darktest/CM0030_darktest_norm_pupil_fig.png',
                   'data/CM0030/darktest/CM0030_darktest_mean_pupil_fig.png',
                   'data/CM0030/darktest/CM0030_on_off.csv')

    # Participant 31: Good; 0 < t < 3
    pupil_analysis('data/CM0031/darktest/darktest13_34_37on04-21-2016.tsv',
                   'data/CM0031/darktest/CM0031_darktest_norm_pupil.csv',
                   'data/CM0031/darktest/CM0031_darktest_unnorm_pupil.csv',
                   'data/CM0031/darktest/CM0031_darktest_mean_pupil.csv',
                   'data/CM0031/darktest/CM0031_darktest_norm_pupil_fig.png',
                   'data/CM0031/darktest/CM0031_darktest_mean_pupil_fig.png',
                   'data/CM0031/darktest/CM0031_on_off.csv')

    # Participant 32: Great
    pupil_analysis('data/CM0032/darktest/darktest11_56_48on04-12-2016.tsv',
                   'data/CM0032/darktest/CM0032_darktest_norm_pupil.csv',
                   'data/CM0032/darktest/CM0032_darktest_unnorm_pupil.csv',
                   'data/CM0032/darktest/CM0032_darktest_mean_pupil.csv',
                   'data/CM0032/darktest/CM0032_darktest_norm_pupil_fig.png',
                   'data/CM0032/darktest/CM0032_darktest_mean_pupil_fig.png',
                   'data/CM0032/darktest/CM0032_on_off.csv')

    # Participant 33: Great
    pupil_analysis('data/CM0033/darktest/darktest10_31_06on04-29-2016.tsv',
                   'data/CM0033/darktest/CM0033_darktest_norm_pupil.csv',
                   'data/CM0033/darktest/CM0033_darktest_unnorm_pupil.csv',
                   'data/CM0033/darktest/CM0033_darktest_mean_pupil.csv',
                   'data/CM0033/darktest/CM0033_darktest_norm_pupil_fig.png',
                   'data/CM0033/darktest/CM0033_darktest_mean_pupil_fig.png',
                   'data/CM0033/darktest/CM0033_on_off.csv')

    # Participant 34: Great
    pupil_analysis('data/CM0034/darktest/darktest10_25_46on04-13-2016.tsv',
                   'data/CM0034/darktest/CM0034_darktest_norm_pupil.csv',
                   'data/CM0034/darktest/CM0034_darktest_unnorm_pupil.csv',
                   'data/CM0034/darktest/CM0034_darktest_mean_pupil.csv',
                   'data/CM0034/darktest/CM0034_darktest_norm_pupil_fig.png',
                   'data/CM0034/darktest/CM0034_darktest_mean_pupil_fig.png',
                   'data/CM0034/darktest/CM0034_on_off.csv')

    # Participant 35: Great
    pupil_analysis('data/CM0035/darktest/darktest11_14_44on04-19-2016.tsv',
                   'data/CM0035/darktest/CM0035_darktest_norm_pupil.csv',
                   'data/CM0035/darktest/CM0035_darktest_unnorm_pupil.csv',
                   'data/CM0035/darktest/CM0035_darktest_mean_pupil.csv',
                   'data/CM0035/darktest/CM0035_darktest_norm_pupil_fig.png',
                   'data/CM0035/darktest/CM0035_darktest_mean_pupil_fig.png',
                   'data/CM0035/darktest/CM0035_on_off.csv')

    # Participant 36: Great
    pupil_analysis('data/CM0036/darktest/darktest15_39_25on04-13-2016.tsv',
                   'data/CM0036/darktest/CM0036_darktest_norm_pupil.csv',
                   'data/CM0036/darktest/CM0036_darktest_unnorm_pupil.csv',
                   'data/CM0036/darktest/CM0036_darktest_mean_pupil.csv',
                   'data/CM0036/darktest/CM0036_darktest_norm_pupil_fig.png',
                   'data/CM0036/darktest/CM0036_darktest_mean_pupil_fig.png',
                   'data/CM0036/darktest/CM0036_on_off.csv')

    # Participant 40: Great
    pupil_analysis('data/CM0040/darktest/darktest12_40_52on04-24-2016.tsv',
                   'data/CM0040/darktest/CM0040_darktest_norm_pupil.csv',
                   'data/CM0040/darktest/CM0040_darktest_unnorm_pupil.csv',
                   'data/CM0040/darktest/CM0040_darktest_mean_pupil.csv',
                   'data/CM0040/darktest/CM0040_darktest_norm_pupil_fig.png',
                   'data/CM0040/darktest/CM0040_darktest_mean_pupil_fig.png',
                   'data/CM0040/darktest/CM0040_on_off.csv')

    # Participant 41: Great
    pupil_analysis('data/CM0041/darktest/darktest16_50_34on04-28-2016.tsv',
                   'data/CM0041/darktest/CM0041_darktest_norm_pupil.csv',
                   'data/CM0041/darktest/CM0041_darktest_unnorm_pupil.csv',
                   'data/CM0041/darktest/CM0041_darktest_mean_pupil.csv',
                   'data/CM0041/darktest/CM0041_darktest_norm_pupil_fig.png',
                   'data/CM0041/darktest/CM0041_darktest_mean_pupil_fig.png',
                   'data/CM0041/darktest/CM0041_on_off.csv')

    # Participant 42: Good
    pupil_analysis('data/CM0042/darktest/darktest15_27_31on04-29-2016.tsv',
                   'data/CM0042/darktest/CM0042_darktest_norm_pupil.csv',
                   'data/CM0042/darktest/CM0042_darktest_unnorm_pupil.csv',
                   'data/CM0042/darktest/CM0042_darktest_mean_pupil.csv',
                   'data/CM0042/darktest/CM0042_darktest_norm_pupil_fig.png',
                   'data/CM0042/darktest/CM0042_darktest_mean_pupil_fig.png',
                   'data/CM0042/darktest/CM0042_on_off.csv')
