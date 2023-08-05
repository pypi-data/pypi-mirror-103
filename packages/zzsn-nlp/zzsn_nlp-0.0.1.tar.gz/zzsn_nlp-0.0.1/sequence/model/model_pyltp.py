#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : model_pyltp
# @Author   : LiuYan
# @version  : v3.4.0
# @Time     : 2021/3/31 10:00

import os
from pyltp import Segmentor, Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller
from pyltp import SentenceSplitter


class LTP(object):
    def __init__(self, model_path: str):
        super(LTP, self).__init__()
        self._model_path = model_path
        self._build_model()

    def _build_model(self):
        self._cws = Segmentor()
        self._pos = Postagger()
        self._ner = NamedEntityRecognizer()
        self._parser = Parser()
        self._role_label = SementicRoleLabeller()
        self._cws.load(os.path.join(self._model_path, 'cws.model'))
        self._pos.load(os.path.join(self._model_path, 'pos.model'))
        self._ner.load(os.path.join(self._model_path, 'ner.model'))
        self._parser.load(os.path.join(self._model_path, 'parser.model'))
        self._role_label.load(os.path.join(self._model_path, 'pisrl.model'))
        pass

    def split(self, sentence: str) -> list:  # 分句
        sents = SentenceSplitter.split(sentence)
        sents_list = list(sents)
        return sents_list

    def cws(self, sentence: str) -> list:
        word_list = list(self._cws.segment(sentence))
        return word_list

    def pos(self, sentence: str) -> [list, list]:
        word_list = self.cws(sentence=sentence)
        tag_list = list(self._pos.postag(word_list))
        return word_list, tag_list

    def ner(self, sentence: str) -> [list, list]:
        word_list, tag_list = self.pos(sentence=sentence)
        tag_list = list(self._ner.recognize(word_list, tag_list))
        return word_list, tag_list

    def parse(self, sentence: str) -> [list, list, list]:
        word_list, tag_list = self.pos(sentence=sentence)
        arc_list = list(self._parser.parse(word_list, tag_list))
        return word_list, tag_list, arc_list

    def role_label(self, sentence: str) -> [list, list, list, list]:
        word_list, tag_list, arc_list = self.parse(sentence=sentence)
        role_list = list(self._role_label.label(word_list, tag_list, arc_list))
        return word_list, tag_list, arc_list, role_list

    def release(self):
        self._cws.release()
        self._pos.release()
        self._ner.release()
        self._parser.release()
        self._role_label.release()
