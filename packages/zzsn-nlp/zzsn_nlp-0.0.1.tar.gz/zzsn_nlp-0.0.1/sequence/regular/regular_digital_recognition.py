#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : regular_digital_recognition
# @Author   : LiuYan
# @Time     : 2021/3/31 10:04

import re


class RDR(object):
    def __init__(self):
        super(RDR, self).__init__()
        # 10.98亿 卡塔尔里亚尔
        self._end_money = ['元', '磅']
        self._end_data = ['年', '月', '日', '天']

    def digital_sorting(self, word_list, tag_list) -> [list, list]:  # 数字分类/筛选
        number_list, money_list = [], []
        for index in range(len(word_list)):
            if tag_list[index] == 'm' and tag_list[index + 1] == 'q' and word_list[index + 1] not in self._end_data:
                result = word_list[index] + word_list[index + 1]
                if bool(re.search(r'\d', result)):
                    if index + 2 < len(tag_list) and tag_list[index + 2] == 'n':
                        result += word_list[index + 2]
                    # 判断是否为金额
                    if result[-1] in self._end_money:
                        money_list.append(result)
                    elif len(result) > 6 and result[-6:] == '卡塔尔里亚尔':
                        money_list.append(result)
                    else:
                        number_list.append(result)
                    # print(result)
        number_list, money_list = list(set(number_list)), list(set(money_list))
        return [number_list, money_list]
