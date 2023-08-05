#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_data_loader
# @Author   : LiuYan
# @Time     : 2021/4/19 9:37

from abc import ABC, abstractmethod


class BaseDataLoader(ABC):
    @abstractmethod
    def __init__(self):
        super(BaseDataLoader, self).__init__()

    @abstractmethod
    def _load_data(self):
        """
        load raw data according to data config
        :return:
        """
        pass

    @abstractmethod
    def load_train(self):
        pass

    @abstractmethod
    def load_valid(self):
        pass

    @abstractmethod
    def load_test(self):
        pass

    pass
