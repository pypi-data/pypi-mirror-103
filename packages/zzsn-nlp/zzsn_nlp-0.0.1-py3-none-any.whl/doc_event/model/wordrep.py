#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : wordrep
# @Author   : LiuYan
# @Time     : 2021/3/23 9:52

from __future__ import print_function
from __future__ import absolute_import
import os
import torch
import torch.nn as nn
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, WordpieceTokenizer

seed_num = 42
torch.manual_seed(seed_num)
np.random.seed(seed_num)

torch.cuda.manual_seed_all(seed_num)
torch.backends.cudnn.deterministic = True


class WordRep(nn.Module):
    def __init__(self, data):
        super(WordRep, self).__init__()
        print('build word representation...')
        self.gpu = data.HP_gpu
        self.batch_size = data.HP_batch_size

        self.embedding_dim = data.word_emb_dim
        self.drop = nn.Dropout(data.HP_dropout)
        self.word_embedding = nn.Embedding(data.word_alphabet.size(), self.embedding_dim)
        if data.pretrain_word_embedding is not None:
            self.word_embedding.weight.data.copy_(torch.from_numpy(data.pretrain_word_embedding))
        else:
            self.word_embedding.weight.data.copy_(
                torch.from_numpy(self.random_embedding(data.word_alphabet.size(), self.embedding_dim)))

        # bert feature
        self.word_alphabet = data.word_alphabet
        self._use_bert = data.use_bert
        self._bert_dir = data.bert_dir

        if self._use_bert:
            # Load pre-trained model (weights)
            self.bert_model = BertModel.from_pretrained(self._bert_dir)
            self.bert_model.eval()
            # Load pre-trained model tokenizer (vocabulary)
            self.tokenizer = BertTokenizer.from_pretrained(self._bert_dir)
            self.wpiecetokenizer = WordpieceTokenizer(self.tokenizer.vocab)
            self.vocab = self._read_vocab(path=self._bert_dir)

        if self.gpu:
            self.drop = self.drop.cuda()
            self.word_embedding = self.word_embedding.cuda()
            if self._use_bert:
                self.bert_model = self.bert_model.cuda()

    def random_embedding(self, vocab_size, embedding_dim):
        pretrain_emb = np.empty([vocab_size, embedding_dim])
        scale = np.sqrt(3.0 / embedding_dim)
        for index in range(vocab_size):
            pretrain_emb[index, :] = np.random.uniform(-scale, scale, [1, embedding_dim])
        return pretrain_emb

    def _read_vocab(self, path):
        result_vocab = list()
        vocab_path = os.path.join(path, 'vocab.txt')
        with open(vocab_path, 'r') as f:
            vocab = f.readlines()
        for v in vocab:
            result_vocab.append(v.strip())
        return result_vocab
        pass

    def _is_vocab(self, token):
        if token in self.vocab:
            return False
        return True
        pass

    def bert_fea(self, ids_batch):
        tokens_tensor_batch = []
        context_tokens_uncased_batch = []
        for ids in ids_batch:
            context_tokens_uncased = []
            for i in ids:
                token = self.word_alphabet.get_instance(i)
                if token == '</unk>' or not token or self._is_vocab(token):
                    context_tokens_uncased.append('[UNK]')
                elif token == '<PAD>':
                    context_tokens_uncased.append('[PAD]')
                else:
                    context_tokens_uncased.append(token)

            context_tokens_uncased_batch.append(context_tokens_uncased)
            # Tokenized input
            # Convert token to vocabulary indices
            indexed_tokens = self.tokenizer.convert_tokens_to_ids(context_tokens_uncased)
            tokens_tensor_batch.append(indexed_tokens)
            # Define sentence A and B indices associated to 1st and 2nd sentences (see paper)

        tokens_tensor_batch = torch.tensor(tokens_tensor_batch)
        if self.gpu:
            tokens_tensor_batch = tokens_tensor_batch.to('cuda')
        # Predict hidden states features for each layer
        with torch.no_grad():
            encoded_layers, _ = self.bert_model(tokens_tensor_batch)
        # get the avg of last 4 layers hidden states (for each token)
        # batchsize * doc len * 768 (bert hidden size)
        avg = sum(encoded_layers) / len(encoded_layers)
        # we do not use [CLS] fea and only use the first 100 of avg4
        context_bert_feature_batch = avg[:, :, :]

        return context_bert_feature_batch

    def forward(self, word_inputs, word_seq_lengths):
        """
            input:
                word_inputs: (batch_size, sent_len)
                word_seq_lengths: list of batch_size, (batch_size,1)
            output:
                Variable(batch_size, sent_len, hidden_dim)
        """
        word_embs = self.word_embedding(word_inputs)
        word_list = [word_embs]

        if self._use_bert:
            context_bert_feature_batch = self.bert_fea(word_inputs)
            word_list.append(context_bert_feature_batch)

        word_embs = torch.cat(word_list, 2)
        word_represent = self.drop(word_embs)

        return word_represent
