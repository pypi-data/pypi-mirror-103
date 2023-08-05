#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : test_sim_hash
# @Author   : LiuYan
# @Time     : 2021/4/8 19:40

from doc_similarity.model.sim_hash import SimHashSimilarity, OldSimHashSimilarity

# 测试
if __name__ == '__main__':
    text_1 = 'simhash算法的主要思想是降维，将高维的特征向量映射成一个低维的特征向量，通过两个向量的Hamming Distance来确定文章是否重复或者高度近似。'
    text_2 = '我们所用到的simhash算法的主要思想是降维，将高维特征向量映射成一个低维特征向量，再通过两个向量的Hamming Distance来确定文章是否重复或高度近似。'

    stop_words_path = '/home/zzsn/liuyan/word2vec/doc_similarity/stop_words.txt'
    sim_hash_sim = SimHashSimilarity(stop_words_path=stop_words_path)
    old_sim_hash_sim = OldSimHashSimilarity()
    with open('../data/sample/sample_x.txt', 'r') as x, open('../data/sample/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        similar = old_sim_hash_sim.calculate(text_1=text_1, text_2=text_2)
        # similar = sim_hash(text_1=content_x, text_2=content_y)
        print(similar)

        similarity = sim_hash_sim.calculate(text_1, text_2)
        # similarity = sim_hash_sim.calculate(content_x, content_y)

        threshold = 3  # 阀值
        print(f'海明距离：{similarity} 判定距离：{threshold} 是否相似：{similarity <= threshold}')
