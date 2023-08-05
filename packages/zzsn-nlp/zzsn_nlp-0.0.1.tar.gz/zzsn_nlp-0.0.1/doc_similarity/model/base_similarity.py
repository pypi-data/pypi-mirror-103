#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_similarity
# @Author   : LiuYan
# @Time     : 2021/4/10 15:34

from abc import ABC, abstractmethod


class BaseSimilarity(ABC):
    def __init__(self):
        super(BaseSimilarity, self).__init__()

    @abstractmethod
    def calculate(self, content_x: str, content_y: str) -> float:
        pass

    @abstractmethod
    def transform(self, content: str) -> object:
        pass

    @abstractmethod
    def calculate_transform(self, transform_x: object, transform_y: object) -> float:
        pass
