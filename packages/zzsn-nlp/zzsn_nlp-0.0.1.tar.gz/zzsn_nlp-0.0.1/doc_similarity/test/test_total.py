#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : test_total
# @Author   : LiuYan
# @Time     : 2021/4/9 10:27

import os

from utils.log import logger
from doc_similarity.model.cosine_similarity import CosineSimilarity
from doc_similarity.model.jaccard import JaccardSimilarity
from doc_similarity.model.levenshtein import LevenshteinSimilarity
from doc_similarity.model.min_hash import MinHashSimilarity
from doc_similarity.model.sim_hash import SimHashSimilarity, OldSimHashSimilarity
from doc_similarity.model.similarity_tx import Similarity

# 测试
if __name__ == '__main__':
    text_1 = 'simhash算法的主要思想是降维，将高维的特征向量映射成一个低维的特征向量，通过两个向量的Hamming Distance来确定文章是否重复或者高度近似。'
    text_2 = '我们所用到的simhash算法的主要思想是降维，将高维特征向量映射成一个低维特征向量，再通过两个向量的Hamming Distance来确定文章是否重复或高度近似。'

    root_path = '/home/zzsn/liuyan/word2vec/doc_similarity'
    stop_words_path = os.path.join(root_path, 'stop_words.txt')
    cos_sim = CosineSimilarity(stop_words_path=stop_words_path)
    jac_sim = JaccardSimilarity(stop_words_path=stop_words_path)
    lev_sim = LevenshteinSimilarity(stop_words_path=stop_words_path)
    min_hash_sim = MinHashSimilarity(stop_words_path=stop_words_path)
    sim_hash_sim = SimHashSimilarity(stop_words_path=stop_words_path)
    old_sim_hash_sim = OldSimHashSimilarity()
    sim_tx = Similarity(
        model_path=os.path.join(root_path, 'Tencent_AILab_ChineseEmbedding_Min.txt'),
        stopword_path=os.path.join(root_path, 'stopwords.txt')
    )
    with open('../data/sample/sample_x.txt', 'r') as x, open('../data/sample/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()

        result_cos_sim = cos_sim.calculate(text_1, text_2)
        # result_cos_sim = cos_sim.calculate(content_x, content_y)
        result_jac_sim = jac_sim.calculate(text_1, text_2)
        # result_jac_sim = jac_sim.calculate(content_x, content_y)
        result_lev_sim = lev_sim.calculate(text_1, text_2)
        # result_lev_sim = lev_sim.calculate(content_x, content_y)
        result_min_hash_sim = min_hash_sim.calculate(text_1, text_2)
        # result_min_hash_sim = min_hash_sim.calculate(content_x, content_y)
        result_old_sim_hash_sim = old_sim_hash_sim.calculate(text_1=text_1, text_2=text_2)
        # result_old_sim_hash_sim = old_sim_hash_sim.calculate(text_1=content_x, text_2=content_y)
        result_new_sim_hash_sim = sim_hash_sim.calculate(text_1, text_2)
        # result_new_sim_hash_sim = sim_hash_sim.calculate(content_x, content_y)
        result_sim_tx = sim_tx.calculation_sim(text_1, text_2)
        # result_sim_tx = sim_tx.calculation_sim(content_x, content_y)

        logger.info('Cosine Similarity \t\t: {:.2f}%'.format(result_cos_sim * 100))
        logger.info('Jaccard Similarity\t\t: {:.2f}%'.format(result_jac_sim * 100))
        logger.info('Levenshtein Similarity\t: {:.2f}%'.format(result_lev_sim * 100))
        logger.info('Min hash Similarity   \t: {:.2f}%'.format(result_min_hash_sim * 100))
        logger.info('Old sim hash Similarity: {:.2f}%'.format(result_old_sim_hash_sim * 100))
        threshold = 3  # 阀值
        logger.info('New sim hash Similarity: 海明距离: {}, 阈值距离: {}, 是否相似: {}'.format(
            result_new_sim_hash_sim, threshold, result_new_sim_hash_sim <= threshold
        ))
        logger.info('CTT Similarity    \t\t: {}'.format(result_sim_tx))
