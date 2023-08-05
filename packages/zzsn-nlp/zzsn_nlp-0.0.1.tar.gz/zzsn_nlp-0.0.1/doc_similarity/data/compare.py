#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : compare
# @Author   : LiuYan
# @Time     : 2021/4/10 14:58

import os

from doc_similarity.model.cosine_similarity import CosineSimilarity
from doc_similarity.model.jaccard import JaccardSimilarity
from doc_similarity.model.levenshtein import LevenshteinSimilarity
from doc_similarity.model.min_hash import MinHashSimilarity
from doc_similarity.model.sim_hash import SimHashSimilarity, OldSimHashSimilarity
# from doc_similarity.model.similarity_tx import Similarity
# from doc_similarity.model.total_sim import TotalSimilarity

root_path = '/home/zzsn/liuyan/word2vec/doc_similarity'
stop_words_path = os.path.join(root_path, 'stop_words.txt')
cos_sim = CosineSimilarity(stop_words_path=stop_words_path)
jac_sim = JaccardSimilarity(stop_words_path=stop_words_path)
lev_sim = LevenshteinSimilarity(stop_words_path=stop_words_path)
min_hash_sim = MinHashSimilarity(stop_words_path=stop_words_path)
sim_hash_sim = SimHashSimilarity(stop_words_path=stop_words_path)
old_sim_hash_sim = OldSimHashSimilarity()
# ctt_sim = Similarity(
#     model_path=os.path.join(root_path, 'Tencent_AILab_ChineseEmbedding_Min.txt'),
#     stopword_path=os.path.join(root_path, 'stopwords.txt')
# )
# total_sim = TotalSimilarity(root_path=root_path)
sim_dict = {
    'cos_sim': cos_sim,
    'jac_sim': jac_sim,
    'lev_sim': lev_sim,
    'min_hash': min_hash_sim,
    'sim_hash': old_sim_hash_sim,
    # 'ctt_sim': ctt_sim,
    'false': False
}


# def compare_all(total_list: list) -> list:
#     result_list = []
#     total_len = len(total_list)
#     for index_x in range(total_len):
#         article_x = total_list[index_x]
#         for index_y in range(index_x + 1, total_len):
#             article_y = total_list[index_y]
#             result_dict_title = total_sim.calculate(article_x['title'], article_y['title'])
#             result_dict_content = total_sim.calculate(article_x['content'], article_y['content'])
#             result_list.append([
#                 article_x['id'], article_y['id'],
#                 result_dict_title, result_dict_content
#             ])
#     return result_list
#     pass


def compare_sim_name(title_sim_name: str or bool, content_sim_name: str or bool) -> dict or list:
    if title_sim_name in sim_dict:
        title_sim = sim_dict[title_sim_name]
    else:
        return {
            'handleMsg': '所选标题相似度算法名称错误或不存在！请核查(cos_sim / jac_sim / lev_sim / min_hash / sim_hash / false)',
            'isHandleSuccess': False,
            'logs': None,
            'resultData': None
        }

    if content_sim_name in sim_dict:
        content_sim = sim_dict[content_sim_name]
    else:
        return {
            'handleMsg': '所选正文相似度算法名称错误或不存在！请核查(cos_sim / jac_sim / lev_sim / min_hash / sim_hash / false)',
            'isHandleSuccess': False,
            'logs': None,
            'resultData': None
        }

    return [title_sim, content_sim]


def compare_single(article_list: list, title_sim_name: str or bool, content_sim_name: str or bool) -> dict:
    judge_sim_name = compare_sim_name(title_sim_name=title_sim_name, content_sim_name=content_sim_name)
    if type(judge_sim_name) is dict:
        return judge_sim_name
    else:
        title_sim, content_sim = judge_sim_name[0], judge_sim_name[1]

    if len(article_list) == 2:
        article_x, article_y = article_list[0], article_list[1]
        title_similarity = title_sim.calculate(
            article_x['title'], article_y['title']
        ) if title_sim else 0.0
        content_similarity = content_sim.calculate(
            article_x['content'], article_y['content']
        ) if content_sim else 0.0
        result_dict = {
            'id_x': article_x['id'],
            'id_y': article_y['id'],
            'title_sim': title_similarity,
            'content_sim': content_similarity
        }
    else:
        return {
            'handleMsg': '所对比文章数量不是 2 篇，请核查！',
            'isHandleSuccess': False,
            'logs': None,
            'resultData': None
        }

    return {
        'handleMsg': 'success',
        'isHandleSuccess': True,
        'logs': None,
        'resultData': result_dict
    }
    pass


def compare_many(article_list: list, title_sim_name: str or bool, content_sim_name: str or bool) -> dict:
    judge_sim_name = compare_sim_name(title_sim_name=title_sim_name, content_sim_name=content_sim_name)
    if type(judge_sim_name) is dict:
        return judge_sim_name
    else:
        title_sim, content_sim = judge_sim_name[0], judge_sim_name[1]

    result_list = []
    total_len = len(article_list)
    if total_len < 3:
        return {
            'handleMsg': '所对比文章数量少于 3 篇，请核查！(2 篇文章对比请使用接口1 similarity)',
            'isHandleSuccess': False,
            'logs': None,
            'resultData': None
        }
    else:
        for index in range(total_len):
            article = article_list[index]
            article_list[index]['title_transform'] = title_sim.transform(article['title']) if title_sim else None
            article_list[index]['content_transform'] = content_sim.transform(
                article['content']) if content_sim else None
        for index_x in range(total_len):
            article_x = article_list[index_x]
            for index_y in range(index_x + 1, total_len):
                article_y = article_list[index_y]
                title_similarity = title_sim.calculate_transform(
                    article_x['title_transform'], article_y['title_transform']
                ) if title_sim else 0.0
                content_similarity = content_sim.calculate_transform(
                    article_x['content_transform'], article_y['content_transform']
                ) if content_sim else 0.0
                result_list.append({
                    'id_x': article_x['id'],
                    'id_y': article_y['id'],
                    'title_sim': title_similarity,
                    'content_sim': content_similarity
                })

    return {
        'handleMsg': 'success',
        'isHandleSuccess': True,
        'logs': None,
        'resultData': {
            'sim_list': result_list
        }
    }
    pass


if __name__ == '__main__':
    result_dict = compare_single([
        {
            'id': 1,
            'title': 'I love YanLiu',
            'content': 'YingLiang love YanLiu'
        },
        {
            'id': 2,
            'title': 'I love YingLiang',
            'content': 'YanLiu love YingLiang'
        }

    ], 'cos_sim', 'sim_hash')
    print(result_dict)
    result_list = compare_many([
        {
            'id': 1,
            'title': 'I love YanLiu',
            'content': 'YingLiang love YanLiu'
        },
        {
            'id': 2,
            'title': 'I love YingLiang',
            'content': 'YanLiu love YingLiang'
        },
        {
            'id': 3,
            'title': 'I love YingLiang',
            'content': 'YanLiu love YingLiang'
        }
    ], 'lev_sim', 'sim_hash')
    print(result_list)
    pass
