#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : jieba_demo
# @Author   : LiuYan
# @Time     : 2021/3/29 18:44

import jieba
import jieba.posseg as posseg

txt1 = '''
文本一：
人民网华盛顿3月28日电（记者郑琪）据美国约翰斯·霍普金斯大学疫情实时监测系统显示，截至美东时间3月28日下午6时，
美国已经至少有新冠病毒感染病例121117例，其中包括死亡病例2010例。
与大约24小时前相比，美国确诊病例至少增加了20400例，死亡病例至少增加了466例。
目前美国疫情最为严重的仍是纽约州，共有确诊病例至少52410例。此外，新泽西州有确诊病例11124例，加利福尼亚州有5065例，
密歇根州有4650例，马塞诸塞州有4257例，华盛顿州有4008例。
'''
# 精确模式
seg_list = jieba.cut(txt1, cut_all=False)
# seg_list = jieba.cut_for_search(txt1)
print("jieba分词：" + "/ ".join(seg_list))  # 精确模式
list = posseg.cut(txt1)
tag_list = []
for tag in list:
    pos_word = {}
    pos_word[1] = tag.word
    pos_word[2] = tag.flag
    tag_list.append(pos_word)
print('jieba词性标注：', tag_list)
