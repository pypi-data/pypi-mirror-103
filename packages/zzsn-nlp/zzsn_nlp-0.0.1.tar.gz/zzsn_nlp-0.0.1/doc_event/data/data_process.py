#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_process
# @Author   : LiuYan
# @Time     : 2021/1/14 20:37

import re
import xlrd
from sklearn.model_selection import train_test_split


def xlsx2list(xlsx_path=None) -> list:
    # 打开excel
    wb = xlrd.open_workbook(xlsx_path)
    # 按工作簿定位工作表
    sh = wb.sheet_by_name('Sheet1')
    print(sh.nrows)  # 有效数据行数
    print(sh.ncols)  # 有效数据列数
    print(sh.cell(0, 0).value)  # 输出第一行第一列的值
    print(sh.row_values(0))  # 输出第一行的所有值
    # 将数据和标题组合成字典
    print(dict(zip(sh.row_values(0), sh.row_values(1))))
    # 遍历excel，打印所有数据
    total_list = list()
    for i in range(sh.nrows):
        row = sh.row_values(i)
        total_list.append({
            'title': row[1].replace('\n', '').replace('\r', '').replace('\t', ''),
            'content': row[2].replace('\n', '').replace('\r', '').replace('\t', ''),
            'amount_of_cooperation': row[3].split(';') if len(row[3]) > 0 else None,
            'project_name': row[4].split(',') if len(row[4]) > 0 else None,
            'state': row[5].split(',') if len(row[5]) > 0 else None,
            'company_identification_Party_A': row[6].split(',') if len(row[6]) > 0 else None,
            'company_identification_Party_B': row[7].split(',') if len(row[7]) > 0 else None,
            'project_cycle': row[8].split(',') if len(row[8]) > 0 else None,
            'project_status': row[9].split(',') if len(row[9]) > 0 else None,
        })
    total_list = total_list[3:]
    return total_list


def stats(content=None, com_list=None) -> list:
    result_list = list()
    for com in com_list:
        pattern = re.compile(com)
        result = pattern.findall(content)
        result_list.append(len(result))
    return result_list


def sentence2tag(sentence=None):
    title, content = sentence['title'], sentence['content']
    content = title + content
    amount_of_cooperation = sentence['amount_of_cooperation']
    project_name = sentence['project_name']
    state = sentence['state']
    company_identification_Party_A = sentence['company_identification_Party_A']
    company_identification_Party_B = sentence['company_identification_Party_B']
    project_cycle = sentence['project_cycle']
    project_status = sentence['project_status']
    word_list = list(content)
    tag_list = ['O' for c in content]

    if amount_of_cooperation is None:
        pass
        # print('None')
    else:
        for aoc in amount_of_cooperation:
            index_list = find_all(content, aoc)
            tag_list = tag_update(tag_list, index_list, aoc, 'amount_of_cooperation')

    if project_name is None:
        pass
        # print('None')
    else:
        for pn in project_name:
            index_list = find_all(content, pn)
            tag_list = tag_update(tag_list, index_list, pn, 'project_name')

    if state is None:
        pass
        # print('None')
    else:
        for s in state:
            index_list = find_all(content, s)
            tag_list = tag_update(tag_list, index_list, s, 'state')

    if company_identification_Party_A is None:
        pass
        # print('None')
    else:
        for ciPA in company_identification_Party_A:
            index_list = find_all(content, ciPA)
            tag_list = tag_update(tag_list, index_list, ciPA, 'company_identification_Party_A')

    if company_identification_Party_B is None:
        pass
        # print('None')
    else:
        for ciPB in company_identification_Party_B:
            index_list = find_all(content, ciPB)
            tag_list = tag_update(tag_list, index_list, ciPB, 'company_identification_Party_B')

    if project_cycle is None:
        # print('None')
        pass
    else:
        for pc in project_cycle:
            index_list = find_all(content, pc)
            tag_list = tag_update(tag_list, index_list, pc, 'project_cycle')

    if project_status is None:
        pass
        # print('None')
    else:
        for ps in project_status:
            index_list = find_all(content, ps[0:2])
            tag_list = tag_update(tag_list, index_list, ps[0:2], 'project_status')

    s_word = ['', '\n', '\t']
    s_tag = ['', ' ', '\n', '\t']
    for word, tag in zip(word_list, tag_list):
        if word in s_word:
            print(111111111)
        if tag in s_tag:
            print(11111)
    return word_list, tag_list
    # result_list = stats(content, amount_of_cooperation)
    pass


