import pandas as pd
import numpy as np


def tsmom(start_date, direction=1, **kwargs):
    data = kwargs['data']
    data['UCODE'] = data['EXCHANGE'] * 1000 + data['PCODE']
    calendar = data['TDATE'].drop_duplicates().tolist()

    window_days = kwargs['window_days']

    if direction == 1:
        index_name = 'tsmom_d' + str(window_days)
    else:
        index_name = 'tsrev_d' + str(window_days)

    start_index = calendar.index(np.array(calendar)[np.array(calendar) >= start_date][0])

    positions = pd.DataFrame()
    for i in range(start_index, len(calendar) - 1):
        t_date = calendar[i]
        lookback_date = calendar[i - window_days]
        data_t = data[
            np.array(data['TDATE'] == t_date) & np.array(data['VOL'] > kwargs['min_volume'])
            ][['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE']]
        data_lookback = data[data['TDATE'] == lookback_date][['TDATE', 'UCODE', 'CLOSE']]

        data_t = pd.merge(
            data_t[['EXCHANGE', 'PCODE', 'UCODE', 'CLOSE']],
            data_lookback[['UCODE', 'CLOSE']].rename(columns={'CLOSE': 'CLOSE0'}),
            on='UCODE', how='left'
        )

        data_t['FACTORVALUE'] = data_t['CLOSE'] / data_t['CLOSE0'] - 1
        data_t['POS'] = data_t['FACTORVALUE'] / data_t['FACTORVALUE'].abs() * direction
        data_t['POS'] = data_t['POS'].fillna(0)

        data_tomorrow = data[np.array(data['TDATE'] == calendar[i + 1])]

        data_t = pd.merge(
            data_t, data_tomorrow[['UCODE', 'CLOSE']].rename(columns={'CLOSE': 'CLOSE1'}),
            on='UCODE', how='left'
        )

        data_t['RETURN'] = (data_t['CLOSE1'] / data_t['CLOSE'] - 1) * data_t['POS']

        # index_all.append(index_all[-1] * (1 + data_t['RETURN'].mean()))
        data_t['TDATE'] = calendar[i + 1]
        data_t['FACTOR'] = index_name
        if sum(data_t['POS'] != 0) > 0:
            data_t['WEIGHT'] = 1 / sum(data_t['POS'] != 0)
        else:
            data_t['WEIGHT'] = 0
        positions = pd.concat([positions, data_t])
        print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    return positions.reset_index(drop=True)


def tsrev(start_date, **kwargs):
    return tsmom(start_date=start_date, direction=-1, **kwargs)


def tswr(start_date, **kwargs):
    # 根据前一日仓单数据计算
    # 当日收盘价开平仓
    data = kwargs['data']
    data_wr = kwargs['data_wr']
    data['UCODE'] = data['EXCHANGE'] * 1000 + data['PCODE']
    data_wr['UCODE'] = data_wr['EXCHANGE'] * 1000 + data_wr['PCODE']

    calendar = data['TDATE'].drop_duplicates().tolist()

    window_days = kwargs['window_days']
    index_name = 'tswr_d' + str(window_days)

    start_index = calendar.index(np.array(calendar)[np.array(calendar) >= start_date][0])

    positions = pd.DataFrame()
    for i in range(start_index, len(calendar) - 1):
        t_date = calendar[i]
        data_wr_0 = data_wr[data_wr['TDATE'] == calendar[i - 1 - window_days]][['UCODE', 'PNAME', 'WRQCURRENT']]
        data_wr_t = data_wr[data_wr['TDATE'] == calendar[i - 1]][['UCODE', 'WRQCURRENT']]

        data_wr_range = pd.merge(
            data_wr_0.rename(columns={'WRQCURRENT': 'WR0'}),
            data_wr_t.rename(columns={'WRQCURRENT': 'WR1'}),
            on='UCODE', how='left'
        )
        data_wr_range['FACTORVALUE'] = data_wr_range['WR1'] - data_wr_range['WR0'] #- 1
        data_wr_range['POS'] = data_wr_range['FACTORVALUE'] / data_wr_range['FACTORVALUE'].abs() * -1
        data_wr_range['POS'] = data_wr_range['POS'].fillna(0)

        data_t = data[
            np.array(data['TDATE'] == t_date) & np.array(data['VOL'] > kwargs['min_volume'])
            ][['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE']]

        data_tomorrow = data[np.array(data['TDATE'] == calendar[i + 1])]

        data_t = pd.merge(data_t[['UCODE', 'CLOSE']], data_wr_range, on='UCODE', how='inner')

        data_t = pd.merge(
            data_t,
            data_tomorrow.rename(columns={'CLOSE': 'CLOSE1'}),
            on='UCODE', how='left'
        )

        data_t['RETURN'] = (data_t['CLOSE1'] / data_t['CLOSE'] - 1) * data_t['POS']

        # index_all.append(index_all[-1] * (1 + data_t['RETURN'].mean()))
        data_t['TDATE'] = calendar[i + 1]
        data_t['FACTOR'] = index_name
        if sum(data_t['POS'] != 0) > 0:
            data_t['WEIGHT'] = 1 / sum(data_t['POS'] != 0)
        else:
            data_t['WEIGHT'] = 0
        positions = pd.concat([positions, data_t])
        print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    return positions[
        ['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE', 'CLOSE1', 'POS', 'RETURN', 'FACTORVALUE', 'FACTOR', 'WEIGHT']
    ].reset_index(drop=True)


