#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : min_hash
# @Author   : LiuYan
# @Time     : 2021/4/8 19:38

from datasketch import MinHash

from doc_similarity.model.base_similarity import BaseSimilarity
from doc_similarity.utils.tool import Tool


class MinHashSimilarity(BaseSimilarity):
    """
    MinHash
    在大数据集中求杰尔德相似度的解决方案，通过对数据文本的降维，大大提高计算速度。
    """

    def __init__(self, stop_words_path: str):
        super(MinHashSimilarity, self).__init__()
        self._tool = Tool(stop_words_path=stop_words_path)

    def calculate(self, content_x: str, content_y: str) -> float:
        m1, m2 = MinHash(), MinHash()  # MinHash计算

        s1 = self._tool.extract_keyword(content_x, withWeigth=False)  # 提取关键词
        s2 = self._tool.extract_keyword(content_y, withWeigth=False)

        for data in s1:
            m1.update(data.encode('utf8'))
        for data in s2:
            m2.update(data.encode('utf8'))

        return m1.jaccard(m2)

    def transform(self, content: str) -> object:
        minhash = MinHash()
        keywords = self._tool.extract_keyword(content, withWeigth=False)
        for keyword in keywords:
            minhash.update(keyword.encode('utf-8'))

        return minhash
        pass

    def calculate_transform(self, transform_x: MinHash, transform_y: MinHash) -> float:
        """

        :param transform_x: minhash_1
        :param transform_y: minhash_2
        :return:
        """
        return transform_x.jaccard(transform_y)
        pass
