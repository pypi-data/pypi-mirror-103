#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : fast_text_config
# @Author   : LiuYan
# @Time     : 2021/4/19 10:46

import dynamic_yaml
import torch

from base.config.base_config import BaseConfig


class FastTextConfig(BaseConfig):
    def __init__(self, config_path):
        super(FastTextConfig, self).__init__()
        self._config_path = config_path
        pass

    def load_config(self):
        with open(self._config_path, mode='r', encoding='UTF-8') as f:
            config = dynamic_yaml.load(f)
        config.device = torch.device(config.device if torch.cuda.is_available() else 'cpu')
        return config
        pass