def carry(start_date, **kwargs):
    data = kwargs['data']
    data['UCODE'] = data['EXCHANGE'] * 1000 + data['PCODE']
    calendar = data['TDATE'].drop_duplicates().tolist()

    window_days = kwargs['window_days']
    quantile = kwargs['quantile']
    index_name = 'carry_d' + str(window_days) + '_q' + str(quantile)

    start_index = calendar.index(np.array(calendar)[np.array(calendar) >= start_date][0])

    positions = pd.DataFrame()
    for i in range(start_index, len(calendar) - 1):
        t_date = calendar[i]
        lookback_date = calendar[i - window_days]
        data_ry = data[
            np.array(data['TDATE'] <= t_date)
            & np.array(data['TDATE'] > lookback_date)
            ].groupby('UCODE').mean().reset_index()[['UCODE', 'RY']]
        data_t = data[
            np.array(data['TDATE'] == t_date)
            & np.array(data['OI'] > kwargs['min_volume'])
            ]
        data_t = pd.merge(data_t.rename(columns={'RY': 'RY0'}), data_ry, on='UCODE')
        data_tomorrow = data[
            np.array(data['TDATE'] == calendar[i + 1])
        ]

        quantile_p = data_t['RY'].quantile(quantile / 100)
        quantile_n = data_t['RY'].quantile(1 - quantile / 100)

        data_t['POS'] = data_t['RY'].apply(lambda x: 1 if x > quantile_p else (-1 if x < quantile_n else 0))
        data_t = pd.merge(
            data_t, data_tomorrow[['UCODE', 'CLOSE']].rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE', how='left'
        )
        data_t['RETURN'] = (data_t['CLOSE1'] / data_t['CLOSE'] - 1) * data_t['POS']
        pos_long = sum(data_t['POS'] == 1)
        pos_short = sum(data_t['POS'] == -1)
        data_t['WEIGHT'] = data_t['POS'].apply(
            lambda x: 0.5 / pos_long if x == 1 else (0.5 / pos_short if x == -1 else 0)
        )
        pos = data_t.rename(columns={'RY': 'FACTORVALUE'})
        # pos_long = data_t[data_t['RY'] > quantile_p][
        #     ['EXCHANGE', 'PCODE', 'UCODE', 'CLOSE', 'RY']
        # ].reset_index(drop=True)
        # pos_short = data_t[data_t['RY'] < quantile_n][
        #     ['EXCHANGE', 'PCODE', 'UCODE', 'CLOSE', 'RY']
        # ].reset_index(drop=True)
        # pos_long_tomorrow = data_tomorrow[
        #     np.array(data_tomorrow['UCODE'].isin(pos_long['UCODE'].tolist()))
        # ][['UCODE', 'CLOSE']]
        # pos_short_tomorrow = data_tomorrow[
        #     np.array(data_tomorrow['UCODE'].isin(pos_short['UCODE'].tolist()))
        # ][['UCODE', 'CLOSE']]
        #
        # pos_long_ret = pd.merge(pos_long, pos_long_tomorrow.rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE')
        # pos_short_ret = pd.merge(pos_short, pos_short_tomorrow.rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE')
        #
        # pos_long_ret['POS'] = 1
        # pos_short_ret['POS'] = -1
        # pos = pd.concat([pos_long_ret, pos_short_ret]).rename(columns={'RY': 'FACTORVALUE'})
        # pos['RETURN'] = (pos['CLOSE1'] / pos['CLOSE'] - 1) * pos['POS']

        pos['TDATE'] = calendar[i + 1]
        pos['FACTOR'] = index_name

        positions = pd.concat([positions, pos])
        print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    return positions[
        ['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE', 'CLOSE1', 'POS', 'RETURN', 'FACTORVALUE', 'FACTOR', 'WEIGHT']
    ].reset_index(drop=True)


