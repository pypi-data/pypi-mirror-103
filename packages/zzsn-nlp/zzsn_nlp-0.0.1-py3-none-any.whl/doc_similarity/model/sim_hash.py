#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : sim_hash
# @Author   : LiuYan
# @Time     : 2021/4/8 19:35

import re
import math

from simhash import Simhash

from doc_similarity.model.base_similarity import BaseSimilarity
from doc_similarity.utils.tool import Tool


class OldSimHashSimilarity(BaseSimilarity):

    def __init__(self):
        super(OldSimHashSimilarity, self).__init__()

    @staticmethod
    def _filter_html(html):
        """
        :param html: html
        :return: 返回去掉html的纯净文本
        """
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html).strip()
        return dd

    def calculate(self, text_1: str, text_2: str):  # 求两篇文章相似度
        """
        :param text_1: 文本_1
        :param text_2: 文本_2
        :return: 返回两篇文章的相似度
        """
        simhash_1 = Simhash(text_1)
        simhash_2 = Simhash(text_2)
        # print(len(bin(simhash_1.value)), (len(bin(simhash_2.value))))

        max_hash_bit = max(len(bin(simhash_1.value)), (len(bin(simhash_2.value))))
        # print(max_hash_bit)

        # 海明距离（Hamming distance）
        hamming_distance = simhash_1.distance(simhash_2)
        # print(hamming_distance)

        similarity = 1 - hamming_distance / max_hash_bit
        return similarity

    def transform(self, content: str) -> object:
        simhash = Simhash(content)

        return simhash
        pass

    def calculate_transform(self, transform_x: Simhash, transform_y: Simhash) -> float:
        """

        :param transform_x: simhash_1
        :param transform_y: simhash_2
        :return:
        """
        max_hash_bit = max(len(bin(transform_x.value)), (len(bin(transform_y.value))))
        hamming_distance = transform_x.distance(transform_y)
        similarity = 1 - hamming_distance / max_hash_bit

        return similarity
        pass


class SimHashSimilarity(object):
    """
    SimHash
    对单词数量低于500的文章误差较大。
    """

    def __init__(self, stop_words_path: str):
        self._tool = Tool(stop_words_path=stop_words_path)
        pass

    @staticmethod
    def get_bin_str(source):  # 字符串转二进制
        if source == '':
            return 0
        else:
            t = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                t = ((t * m) ^ ord(c)) & mask
            t ^= len(source)
            if t == -1:
                t = -2
            t = bin(t).replace('0b', '').zfill(64)[-64:]
            return str(t)

    def _run(self, keywords):
        ret = []
        for keyword, weight in keywords:
            bin_str = self.get_bin_str(keyword)
            key_list = []
            for c in bin_str:
                weight = math.ceil(weight)
                if c == '1':
                    key_list.append(int(weight))
                else:
                    key_list.append(-int(weight))
            ret.append(key_list)
        # 对列表进行"降维"
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = '1'
            elif tmp <= 0:
                tmp = '0'
            result.append(tmp)
        return ''.join(result)

    def calculate(self, content_x: str, content_y: str):
        # 提取关键词
        s1 = self._tool.extract_keyword(content_x, withWeigth=True)
        s2 = self._tool.extract_keyword(content_y, withWeigth=True)

        sim_hash_1 = self._run(s1)
        sim_hash_2 = self._run(s2)
        # print(f'相似哈希指纹1: {sim_hash1}\n相似哈希指纹2: {sim_hash2}')
        length = 0
        for index, char in enumerate(sim_hash_1):
            if char == sim_hash_2[index]:
                continue
            else:
                length += 1
        return length
