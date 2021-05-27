import pandas as pd


def pupil_aggregate():
    """
    :return: aggregates data from all participants into one .csv
    """
    good_data = [4, 11, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26, 31, 33, 34, 35, 36, 40, 41, 42]
    good_data = [int(participant) for participant in good_data]
    starting_norm_df = pd.read_csv(
        '../pyanalysis/data/CM0004/lighttest/CM0004_lighttest_norm_dvs.csv')
    starting_unnorm_df = pd.read_csv(
        '../pyanalysis/data/CM0004/lighttest/CM0004_lighttest_unnorm_dvs.csv')
    starting_norm_avg_df = pd.read_csv(
        '../pyanalysis/data/CM0004/lighttest/CM0004_lighttest_norm_dvs_avg.csv')
    starting_unnorm_avg_df = pd.read_csv(
        '../pyanalysis/data/CM0004/lighttest/CM0004_lighttest_unnorm_dvs_avg.csv')

    for p_num in good_data[1:]:
        p_num = str(p_num)
        if len(p_num) == 1:
            starting_norm_df = starting_norm_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/lighttest/CM000' + p_num + '_lighttest_norm_dvs.csv'))
            starting_unnorm_df = starting_unnorm_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/lighttest/CM000' + p_num + '_lighttest_unnorm_dvs.csv'))
            starting_norm_avg_df = starting_norm_avg_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/lighttest/CM000' + p_num + '_lighttest_norm_dvs_avg.csv'))
            starting_unnorm_avg_df = starting_unnorm_avg_df.append(pd.read_csv(
                '../pyanalysis/data/CM000' + p_num + '/lighttest/CM000' + p_num + '_lighttest_unnorm_dvs_avg.csv'))
        else:
            starting_norm_df = starting_norm_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/lighttest/CM00' + p_num + '_lighttest_norm_dvs.csv'))
            starting_unnorm_df = starting_unnorm_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/lighttest/CM00' + p_num + '_lighttest_unnorm_dvs.csv'))
            starting_norm_avg_df = starting_norm_avg_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/lighttest/CM00' + p_num + '_lighttest_norm_dvs_avg.csv'))
            starting_unnorm_avg_df = starting_unnorm_avg_df.append(pd.read_csv(
                '../pyanalysis/data/CM00' + p_num + '/lighttest/CM00' + p_num + '_lighttest_unnorm_dvs_avg.csv'))
    
    starting_norm_df = starting_norm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0001/lighttest/CM0001_lighttest_norm_dvs.csv'))
    starting_unnorm_df = starting_unnorm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0001/lighttest/CM0001_lighttest_unnorm_dvs.csv'))
    starting_norm_avg_df = starting_norm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0001/lighttest/CM0001_lighttest_norm_dvs_avg.csv'))
    starting_unnorm_avg_df = starting_unnorm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0001/lighttest/CM0001_lighttest_unnorm_dvs_avg.csv'))

    starting_norm_df = starting_norm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0003/lighttest/CM0003_lighttest_norm_dvs.csv'))
    starting_unnorm_df = starting_unnorm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0003/lighttest/CM0003_lighttest_unnorm_dvs.csv'))
    starting_norm_avg_df = starting_norm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0003/lighttest/CM0003_lighttest_norm_dvs_avg.csv'))
    starting_unnorm_avg_df = starting_unnorm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0003/lighttest/CM0003_lighttest_unnorm_dvs_avg.csv'))

    starting_norm_df = starting_norm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_norm_dvs.csv'))
    starting_unnorm_df = starting_unnorm_df.append(pd.read_csv(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_unnorm_dvs.csv'))
    starting_norm_avg_df = starting_norm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_norm_dvs_avg.csv'))
    starting_unnorm_avg_df = starting_unnorm_avg_df.append(pd.read_csv(
        '../pyanalysis/data/CM0029/lighttest/CM0029_lighttest_unnorm_dvs_avg.csv'))

    starting_norm_df.rename(columns={'Unnamed: 0': 'trial'}, inplace=True)
    starting_unnorm_df.rename(columns={'Unnamed: 0': 'trial'}, inplace=True)

    p_id = {'participant': []}
    for num in good_data:
        p_id['participant'].extend([num, num, num, num])
    p_id['participant'].extend([1.0, 3.0, 3.0, 3.0, 29.0, 29.0])

    starting_norm_avg_df.rename(columns={'Unnamed: 0': 'ignore'}, inplace=True)
    starting_unnorm_avg_df.rename(columns={'Unnamed: 0': 'ignore'}, inplace=True)

    p_id_avg = {'participant': good_data}
    p_id_avg['participant'].extend([1.0, 3.0, 29.0])

    starting_norm_df = starting_norm_df.reset_index(drop=True)
    starting_unnorm_df = starting_unnorm_df.reset_index(drop=True)
    starting_norm_avg_df = starting_norm_avg_df.reset_index(drop=True)
    starting_unnorm_avg_df = starting_unnorm_avg_df.reset_index(drop=True)

    starting_norm_df = pd.concat([starting_norm_df, pd.DataFrame(p_id)], axis=1)
    starting_unnorm_df = pd.concat([starting_unnorm_df, pd.DataFrame(p_id)], axis=1)
    starting_norm_avg_df = pd.concat([starting_norm_avg_df, pd.DataFrame(p_id_avg)], axis=1)
    starting_unnorm_avg_df = pd.concat([starting_unnorm_avg_df, pd.DataFrame(p_id_avg)], axis=1)

    starting_norm_df.to_csv('../pyanalysis/lighttest_norm_dvs_aggregated.csv', index=False)
    starting_unnorm_df.to_csv('../pyanalysis/lighttest_unnorm_dvs_aggregated.csv', index=False)
    starting_norm_avg_df.to_csv('../pyanalysis/lighttest_norm_dvs_avg_aggregated.csv', index=False)
    starting_unnorm_avg_df.to_csv('../pyanalysis/lighttest_unnorm_dvs_avg_aggregated.csv', index=False)


if __name__ == '__main__':
    pupil_aggregate()
