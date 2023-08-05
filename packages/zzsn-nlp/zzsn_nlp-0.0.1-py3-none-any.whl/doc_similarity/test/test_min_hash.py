#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : test_min_hash
# @Author   : LiuYan
# @Time     : 2021/4/9 9:10

from doc_similarity.model.min_hash import MinHashSimilarity

# 测试
if __name__ == '__main__':
    text_1 = 'simhash算法的主要思想是降维，将高维的特征向量映射成一个低维的特征向量，通过两个向量的Hamming Distance来确定文章是否重复或者高度近似。'
    text_2 = '我们所用到的simhash算法的主要思想是降维，将高维特征向量映射成一个低维特征向量，再通过两个向量的Hamming Distance来确定文章是否重复或高度近似。'

    # stop_words_path = '../data/stopwords.txt'
    stop_words_path = '../data/stop_words.txt'
    min_hash_sim = MinHashSimilarity(stop_words_path=stop_words_path)
    with open('../data/sample_x.txt', 'r') as x, open('../data/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()

        similarity = min_hash_sim.calculate(text_1, text_2)
        # similarity = min_hash_sim.calculate(content_x, content_y)
        print('相似度: %.2f%%' % (similarity * 100))
