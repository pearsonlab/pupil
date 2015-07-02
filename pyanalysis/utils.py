import numpy as np
import pandas as pd
import re
import math
import matplotlib.pyplot as plt
from scipy.stats import norm


def gauss_convolve(x, sigma):
    edge = int(math.ceil(5 * sigma))
    fltr = norm.pdf(range(-edge, edge), loc=0, scale=sigma)
    fltr = fltr / sum(fltr)

    buff = np.ones((1, edge))[0]

    szx = x.size

    xx = np.append((buff * x[0]), x)
    xx = np.append(xx, (buff * x[-1]))

    y = np.convolve(xx, fltr, mode='valid')
    y = y[:szx]
    return y


def plot_with_sem(x, smwid, flag, bin_t, color):
    ntrials = x.columns.size

    xm = np.nanmean(x, 1)
    sd = np.nanstd(x, 1)
    effsamp = np.sum(np.logical_not(np.isnan(x)), 1)
    sem = sd / np.sqrt(effsamp)
    sem = list(sem)

    if smwid != 0:  # smoothing goes here
        xsm = gauss_convolve(xm, smwid)
        xhi = gauss_convolve(xm + sem, smwid)
        xlo = gauss_convolve(xm - sem, smwid)
    else:
        xsm = xm
        xhi = xm + sem
        xlo = xm - sem

    plt.hold(True)
    if flag == 0:
        plt.plot(bin_t, xsm, color=color, linewidth=2.0)
    elif flag == 1:
        x_ptch = np.append(bin_t, bin_t[::-1])
        y_ptch = np.append(xlo, xhi[::-1])

        if ntrials > 1:
            plt.fill(x_ptch, y_ptch, color=color, alpha=0.25, edgecolor=None)

        plt.plot(bin_t, xsm, color=color, linewidth=2.0)
    elif flag == 2:
        plt.plot(bin_t, xsm, color=color, linewidth=2.0)
        plt.plot(
            bin_t, xhi, '--', color=[i * 0.5 for i in color], linewidth=1.0)
        plt.plot(
            bin_t, xlo, '--', color=[i * 0.5 for i in color], linewidth=1.0)
    plt.hold(False)


def cleanseries(data):
    should_clean = ('LeftPupil', 'RightPupil')
    if data.name not in should_clean:
        return data

    bad = (data == -1)

    dd = data.diff()
    sig = np.median(np.absolute(dd) / 0.67449)
    th = 5
    disc = np.absolute(dd) > th * sig

    to_remove = np.nonzero(bad | disc)[0]
    up_one = range(len(to_remove))
    for i in range(len(to_remove)):
        up_one[i] = to_remove[i] + 1
    down_one = range(len(to_remove))
    for i in range(len(to_remove)):
        down_one[i] = to_remove[i] - 1
    isolated = np.intersect1d(up_one, down_one)

    allbad = np.union1d(to_remove, isolated)

    newdat = pd.Series(data)
    newdat[allbad] = np.nan

    goodinds = np.nonzero(np.invert(np.isnan(newdat)))[0]
    if len(goodinds) == 0:
        print "Not enough good data to clean. Aborting."
        return data
    else:
        return pd.Series.interpolate(newdat, method='linear')


def convert_tuples(df):
    should_convert = ('LeftEyePosition3D',
                      'LeftEyePosition3DRelative',
                      'LeftGazePoint3D',
                      'LeftGazePoint2D',
                      'RightEyePosition3D',
                      'RightEyePosition3DRelative',
                      'RightGazePoint3D',
                      'RightGazePoint2D')
    for column in df:  # iterate through column names in DataFrame
        if column in should_convert:
            # convert strings in column to tuples
            df[column] = df[column].apply(string_to_tuple)
    return df


def string_to_tuple(string):
    string = re.sub('[(),]', '', string)
    temp = []
    for s in string.split():
        temp.append(float(s))
    return tuple(temp)


# convert a column in timestamps to seconds
def timestamp_to_seconds(df, convert_column_name, new_column_name):
    df[new_column_name] = (
        df[convert_column_name] - df['Timestamp'][0]) / 1000000.0
    return df


