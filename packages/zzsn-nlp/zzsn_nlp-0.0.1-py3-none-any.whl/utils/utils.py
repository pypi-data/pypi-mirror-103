#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : utils
# @Author   : LiuYan
# @Time     : 2021/4/16 17:54

from __future__ import unicode_literals, print_function, division

import time
import xlsxwriter


def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        print('......begin     {0:8s}......'.format(f.__name__))
        result = f(*args, **kw)
        te = time.time()
        print('......finish    {0:8s}, took:{1:.4f} sec......'.format(f.__name__, te - ts))
        return result

    return timed


def list2xlsx(result_list=None, xlsx_path=None):
    """

    :param result_lists: [
                            {
                                'id': 1,
                                'title': 't',
                                ...
                            }
                            ...
                        ]
    :param xlsx_path: '/home/zzsn/liuyan/result/result.xlsx'
    :return:
    """
    workbook = xlsxwriter.Workbook(xlsx_path)
    worksheet = workbook.add_worksheet('sheet1')
    worksheet.write_row(row=0, col=0, data=list(result_list[0].keys()))

    for row_index, result_dict in enumerate(result_list):
        worksheet.write_row(row=row_index + 1, col=0, data=list(result_dict.values()))

    workbook.close()
