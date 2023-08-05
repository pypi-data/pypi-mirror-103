#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : total_sim
# @Author   : LiuYan
# @Time     : 2021/4/9 15:49

import os

from doc_similarity.model.cosine_similarity import CosineSimilarity
from doc_similarity.model.jaccard import JaccardSimilarity
from doc_similarity.model.levenshtein import LevenshteinSimilarity
from doc_similarity.model.min_hash import MinHashSimilarity
from doc_similarity.model.sim_hash import SimHashSimilarity, OldSimHashSimilarity
from doc_similarity.model.similarity_tx import Similarity


class TotalSimilarity(object):
    def __init__(self, root_path: str):
        super(TotalSimilarity, self).__init__()
        stop_words_path = os.path.join(root_path, 'stop_words.txt')
        self._cos_sim = CosineSimilarity(stop_words_path=stop_words_path)
        self._jac_sim = JaccardSimilarity(stop_words_path=stop_words_path)
        self._lev_sim = LevenshteinSimilarity(stop_words_path=stop_words_path)
        self._min_hash_sim = MinHashSimilarity(stop_words_path=stop_words_path)
        self._sim_hash_sim = SimHashSimilarity(stop_words_path=stop_words_path)
        self._old_sim_hash_sim = OldSimHashSimilarity()
        self._ctt_sim = Similarity(
            model_path=os.path.join(root_path, 'Tencent_AILab_ChineseEmbedding_Min.txt'),
            stopword_path=os.path.join(root_path, 'stopwords.txt')
        )
        pass

    def calculate(self, content_x: str, content_y: str) -> dict:
        result_dict = {
            'result_cos_sim': self._cos_sim.calculate(content_x, content_y),
            'result_jac_sim': self._jac_sim.calculate(content_x, content_y),
            'result_lev_sim': self._lev_sim.calculate(content_x, content_y),
            'result_min_hash_sim': self._min_hash_sim.calculate(content_x, content_y),
            'result_old_sim_hash_sim': self._old_sim_hash_sim.calculate(text_1=content_x, text_2=content_y),
            'result_new_sim_hash_sim': self._sim_hash_sim.calculate(content_x, content_y),
            'result_ctt_sim': self._ctt_sim.calculation_sim(content_x, content_y)
        }
        return result_dict
        pass
