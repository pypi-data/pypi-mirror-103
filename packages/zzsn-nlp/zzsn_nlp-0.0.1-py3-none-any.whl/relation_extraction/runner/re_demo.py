#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : re_demo
# @Author   : LiuYan
# @Time     : 2021/3/20 14:37

import opennre

model = opennre.get_model('wiki80_bert_softmax')
result = model.infer(
    {
        'text': 'He was the son of Máel Dúin mac Máele Fithrich, and grandson of the high king Áed Uaridnach (died 612).',
        'h': {'pos': (18, 46)},
        't': {'pos': (78, 91)}
    }
)
print(result)