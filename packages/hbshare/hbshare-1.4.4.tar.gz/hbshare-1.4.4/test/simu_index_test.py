#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :simu_index_test.py
# @Time      :2021/4/27 2:18 下午
# @Author    :meng.lv

import hbshare as hbs
import pandas  as pd
import time

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)  # 设置打印宽度(**重要**)
    data = hbs.simu_index("RISK_DOWNSIDE_WEEK","S00748", '20210423', ["2101"],show_log=True)
    print(data)
    si = hbs.SimuIndex("RISK_MAX_DRAWDOWN_RANK_DAY",show_log=True)
    dt = si.get("S00748", '20210419', ["2101"])
    print(dt)
    c = si.get_config()
    print(c)
