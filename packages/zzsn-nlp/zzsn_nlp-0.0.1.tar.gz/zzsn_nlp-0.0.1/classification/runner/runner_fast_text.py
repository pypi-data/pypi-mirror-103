#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : runner_fast_text
# @Author   : LiuYan
# @Time     : 2021/4/15 16:44


import fasttext

from pathlib import Path

from utils.log import logger
from utils.utils import timeit
from base.runner.base_runner import BaseRunner
from classification.config.fast_text_config import FastTextConfig
from classification.evaluation.classify_evaluator import ClassifyEvaluator
from classification.utils.utils import *


class FastTextRunner(BaseRunner):
    def __init__(self, config_path: str):
        super(FastTextRunner, self).__init__()
        self._config_path = config_path
        self._config = None

        self._train_dataloader = None
        self._valid_dataloader = None
        self._test_dataloader = None

        self._model = None
        self._loss = None
        self._optimizer = None

        self._evaluator = None
        self._build()

    @timeit
    def _build(self):
        self._build_config()
        self._build_data()
        self._build_model()
        self._build_loss()
        self._build_optimizer()
        self._build_evaluator()
        pass

    def _build_config(self):
        self._config = FastTextConfig(config_path=self._config_path).load_config()
        pass

    def _build_data(self):
        self._train_path = self._config.data.train_path
        self._valid_path = self._config.data.valid_path
        self._test_path = self._config.data.test_path
        pass

    def _build_model(self):
        if self._config.status == 'test' or 'pred':
            self._load_checkpoint()
        pass

    def _build_loss(self):
        pass

    def _build_optimizer(self):
        pass

    def _build_evaluator(self):
        self._evaluator = ClassifyEvaluator()
        pass

    @timeit
    def train(self):
        self._model = fasttext.train_supervised(
            input=self._train_path, autotuneValidationFile=self._test_path,
            autotuneDuration=3000, autotuneModelSize='200M'
        )
        self._save_checkpoint(epoch=100)
        self._valid(epoch=100)
        pass

    def _train_epoch(self, epoch: int):
        pass

    def _valid(self, epoch: int):
        with open(self._valid_path, encoding='utf-8') as file:
            self._valid_dataloader = file.readlines()
        labels = []
        pre_labels = []
        for text in self._valid_dataloader:
            label = text.replace('__label__', '')[0]
            text = text.replace('__label__', '')[1:-1]
            labels.append(int(label))
            # print(model.predict(text))
            pre_label = self._model.predict(text)[0][0].replace('__label__', '')
            # print(pre_label)
            pre_labels.append(int(pre_label))
            # print(model.predict(text))

        # p = precision_score(labels, pre_labels)
        # r = recall_score(labels, pre_labels)
        # f1 = f1_score(labels, pre_labels)
        p, r, f1 = self._evaluator.evaluate(true_list=labels, pred_list=pre_labels)

        logger.info('P: {:.4f}, R: {:.4f}, F1: {:.4f}'.format(p, r, f1))
        pass

    def test(self):
        self._valid(epoch=100)
        pass

    def pred(self, id: int, title: str, content: str):
        text = (title + '。') * 2 + content
        text = clean_txt(raw=clean_tag(text=text))
        if type(text) is str:
            text = text.replace('\n', '').replace('\r', '').replace('\t', '')
        pre_label = self._model.predict(text)[0][0].replace('__label__', '')
        if pre_label == '0':
            label = '非招聘股票'
        elif pre_label == '1':
            label = '招聘信息'
        else:
            label = '股票信息'

        return {
            'handleMsg': 'success',
            'isHandleSuccess': True,
            'logs': None,
            'resultData': {
                'id': id,
                'label': label
            }
        }
        pass

    def _display_result(self, epoch: int):
        pass

    @timeit
    def _save_checkpoint(self, epoch: int):
        Path(self._config.learn.dir.saved).mkdir(parents=True, exist_ok=True)
        self._model.save_model(self._config.learn.dir.save_model)
        pass

    def _load_checkpoint(self):
        self._model = fasttext.load_model(self._config.learn.dir.save_model)
        pass


if __name__ == '__main__':
    ft_config_path = '../config/fast_text_config.yml'
    runner = FastTextRunner(config_path=ft_config_path)
    # runner.train()
    runner.test()
