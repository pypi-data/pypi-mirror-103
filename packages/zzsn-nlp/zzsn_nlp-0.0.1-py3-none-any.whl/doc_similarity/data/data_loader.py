#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_loader
# @Author   : LiuYan
# @Time     : 2021/4/9 15:01

from doc_similarity.data.data_process import xlsx2list, list2xlsx
from doc_similarity.model.total_sim import TotalSimilarity


def compare_list(sim: object, total_list: list) -> list:
    result_list = []
    total_len = len(total_list)
    for index_x in range(total_len):
        content_x = total_list[index_x]
        for index_y in range(index_x + 1, total_len):
            content_y = total_list[index_y]
            result_dict_title = sim.calculate(content_x['title'], content_y['title'])
            result_dict_content = sim.calculate(content_x['content'], content_y['content'])
            result_list.append([
                content_x['id'], content_y['id'],
                result_dict_title, result_dict_content
            ])
    return result_list
    pass


if __name__ == '__main__':
    stop_words_path = '../data/stop_words.txt'
    xlsx_path = '../data/total_datasets.xlsx'
    total_sim = TotalSimilarity(stop_words_path=stop_words_path)
    total_list = xlsx2list(xlsx_path=xlsx_path)
    result_list = compare_list(sim=total_sim, total_list=total_list)
    list2xlsx(xlsx_path='../data/result/result_total_datasets.xlsx', result_lists=result_list)
    pass
