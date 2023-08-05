#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_evaluator
# @Author   : LiuYan
# @Time     : 2021/4/19 10:39

from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    @abstractmethod
    def __init__(self):
        super(BaseEvaluator, self).__init__()

    @abstractmethod
    def evaluate(self):
        pass
