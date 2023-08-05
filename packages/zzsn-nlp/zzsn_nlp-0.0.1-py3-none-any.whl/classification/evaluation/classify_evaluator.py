#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : eval_classification
# @Author   : LiuYan
# @Time     : 2021/4/20 21:19

from base.evaluation.base_evaluator import BaseEvaluator


class ClassifyEvaluator(BaseEvaluator):

    def __init__(self):
        super(ClassifyEvaluator, self).__init__()
        pass

    def evaluate(self, true_list: list, pred_list: list) -> tuple:
        TP, FP = 0, 0
        TP_FN = len(true_list)
        for true, pred in zip(true_list, pred_list):
            if true == pred:
                TP += 1
            else:
                FP += 1

        p = TP / (TP + FP) if (TP + FP) != 0 else 0
        r = TP / TP_FN if TP_FN != 0 else 0
        f1 = (2 * p * r) / (p + r) if (p + r) != 0 else 0
        return p, r, f1
        pass
