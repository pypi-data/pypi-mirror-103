#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : base_loss
# @Author   : LiuYan
# @Time     : 2021/4/19 10:41

from abc import abstractmethod
import torch.nn as nn


class BaseLoss(nn.Module):

    def __init__(self, loss_config):
        super(BaseLoss, self).__init__()
        self._config = loss_config

    @abstractmethod
    def forward(self, dict_outputs: dict) -> dict:
        pass
