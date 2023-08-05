#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_data_process
# @Author   : LiuYan
# @Time     : 2021/4/19 9:37

from abc import ABC, abstractmethod


class BaseDataProcess(ABC):
    """
    data processing
    """

    @abstractmethod
    def __init__(self):
        super(BaseDataProcess, self).__init__()

    @abstractmethod
    def process(self):
        pass