def xsmom(start_date, direction=1, **kwargs):
    data = kwargs['data']
    data['UCODE'] = data['EXCHANGE'] * 1000 + data['PCODE']
    calendar = data['TDATE'].drop_duplicates().tolist()

    window_days = kwargs['window_days']
    quantile = kwargs['quantile']

    if direction == 1:
        index_name = 'xsmom_d' + str(window_days) + '_q' + str(quantile)
    else:
        index_name = 'xsrev_d' + str(window_days) + '_q' + str(quantile)

    start_index = calendar.index(np.array(calendar)[np.array(calendar) >= start_date][0])

    positions = pd.DataFrame()

    for i in range(start_index, len(calendar) - 1):
        t_date = calendar[i]
        lookback_date = calendar[i - window_days]
        data_t = data[
            np.array(data['TDATE'] == t_date) & np.array(data['VOL'] > kwargs['min_volume'])
            ][['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE']]
        data_lookback = data[data['TDATE'] == lookback_date][['TDATE', 'UCODE', 'CLOSE']]
        data_tomorrow = data[
            np.array(data['TDATE'] == calendar[i + 1])
        ]

        data_t = pd.merge(
            data_t[['EXCHANGE', 'PCODE', 'UCODE', 'CLOSE']],
            data_lookback[['UCODE', 'CLOSE']].rename(columns={'CLOSE': 'CLOSE0'}),
            on='UCODE', how='left'
        )
        data_t['FACTORVALUE'] = data_t['CLOSE'] / data_t['CLOSE0'] - 1

        quantile_p = data_t['FACTORVALUE'].quantile(quantile / 100)
        quantile_n = data_t['FACTORVALUE'].quantile(1 - quantile / 100)

        data_t['POS'] = data_t['FACTORVALUE'].apply(
            lambda x: direction if x > quantile_p else (-direction if x < quantile_n else 0)
        )
        data_t = pd.merge(
            data_t, data_tomorrow[['UCODE', 'CLOSE']].rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE', how='left'
        )
        data_t['RETURN'] = (data_t['CLOSE1'] / data_t['CLOSE'] - 1) * data_t['POS']
        pos_long = sum(data_t['POS'] == 1)
        pos_short = sum(data_t['POS'] == -1)
        data_t['WEIGHT'] = data_t['POS'].apply(
            lambda x: 0.5 / pos_long if x == 1 else (0.5 / pos_short if x == -1 else 0)
        )
        pos = data_t

        # pos_long = data_t[data_t['FACTORVALUE'] > quantile_p][
        #     ['EXCHANGE', 'PCODE', 'UCODE', 'FACTORVALUE', 'CLOSE']
        # ].reset_index(drop=True)
        # pos_short = data_t[data_t['FACTORVALUE'] < quantile_n][
        #     ['EXCHANGE', 'PCODE', 'UCODE', 'FACTORVALUE', 'CLOSE']
        # ].reset_index(drop=True)
        #

        #
        # pos_long_tomorrow = data_tomorrow[
        #     np.array(data_tomorrow['UCODE'].isin(pos_long['UCODE'].tolist()))
        # ][['UCODE', 'CLOSE']]
        # pos_short_tomorrow = data_tomorrow[
        #     np.array(data_tomorrow['UCODE'].isin(pos_short['UCODE'].tolist()))
        # ][['UCODE', 'CLOSE']]
        #
        # pos_long_ret = pd.merge(pos_long, pos_long_tomorrow.rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE')
        # pos_short_ret = pd.merge(pos_short, pos_short_tomorrow.rename(columns={'CLOSE': 'CLOSE1'}), on='UCODE')
        #
        # pos_long_ret['POS'] = direction
        # pos_short_ret['POS'] = -direction
        # pos = pd.concat([pos_long_ret, pos_short_ret])
        # pos['RETURN'] = (pos['CLOSE1'] / pos['CLOSE'] - 1) * pos['POS']

        pos['TDATE'] = calendar[i + 1]
        pos['FACTOR'] = index_name
        positions = pd.concat([positions, pos])
        print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    return positions.reset_index(drop=True)


def xsrev(start_date, **kwargs):
    return xsmom(start_date=start_date, direction=-1, **kwargs)