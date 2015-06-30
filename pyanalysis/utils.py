import numpy as np
import pandas as pd
import sys
import wx
import re


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

    df['MeanPupil'] = df[['LeftPupil', 'RightPupil']].mean(
        axis=1)  # Create mean pupil size Series
    return df


def basenorm(df, taxis, Tint, flag):  # taxis is name of axis within df
    if not Tint[1] > Tint[0]:
        print 'Normalizing epoch endpoint must be after start point.'
        return None

    sel = np.logical_and(df[taxis] >= Tint[0], df[taxis] < Tint[1])
    B = df[sel]
    baseline = B.mean()
    Dnorm = pd.DataFrame()

    if flag == 0:
        for column in baseline.index:
            Dnorm[column] = df[column] - baseline[column]
    elif flag == 1:
        for column in baseline.index:
            Dnorm[column] = df[column] / baseline[column]

    return Dnorm

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

    basenorm(df, 'Seconds', [float('-inf'), 0], 0)
