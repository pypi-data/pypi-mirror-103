#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : functions
# @Author   : LiuYan
# @Time     : 2021/3/23 9:57

from __future__ import print_function
from __future__ import absolute_import
import numpy as np


def normalize_word(word):
    new_word = ''
    for char in word:
        if char.isdigit():
            new_word += '0'
        else:
            new_word += char
    return new_word


def read_instance(input_file, word_alphabet, label_alphabet, number_normalized, max_sent_length, split_token='\t'):
    in_lines = open(input_file, 'r', encoding='utf-8').readlines()
    instance_texts, instance_Ids = [], []
    doc_id = ''
    words, labels = [], []
    word_Ids, label_Ids = [], []

    # for sequence labeling data format i.e. CoNLL 2003
    for line in in_lines:
        if not doc_id:
            doc_id = line.strip()
            continue
        if len(line) > 2:
            pairs = line.strip('\n').split(split_token)
            word = pairs[0]
            words.append(word)
            if number_normalized:
                word = normalize_word(word)
            label = pairs[-1]
            labels.append(label)
            word_Ids.append(word_alphabet.get_index(word))
            label_Ids.append(label_alphabet.get_index(label))
        else:
            if (len(words) > 0) and ((max_sent_length < 0) or (len(words) < max_sent_length)):
                # get sent_word_Ids_list (split with '.')
                period_id = word_alphabet.get_index('#####')
                sent_word_Ids_list = []
                idx = 0
                sent_word_Ids = []
                while idx <= len(word_Ids) - 1:
                    sent_word_Ids.append(word_Ids[idx])
                    if word_Ids[idx] == period_id:
                        sent_word_Ids_list.append(sent_word_Ids)
                        sent_word_Ids = []
                    idx += 1
                if sent_word_Ids:
                    sent_word_Ids_list.append(sent_word_Ids)

                instance_texts.append([words, labels, doc_id])
                instance_Ids.append([word_Ids, sent_word_Ids_list, label_Ids])
            doc_id = ''
            words, labels = [], []
            word_Ids, label_Ids = [], []

    return instance_texts, instance_Ids


def build_pretrain_embedding(embedding_path, word_alphabet, embedd_dim=100, norm=True):
    embedd_dict = dict()
    if embedding_path != None:
        embedd_dict, embedd_dim = load_pretrain_emb(embedding_path)
    alphabet_size = word_alphabet.size()
    scale = np.sqrt(3.0 / embedd_dim)
    pretrain_emb = np.empty([word_alphabet.size(), embedd_dim])
    perfect_match = 0
    case_match = 0
    not_match = 0
    for word, index in word_alphabet.iteritems():
        if word in embedd_dict:
            if norm:
                pretrain_emb[index, :] = norm2one(embedd_dict[word])
            else:
                pretrain_emb[index, :] = embedd_dict[word]
            perfect_match += 1
        elif word.lower() in embedd_dict:
            if norm:
                pretrain_emb[index, :] = norm2one(embedd_dict[word.lower()])
            else:
                pretrain_emb[index, :] = embedd_dict[word.lower()]
            case_match += 1
        else:
            pretrain_emb[index, :] = np.random.uniform(-scale, scale, [1, embedd_dim])
            not_match += 1
    pretrained_size = len(embedd_dict)
    print('Embedding:\n     pretrain word:%s, prefect match:%s, case_match:%s, oov:%s, oov%%:%s' % (
        pretrained_size, perfect_match, case_match, not_match, (not_match + 0.) / alphabet_size))
    return pretrain_emb, embedd_dim


def norm2one(vec):
    root_sum_square = np.sqrt(np.sum(np.square(vec)))
    return vec / root_sum_square


def load_pretrain_emb(embedding_path):
    embedd_dim = -1
    embedd_dict = dict()
    with open(embedding_path, 'r', encoding='ISO-8859-1') as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                continue
            tokens = line.split()
            if embedd_dim < 0:
                embedd_dim = len(tokens) - 1
            elif embedd_dim + 1 != len(tokens):
                # ignore illegal embedding line
                continue
                # assert (embedd_dim + 1 == len(tokens))
            embedd = np.empty([1, embedd_dim])
            embedd[:] = tokens[1:]
            first_col = tokens[0]
            embedd_dict[first_col] = embedd
    return embedd_dict, embedd_dim


if __name__ == '__main__':
    a = np.arange(9.0)
    print(a)
    print(norm2one(a))
