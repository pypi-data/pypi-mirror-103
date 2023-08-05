#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : utils
# @Author   : LiuYan
# @Time     : 2021/4/16 16:40

import re
import jieba

from bs4 import BeautifulSoup


def clean_tag(text):
    """
    清除网页标签
    :param text:
    :return:
    """
    # print(text)
    bs = BeautifulSoup(text, 'html.parser')
    # print(bs.text)
    return bs.text


def clean_txt(raw):
    """
    去除表情
    :param raw:
    :return:
    """
    res = re.compile(u'[\U00010000-\U0010ffff\uD800-\uDBFF\uDC00-\uDFFF]')
    return res.sub('', raw)


def seg(text, sw):
    """
    分词，NLPTokenizer会基于全部命名实体识别和词性标注进行分词
    :param text:
    :param NLPTokenizer:
    :param sw:
    :return:
    """
    # text = ' '.join([i.word for i in NLPTokenizer.segment(text) if i.word.strip() and i.word not in sw])
    text = ' '.join([i.strip() for i in jieba.cut(text) if i.strip() and i not in sw])
    return text


def stop_words(path: str) -> list:
    """
    去除停用词
    :return:
    """
    with open(path, 'r', encoding='utf-8') as swf:
        return [line.strip() for line in swf]


def segment_para(text):
    """

    :param text:
    :return:
    """
    split_pattern = re.compile(r'\n|。|？|！|\?|\!|\s')
    global_sentences = split_pattern.split(text)
    global_sentences = ''.join([str(i).strip() + '。' for i in global_sentences if len(i) >= 13])
    return global_sentences


def cut_sent(para):
    """

    :param para:
    :return:
    """
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    return para.split("\n")


def transform_data(text, label):
    """

    :param text:
    :param label:
    :return:
    """
    fasttext_line = "__label__{} {}".format(label, text)
    return fasttext_line
