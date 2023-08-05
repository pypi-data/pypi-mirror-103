#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : ltp_demo
# @Author   : LiuYan
# @Time     : 2021/3/29 15:23

from ltp import LTP

ltp = LTP()
seg, hidden = ltp.seg(["他叫汤姆去拿外衣。"])
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)
sentences = ltp.sent_split(["他叫汤姆去拿外衣。", "汤姆生病了。他去了医院。"])
print(sentences)
