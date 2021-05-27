# preparatory work
import utils
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

# set up plotting
import matplotlib.pyplot as plt
import seaborn as sns

# make plots pretty
sns.set_style('darkgrid')
sns.set_context('talk', font_scale=1.4)
colors = sns.color_palette("Set2")


def pupil_analysis(datafile_path,
                   norm_pupil_std_path,
                   norm_pupil_odd_path,
                   unnorm_pupil_std_path,
                   unnorm_pupil_odd_path,
                   norm_pupil_bytrial_fig_path,
                   norm_pupil_fig_path,
                   event_times_path):
    """
    :param datafile_path: input datafile path
    :param norm_pupil_std_path: output normed standard datafile path
    :param unnorm_pupil_std_path: output unnormed standard datafile path
    :param norm_pupil_odd_path: output normed oddball datafile path
    :param unnorm_pupil_odd_path: output unnormed oddball datafile path
    :param norm_pupil_bytrial_fig_path: output figure path of all normed trial data
    :param norm_pupil_fig_path: output figure path of average normed trial data
    :param event_times_path: output path of event start and end times
    :return: Several .csv files containing normed and unnormed data plus two figures
    """
    df = pd.read_csv(datafile_path, sep='\t')
    df = utils.prepdata(df)

    # converts from soundtime (which is in Tobii clock time)
    df = utils.timestamp_to_seconds(df, 'soundtime', 'soundtimes')
    df = utils.timestamp_to_seconds(df, 'presstime', 'presstimes')

    converted_soundtime = df['soundtimes']
    converted_presstime = df['presstimes']

    wasodd = list(df['trialvec'].dropna() == 1)
    wasnotodd = list(df['trialvec'].dropna() != 1)
    where_odd = np.nonzero(wasodd)[0]
    where_notodd = np.nonzero(wasnotodd)[0]

    # parameters
    tpre = -0.6
    tpost = .75
    plottype = 1  # changes depending on x-axis range of interest

    chunklist, idx = utils.evtsplit(df, df['soundtimes'], tpre, tpost)

    norm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[0]
    unnorm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[1]

    norm_pupil_std = norm_data[idx.get_loc('MeanPupil')][where_notodd]
    norm_pupil_odd = norm_data[idx.get_loc('MeanPupil')][where_odd]
    unnorm_pupil_std = unnorm_data[idx.get_loc('MeanPupil')][where_notodd]
    unnorm_pupil_odd = unnorm_data[idx.get_loc('MeanPupil')][where_odd]

    # Applying Savitzky-Golay filter (M=55, k=2)

    # Norm Pupil Standard
    norm_pupil_std = pd.DataFrame(norm_pupil_std)
    norm_pupil_std_unsmoothed_avg = np.nanmean(norm_pupil_std, 1)
    norm_pupil_std_unsmoothed_stdev = np.nanstd(norm_pupil_std, 1)

    norm_pupil_std_last = len(norm_pupil_std.columns)

    for colhead, colseries in norm_pupil_std.iteritems():
        try:
            norm_pupil_std['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)
        except:
            pass

    norm_pupil_std_smooth = norm_pupil_std.iloc[:, norm_pupil_std_last:]

    norm_pupil_std_smoothed_avg = np.nanmean(norm_pupil_std_smooth, 1)
    norm_pupil_std_smoothed_stdev = np.nanstd(norm_pupil_std_smooth, 1)

    norm_pupil_std['unsmoothed_avg'] = norm_pupil_std_unsmoothed_avg
    norm_pupil_std['unsmoothed_stdev'] = norm_pupil_std_unsmoothed_stdev
    norm_pupil_std['smoothed_avg'] = norm_pupil_std_smoothed_avg
    norm_pupil_std['smoothed_stdev'] = norm_pupil_std_smoothed_stdev

    # Norm Pupil Oddball
    norm_pupil_odd = pd.DataFrame(norm_pupil_odd)
    norm_pupil_odd_unsmoothed_avg = np.nanmean(norm_pupil_odd, 1)
    norm_pupil_odd_unsmoothed_stdev = np.nanstd(norm_pupil_odd, 1)

    norm_pupil_odd_last = len(norm_pupil_odd.columns)

    for colhead, colseries in norm_pupil_odd.iteritems():
        norm_pupil_odd['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    norm_pupil_odd_smooth = norm_pupil_odd.iloc[:, norm_pupil_odd_last:]

    norm_pupil_odd_smoothed_avg = np.nanmean(norm_pupil_odd_smooth, 1)
    norm_pupil_odd_smoothed_stdev = np.nanstd(norm_pupil_odd_smooth, 1)

    norm_pupil_odd['unsmoothed_avg'] = norm_pupil_odd_unsmoothed_avg
    norm_pupil_odd['unsmoothed_stdev'] = norm_pupil_odd_unsmoothed_stdev
    norm_pupil_odd['smoothed_avg'] = norm_pupil_odd_smoothed_avg
    norm_pupil_odd['smoothed_stdev'] = norm_pupil_odd_smoothed_stdev

    # Unnorm Pupil Standard
    unnorm_pupil_std = pd.DataFrame(unnorm_pupil_std)
    unnorm_pupil_std_unsmoothed_avg = np.nanmean(unnorm_pupil_std, 1)
    unnorm_pupil_std_unsmoothed_stdev = np.nanstd(unnorm_pupil_std, 1)

    unnorm_pupil_std_last = len(unnorm_pupil_std.columns)

    for colhead, colseries in unnorm_pupil_std.iteritems():
        try:
            unnorm_pupil_std['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)
        except:
            pass
    unnorm_pupil_std_smooth = unnorm_pupil_std.iloc[:, unnorm_pupil_std_last:]

    unnorm_pupil_std_smoothed_avg = np.nanmean(unnorm_pupil_std_smooth, 1)
    unnorm_pupil_std_smoothed_stdev = np.nanstd(unnorm_pupil_std_smooth, 1)

    unnorm_pupil_std['unsmoothed_avg'] = unnorm_pupil_std_unsmoothed_avg
    unnorm_pupil_std['unsmoothed_stdev'] = unnorm_pupil_std_unsmoothed_stdev
    unnorm_pupil_std['smoothed_avg'] = unnorm_pupil_std_smoothed_avg
    unnorm_pupil_std['smoothed_stdev'] = unnorm_pupil_std_smoothed_stdev

    # Unnorm Pupil Oddball
    unnorm_pupil_odd = pd.DataFrame(unnorm_pupil_odd)
    unnorm_pupil_odd_unsmoothed_avg = np.nanmean(unnorm_pupil_odd, 1)
    unnorm_pupil_odd_unsmoothed_stdev = np.nanstd(unnorm_pupil_odd, 1)

    unnorm_pupil_odd_last = len(unnorm_pupil_odd.columns)

    for colhead, colseries in unnorm_pupil_odd.iteritems():
        unnorm_pupil_odd['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    unnorm_pupil_odd_smooth = unnorm_pupil_odd.iloc[:, unnorm_pupil_odd_last:]

    unnorm_pupil_odd_smoothed_avg = np.nanmean(unnorm_pupil_odd_smooth, 1)
    unnorm_pupil_odd_smoothed_stdev = np.nanstd(unnorm_pupil_odd_smooth, 1)

    unnorm_pupil_odd['unsmoothed_avg'] = unnorm_pupil_odd_unsmoothed_avg
    unnorm_pupil_odd['unsmoothed_stdev'] = unnorm_pupil_odd_unsmoothed_stdev
    unnorm_pupil_odd['smoothed_avg'] = unnorm_pupil_odd_smoothed_avg
    unnorm_pupil_odd['smoothed_stdev'] = unnorm_pupil_odd_smoothed_stdev

    event_times = pd.DataFrame({
        'soundtimes': converted_soundtime,
        'presstimes': converted_presstime
    })

    event_times.to_csv(event_times_path)  # Write stimulus onset and response time to .csv

    norm_pupil_std.to_csv(norm_pupil_std_path)  # Write normed odd data to .csv
    norm_pupil_odd.to_csv(norm_pupil_odd_path)  # Write normed std data to .csv

    unnorm_pupil_std.to_csv(unnorm_pupil_std_path)  # Write unnormed odd data to .csv
    unnorm_pupil_odd.to_csv(unnorm_pupil_odd_path)  # Write unnormed std data to .csv

    # Plot smoothed averages for std and odd
    plt.figure(figsize=(10, 6))
    for colhead, colseries in norm_pupil_std_smooth.iteritems():
        try:
            plt.plot(norm_pupil_std.index, norm_pupil_std[colhead], '#347ae3')
        except:
            pass
    for colhead, colseries in norm_pupil_odd_smooth.iteritems():
        try:
            plt.plot(norm_pupil_odd_smooth.index, norm_pupil_odd_smooth[colhead], 'orange')
        except:
            pass
    plt.xlim([tpre, tpost])
    plt.title('Pupillary response to oddball');
    plt.ylabel('Normalized Pupil Size (arbitrary units)');
    plt.xlabel('Time from sound (s)');
    if plottype == 0:
        plt.legend(['Oddball', 'Standard'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    elif plottype == 1:
        plt.legend([], bbox_to_anchor=(1.05, 1), loc=2,
                   borderaxespad=0.);
    elif plottype == 2:
        plt.legend(['Oddball', '', '', 'Standard'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    plt.gca().get_legend().get_title().set_fontsize('14');
    plt.savefig(norm_pupil_bytrial_fig_path, bbox_inches='tight');
    plt.close("all")

    plt.figure(figsize=(10, 6))
    plt.plot(norm_pupil_std.index, norm_pupil_std['smoothed_avg'])
    plt.plot(norm_pupil_odd.index, norm_pupil_odd['smoothed_avg'])
    plt.xlim([tpre, tpost])
    plt.title('Pupillary response to oddball');
    plt.ylabel('Normalized Pupil Size (arbitrary units)');
    plt.xlabel('Time from sound (s)');
    if plottype == 0:
        plt.legend(['Oddball', 'Standard'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    elif plottype == 1:
        plt.legend(['Oddball', 'Standard', 'Oddball SEM', 'Standard SEM'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    elif plottype == 2:
        plt.legend(['Oddball', '', '', 'Standard'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    plt.gca().get_legend().get_title().set_fontsize('14');
    plt.savefig(norm_pupil_fig_path, bbox_inches='tight');
    plt.close("all")


if __name__ == '__main__':
    # # Participant 1: Good
    # pupil_analysis('data/CM0001/oddball/oddball11_36_54on04-06-2016.tsv',
    #                'data/CM0001/oddball/CM0001_oddball_norm_pupil_std.csv',
    #                'data/CM0001/oddball/CM0001_oddball_norm_pupil_odd.csv',
    #                'data/CM0001/oddball/CM0001_oddball_unnorm_pupil_std.csv',
    #                'data/CM0001/oddball/CM0001_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0001/oddball/CM0001_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0001/oddball/CM0001_oddball_norm_pupil_fig.png',
    #                'data/CM0001/oddball/CM0001_event_times.csv')
    #
    # # Participant 3: Good
    # pupil_analysis('data/CM0003/oddball/oddball15_20_05on04-26-2016.tsv',
    #                'data/CM0003/oddball/CM0003_oddball_norm_pupil_std.csv',
    #                'data/CM0003/oddball/CM0003_oddball_norm_pupil_odd.csv',
    #                'data/CM0003/oddball/CM0003_oddball_unnorm_pupil_std.csv',
    #                'data/CM0003/oddball/CM0003_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0003/oddball/CM0003_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0003/oddball/CM0003_oddball_norm_pupil_fig.png',
    #                'data/CM0003/oddball/CM0003_event_times.csv')
    #
    # # Participant 4: Good
    # pupil_analysis('data/CM0004/oddball/oddball14_35_28on04-14-2016.tsv',
    #                'data/CM0004/oddball/CM0004_oddball_norm_pupil_std.csv',
    #                'data/CM0004/oddball/CM0004_oddball_norm_pupil_odd.csv',
    #                'data/CM0004/oddball/CM0004_oddball_unnorm_pupil_std.csv',
    #                'data/CM0004/oddball/CM0004_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0004/oddball/CM0004_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0004/oddball/CM0004_oddball_norm_pupil_fig.png',
    #                'data/CM0004/oddball/CM0004_event_times.csv')
    #
    # # Participant 11: Great
    # pupil_analysis('data/CM0011/oddball/oddball15_58_59on04-20-2016.tsv',
    #                'data/CM0011/oddball/CM0011_oddball_norm_pupil_std.csv',
    #                'data/CM0011/oddball/CM0011_oddball_norm_pupil_odd.csv',
    #                'data/CM0011/oddball/CM0011_oddball_unnorm_pupil_std.csv',
    #                'data/CM0011/oddball/CM0011_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0011/oddball/CM0011_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0011/oddball/CM0011_oddball_norm_pupil_fig.png',
    #                'data/CM0011/oddball/CM0011_event_times.csv')
    #
    # # Participant 14: Great
    # pupil_analysis('data/CM0014/oddball/oddball15_13_28on04-11-2016.tsv',
    #                'data/CM0014/oddball/CM0014_oddball_norm_pupil_std.csv',
    #                'data/CM0014/oddball/CM0014_oddball_norm_pupil_odd.csv',
    #                'data/CM0014/oddball/CM0014_oddball_unnorm_pupil_std.csv',
    #                'data/CM0014/oddball/CM0014_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0014/oddball/CM0014_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0014/oddball/CM0014_oddball_norm_pupil_fig.png',
    #                'data/CM0014/oddball/CM0014_event_times.csv')
    #
    # # Participant 15: Great
    # pupil_analysis('data/CM0015/oddball/oddball19_10_20on04-12-2016.tsv',
    #                'data/CM0015/oddball/CM0015_oddball_norm_pupil_std.csv',
    #                'data/CM0015/oddball/CM0015_oddball_norm_pupil_odd.csv',
    #                'data/CM0015/oddball/CM0015_oddball_unnorm_pupil_std.csv',
    #                'data/CM0015/oddball/CM0015_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0015/oddball/CM0015_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0015/oddball/CM0015_oddball_norm_pupil_fig.png',
    #                'data/CM0015/oddball/CM0015_event_times.csv')

    # # Participant 16: Unusable (Insufficient Data)
    # pupil_analysis('data/CM0016/oddball/oddball17_13_09on04-14-2016.tsv',
    #                'data/CM0016/oddball/CM0016_oddball_norm_pupil_std.csv',
    #                'data/CM0016/oddball/CM0016_oddball_norm_pupil_odd.csv',
    #                'data/CM0016/oddball/CM0016_oddball_unnorm_pupil_std.csv',
    #                'data/CM0016/oddball/CM0016_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0016/oddball/CM0016_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0016/oddball/CM0016_oddball_norm_pupil_fig.png',
    #                'data/CM0016/oddball/CM0016_event_times.csv')
    #
    # # Participant 19: Great
    # pupil_analysis('data/CM0019/oddball/oddball11_25_08on04-01-2016.tsv',
    #                'data/CM0019/oddball/CM0019_oddball_norm_pupil_std.csv',
    #                'data/CM0019/oddball/CM0019_oddball_norm_pupil_odd.csv',
    #                'data/CM0019/oddball/CM0019_oddball_unnorm_pupil_std.csv',
    #                'data/CM0019/oddball/CM0019_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0019/oddball/CM0019_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0019/oddball/CM0019_oddball_norm_pupil_fig.png',
    #                'data/CM0019/oddball/CM0019_event_times.csv')
    #
    # # Participant 20: Good
    # pupil_analysis('data/CM0020/oddball/oddball12_36_44on04-20-2016.tsv',
    #                'data/CM0020/oddball/CM0020_oddball_norm_pupil_std.csv',
    #                'data/CM0020/oddball/CM0020_oddball_norm_pupil_odd.csv',
    #                'data/CM0020/oddball/CM0020_oddball_unnorm_pupil_std.csv',
    #                'data/CM0020/oddball/CM0020_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0020/oddball/CM0020_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0020/oddball/CM0020_oddball_norm_pupil_fig.png',
    #                'data/CM0020/oddball/CM0020_event_times.csv')
    #
    # # Participant 21: Great
    # pupil_analysis('data/CM0021/oddball/oddball10_51_43on04-30-2016.tsv',
    #                'data/CM0021/oddball/CM0021_oddball_norm_pupil_std.csv',
    #                'data/CM0021/oddball/CM0021_oddball_norm_pupil_odd.csv',
    #                'data/CM0021/oddball/CM0021_oddball_unnorm_pupil_std.csv',
    #                'data/CM0021/oddball/CM0021_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0021/oddball/CM0021_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0021/oddball/CM0021_oddball_norm_pupil_fig.png',
    #                'data/CM0021/oddball/CM0021_event_times.csv')

    # Participant 22: Usable (0 < t < .75)
    pupil_analysis('data/CM0022/oddball/oddball14_58_31on04-19-2016.tsv',
                   'data/CM0022/oddball/CM0022_oddball_norm_pupil_std.csv',
                   'data/CM0022/oddball/CM0022_oddball_norm_pupil_odd.csv',
                   'data/CM0022/oddball/CM0022_oddball_unnorm_pupil_std.csv',
                   'data/CM0022/oddball/CM0022_oddball_unnorm_pupil_odd.csv',
                   'data/CM0022/oddball/CM0022_oddball_norm_pupil_bytrial_fig.png',
                   'data/CM0022/oddball/CM0022_oddball_norm_pupil_fig.png',
                   'data/CM0022/oddball/CM0022_event_times.csv')

    # # Participant 24: Good
    # pupil_analysis('data/CM0024/oddball/oddball13_24_10on04-13-2016.tsv',
    #                'data/CM0024/oddball/CM0024_oddball_norm_pupil_std.csv',
    #                'data/CM0024/oddball/CM0024_oddball_norm_pupil_odd.csv',
    #                'data/CM0024/oddball/CM0024_oddball_unnorm_pupil_std.csv',
    #                'data/CM0024/oddball/CM0024_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0024/oddball/CM0024_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0024/oddball/CM0024_oddball_norm_pupil_fig.png',
    #                'data/CM0024/oddball/CM0024_event_times.csv')
    #
    # # Participant 25: Great
    # pupil_analysis('data/CM0025/oddball/oddball14_06_16on04-04-2016.tsv',
    #                'data/CM0025/oddball/CM0025_oddball_norm_pupil_std.csv',
    #                'data/CM0025/oddball/CM0025_oddball_norm_pupil_odd.csv',
    #                'data/CM0025/oddball/CM0025_oddball_unnorm_pupil_std.csv',
    #                'data/CM0025/oddball/CM0025_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0025/oddball/CM0025_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0025/oddball/CM0025_oddball_norm_pupil_fig.png',
    #                'data/CM0025/oddball/CM0025_event_times.csv')
    #
    # # Participant 26: Great
    # pupil_analysis('data/CM0026/oddball/oddball14_09_24on04-01-2016.tsv',
    #                'data/CM0026/oddball/CM0026_oddball_norm_pupil_std.csv',
    #                'data/CM0026/oddball/CM0026_oddball_norm_pupil_odd.csv',
    #                'data/CM0026/oddball/CM0026_oddball_unnorm_pupil_std.csv',
    #                'data/CM0026/oddball/CM0026_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0026/oddball/CM0026_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0026/oddball/CM0026_oddball_norm_pupil_fig.png',
    #                'data/CM0026/oddball/CM0026_event_times.csv')

    # # Participant 29: Usable (0 < t < 1)
    # pupil_analysis('data/CM0029/oddball/oddball14_00_25on04-22-2016.tsv',
    #                'data/CM0029/oddball/CM0029_oddball_norm_pupil_std.csv',
    #                'data/CM0029/oddball/CM0029_oddball_norm_pupil_odd.csv',
    #                'data/CM0029/oddball/CM0029_oddball_unnorm_pupil_std.csv',
    #                'data/CM0029/oddball/CM0029_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0029/oddball/CM0029_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0029/oddball/CM0029_oddball_norm_pupil_fig.png',
    #                'data/CM0029/oddball/CM0029_event_times.csv')

    # # Participant 30: Good
    # pupil_analysis('data/CM0030/oddball/oddball14_05_37on04-29-2016.tsv',
    #                'data/CM0030/oddball/CM0030_oddball_norm_pupil_std.csv',
    #                'data/CM0030/oddball/CM0030_oddball_norm_pupil_odd.csv',
    #                'data/CM0030/oddball/CM0030_oddball_unnorm_pupil_std.csv',
    #                'data/CM0030/oddball/CM0030_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0030/oddball/CM0030_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0030/oddball/CM0030_oddball_norm_pupil_fig.png',
    #                'data/CM0030/oddball/CM0030_event_times.csv')
    #
    # # Participant 31: Usable (Standard > Oddball)
    # pupil_analysis('data/CM0031/oddball/oddball13_42_17on04-21-2016.tsv',
    #                'data/CM0031/oddball/CM0031_oddball_norm_pupil_std.csv',
    #                'data/CM0031/oddball/CM0031_oddball_norm_pupil_odd.csv',
    #                'data/CM0031/oddball/CM0031_oddball_unnorm_pupil_std.csv',
    #                'data/CM0031/oddball/CM0031_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0031/oddball/CM0031_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0031/oddball/CM0031_oddball_norm_pupil_fig.png',
    #                'data/CM0031/oddball/CM0031_event_times.csv')

    # # Participant 32: Usable (0 < t < 1.5)
    # pupil_analysis('data/CM0032/oddball/oddball12_04_13on04-12-2016.tsv',
    #                'data/CM0032/oddball/CM0032_oddball_norm_pupil_std.csv',
    #                'data/CM0032/oddball/CM0032_oddball_norm_pupil_odd.csv',
    #                'data/CM0032/oddball/CM0032_oddball_unnorm_pupil_std.csv',
    #                'data/CM0032/oddball/CM0032_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0032/oddball/CM0032_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0032/oddball/CM0032_oddball_norm_pupil_fig.png',
    #                'data/CM0032/oddball/CM0032_event_times.csv')

    # # Participant 33: Good (Standard > Oddball)
    # pupil_analysis('data/CM0033/oddball/oddball10_38_21on04-29-2016.tsv',
    #                'data/CM0033/oddball/CM0033_oddball_norm_pupil_std.csv',
    #                'data/CM0033/oddball/CM0033_oddball_norm_pupil_odd.csv',
    #                'data/CM0033/oddball/CM0033_oddball_unnorm_pupil_std.csv',
    #                'data/CM0033/oddball/CM0033_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0033/oddball/CM0033_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0033/oddball/CM0033_oddball_norm_pupil_fig.png',
    #                'data/CM0033/oddball/CM0033_event_times.csv')
    #
    # # Participant 34: Good
    # pupil_analysis('data/CM0034/oddball/oddball10_33_39on04-13-2016.tsv',
    #                'data/CM0034/oddball/CM0034_oddball_norm_pupil_std.csv',
    #                'data/CM0034/oddball/CM0034_oddball_norm_pupil_odd.csv',
    #                'data/CM0034/oddball/CM0034_oddball_unnorm_pupil_std.csv',
    #                'data/CM0034/oddball/CM0034_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0034/oddball/CM0034_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0034/oddball/CM0034_oddball_norm_pupil_fig.png',
    #                'data/CM0034/oddball/CM0034_event_times.csv')
    #
    # # Participant 35: Good
    # pupil_analysis('data/CM0035/oddball/oddball11_22_56on04-19-2016.tsv',
    #                'data/CM0035/oddball/CM0035_oddball_norm_pupil_std.csv',
    #                'data/CM0035/oddball/CM0035_oddball_norm_pupil_odd.csv',
    #                'data/CM0035/oddball/CM0035_oddball_unnorm_pupil_std.csv',
    #                'data/CM0035/oddball/CM0035_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0035/oddball/CM0035_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0035/oddball/CM0035_oddball_norm_pupil_fig.png',
    #                'data/CM0035/oddball/CM0035_event_times.csv')
    #
    # # Participant 36: Great
    # pupil_analysis('data/CM0036/oddball/oddball15_47_09on04-13-2016.tsv',
    #                'data/CM0036/oddball/CM0036_oddball_norm_pupil_std.csv',
    #                'data/CM0036/oddball/CM0036_oddball_norm_pupil_odd.csv',
    #                'data/CM0036/oddball/CM0036_oddball_unnorm_pupil_std.csv',
    #                'data/CM0036/oddball/CM0036_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0036/oddball/CM0036_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0036/oddball/CM0036_oddball_norm_pupil_fig.png',
    #                'data/CM0036/oddball/CM0036_event_times.csv')
    #
    # # Participant 40: Good
    # pupil_analysis('data/CM0040/oddball/oddball12_49_33on04-24-2016.tsv',
    #                'data/CM0040/oddball/CM0040_oddball_norm_pupil_std.csv',
    #                'data/CM0040/oddball/CM0040_oddball_norm_pupil_odd.csv',
    #                'data/CM0040/oddball/CM0040_oddball_unnorm_pupil_std.csv',
    #                'data/CM0040/oddball/CM0040_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0040/oddball/CM0040_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0040/oddball/CM0040_oddball_norm_pupil_fig.png',
    #                'data/CM0040/oddball/CM0040_event_times.csv')
    #
    # # Participant 41: Great
    # pupil_analysis('data/CM0041/oddball/oddball16_57_51on04-28-2016.tsv',
    #                'data/CM0041/oddball/CM0041_oddball_norm_pupil_std.csv',
    #                'data/CM0041/oddball/CM0041_oddball_norm_pupil_odd.csv',
    #                'data/CM0041/oddball/CM0041_oddball_unnorm_pupil_std.csv',
    #                'data/CM0041/oddball/CM0041_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0041/oddball/CM0041_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0041/oddball/CM0041_oddball_norm_pupil_fig.png',
    #                'data/CM0041/oddball/CM0041_event_times.csv')
    #
    # # Participant 42: Great
    # pupil_analysis('data/CM0042/oddball/oddball15_34_41on04-29-2016.tsv',
    #                'data/CM0042/oddball/CM0042_oddball_norm_pupil_std.csv',
    #                'data/CM0042/oddball/CM0042_oddball_norm_pupil_odd.csv',
    #                'data/CM0042/oddball/CM0042_oddball_unnorm_pupil_std.csv',
    #                'data/CM0042/oddball/CM0042_oddball_unnorm_pupil_odd.csv',
    #                'data/CM0042/oddball/CM0042_oddball_norm_pupil_bytrial_fig.png',
    #                'data/CM0042/oddball/CM0042_oddball_norm_pupil_fig.png',
    #                'data/CM0042/oddball/CM0042_event_times.csv')
