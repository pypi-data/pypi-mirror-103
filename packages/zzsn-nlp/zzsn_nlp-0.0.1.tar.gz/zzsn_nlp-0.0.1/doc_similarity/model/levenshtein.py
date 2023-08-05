#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : levenshtein
# @Author   : LiuYan
# @Time     : 2021/4/8 19:38

import Levenshtein

from doc_similarity.model.base_similarity import BaseSimilarity
from doc_similarity.utils.tool import Tool


class LevenshteinSimilarity(BaseSimilarity):
    """
    编辑距离
    """

    def __init__(self, stop_words_path: str):
        super(LevenshteinSimilarity, self).__init__()
        self._tool = Tool(stop_words_path=stop_words_path)

    def calculate(self, content_x: str, content_y: str) -> float:
        # 提取关键词
        keywords_1 = ', '.join(self._tool.extract_keyword(content_x, withWeigth=False))
        keywords_2 = ', '.join(self._tool.extract_keyword(content_y, withWeigth=False))

        # ratio计算2个字符串的相似度，它是基于最小编辑距离
        distances = Levenshtein.ratio(keywords_1, keywords_2)
        return distances

    def transform(self, content: str) -> object:
        keywords = ', '.join(self._tool.extract_keyword(content, withWeigth=False))
        return keywords
        pass

    def calculate_transform(self, transform_x: object, transform_y: object) -> float:
        """

        :param transform_x: keywords_1
        :param transform_y: keywords_2
        :return:
        """
        distances = Levenshtein.ratio(transform_x, transform_y)
        return distances
        pass
