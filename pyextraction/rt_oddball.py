import pandas as pd
from numpy import nanmean

all_rts_avg = []

def rt_extract(datafile_input_path):
    """
    :param datafile_input_path: the input datafile path
    :return: a .csv file containing the event time specifics
    """
    df = pd.read_csv(datafile_input_path)
    df['rt'] = df['presstimes'] - df['soundtimes']
    rt = df['rt'].to_list()
    rt_avg = nanmean(rt)
    all_rts_avg.append(rt_avg)


if __name__ == '__main__':
    # unusable_data = [16]
    # usable = [22, 29, 31, 32]
    # std_exceed_odd = [31, 33]
    good_data = [1, 3, 4, 11, 14, 15, 19, 20, 21, 22, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42]
    for p_num in good_data:
        p_num = str(p_num)
        if len(p_num) == 1:
            rt_extract(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_event_times.csv')
        else:
            rt_extract(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_event_times.csv')

    pd.DataFrame({'participant': good_data, 'rt_avg': all_rts_avg}).to_csv('../pyanalysis/rt_oddball.csv', index=False)