def tag_update(tag_list, index_list, s, tag_name):
    if index_list is False:
        return tag_list

    for index in index_list:
        if judge_all_o(tag_list, index, index + len(s)):
            tag_list[index] = 'B-' + tag_name
            for i in range(index + 1, index + len(s) - 1):
                tag_list[i] = 'I-' + tag_name
            tag_list[index + len(s) - 1] = 'E-' + tag_name
    return tag_list


def judge_all_o(tag_list, index, index_end):
    if tag_list[index][0] == 'O' or tag_list[index][0] == 'B':
        if tag_list[index_end - 1][0] == 'O' or tag_list[index_end - 1][0] == 'E':
            if tag_list[index][0] == 'B':
                pass
            return True

    return False


def find_all(sub, s):
    """
    从一篇文章(sub)中找到所有符合要素(s)的chunk，并返回起始下标
    :param sub: role
    :param s: doc
    :return: index: list
    """
    if len(s) < 2:
        print('要素名过短: {}'.format(s))  # 要素名过短提示
    index_list = []
    index = sub.find(s)
    while index != -1:
        index_list.append(index)
        index = sub.find(s, index + 1)

    if len(index_list) > 0:
        return index_list
    else:
        print('事件要素: {} 在文章中未能匹配成功！'.format(s))  # 文章中未匹配的要素
        return False


def check_all(result_list):
    for word_list, tag_list in result_list:
        suffix = None
        for word, tag in zip(word_list, tag_list):
            if suffix is None:
                if tag[0] == 'I' or tag[0] == 'E':
                    print(111)
            if tag[0] == 'B':
                suffix = tag[2:]
            if suffix is not None:
                if tag[0] == 'I' or tag[0] == 'E':
                    if tag[2:] != suffix:
                        print(111)
            if tag[0] == 'O':
                suffix = None

            if word is ' ':
                if tag[0] is not 'O':
                    pass
    pass


def write2txt(docs_list, txt_path, typ):
    i = 0
    with open(txt_path, 'w', encoding='utf-8') as f:
        for doc_list in docs_list:
            for word_list, tag_list in doc_list:
                if len(word_list) >= 250:
                    print(len(word_list))
                f.write(typ + '-' + str(i) + '\n')
                for index, word, tag in zip(range(len(word_list)), word_list, tag_list):
                    # if word == ' '
                    f.write(word + '\t' + tag + '\n')
                    if index + 1 == len(word_list):
                        f.write('\n')
            i += 1


def data_split_write2txt(result_list, txt_path, typ):
    """
    data_split + write2txt
    :param result_list: list
    :param txt_path:
    :param typ: train/dev/test
    :return:
    """
    i = 0
    # split_str = '，,、；;。'
    split_str = '；;。'
    # 同时也可以以空格 ‘ ’ 为边界进行切分 即split_str = '，,、；;。 '
    with open(txt_path, 'w', encoding='utf-8') as f:
        for word_list, tag_list in result_list:
            f.write(typ + '-' + str(i) + '\n')
            length = 1
            for index, word, tag in zip(range(len(word_list)), word_list, tag_list):
                f.write(word + '\t' + tag + '\n')
                if index + 1 == len(word_list):
                    f.write('\n')
                elif length > 30 and tag[0] in ['O', 'E'] and word in split_str:
                    f.write('\n' + typ + '-' + str(i) + '\n')
                    length = 1
                elif length > 120 and tag[0] in ['O', 'E']:
                    f.write('\n' + typ + '-' + str(i) + '\n')
                    length = 1
                if length >= 200:
                    print(111111111111111111111111111111111)
                length += 1
                pass
            i += 1


if __name__ == '__main__':
    s = '27.52亿美元,2,436.03亿元'
    s_list = re.split('元,|币,', s)
    xlsx_path = './sample/total_datasets.xlsx'
    total_list = xlsx2list(xlsx_path=xlsx_path)
    result_list = list()
    for sentence in total_list:
        word_list, tag_list = sentence2tag(sentence)
        result_list.append([word_list, tag_list])
    check_all(result_list)

    train_list, dev_list = train_test_split(
        result_list, test_size=0.1, random_state=2021
    )
    data_split_write2txt(train_list, 'train_1_.txt', 'train')
    data_split_write2txt(dev_list, 'dev_1_.txt', 'dev')
    data_split_write2txt(dev_list, 'test_1_.txt', 'test')
pass
