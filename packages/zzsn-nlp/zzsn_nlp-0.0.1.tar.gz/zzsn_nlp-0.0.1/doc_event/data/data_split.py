#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_split
# @Author   : LiuYan
# @Time     : 2021/1/15 14:32

import xlsxwriter
from sklearn.model_selection import train_test_split

from data_process import *


def build_list2dict(_len, _word_list, _tag_list):
    result_dict = {
        'content': ''.join(_word_list),
        'amount_of_cooperation': set(),
        'project_name': set(),
        'state': set(),
        'company_identification_Party_A': set(),
        'company_identification_Party_B': set(),
        'project_cycle': set(),
        'project_status': set()
    }
    # tag_dict = {
    #     'amount_of_cooperation': '合作金额',
    #     'project_name': '项目名称',
    #     'state': '国家',
    #     'company_identification_Party_A': '企业识别甲方',
    #     'company_identification_Party_B': '企业识别乙方',
    #     'project_cycle': '项目周期',
    #     'project_status': '项目状态'
    # }
    for index, word, tag in zip(range(_len), _word_list, _tag_list):
        start_pos = index
        end_pos = index + 1
        label_type = tag[2:]
        if tag[0] == 'B' and end_pos != _len:
            # two !=
            while _tag_list[end_pos][0] == 'I' and _tag_list[end_pos][2:] == label_type and end_pos + 1 != _len:
                end_pos += 1
            if _tag_list[end_pos][0] == 'E':
                result_dict[label_type].add(''.join(_word_list[start_pos: end_pos + 1]))
                # build_list.append({'start_pos': start_pos,
                #                    'end_pos': end_pos + 1,
                #                    'label_type': tag_dict[label_type]})
    return result_dict


def list2xlsx(xlsx_path=None, result_lists=None):
    # 创建工作簿
    workbook = xlsxwriter.Workbook(xlsx_path)
    # 创建工作表
    worksheet = workbook.add_worksheet('sheet1')
    # 按行写
    worksheet.write_row(
        0, 0, [
            '合同金额',
            '项目名称',
            '国家',
            '企业识别甲方',
            '企业识别乙方',
            '项目周期',
            '项目状态'
        ]
    )
    for index, result in enumerate(result_lists):
        worksheet.write_row(
            index + 1, 0, [
                ','.join(result['amount_of_cooperation']),
                ','.join(result['project_name']),
                ','.join(result['state']),
                ','.join(result['company_identification_Party_A']),
                ','.join(result['company_identification_Party_B']),
                ','.join(result['project_cycle']),
                ','.join(result['project_status'])
            ]
        )

    workbook.close()


def data_split(data_list):
    # split_str = '，,、；;。'  #
    # split_str = '；;。'   # 1
    # split_str = '；;。！!'   # 2
    split_str = '；;。！!？?'   # 3
    result_list = []
    # 同时也可以以空格 ‘ ’ 为边界进行切分 即split_str = '，,、；;。 '
    for word_list, tag_list in data_list:
        length = 1
        split_words, split_tags = [], []
        split_list = []
        for word, tag in zip(word_list, tag_list):
            split_words.append(word)
            split_tags.append(tag)
            if length > 30 and tag[0] in ['O', 'E'] and word in split_str:
                split_list.append([split_words, split_tags])
                split_words, split_tags = [], []
                length = 1
            elif length > 120 and tag[0] in ['O', 'E']:
                split_list.append([split_words, split_tags])
                split_words, split_tags = [], []
                length = 1
            if length >= 200:
                print(111111111111111111111111111111111)  # Warning
            length += 1

        merge_list = merge_seq(seq_list=split_list)
        result_list.append(merge_list)

    assert len(data_list) == len(result_list), 'data_list: {} != result_list: {} !'.format(
        len(data_list), len(result_list)
    )
    return result_list


def merge_seq(seq_list):
    i = 0
    num_sent_to_include, max_length = 3, 200
    merge_words, merge_tags = [], []
    merge_list, stats_list = [], []
    for word_list, tag_list in seq_list:
        if i == 0:
            merge_words.extend(word_list)
            merge_tags.extend(tag_list)
            i += 1
        elif i == 3:
            merge_list.append([merge_words, merge_tags])
            stats_list.append(i)
            merge_words = word_list
            merge_tags = tag_list
            i = 1
        elif len(merge_words) + len(word_list) < max_length:
            merge_words.append('#####')
            merge_tags.append('O')
            merge_words.extend(word_list)
            merge_tags.extend(tag_list)
            i += 1
        else:
            merge_list.append([merge_words, merge_tags])
            stats_list.append(i)
            merge_words = word_list
            merge_tags = tag_list
            i = 1
    print('段 平均由 {} 句构成'.format(sum(stats_list) / len(stats_list)))
    return merge_list
    pass


if __name__ == '__main__':
    xlsx_path = './sample/total_datasets.xlsx'
    total_list = xlsx2list(xlsx_path=xlsx_path)
    data_list = list()
    for sentence in total_list:
        word_list, tag_list = sentence2tag(sentence)
        data_list.append([word_list, tag_list])
    result_list = data_split(data_list=data_list)
    train_list, dev_list = train_test_split(
        result_list, test_size=0.1, random_state=2021
    )
    write2txt(train_list, 'train_3.txt', 'train')
    write2txt(dev_list, 'dev_3.txt', 'dev')
    write2txt(dev_list, 'test_3.txt', 'test')

    # test_data_path = 'test.txt'
    # with open(test_data_path, 'r', encoding='utf-8') as f:
    #     file = f.readlines()
    # doc_id = None
    # word_list, tag_list = list(), list()
    # for line in file:
    #     if doc_id is None:
    #         doc_id = line.strip('\n')
    #     else:
    #         word, tag = line.strip('\n').split('\t')
    #     pass
    # result_lists = list()
    # for word_list, tag_list in result_list:
    #     result_dict = build_list2dict(len(word_list), word_list, tag_list)
    #     result_lists.append(result_dict)
    # list2xlsx(xlsx_path='test_result_true.xlsx', result_lists=result_lists)
    pass
