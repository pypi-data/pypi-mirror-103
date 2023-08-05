#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_process
# @Author   : LiuYan
# @Time     : 2021/4/15 17:39

import os
import random
import pandas as pd

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from classification.utils.utils import *
from doc_similarity.model.cosine_similarity import CosineSimilarity
from doc_similarity.model.jaccard import JaccardSimilarity
from doc_similarity.model.levenshtein import LevenshteinSimilarity
from doc_similarity.model.min_hash import MinHashSimilarity
from doc_similarity.model.sim_hash import OldSimHashSimilarity
from utils.utils import *

root_path = '/home/zzsn/liuyan/word2vec/doc_similarity'
stop_words_path = os.path.join(root_path, 'stop_words.txt')
cos_sim = CosineSimilarity(stop_words_path=stop_words_path)
jac_sim = JaccardSimilarity(stop_words_path=stop_words_path)
lev_sim = LevenshteinSimilarity(stop_words_path=stop_words_path)
min_hash_sim = MinHashSimilarity(stop_words_path=stop_words_path)
old_sim_hash_sim = OldSimHashSimilarity()


def remove_repetition(path: str) -> list:
    """
    根据文章标题进行数据去重清洗
    :param path:
    :return:
    """
    data_loader = pd.read_excel(path)
    delete_num = 0
    article_list = []
    for index in range(len(data_loader['id'])):
        title = data_loader['title'][index].replace('\n', '').replace('\r', '').replace('\t', '')

        if judge_sim(article_list=article_list, title=title):
            print('Add   : \tindex: {} \t id: {} \t title: {}'.format(
                index, data_loader['id'][index], data_loader['title'][index])
            )
            article_list.append({
                'id': data_loader['id'][index],
                'title': title,
                'content': data_loader['content'][index].replace(
                    '\n', ''
                ).replace('\r', '').replace('\t', ''),
                'origin': data_loader['origin'][index],
                'source_address': data_loader['sourceaddress'][index]
            })
        else:
            delete_num += 1
            print('Delete: \tindex: {} \t id: {} \t title: {}'.format(
                index, data_loader['id'][index], data_loader['title'][index])
            )
    print('Delete: \t{}'.format(delete_num))
    return article_list
    pass


def judge_sim(article_list: list, title: str) -> bool:
    if len(article_list) < 1:
        return True
    if len(article_list) > 100:
        article_list = article_list[-100: -1]
    for article in article_list:
        if cos_sim.calculate(article['title'], title) > 0.9:
            print('{} --- {}'.format(title, article['title']))
            return False

    return True
    pass


def process_txt(data_loader: DataFrame, train_file_path: str, valid_file_path: str):
    articles = data_loader['article']
    labels = data_loader['label']

    article_list = []
    for article, label in zip(articles, labels):
        if type(article) is str:
            text = article.replace('\n', '').replace('\r', '').replace('\t', '')
        else:
            print('{} is not str!'.format(article))
            continue
        text = seg(text=text, sw=stop_words(path='sample/stop_words.txt'))
        text = '__label__{} {}'.format(label, text)
        article_list.append(text)
    # for index in range(len(data_loader['article'])):
    #     content = data_loader['article'][index].replace('\n', '').replace('\r', '').replace('\t', '')
    #     # text = seg(content, NLPTokenizer, stop_words())
    #     text = seg(content, stop_words(path='sample/stop_words.txt'))
    #     text = '__label__1 {}'.format(text)
    #     # text = transform_data(text, data_loader['label'][index])
    #     article_list.append(text)

    train_data, valid_data = train_test_split(
        article_list, train_size=0.8, random_state=2021, shuffle=True
    )
    with open(
            train_file_path, 'w', encoding='utf-8'
    ) as train_file, open(
        valid_file_path, 'w', encoding='utf-8'
    ) as valid_file:
        for train in train_data:
            train_file.write(train + '\n')
        for valid in valid_data:
            valid_file.write(valid + '\n')
    pass


def process_fx(path='sample/风险训练集.xlsx'):
    data_list = pd.read_excel(path)
    data_list['article'] = (data_list['title'] + '。') * 2 + data_list['content']
    pass


def process_f_zp_gp(path: str, train_file_path: str, valid_file_path: str):
    data_loader = pd.read_excel(path)
    # data_loader['article'] = '{}。{}'.format(data_loader['title'] * 2, data_loader['content'])
    data_loader['article'] = data_loader['title'] * 2 + '。' + data_loader['content']
    data_loader['article'] = data_loader.article.apply(clean_tag).apply(clean_txt)

    process_txt(
        data_loader=data_loader,
        train_file_path=train_file_path,
        valid_file_path=valid_file_path
    )
    pass


def merge_f_zp_gp(f_path: str, zp_path: str, gp_path: str, result_path: str):
    result_list = []
    f_list = read_excel_random(f_path, label=0)
    zp_list = read_excel_random(zp_path, label=1)
    gp_list = read_excel_random(gp_path, label=2)
    result_list.extend(f_list)
    result_list.extend(zp_list)
    result_list.extend(gp_list[:5000])
    df = pd.DataFrame(result_list)
    df.to_excel(result_path)
    pass


def read_excel_random(path: str, label: int) -> list:
    df = pd.read_excel(path)
    result_list = []
    titles, contents = df['title'], df['content']
    for title, content in zip(titles, contents):
        result_list.append({
            'title': title,
            'content': content,
            'label': label
        })
    random.shuffle(result_list)
    return result_list
    # return result_list[:5000] if len(result_list) > 5000 else result_list
    pass


if __name__ == '__main__':
    # 源语料去重
    # article_list = remove_repetition(path='sample/股票信息.xlsx')
    # df = pd.DataFrame(article_list)
    # df.to_excel('sample/去重股票信息.xlsx')

    # merge
    # merge_f_zp_gp(
    #     f_path='sample/去重非招聘股票.xlsx',
    #     zp_path='sample/去重招聘信息.xlsx',
    #     gp_path='sample/去重股票信息.xlsx',
    #     result_path='sample/去重_F_ZP_GP.xlsx'
    # )

    # excel2txt 准备训练
    # process_fx()
    process_f_zp_gp(
        path='sample/去重_F_ZP_GP.xlsx',
        train_file_path='/home/zzsn/liuyan/data/f_zp_gp/train.txt',
        valid_file_path='/home/zzsn/liuyan/data/f_zp_gp/valid.txt'
    )

    # list2xlsx(result_list=article_list, xlsx_path='sample/去重招聘信息.xlsx')
    pass
