import pandas as pd


def pupil_aggregate():
    """
    :return: aggregates data from all participants into one .csv
    """
    # unusable_data = [16]
    # usable = [22, 29, 31, 32]
    # std_exceed_odd = [31, 33]
    good_data = [1, 3, 4, 11, 14, 15, 19, 20, 21, 22, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42]
    starting_norm_std_df = pd.read_csv(
        '../pyanalysis/data/CM0001/oddball/CM0001_oddball_norm_std_dvs.csv')
    starting_unnorm_std_df = pd.read_csv(
        '../pyanalysis/data/CM0001/oddball/CM0001_oddball_unnorm_std_dvs.csv')
    starting_norm_odd_df = pd.read_csv(
        '../pyanalysis/data/CM0001/oddball/CM0001_oddball_norm_odd_dvs.csv')
    starting_unnorm_odd_df = pd.read_csv(
        '../pyanalysis/data/CM0001/oddball/CM0001_oddball_unnorm_odd_dvs.csv')

    for p_num in good_data[1:]:
        p_num = str(p_num)
        if len(p_num) == 1:
            starting_norm_std_df = starting_norm_std_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_std_dvs.csv'))
            starting_unnorm_std_df = starting_unnorm_std_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_std_dvs.csv'))
            starting_norm_odd_df = starting_norm_odd_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_norm_odd_dvs.csv'))
            starting_unnorm_odd_df = starting_unnorm_odd_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/oddball/CM000' + p_num + '_oddball_unnorm_odd_dvs.csv'))
        else:
            starting_norm_std_df = starting_norm_std_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_std_dvs.csv'))
            starting_unnorm_std_df = starting_unnorm_std_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_std_dvs.csv'))
            starting_norm_odd_df = starting_norm_odd_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_norm_odd_dvs.csv'))
            starting_unnorm_odd_df = starting_unnorm_odd_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/oddball/CM00' + p_num + '_oddball_unnorm_odd_dvs.csv'))

    p_id_std = {'participant': good_data, 'sound_type': []}
    p_id_std['sound_type'] = ['std'] * len(good_data)

    p_id_odd = {'participant': good_data, 'sound_type': []}
    p_id_odd['sound_type'] = ['odd'] * len(good_data)

    starting_norm_std_df = starting_norm_std_df.reset_index(drop=True)
    starting_unnorm_std_df = starting_unnorm_std_df.reset_index(drop=True)
    starting_norm_odd_df = starting_norm_odd_df.reset_index(drop=True)
    starting_unnorm_odd_df = starting_unnorm_odd_df.reset_index(drop=True)

    starting_norm_std_df = pd.concat([starting_norm_std_df, pd.DataFrame(p_id_std)], axis=1)
    starting_unnorm_std_df = pd.concat([starting_unnorm_std_df, pd.DataFrame(p_id_std)], axis=1)
    starting_norm_odd_df = pd.concat([starting_norm_odd_df, pd.DataFrame(p_id_odd)], axis=1)
    starting_unnorm_odd_df = pd.concat([starting_unnorm_odd_df, pd.DataFrame(p_id_odd)], axis=1)

    norm = pd.concat([starting_norm_std_df, starting_norm_odd_df])
    unnorm = pd.concat([starting_unnorm_std_df, starting_unnorm_odd_df])

    norm.to_csv('../pyanalysis/oddball_norm_dvs_aggregated.csv', index=False)
    unnorm.to_csv('../pyanalysis/oddball_unnorm_dvs_aggregated.csv', index=False)


if __name__ == '__main__':
    pupil_aggregate()
