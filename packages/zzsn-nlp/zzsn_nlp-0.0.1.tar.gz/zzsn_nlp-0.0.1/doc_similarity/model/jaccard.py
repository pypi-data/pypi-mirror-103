#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : jaccard
# @Author   : LiuYan
# @Time     : 2021/4/8 19:37

from doc_similarity.model.base_similarity import BaseSimilarity
from doc_similarity.utils.tool import Tool


class JaccardSimilarity(BaseSimilarity):
    """
    jaccard相似度
    在产品描述中，很多运营人员为了偷懒，喜欢复制粘贴稍作修改，造成产品描述重复度高。通过提取产品描述的关键词，再计算两组关键词的交集并集非常适合在此场景下检测产品描述的重复度，即杰卡德相似度。
    """

    def __init__(self, stop_words_path: str):
        super(JaccardSimilarity, self).__init__()
        self._tool = Tool(stop_words_path=stop_words_path)
        pass

    def calculate(self, content_x: str, content_y: str) -> float:
        # 分词与关键词提取
        keywords_x = self._tool.extract_keyword(content_x, withWeigth=False)
        keywords_y = self._tool.extract_keyword(content_y, withWeigth=False)

        # jaccard相似度计算
        intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
        union = len(list(set(keywords_x).union(set(keywords_y))))

        sim = float(intersection) / union if union != 0 else 0
        return sim

    def transform(self, content: str) -> object:
        keywords = self._tool.extract_keyword(content, withWeigth=False)
        return keywords
        pass

    def calculate_transform(self, transform_x: object, transform_y: object) -> float:
        """

        :param transform_x: keywords_x
        :param transform_y: keywords_y
        :return:
        """
        # jaccard相似度计算
        intersection = len(list(set(transform_x).intersection(set(transform_y))))
        union = len(list(set(transform_x).union(set(transform_y))))

        sim = float(intersection) / union if union != 0 else 0
        return sim
        pass
