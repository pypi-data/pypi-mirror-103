#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : cosine_similarity
# @Author   : LiuYan
# @Time     : 2021/4/8 19:36

from sklearn.metrics.pairwise import cosine_similarity

from doc_similarity.model.base_similarity import BaseSimilarity
from doc_similarity.utils.tool import Tool


class CosineSimilarity(BaseSimilarity):
    """
    余弦相似度
    """

    def __init__(self, stop_words_path):
        super(CosineSimilarity, self).__init__()
        self._tool = Tool(stop_words_path=stop_words_path)

    @staticmethod
    def one_hot(word_dict, keywords):  # oneHot编码
        # cut_code = [word_dict[word] for word in keywords]
        cut_code = [0] * len(word_dict)
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code

    def calculate(self, content_x, content_y):
        keywords_1 = self._tool.extract_keyword(content_x, withWeigth=False)  # 提取关键词
        keywords_2 = self._tool.extract_keyword(content_y, withWeigth=False)
        # 词的并集
        union = set(keywords_1).union(set(keywords_2))
        # 编码
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        # oneHot编码
        s1_cut_code = self.one_hot(word_dict, keywords_1)
        s2_cut_code = self.one_hot(word_dict, keywords_2)
        # 余弦相似度计算
        sample = [s1_cut_code, s2_cut_code]
        # 除零处理
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0

    def transform(self, content: str) -> object:
        keywords = self._tool.extract_keyword(content, withWeigth=False)  # 提取关键词
        return keywords
        pass

    def calculate_transform(self, transform_x: object, transform_y: object) -> float:
        """
        :param transform_x: keywords_1
        :param transform_y: keywords_2
        :return: float
        """
        # 词的并集
        union = set(transform_x).union(set(transform_y))
        # 编码
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        # oneHot编码
        s1_cut_code = self.one_hot(word_dict, transform_x)
        s2_cut_code = self.one_hot(word_dict, transform_y)
        # 余弦相似度计算
        sample = [s1_cut_code, s2_cut_code]
        # 除零处理
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0
        pass
