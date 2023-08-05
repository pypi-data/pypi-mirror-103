#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : tool
# @Author   : LiuYan
# @Time     : 2021/4/9 9:57

import re
import html
import jieba
import jieba.analyse


class Tool(object):
    def __init__(self, stop_words_path: str):
        jieba.analyse.set_stop_words(stop_words_path=stop_words_path)  # 去除停用词
        jieba.cut('北京天安门', cut_all=True)  # 切割

    @staticmethod
    def extract_keyword(content: str, withWeigth: bool):  # 提取关键词
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)  # 正则过滤 html 标签
        content = re_exp.sub(' ', content)

        content = html.unescape(content)  # html 转义符实体化

        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']  # 切割

        keywords = jieba.analyse.extract_tags('|'.join(seg), topK=200, withWeight=withWeigth)    # 提取关键词
        return keywords
