#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_stats
# @Author   : LiuYan
# @Time     : 2021/3/11 11:12

import pandas as pd

total_list = ['资讯 研究热词', '研究领域 地域',
              '研究领域 企业',
              '研究领域 资讯',
              '研究领域 专家',
              '研究领域 领导',
              '研究领域 研究领域',
              '地域 资讯',
              '专家 地域',
              '专家 企业',
              '企业 资讯',
              '专家 专家',
              '专家 资讯',
              '领导 企业',
              '领导 地域',
              '领导 专家',
              '领导 资讯',
              '领导 领导',
              '企业 企业']


def stat(data_path: str):
    total_dict = {
        '资讯 研究热词': [],
        '研究领域 地域': [],
        '研究领域 企业': [],
        '研究领域 资讯': [],
        '研究领域 专家': [],
        '研究领域 领导': [],
        '研究领域 研究领域': [],
        '地域 资讯': [],
        '专家 地域': [],
        '专家 企业': [],
        '企业 资讯': [],
        '专家 专家': [],
        '专家 资讯': [],
        '领导 企业': [],
        '领导 地域': [],
        '领导 专家': [],
        '领导 资讯': [],
        '领导 领导': [],
        '企业 企业': []
    }

    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        le_list, le_label_list, re_list, ri_list, ri_label_list, id_list, bo_list = [], [], [], [], [], [], []
        data_list = []
        double_list = []
        for line in lines:
            list_ = line.strip('\n').split(',')

            left = list_[0].strip()[1: -1]
            left_label = list_[1].strip()[1: -1]
            relation = list_[2].strip()[1: -1]
            right = list_[3].strip()[1: -1]
            right_label = list_[4].strip()[1: -1]
            corpusID = list_[5].strip()
            bool_ = True if list_[6].strip()[1: -1] == '1' else False

            le_list.append(left)
            le_label_list.append(left_label)
            re_list.append(relation)
            ri_list.append(right)
            ri_label_list.append(right_label)
            # id_list.append(corpusID)
            bo_list.append(bool_)
            double_list.append(left_label + ' ' + right_label)

            # data_list.append({
            #     'left': left,
            #     'left_label': left_label,
            #     'relation': relation,
            #     'right': right,
            #     'right_label': right_label,
            #     'corpusID': corpusID,
            #     'valid': bool_
            # })

            bool_dt = False
            for double_type in total_list:
                if bool_dt:
                    break
                type_L, type_R = double_type.split(' ')
                if left_label == type_L and right_label == type_R:
                    total_dict[double_type].append({
                        'left': left,
                        'left_label': left_label,
                        'relation': relation,
                        'right': right,
                        'right_label': right_label,
                        'corpusID': corpusID,
                        'bool': bool_
                    })
                    bool_dt = True
                elif left_label == type_R and right_label == type_L:
                    total_dict[double_type].append({
                        'left': left,
                        'left_label': left_label,
                        'relation': relation,
                        'right': right,
                        'right_label': right_label,
                        'corpusID': corpusID,
                        'bool': bool_
                    })
                    bool_dt = True
            if not bool_dt:
                print('得了呵的！！！')

    # result_re = pd.value_counts(re_list)
    result_bo = pd.value_counts(bo_list)
    # result_double = pd.value_counts(double_list)
    # print(result_re)
    print(result_bo)
    # print(result_double)

    return total_dict


def stats_re(total_dict: dict):
    for double_type in total_list:
        type_list = total_dict[double_type]
        re_list = []
        for type_dict in type_list:
            if type_dict['bool']:
                re_list.append(type_dict['relation'])
        print('{}: \n{}\n'.format(double_type, pd.value_counts(re_list)))


if __name__ == '__main__':
    data_path = '/home/zutnlp/zutnlp_student_2017/liuyan/datasets/zzsn/re/实体标签.csv'
    total_dict = stat(data_path=data_path)
    stats_re(total_dict=total_dict)
    pass
