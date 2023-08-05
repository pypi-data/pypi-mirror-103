#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_data_reader
# @Author   : LiuYan
# @Time     : 2021/4/19 9:37

from abc import ABC, abstractmethod


class BaseDataReader(ABC):
    @abstractmethod
    def __init__(self):
        super(BaseDataReader, self).__init__()

    @abstractmethod
    def reade(self):
        pass

    @abstractmethod
    def save(self):
        pass
