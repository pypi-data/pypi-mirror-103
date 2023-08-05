#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 14:10
# @Author  : 程婷婷
# @FileName: similarity_tx.py
# @Software: PyCharm

import numpy as np
import gensim
import jieba
import re
from sklearn.metrics.pairwise import cosine_similarity


class Similarity(object):
    def __init__(self, model_path, stopword_path):
        self.Word2VecModel = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)
        self.vocab_list = [word for word, vocab in self.Word2VecModel.wv.vocab.items()]
        self.stopword_path = stopword_path

    def stop_word_list(self, path):
        '''
        创建停用词list
        :param path:
        :return:
        '''
        stopwords = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
        return stopwords

    def remove_char(self, text):
        '''
        保留中文、英语字母、数字和标点
        :param text:
        :return:
        '''
        graph_filter = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。\.,？\?!！；;]')
        graph = graph_filter.sub('', text)
        if len(graph) == 0:
            return ''
        else:
            return graph

    def preprocess(self, text):
        '''
        预处理文本
        :param text:
        :return:
        '''
        if isinstance(text, str):
            text = self.remove_char(text)
            textcut = jieba.cut(text.strip())
            stopwords = self.stop_word_list(self.stopword_path)
            textcut = filter(lambda x: x in stopwords, textcut)
        else:
            raise TypeError('text should be str')
        return textcut

    # 第1个参数是每篇文章分词的结果，第2个参数是word2vec模型对象
    def getVector_v4(self, cutWords):
        article_vector = np.zeros((1, 200))
        for cutWord in cutWords:
            if cutWord in self.vocab_list:
                article_vector += np.array(self.Word2VecModel.wv[cutWord])
        cutWord_vector = article_vector.mean(axis=0)
        return cutWord_vector

    def calculation_sim(self, text1, text2):
        '''
        计算相似度
        :param texts_train:
        :param texts_test:
        :return:
        '''
        text1 = self.preprocess(text1)
        text2 = self.preprocess(text2)
        matrix_text1 = self.getVector_v4(text1)
        matrix_text2 = self.getVector_v4(text2)
        dis = cosine_similarity(matrix_text1.reshape(1, -1), matrix_text2.reshape(1, -1))
        return dis
