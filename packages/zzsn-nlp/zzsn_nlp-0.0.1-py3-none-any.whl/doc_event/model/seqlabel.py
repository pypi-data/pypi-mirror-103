#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : seqlabel
# @Author   : LiuYan
# @Time     : 2021/3/23 9:50

from __future__ import print_function
from __future__ import absolute_import
import torch
import torch.nn as nn
import torch.nn.functional as F

from doc_event.model.wordsequence import WordSequence
from doc_event.model.crf import CRF


class SeqLabel(nn.Module):
    def __init__(self, data):
        super(SeqLabel, self).__init__()
        self.use_crf = data.use_crf
        print('build sequence labeling network...')
        print('word feature extractor: ', data.word_feature_extractor)
        print('use crf: ', self.use_crf)

        self.gpu = data.HP_gpu
        self.average_batch = data.average_batch_loss
        # add two more label for downlayer lstm, use original label size for CRF
        label_size = data.label_alphabet_size
        data.label_alphabet_size += 2
        self.word_hidden = WordSequence(data)
        if self.use_crf:
            self.crf = CRF(label_size, self.gpu)

    def calculate_loss(self, word_inputs, word_seq_lengths, list_sent_words_tensor, batch_label, mask):
        outs = self.word_hidden(word_inputs, list_sent_words_tensor, word_seq_lengths)
        batch_size = word_inputs.size(0)
        seq_len = word_inputs.size(1)
        if self.use_crf:
            total_loss = self.crf.neg_log_likelihood_loss(outs, mask, batch_label)
            scores, tag_seq = self.crf._viterbi_decode(outs, mask)
        else:
            loss_function = nn.NLLLoss(ignore_index=0, size_average=False)
            outs = outs.view(batch_size * seq_len, -1)
            score = F.log_softmax(outs, 1)
            total_loss = loss_function(score, batch_label.view(batch_size * seq_len))
            _, tag_seq = torch.max(score, 1)
            tag_seq = tag_seq.view(batch_size, seq_len)
        if self.average_batch:
            total_loss = total_loss / batch_size
        return total_loss, tag_seq

    def forward(self, word_inputs, word_seq_lengths, list_sent_words_tensor, mask):
        outs = self.word_hidden(word_inputs, list_sent_words_tensor, word_seq_lengths)
        batch_size = word_inputs.size(0)
        seq_len = word_inputs.size(1)
        if self.use_crf:
            scores, tag_seq = self.crf._viterbi_decode(outs, mask)
        else:
            outs = outs.view(batch_size * seq_len, -1)
            _, tag_seq = torch.max(outs, 1)
            tag_seq = tag_seq.view(batch_size, seq_len)
            # filter padded position with zero
            tag_seq = mask.long() * tag_seq
        return tag_seq