def prepdata(df):  # sets up and formats df read from .tsv to be analyzed
    df = df.reset_index()  # change timestamp into a column and index from 0
    df = convert_tuples(df)  # convert tuple strings to actual tuples
    df = df.apply(cleanseries)  # clean data
    # Add Seconds column
    df = timestamp_to_seconds(df, 'Timestamp', 'Seconds')
    df = df.set_index('Seconds', drop=True)  # set index to Seconds

    df['MeanPupil'] = df[['LeftPupil', 'RightPupil']].mean(
        axis=1)  # Create mean pupil size Series
    return df


def basenorm(chunklist, idx, t_int, flag):
    if not t_int[1] > t_int[0]:
        print 'Normalizing epoch endpoint must be after start point.'
        return None

    norm_chunks = list()

    # normalizes each chunk
    for df in chunklist:
        t_axis = df.index
        sel = np.logical_and(t_axis >= t_int[0], t_axis < t_int[1])
        base = df[sel]
        baseline = base.mean()
        norm_data = pd.DataFrame()

        if flag == 0:
            for column in baseline.index:
                norm_data[column] = df[column] - baseline[column]
        elif flag == 1:
            for column in baseline.index:
                norm_data[column] = df[column] / baseline[column]
        norm_chunks.append(norm_data)

    return norm_chunks


def find_closest(a, target):
    # a must be sorted
    idx = a.searchsorted(target)
    idx = np.clip(idx, 1, len(a) - 1)
    left = a[idx - 1]
    right = a[idx]
    idx -= target - left < right - target
    return idx


def splitseries(ser, ts, t_pre, t_post, t0=0.0):
    xx = ser.values.squeeze()  # convert to 1d numpy array
    tt = ser.index
    nevt = ts.dropna().size

    if t_pre < 0:
        negstart = find_closest(tt, -t_pre)
        nend = find_closest(tt, t_post)
        negslice = slice(1, negstart)
        posslice = slice(0, nend)
        bin_t = (-tt[negslice][::-1]).append(tt[posslice])
    else:
        nstart = find_closest(tt, t_pre)
        nend = find_closest(tt, t_post)
        nslice = slice(nstart, nend)
        bin_t = tt[nslice]

    evtrel = ts - t0

    elist = []
    for time in evtrel:
        if math.isnan(time):
            break
        start_index = find_closest(tt, t_pre + time)
        end_index = find_closest(tt, t_post + time)
        diff = (end_index - start_index) - len(bin_t)
        ss = slice(start_index, end_index - diff)
        elist.append(pd.DataFrame(xx[ss], columns=[time]))
    alltrials = pd.concat(elist, axis=1)
    alltrials = alltrials.set_index(bin_t)
    alltrials.index.name = 'time'
    alltrials.columns = pd.Index(np.arange(nevt), name='trial')
    return alltrials


def evtsplit(df, events, t_pre, t_post, t0=0.0):
    """
    split frame into chunks (t_pre, t_post) around each event in events
    t_pre should be < 0 for times before event
    if multiple series are passed, return a list of dataframes, one per series
    if return_by_event is True, return a list of dataframes, one per event
    """

    chunklist = []
    for col in df.columns.values:
        chunklist.append(splitseries(df[col], events, t_pre, t_post, t0))
    idx = df.columns

    return chunklist, idx

if __name__ == "__main__":
    # GUI_app = wx.App()

    # path_dlg = wx.FileDialog(None, "Open TSV file", "", "",
    #                          "TSV files (*.tsv)|*.tsv", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    # while path_dlg.ShowModal() == wx.ID_CANCEL:  # quit if cancelled
    #     sys.exit()

    # datafile_path = path_dlg.GetPath()

    datafile_path = '/Users/shariqiqbal/data/test/PST/09_07_58on06-30-2015.tsv'

    df = pd.DataFrame.from_csv(datafile_path, sep='\t')

    df = prepdata(df)
