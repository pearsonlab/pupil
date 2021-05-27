import pandas as pd


def pupil_aggregate():
    """
    :return: aggregates data from all participants into one .csv
    """
    # unusable_data = [16]
    # usable = [11, 14, 26, 29, 31, 34]
    # corr_exceed_inc = [31, 34]
    good_data = [1, 3, 4, 11, 14, 15, 19, 20, 21, 22, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42]
    starting_norm_corr_df = pd.read_csv(
        '../pyanalysis/data/CM0001/revlearn/CM0001_revlearn_norm_corr_dvs.csv')
    starting_unnorm_corr_df = pd.read_csv(
        '../pyanalysis/data/CM0001/revlearn/CM0001_revlearn_unnorm_corr_dvs.csv')
    starting_norm_inc_df = pd.read_csv(
        '../pyanalysis/data/CM0001/revlearn/CM0001_revlearn_norm_inc_dvs.csv')
    starting_unnorm_inc_df = pd.read_csv(
        '../pyanalysis/data/CM0001/revlearn/CM0001_revlearn_unnorm_inc_dvs.csv')

    for p_num in good_data[1:]:
        p_num = str(p_num)
        if len(p_num) == 1:
            starting_norm_corr_df = starting_norm_corr_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/revlearn/CM000' + p_num + '_revlearn_norm_corr_dvs.csv'))
            starting_unnorm_corr_df = starting_unnorm_corr_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/revlearn/CM000' + p_num + '_revlearn_unnorm_corr_dvs.csv'))
            starting_norm_inc_df = starting_norm_inc_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/revlearn/CM000' + p_num + '_revlearn_norm_inc_dvs.csv'))
            starting_unnorm_inc_df = starting_unnorm_inc_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/revlearn/CM000' + p_num + '_revlearn_unnorm_inc_dvs.csv'))
        else:
            starting_norm_corr_df = starting_norm_corr_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/revlearn/CM00' + p_num + '_revlearn_norm_corr_dvs.csv'))
            starting_unnorm_corr_df = starting_unnorm_corr_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/revlearn/CM00' + p_num + '_revlearn_unnorm_corr_dvs.csv'))
            starting_norm_inc_df = starting_norm_inc_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/revlearn/CM00' + p_num + '_revlearn_norm_inc_dvs.csv'))
            starting_unnorm_inc_df = starting_unnorm_inc_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/revlearn/CM00' + p_num + '_revlearn_unnorm_inc_dvs.csv'))

    p_id_corr = {'participant': good_data, 'response_type': []}
    p_id_inc = {'participant': good_data, 'response_type': []}
    p_id_corr['response_type'] = ['corr'] * len(good_data)
    p_id_inc['response_type'] = ['inc'] * len(good_data)

    starting_norm_corr_df = starting_norm_corr_df.reset_index(drop=True)
    starting_unnorm_corr_df = starting_unnorm_corr_df.reset_index(drop=True)
    starting_norm_inc_df = starting_norm_inc_df.reset_index(drop=True)
    starting_unnorm_inc_df = starting_unnorm_inc_df.reset_index(drop=True)

    starting_norm_corr_df = pd.concat([starting_norm_corr_df, pd.DataFrame(p_id_corr)], axis=1)
    starting_unnorm_corr_df = pd.concat([starting_unnorm_corr_df, pd.DataFrame(p_id_corr)], axis=1)
    starting_norm_inc_df = pd.concat([starting_norm_inc_df, pd.DataFrame(p_id_inc)], axis=1)
    starting_unnorm_inc_df = pd.concat([starting_unnorm_inc_df, pd.DataFrame(p_id_inc)], axis=1)

    norm = pd.concat([starting_norm_corr_df, starting_norm_inc_df])
    unnorm = pd.concat([starting_unnorm_corr_df, starting_unnorm_inc_df])

    norm.to_csv('../pyanalysis/revlearn_norm_dvs_aggregated.csv', index=False)
    unnorm.to_csv('../pyanalysis/revlearn_unnorm_dvs_aggregated.csv', index=False)


if __name__ == '__main__':
    pupil_aggregate()
