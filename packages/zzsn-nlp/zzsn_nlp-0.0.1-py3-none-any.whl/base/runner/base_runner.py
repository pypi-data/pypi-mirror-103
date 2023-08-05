#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_runner
# @Author   : LiuYan
# @Time     : 2021/4/19 10:42

from abc import ABC, abstractmethod


class BaseRunner(ABC):
    """
    Abstract definition for runner
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _build_config(self):
        pass

    @abstractmethod
    def _build_data(self):
        pass

    @abstractmethod
    def _build_model(self):
        pass

    @abstractmethod
    def _build_loss(self):
        pass

    @abstractmethod
    def _build_optimizer(self):
        pass

    @abstractmethod
    def _build_evaluator(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def _train_epoch(self, epoch: int):
        pass

    @abstractmethod
    def _valid(self, epoch: int):
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def pred(self):
        pass

    @abstractmethod
    def _display_result(self, epoch: int):
        pass

    @abstractmethod
    def _save_checkpoint(self, epoch: int):
        pass

    @abstractmethod
    def _load_checkpoint(self):
        pass
