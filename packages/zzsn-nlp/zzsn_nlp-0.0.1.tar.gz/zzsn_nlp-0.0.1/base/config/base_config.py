#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_config
# @Author   : LiuYan
# @Time     : 2021/4/16 18:06

from abc import abstractmethod, ABC


class BaseConfig(ABC):
    @abstractmethod
    def __init__(self):
        super(BaseConfig, self).__init__()

    @abstractmethod
    def load_config(self):
        """
        Add the config you need.
        :return: config(YamlDict)
        """
        pass
