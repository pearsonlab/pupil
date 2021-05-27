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
                   norm_pupil_corr_path,
                   norm_pupil_inc_path,
                   unnorm_pupil_corr_path,
                   unnorm_pupil_inc_path,
                   norm_pupil_bytrial_fig_path,
                   norm_pupil_fig_path,
                   event_times_path):
    """
    :param datafile_path:
    :param norm_pupil_corr_path:
    :param unnorm_pupil_corr_path:
    :param norm_pupil_inc_path:
    :param unnorm_pupil_inc_path:
    :param norm_pupil_bytrial_fig_path:
    :param norm_pupil_fig_path:
    :param event_times_path:
    :return:
    """
    df = pd.read_csv(datafile_path, sep='\t')  # load .tsv into dataframe
    df = utils.prepdata(df)  # run preparations

    # etimes are the event times in seconds.
    # converts from soundtime (which is in Tobii clock time)
    df = utils.timestamp_to_seconds(df, 'soundtime', 'soundtimes')
    df = utils.timestamp_to_seconds(df, 'presstime', 'presstimes')
    df = utils.timestamp_to_seconds(df, 'cuetime', 'cuetimes')

    converted_soundtime = df['soundtimes']
    converted_presstime = df['presstimes']
    converted_cuetime = df['cuetimes']

    wascorr = list(df['correct'].dropna() == 1)
    wasinc = list(df['correct'].dropna() != 1)
    where_corr = np.nonzero(wascorr)[0]
    where_inc = np.nonzero(wasinc)[0]

    # PARAMETERS
    tpre = -0.6
    tpost = 2
    plottype = 1

    chunklist, idx = utils.evtsplit(df, df['soundtimes'], tpre, tpost)

    norm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[0]
    unnorm_data = utils.basenorm(chunklist, idx, [float('-inf'), 0], 0)[1]

    norm_pupil_corr = norm_data[idx.get_loc('MeanPupil')][where_corr]
    norm_pupil_inc = norm_data[idx.get_loc('MeanPupil')][where_inc]
    unnorm_pupil_corr = unnorm_data[idx.get_loc('MeanPupil')][where_corr]
    unnorm_pupil_inc = unnorm_data[idx.get_loc('MeanPupil')][where_inc]

    # Applying Savitzky-Golay filter (M=55, k=2)

    # Norm Pupil Correct
    norm_pupil_corr = pd.DataFrame(norm_pupil_corr)
    norm_pupil_corr_unsmoothed_avg = np.nanmean(norm_pupil_corr, 1)
    norm_pupil_corr_unsmoothed_stdev = np.nanstd(norm_pupil_corr, 1)

    norm_pupil_corr_last = len(norm_pupil_corr.columns)

    for colhead, colseries in norm_pupil_corr.iteritems():
        norm_pupil_corr['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    norm_pupil_corr_smooth = norm_pupil_corr.iloc[:, norm_pupil_corr_last:]

    norm_pupil_corr_smoothed_avg = np.nanmean(norm_pupil_corr_smooth, 1)
    norm_pupil_corr_smoothed_stdev = np.nanstd(norm_pupil_corr_smooth, 1)
    
    norm_pupil_corr['unsmoothed_avg'] = norm_pupil_corr_unsmoothed_avg
    norm_pupil_corr['unsmoothed_stdev'] = norm_pupil_corr_unsmoothed_stdev
    norm_pupil_corr['smoothed_avg'] = norm_pupil_corr_smoothed_avg
    norm_pupil_corr['smoothed_stdev'] = norm_pupil_corr_smoothed_stdev

    # Norm Pupil Incorrect
    norm_pupil_inc = pd.DataFrame(norm_pupil_inc)
    norm_pupil_inc_unsmoothed_avg = np.nanmean(norm_pupil_inc, 1)
    norm_pupil_inc_unsmoothed_stdev = np.nanstd(norm_pupil_inc, 1)

    norm_pupil_inc_last = len(norm_pupil_inc.columns)

    for colhead, colseries in norm_pupil_inc.iteritems():
        norm_pupil_inc['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    norm_pupil_inc_smooth = norm_pupil_inc.iloc[:, norm_pupil_inc_last:]

    norm_pupil_inc_smoothed_avg = np.nanmean(norm_pupil_inc_smooth, 1)
    norm_pupil_inc_smoothed_stdev = np.nanstd(norm_pupil_inc_smooth, 1)

    norm_pupil_inc['unsmoothed_avg'] = norm_pupil_inc_unsmoothed_avg
    norm_pupil_inc['unsmoothed_stdev'] = norm_pupil_inc_unsmoothed_stdev
    norm_pupil_inc['smoothed_avg'] = norm_pupil_inc_smoothed_avg
    norm_pupil_inc['smoothed_stdev'] = norm_pupil_inc_smoothed_stdev
    
    # Unnorm Pupil Correct
    unnorm_pupil_corr = pd.DataFrame(unnorm_pupil_corr)
    unnorm_pupil_corr_unsmoothed_avg = np.nanmean(unnorm_pupil_corr, 1)
    unnorm_pupil_corr_unsmoothed_stdev = np.nanstd(unnorm_pupil_corr, 1)

    unnorm_pupil_corr_last = len(unnorm_pupil_corr.columns)

    for colhead, colseries in unnorm_pupil_corr.iteritems():
        unnorm_pupil_corr['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    unnorm_pupil_corr_smooth = unnorm_pupil_corr.iloc[:, unnorm_pupil_corr_last:]

    unnorm_pupil_corr_smoothed_avg = np.nanmean(unnorm_pupil_corr_smooth, 1)
    unnorm_pupil_corr_smoothed_stdev = np.nanstd(unnorm_pupil_corr_smooth, 1)

    unnorm_pupil_corr['unsmoothed_avg'] = unnorm_pupil_corr_unsmoothed_avg
    unnorm_pupil_corr['unsmoothed_stdev'] = unnorm_pupil_corr_unsmoothed_stdev
    unnorm_pupil_corr['smoothed_avg'] = unnorm_pupil_corr_smoothed_avg
    unnorm_pupil_corr['smoothed_stdev'] = unnorm_pupil_corr_smoothed_stdev
    
    # Unnorm Pupil Incorrect
    unnorm_pupil_inc = pd.DataFrame(unnorm_pupil_inc)
    unnorm_pupil_inc_unsmoothed_avg = np.nanmean(unnorm_pupil_inc, 1)
    unnorm_pupil_inc_unsmoothed_stdev = np.nanstd(unnorm_pupil_inc, 1)

    unnorm_pupil_inc_last = len(unnorm_pupil_inc.columns)

    for colhead, colseries in unnorm_pupil_inc.iteritems():
        unnorm_pupil_inc['trial' + str(colhead) + '_smoothed'] = savgol_filter(colseries, 55, 2)

    unnorm_pupil_inc_smooth = unnorm_pupil_inc.iloc[:, unnorm_pupil_inc_last:]

    unnorm_pupil_inc_smoothed_avg = np.nanmean(unnorm_pupil_inc_smooth, 1)
    unnorm_pupil_inc_smoothed_stdev = np.nanstd(unnorm_pupil_inc_smooth, 1)

    unnorm_pupil_inc['unsmoothed_avg'] = unnorm_pupil_inc_unsmoothed_avg
    unnorm_pupil_inc['unsmoothed_stdev'] = unnorm_pupil_inc_unsmoothed_stdev
    unnorm_pupil_inc['smoothed_avg'] = unnorm_pupil_inc_smoothed_avg
    unnorm_pupil_inc['smoothed_stdev'] = unnorm_pupil_inc_smoothed_stdev
    
    event_times = pd.DataFrame({
        'soundtimes': converted_soundtime,
        'presstimes': converted_presstime,
        'cuetimes': converted_cuetime
    })

    event_times.to_csv(event_times_path)  # Write stimulus onset and response time to .csv

    norm_pupil_corr.to_csv(norm_pupil_corr_path)  # Write normed odd data to .csv
    norm_pupil_inc.to_csv(norm_pupil_inc_path)  # Write normed std data to .csv

    unnorm_pupil_corr.to_csv(unnorm_pupil_corr_path)  # Write unnormed odd data to .csv
    unnorm_pupil_inc.to_csv(unnorm_pupil_inc_path)  # Write unnormed std data to .csv

    # Plot smoothed averages for std and odd
    plt.figure(figsize=(10, 6))
    for colhead, colseries in norm_pupil_corr_smooth.iteritems():
        try:
            plt.plot(norm_pupil_corr.index, norm_pupil_corr[colhead], '#347ae3')
        except:
            pass
    for colhead, colseries in norm_pupil_inc_smooth.iteritems():
        try:
            plt.plot(norm_pupil_inc_smooth.index, norm_pupil_inc_smooth[colhead], 'orange')
        except:
            pass
    plt.xlim([tpre, tpost])
    plt.title('Pupillary response to negative feedback');
    plt.ylabel('Normalized Pupil Size (arbitrary units)');
    plt.xlabel('Time from buzzer (s)');
    if plottype == 0:
        plt.legend(['Correct', 'Incorrect'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    elif plottype == 1:
        pass
    elif plottype == 2:
        plt.legend(['Correct', '', '', 'Incorrect'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    plt.savefig(norm_pupil_bytrial_fig_path, bbox_inches='tight');
    plt.close("all")

    plt.figure(figsize=(10, 6))
    plt.plot(norm_pupil_corr.index, norm_pupil_corr['smoothed_avg'])
    plt.plot(norm_pupil_inc.index, norm_pupil_inc['smoothed_avg'])
    plt.xlim([tpre, tpost])
    plt.title('Pupillary response to negative feedback');
    plt.ylabel('Normalized Pupil Size (arbitrary units)');
    plt.xlabel('Time from buzzer (s)');
    if plottype == 0:
        plt.legend(['Correct', 'Incorrect'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    elif plottype == 1:
        plt.legend(['Correct', 'Incorrect'], bbox_to_anchor=(1.05, 1), loc=2,
                   borderaxespad=0.);
    elif plottype == 2:
        plt.legend(['Correct', '', '', 'Incorrect'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);
    plt.savefig(norm_pupil_fig_path, bbox_inches='tight');
    plt.close("all")


if __name__ == '__main__':
    # Participant 1: Great
    pupil_analysis('data/CM0001/revlearn/revlearn11_33_45on04-06-2016.tsv',
                   'data/CM0001/revlearn/CM0001_revlearn_norm_pupil_corr.csv',
                   'data/CM0001/revlearn/CM0001_revlearn_norm_pupil_inc.csv',
                   'data/CM0001/revlearn/CM0001_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0001/revlearn/CM0001_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0001/revlearn/CM0001_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0001/revlearn/CM0001_revlearn_norm_pupil_fig.png',
                   'data/CM0001/revlearn/CM0001_event_times.csv')

    # Participant 3: Good
    pupil_analysis('data/CM0003/revlearn/revlearn15_17_03on04-26-2016.tsv',
                   'data/CM0003/revlearn/CM0003_revlearn_norm_pupil_corr.csv',
                   'data/CM0003/revlearn/CM0003_revlearn_norm_pupil_inc.csv',
                   'data/CM0003/revlearn/CM0003_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0003/revlearn/CM0003_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0003/revlearn/CM0003_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0003/revlearn/CM0003_revlearn_norm_pupil_fig.png',
                   'data/CM0003/revlearn/CM0003_event_times.csv')

    # Participant 4: Great
    pupil_analysis('data/CM0004/revlearn/revlearn14_31_38on04-14-2016.tsv',
                   'data/CM0004/revlearn/CM0004_revlearn_norm_pupil_corr.csv',
                   'data/CM0004/revlearn/CM0004_revlearn_norm_pupil_inc.csv',
                   'data/CM0004/revlearn/CM0004_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0004/revlearn/CM0004_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0004/revlearn/CM0004_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0004/revlearn/CM0004_revlearn_norm_pupil_fig.png',
                   'data/CM0004/revlearn/CM0004_event_times.csv')

    # # Participant 11: Usable (0 < t < 1.5)
    # pupil_analysis('data/CM0011/revlearn/revlearn15_55_45on04-20-2016.tsv',
    #                'data/CM0011/revlearn/CM0011_revlearn_norm_pupil_corr.csv',
    #                'data/CM0011/revlearn/CM0011_revlearn_norm_pupil_inc.csv',
    #                'data/CM0011/revlearn/CM0011_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0011/revlearn/CM0011_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0011/revlearn/CM0011_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0011/revlearn/CM0011_revlearn_norm_pupil_fig.png',
    #                'data/CM0011/revlearn/CM0011_event_times.csv')

    # # Participant 14: Usable (0 < t < .75)
    # pupil_analysis('data/CM0014/revlearn/revlearn15_10_11on04-11-2016.tsv',
    #                'data/CM0014/revlearn/CM0014_revlearn_norm_pupil_corr.csv',
    #                'data/CM0014/revlearn/CM0014_revlearn_norm_pupil_inc.csv',
    #                'data/CM0014/revlearn/CM0014_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0014/revlearn/CM0014_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0014/revlearn/CM0014_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0014/revlearn/CM0014_revlearn_norm_pupil_fig.png',
    #                'data/CM0014/revlearn/CM0014_event_times.csv')

    # Participant 15: Great
    pupil_analysis('data/CM0015/revlearn/revlearn19_07_17on04-12-2016.tsv',
                   'data/CM0015/revlearn/CM0015_revlearn_norm_pupil_corr.csv',
                   'data/CM0015/revlearn/CM0015_revlearn_norm_pupil_inc.csv',
                   'data/CM0015/revlearn/CM0015_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0015/revlearn/CM0015_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0015/revlearn/CM0015_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0015/revlearn/CM0015_revlearn_norm_pupil_fig.png',
                   'data/CM0015/revlearn/CM0015_event_times.csv')

    # # Participant 16: Unusable
    # pupil_analysis('data/CM0016/revlearn/revlearn17_10_15on04-14-2016.tsv',
    #                'data/CM0016/revlearn/CM0016_revlearn_norm_pupil_corr.csv',
    #                'data/CM0016/revlearn/CM0016_revlearn_norm_pupil_inc.csv',
    #                'data/CM0016/revlearn/CM0016_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0016/revlearn/CM0016_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0016/revlearn/CM0016_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0016/revlearn/CM0016_revlearn_norm_pupil_fig.png',
    #                'data/CM0016/revlearn/CM0016_event_times.csv')

    # Participant 19: Good
    pupil_analysis('data/CM0019/revlearn/revlearn11_22_09on04-01-2016.tsv',
                   'data/CM0019/revlearn/CM0019_revlearn_norm_pupil_corr.csv',
                   'data/CM0019/revlearn/CM0019_revlearn_norm_pupil_inc.csv',
                   'data/CM0019/revlearn/CM0019_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0019/revlearn/CM0019_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0019/revlearn/CM0019_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0019/revlearn/CM0019_revlearn_norm_pupil_fig.png',
                   'data/CM0019/revlearn/CM0019_event_times.csv')

    # Participant 20: Great
    pupil_analysis('data/CM0020/revlearn/revlearn12_33_49on04-20-2016.tsv',
                   'data/CM0020/revlearn/CM0020_revlearn_norm_pupil_corr.csv',
                   'data/CM0020/revlearn/CM0020_revlearn_norm_pupil_inc.csv',
                   'data/CM0020/revlearn/CM0020_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0020/revlearn/CM0020_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0020/revlearn/CM0020_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0020/revlearn/CM0020_revlearn_norm_pupil_fig.png',
                   'data/CM0020/revlearn/CM0020_event_times.csv')

    # Participant 21: Good
    pupil_analysis('data/CM0021/revlearn/revlearn10_48_45on04-30-2016.tsv',
                   'data/CM0021/revlearn/CM0021_revlearn_norm_pupil_corr.csv',
                   'data/CM0021/revlearn/CM0021_revlearn_norm_pupil_inc.csv',
                   'data/CM0021/revlearn/CM0021_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0021/revlearn/CM0021_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0021/revlearn/CM0021_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0021/revlearn/CM0021_revlearn_norm_pupil_fig.png',
                   'data/CM0021/revlearn/CM0021_event_times.csv')

    # Participant 22: Great
    pupil_analysis('data/CM0022/revlearn/revlearn14_55_29on04-19-2016.tsv',
                   'data/CM0022/revlearn/CM0022_revlearn_norm_pupil_corr.csv',
                   'data/CM0022/revlearn/CM0022_revlearn_norm_pupil_inc.csv',
                   'data/CM0022/revlearn/CM0022_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0022/revlearn/CM0022_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0022/revlearn/CM0022_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0022/revlearn/CM0022_revlearn_norm_pupil_fig.png',
                   'data/CM0022/revlearn/CM0022_event_times.csv')

    # Participant 24: Good
    pupil_analysis('data/CM0024/revlearn/revlearn13_20_54on04-13-2016.tsv',
                   'data/CM0024/revlearn/CM0024_revlearn_norm_pupil_corr.csv',
                   'data/CM0024/revlearn/CM0024_revlearn_norm_pupil_inc.csv',
                   'data/CM0024/revlearn/CM0024_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0024/revlearn/CM0024_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0024/revlearn/CM0024_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0024/revlearn/CM0024_revlearn_norm_pupil_fig.png',
                   'data/CM0024/revlearn/CM0024_event_times.csv')

    # Participant 25: Great
    pupil_analysis('data/CM0025/revlearn/revlearn14_03_24on04-04-2016.tsv',
                   'data/CM0025/revlearn/CM0025_revlearn_norm_pupil_corr.csv',
                   'data/CM0025/revlearn/CM0025_revlearn_norm_pupil_inc.csv',
                   'data/CM0025/revlearn/CM0025_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0025/revlearn/CM0025_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0025/revlearn/CM0025_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0025/revlearn/CM0025_revlearn_norm_pupil_fig.png',
                   'data/CM0025/revlearn/CM0025_event_times.csv')

    # # Participant 26: Usable (0 < t < 1)
    # pupil_analysis('data/CM0026/revlearn/revlearn14_06_14on04-01-2016.tsv',
    #                'data/CM0026/revlearn/CM0026_revlearn_norm_pupil_corr.csv',
    #                'data/CM0026/revlearn/CM0026_revlearn_norm_pupil_inc.csv',
    #                'data/CM0026/revlearn/CM0026_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0026/revlearn/CM0026_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0026/revlearn/CM0026_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0026/revlearn/CM0026_revlearn_norm_pupil_fig.png',
    #                'data/CM0026/revlearn/CM0026_event_times.csv')
    #
    # # Participant 29: Usable (0 < t < 1)
    # pupil_analysis('data/CM0029/revlearn/revlearn13_57_00on04-22-2016.tsv',
    #                'data/CM0029/revlearn/CM0029_revlearn_norm_pupil_corr.csv',
    #                'data/CM0029/revlearn/CM0029_revlearn_norm_pupil_inc.csv',
    #                'data/CM0029/revlearn/CM0029_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0029/revlearn/CM0029_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0029/revlearn/CM0029_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0029/revlearn/CM0029_revlearn_norm_pupil_fig.png',
    #                'data/CM0029/revlearn/CM0029_event_times.csv')

    # Participant 30: Great
    pupil_analysis('data/CM0030/revlearn/revlearn14_02_39on04-29-2016.tsv',
                   'data/CM0030/revlearn/CM0030_revlearn_norm_pupil_corr.csv',
                   'data/CM0030/revlearn/CM0030_revlearn_norm_pupil_inc.csv',
                   'data/CM0030/revlearn/CM0030_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0030/revlearn/CM0030_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0030/revlearn/CM0030_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0030/revlearn/CM0030_revlearn_norm_pupil_fig.png',
                   'data/CM0030/revlearn/CM0030_event_times.csv')

    # Participant 31: Usable (Correct > Incorrect)
    pupil_analysis('data/CM0031/revlearn/revlearn13_38_55on04-21-2016.tsv',
                   'data/CM0031/revlearn/CM0031_revlearn_norm_pupil_corr.csv',
                   'data/CM0031/revlearn/CM0031_revlearn_norm_pupil_inc.csv',
                   'data/CM0031/revlearn/CM0031_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0031/revlearn/CM0031_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0031/revlearn/CM0031_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0031/revlearn/CM0031_revlearn_norm_pupil_fig.png',
                   'data/CM0031/revlearn/CM0031_event_times.csv')

    # Participant 32: Great
    pupil_analysis('data/CM0032/revlearn/revlearn12_01_11on04-12-2016.tsv',
                   'data/CM0032/revlearn/CM0032_revlearn_norm_pupil_corr.csv',
                   'data/CM0032/revlearn/CM0032_revlearn_norm_pupil_inc.csv',
                   'data/CM0032/revlearn/CM0032_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0032/revlearn/CM0032_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0032/revlearn/CM0032_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0032/revlearn/CM0032_revlearn_norm_pupil_fig.png',
                   'data/CM0032/revlearn/CM0032_event_times.csv')

    # Participant 33: Great
    pupil_analysis('data/CM0033/revlearn/revlearn10_35_33on04-29-2016.tsv',
                   'data/CM0033/revlearn/CM0033_revlearn_norm_pupil_corr.csv',
                   'data/CM0033/revlearn/CM0033_revlearn_norm_pupil_inc.csv',
                   'data/CM0033/revlearn/CM0033_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0033/revlearn/CM0033_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0033/revlearn/CM0033_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0033/revlearn/CM0033_revlearn_norm_pupil_fig.png',
                   'data/CM0033/revlearn/CM0033_event_times.csv')

    # # Participant 34: Usable (0 < t < 1; Correct > Incorrect)
    # pupil_analysis('data/CM0034/revlearn/revlearn10_30_21on04-13-2016.tsv',
    #                'data/CM0034/revlearn/CM0034_revlearn_norm_pupil_corr.csv',
    #                'data/CM0034/revlearn/CM0034_revlearn_norm_pupil_inc.csv',
    #                'data/CM0034/revlearn/CM0034_revlearn_unnorm_pupil_corr.csv',
    #                'data/CM0034/revlearn/CM0034_revlearn_unnorm_pupil_inc.csv',
    #                'data/CM0034/revlearn/CM0034_revlearn_norm_pupil_bytrial_fig.png',
    #                'data/CM0034/revlearn/CM0034_revlearn_norm_pupil_fig.png',
    #                'data/CM0034/revlearn/CM0034_event_times.csv')

    # Participant 35: Great
    pupil_analysis('data/CM0035/revlearn/revlearn11_19_13on04-19-2016.tsv',
                   'data/CM0035/revlearn/CM0035_revlearn_norm_pupil_corr.csv',
                   'data/CM0035/revlearn/CM0035_revlearn_norm_pupil_inc.csv',
                   'data/CM0035/revlearn/CM0035_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0035/revlearn/CM0035_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0035/revlearn/CM0035_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0035/revlearn/CM0035_revlearn_norm_pupil_fig.png',
                   'data/CM0035/revlearn/CM0035_event_times.csv')

    # Participant 36: Great
    pupil_analysis('data/CM0036/revlearn/revlearn15_43_52on04-13-2016.tsv',
                   'data/CM0036/revlearn/CM0036_revlearn_norm_pupil_corr.csv',
                   'data/CM0036/revlearn/CM0036_revlearn_norm_pupil_inc.csv',
                   'data/CM0036/revlearn/CM0036_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0036/revlearn/CM0036_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0036/revlearn/CM0036_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0036/revlearn/CM0036_revlearn_norm_pupil_fig.png',
                   'data/CM0036/revlearn/CM0036_event_times.csv')

    # Participant 40: Good
    pupil_analysis('data/CM0040/revlearn/revlearn12_46_15on04-24-2016.tsv',
                   'data/CM0040/revlearn/CM0040_revlearn_norm_pupil_corr.csv',
                   'data/CM0040/revlearn/CM0040_revlearn_norm_pupil_inc.csv',
                   'data/CM0040/revlearn/CM0040_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0040/revlearn/CM0040_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0040/revlearn/CM0040_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0040/revlearn/CM0040_revlearn_norm_pupil_fig.png',
                   'data/CM0040/revlearn/CM0040_event_times.csv')

    # Participant 41: Great
    pupil_analysis('data/CM0041/revlearn/revlearn16_54_57on04-28-2016.tsv',
                   'data/CM0041/revlearn/CM0041_revlearn_norm_pupil_corr.csv',
                   'data/CM0041/revlearn/CM0041_revlearn_norm_pupil_inc.csv',
                   'data/CM0041/revlearn/CM0041_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0041/revlearn/CM0041_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0041/revlearn/CM0041_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0041/revlearn/CM0041_revlearn_norm_pupil_fig.png',
                   'data/CM0041/revlearn/CM0041_event_times.csv')

    # Participant 42: Great
    pupil_analysis('data/CM0042/revlearn/revlearn15_31_49on04-29-2016.tsv',
                   'data/CM0042/revlearn/CM0042_revlearn_norm_pupil_corr.csv',
                   'data/CM0042/revlearn/CM0042_revlearn_norm_pupil_inc.csv',
                   'data/CM0042/revlearn/CM0042_revlearn_unnorm_pupil_corr.csv',
                   'data/CM0042/revlearn/CM0042_revlearn_unnorm_pupil_inc.csv',
                   'data/CM0042/revlearn/CM0042_revlearn_norm_pupil_bytrial_fig.png',
                   'data/CM0042/revlearn/CM0042_revlearn_norm_pupil_fig.png',
                   'data/CM0042/revlearn/CM0042_event_times.csv')
