#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : text_cnn
# @Author   : LiuYan
# @Time     : 2021/4/19 11:10

import torch

from torch import nn
from torch.nn import functional as F

from base.model.base_model import BaseModel


class TextCNN(BaseModel):
    def __init__(self, model_config):
        super(TextCNN, self).__init__()
        self._config = model_config
        self._device = self._config.device

        self._num_vocab = self._config.data.num_vocab
        self._num_category = self._config.data.num_category

        self._dim_embed = self._config.model.dim_embed
        self._dim_hidden = self._config.model.dim_hidden
        self._size_kernel = self._config.model.size_kernel

        self._rate_dropout = self._config.learn.rate_dropout

        # for embedding
        self.embed = nn.Embedding(self._num_vocab, self._dim_embed)
        # for conv
        self.conv = nn.Conv1d(self._dim_embed, self._dim_hidden, self._size_kernel)

        self.dropout = nn.Dropout(p=self._rate_dropout)

        # for pool
        self.pool = nn.MaxPool1d(kernel_size=self._size_kernel)

        # FC layer
        self.fc = nn.Linear(self._dim_hidden, self._num_category)

        pass

    def forward(self, dict_inputs: dict) -> dict:
        dict_outputs = dict()
        (text, length), label = dict_inputs
        # batch_size = len(label.T)

        input_embed = torch.transpose(self.embed(text), 0, 1)
        input_feature = input_embed.permute(0, 2, 1).contiguous()
        # input_feature = self.dropout(input_feature)

        output_conv = self.conv(input_feature)
        output_conv = self.dropout(output_conv)

        output_pool = torch.squeeze(F.max_pool1d(output_conv, output_conv.size(2)), dim=-1)
        output_pool = self.dropout(output_pool)

        outputs = self.fc(output_pool)
        dict_outputs['outputs'] = outputs

        output_predicts = torch.argmax(outputs, dim=-1)
        dict_outputs['predicts'] = output_predicts

        dict_outputs['labels'] = label

        return dict_outputs
        pass
