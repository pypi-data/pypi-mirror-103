#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_stats
# @Author   : LiuYan
# @Time     : 2021/4/15 16:52

import pandas as pd

from collections import Counter


def stat_fx():
    """

    :return:
    """
    data_list = pd.read_excel('sample/风险训练集.xlsx')
    label_list = data_list['label']
    print(Counter(label_list))


if __name__ == '__main__':
    stat_fx()
    pass
