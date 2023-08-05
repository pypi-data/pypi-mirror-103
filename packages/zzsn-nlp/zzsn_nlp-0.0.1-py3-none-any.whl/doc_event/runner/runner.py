#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : runner
# @Author   : LiuYan
# @Time     : 2021/3/23 9:59

from __future__ import print_function
import os
import time
import sys
import random
import torch
import gc
import xlsxwriter
import torch.optim as optim
import numpy as np

from doc_event.model.seqlabel import SeqLabel
from doc_event.data.data_loader import Data
from doc_event.evaluate.eval_entity import eval_entity

try:
    import cPickle as pickle
except ImportError:
    import pickle

seed_num = 42
random.seed(seed_num)
torch.manual_seed(seed_num)
np.random.seed(seed_num)

torch.cuda.manual_seed_all(seed_num)
torch.backends.cudnn.deterministic = True


def data_initialization(data):
    data.build_alphabet(data.train_dir)
    data.build_alphabet(data.dev_dir)
    data.build_alphabet(data.test_dir)
    data.fix_alphabet()


def predict_check(pred_variable, gold_variable, mask_variable):
    """
        input:
            pred_variable (batch_size, sent_len): pred tag result, in numpy format
            gold_variable (batch_size, sent_len): gold result variable
            mask_variable (batch_size, sent_len): mask variable
    """
    pred = pred_variable.cpu().data.numpy()
    gold = gold_variable.cpu().data.numpy()
    mask = mask_variable.cpu().data.numpy()
    overlaped = (pred == gold)

    right_token = np.sum(overlaped * mask)
    total_token = mask.sum()
    # print("right: %s, total: %s"%(right_token, total_token))
    return right_token, total_token


def recover_label(pred_variable, gold_variable, mask_variable, label_alphabet, word_recover):
    """
        input:
            pred_variable (batch_size, sent_len): pred tag result
            gold_variable (batch_size, sent_len): gold result variable
            mask_variable (batch_size, sent_len): mask variable
    """
    pred_variable = pred_variable[word_recover]
    gold_variable = gold_variable[word_recover]
    mask_variable = mask_variable[word_recover]
    batch_size = gold_variable.size(0)
    seq_len = gold_variable.size(1)
    mask = mask_variable.cpu().data.numpy()
    pred_tag = pred_variable.cpu().data.numpy()
    gold_tag = gold_variable.cpu().data.numpy()
    batch_size = mask.shape[0]
    pred_label = []
    gold_label = []
    for idx in range(batch_size):
        pred = [label_alphabet.get_instance(pred_tag[idx][idy]) for idy in range(seq_len) if mask[idx][idy] != 0]
        gold = [label_alphabet.get_instance(gold_tag[idx][idy]) for idy in range(seq_len) if mask[idx][idy] != 0]
        assert (len(pred) == len(gold))
        pred_label.append(pred)
        gold_label.append(gold)
    return pred_label, gold_label


def lr_decay(optimizer, epoch, decay_rate, init_lr):
    lr = init_lr / (1 + decay_rate * epoch)
    print(' Learning rate is set as:', lr)
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
    return optimizer


def evaluate(data, model, name):
    if name == 'train':
        instances = data.train_Ids
    elif name == 'dev':
        instance_texts, instances = data.dev_texts, data.dev_Ids
    elif name == 'test':
        instance_texts, instances = data.test_texts, data.test_Ids
    else:
        print('Error: wrong evaluate name,', name)
        exit(1)
    right_token = 0
    whole_token = 0
    pred_results = []
    gold_results = []

    sequences, doc_ids = [], []
    # set model in eval model
    model.eval()
    batch_size = data.HP_batch_size
    start_time = time.time()
    train_num = len(instances)
    total_batch = train_num // batch_size + 1
    for batch_id in range(total_batch):
        start = batch_id * batch_size
        end = (batch_id + 1) * batch_size
        if end > train_num:
            end = train_num
        instance = instances[start:end]
        instance_text = instance_texts[start:end]
        if not instance:
            continue

        batch_word, batch_word_len, batch_word_recover, list_sent_words_tensor, batch_label, mask = batchify_sequence_labeling_with_label(
            instance, data.HP_gpu, False)
        tag_seq = model(batch_word, batch_word_len, list_sent_words_tensor, mask)

        pred_label, gold_label = recover_label(tag_seq, batch_label, mask, data.label_alphabet, batch_word_recover)
        pred_results += pred_label
        gold_results += gold_label

        sequences += [item[0] for item in instance_text]
        doc_ids += [item[-1] for item in instance_text]

    # import ipdb; ipdb.set_trace()
    decode_time = time.time() - start_time
    speed = len(instances) / decode_time
    # acc, p, r, f = get_ner_fmeasure(gold_results, pred_results, data.tagScheme)
    # p, r, f = get_macro_avg(sequences, pred_results, doc_ids)

    labels = list()
    for label in data.label_alphabet.instances:
        labels.append(label)
    labels.remove('O')
    from sklearn.metrics import classification_report
    tag_true_all, tag_pred_all, text_all = list(), list(), list()
    for gold_list, pred_list, seq_list in zip(gold_results, pred_results, sequences):
        tag_true_all.extend(gold_list)
        tag_pred_all.extend(pred_list)
        text_all.extend(seq_list)
    stat_info = classification_report(tag_true_all, tag_pred_all, labels=labels, output_dict=True)
    # print(stat_info)
    macro_avg = stat_info['macro avg']
    p, r, f1 = macro_avg['precision'], macro_avg['recall'], macro_avg['f1-score']
    print('macro avg precision: %.4f, recall: %.4f, f1-score: %.4f' % (p, r, f1))

    # merge
    result_true = merge(seq_lists=sequences, tag_lists=gold_results, doc_ids=doc_ids)
    result_pred = merge(seq_lists=sequences, tag_lists=pred_results, doc_ids=doc_ids)

    return speed, p, r, f1, pred_results, result_true, result_pred


def merge(seq_lists, tag_lists, doc_ids):
    # merge the result [sequences, pred_results, doc_ids]
    doc_id_ = None
    text_all, tag_all = list(), list()
    text, tag = [], []
    for text_list, tag_list, doc_id in zip(seq_lists, tag_lists, doc_ids):
        if doc_id_ is None or doc_id_ == doc_id:
            doc_id_ = doc_id
            text.extend(text_list)
            tag.extend(tag_list)
        else:
            text_all.append(text)
            tag_all.append(tag)
            doc_id_ = doc_id
            text = text_list
            tag = tag_list

    text_all.append(text)
    tag_all.append(tag)

    return [text_all, tag_all]


def batchify_sequence_labeling_with_label(input_batch_list, gpu, if_train=True):
    """
        input: list of words, chars and labels, various length. [[words, features, chars, labels],[words, features, chars,labels],...]
            words: word ids for one sentence. (batch_size, sent_len)
            labels: label ids for one sentence. (batch_size, sent_len)

        output:
            zero padding for word and char, with their batch length
            word_seq_tensor: (batch_size, max_sent_len) Variable
            word_seq_lengths: (batch_size,1) Tensor
            label_seq_tensor: (batch_size, max_sent_len)
            mask: (batch_size, max_sent_len)
    """
    batch_size = len(input_batch_list)
    words = [sent[0] for sent in input_batch_list]
    sent_words = [sent[1] for sent in input_batch_list]
    labels = [sent[2] for sent in input_batch_list]

    word_seq_lengths = torch.LongTensor(list(map(len, words)))
    max_seq_len = word_seq_lengths.max().item()
    word_seq_tensor = torch.zeros((batch_size, max_seq_len), requires_grad=if_train).long()
    label_seq_tensor = torch.zeros((batch_size, max_seq_len), requires_grad=if_train).long()

    mask = torch.zeros((batch_size, max_seq_len), requires_grad=if_train).bool()
    for idx, (seq, label, seqlen) in enumerate(zip(words, labels, word_seq_lengths)):
        seqlen = seqlen.item()
        word_seq_tensor[idx, :seqlen] = torch.LongTensor(seq)
        label_seq_tensor[idx, :seqlen] = torch.LongTensor(label)
        mask[idx, :seqlen] = torch.Tensor([1] * seqlen)
    word_seq_lengths, word_perm_idx = word_seq_lengths.sort(0, descending=True)
    word_seq_tensor = word_seq_tensor[word_perm_idx]

    label_seq_tensor = label_seq_tensor[word_perm_idx]
    mask = mask[word_perm_idx]

    _, word_seq_recover = word_perm_idx.sort(0, descending=False)

    list_sent_words_tensor = []
    for sent_words_one_example in sent_words:
        one_example_list = []
        for sent in sent_words_one_example:
            sent_tensor = torch.zeros((1, len(sent)), requires_grad=if_train).long()
            sent_tensor[0, :len(sent)] = torch.LongTensor(sent)
            if gpu:
                one_example_list.append(sent_tensor.cuda())
            else:
                one_example_list.append(sent_tensor)
        list_sent_words_tensor.append(one_example_list)

    word_perm_idx = word_perm_idx.data.numpy().tolist()
    list_sent_words_tensor_perm = []
    for idx in word_perm_idx:
        list_sent_words_tensor_perm.append(list_sent_words_tensor[idx])

    if gpu:
        word_seq_tensor = word_seq_tensor.cuda()
        word_seq_lengths = word_seq_lengths.cuda()
        word_seq_recover = word_seq_recover.cuda()
        label_seq_tensor = label_seq_tensor.cuda()
        mask = mask.cuda()
    return word_seq_tensor, word_seq_lengths, word_seq_recover, list_sent_words_tensor_perm, label_seq_tensor, mask


def train(data):
    print('Training model...')
    data.show_data_summary()
    save_data_name = data.model_dir + '.dset'
    data.save(save_data_name)
    model = SeqLabel(data)

    if data.optimizer.lower() == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=data.HP_lr, momentum=data.HP_momentum, weight_decay=data.HP_l2)
    elif data.optimizer.lower() == 'adagrad':
        optimizer = optim.Adagrad(model.parameters(), lr=data.HP_lr, weight_decay=data.HP_l2)
    elif data.optimizer.lower() == 'adadelta':
        optimizer = optim.Adadelta(model.parameters(), lr=data.HP_lr, weight_decay=data.HP_l2)
    elif data.optimizer.lower() == "rmsprop":
        optimizer = optim.RMSprop(model.parameters(), lr=data.HP_lr, weight_decay=data.HP_l2)
    elif data.optimizer.lower() == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=data.HP_lr, weight_decay=data.HP_l2)
    else:
        print('Optimizer illegal: %s' % (data.optimizer))
        exit(1)

    best_dev = -10
    best_epoch = -10
    # start training
    for idx in range(data.HP_iteration):
        epoch_start = time.time()
        temp_start = epoch_start
        print('\nEpoch: %s/%s' % (idx + 1, data.HP_iteration))
        if data.optimizer == 'SGD':
            optimizer = lr_decay(optimizer, idx, data.HP_lr_decay, data.HP_lr)
        instance_count = 0
        sample_id = 0
        sample_loss = 0
        total_loss = 0
        right_token = 0
        whole_token = 0
        random.shuffle(data.train_Ids)
        print('Shuffle: first input word list:', data.train_Ids[0][0])
        # set model in train model
        model.train()
        model.zero_grad()
        batch_size = data.HP_batch_size
        train_num = len(data.train_Ids)
        total_batch = train_num // batch_size + 1
        for batch_id in range(total_batch):
            start = batch_id * batch_size
            end = (batch_id + 1) * batch_size
            if end > train_num:
                end = train_num
            instance = data.train_Ids[start: end]
            if not instance:
                continue
            batch_word, batch_word_len, batch_word_recover, list_sent_words_tensor, batch_label, mask = batchify_sequence_labeling_with_label(
                instance, data.HP_gpu, True)
            instance_count += 1
            loss, tag_seq = model.calculate_loss(batch_word, batch_word_len, list_sent_words_tensor, batch_label, mask)
            right, whole = predict_check(tag_seq, batch_label, mask)
            right_token += right
            whole_token += whole
            # print("loss:",loss.item())
            sample_loss += loss.item()
            total_loss += loss.item()
            if end % 500 == 0:
                temp_time = time.time()
                temp_cost = temp_time - temp_start
                temp_start = temp_time
                print('     Instance: %s; Time: %.2fs; loss: %.4f; acc: %s/%s=%.4f' % (
                    end, temp_cost, sample_loss, right_token, whole_token, (right_token + 0.) / whole_token))
                if sample_loss > 1e8 or str(sample_loss) == 'nan':
                    print('ERROR: LOSS EXPLOSION (>1e8) ! PLEASE SET PROPER PARAMETERS AND STRUCTURE! EXIT....')
                    exit(1)
                sys.stdout.flush()
                sample_loss = 0
            loss.backward()
            optimizer.step()
            model.zero_grad()
        temp_time = time.time()
        temp_cost = temp_time - temp_start
        print('     Instance: %s; Time: %.2fs; loss: %.4f; acc: %s/%s=%.4f' % (
            end, temp_cost, sample_loss, right_token, whole_token, (right_token + 0.) / whole_token))

        epoch_finish = time.time()
        epoch_cost = epoch_finish - epoch_start
        print('Epoch: %s training finished. Time: %.2fs, speed: %.2fst/s,  total loss: %s' % (
            idx + 1, epoch_cost, train_num / epoch_cost, total_loss))
        print('total_loss:', total_loss)
        if total_loss > 1e8 or str(total_loss) == 'nan':
            print('ERROR: LOSS EXPLOSION (>1e8) ! PLEASE SET PROPER PARAMETERS AND STRUCTURE! EXIT....')
            exit(1)

        # continue
        speed, p, r, f, _, result_true, result_pred = evaluate(data, model, 'dev')
        # generate results {true, pred}
        result_true_lists, result_pred_lists = generate_result_lists(result_true, result_pred)
        p, r, f1 = eval_entity(result_true_lists, result_pred_lists)

        dev_finish = time.time()
        dev_cost = dev_finish - epoch_finish

        current_score = f1
        print(
            'Dev: time: %.2fs, speed: %.2fst/s; precision: %.4f, recall: %.4f, f1-score: %.4f' % (
                dev_cost, speed, p, r, f1
            )
        )

        if current_score > best_dev:
            print('\n!!! Exceed previous best f1-score: {}'.format(best_dev))
            model_name = data.model_dir + '.best.model'
            print('Save current best model in file: {}\n'.format(model_name))
            torch.save(model.state_dict(), model_name)
            best_dev = current_score
            best_epoch = idx + 1
        else:
            print('\nBest model in epoch: {}, f1-score: {}\n'.format(best_epoch, best_dev))

        gc.collect()


def load_model_decode(data, name):
    print('Load Model from file: ', data.model_dir)
    model = SeqLabel(data)
    if data.HP_gpu:
        model.load_state_dict(torch.load(data.load_model_dir))
    else:
        model.load_state_dict(torch.load(data.load_model_dir, map_location=lambda storage, loc: storage))

    start_time = time.time()
    speed, p, r, f, pred_results, result_true, result_pred = evaluate(data, model, name)
    end_time = time.time()
    time_cost = end_time - start_time

    # generate results {true, pred}
    result_true_lists, result_pred_lists = generate_result_lists(result_true, result_pred)
    p, r, f1 = eval_entity(result_true_lists, result_pred_lists)
    print('\n{}: time_cost: {:.2f}s, speed: {:.2f}st/s, precision: {:.4f}, recall: {:.4f}, f1-score: {:.4f}'.format(
        name, time_cost, speed, p, r, f1
    ))

    list2xlsx(xlsx_path=data.result_true_path, result_lists=result_true_lists)
    list2xlsx(xlsx_path=data.result_pred_path, result_lists=result_pred_lists)

    return pred_results


def generate_result_lists(result_true, result_pred):
    # generate results {true, pred}
    result_true_lists, result_pred_lists = list(), list()
    for word_true_list, tag_true_list, word_pred_list, tag_pred_list in zip(
            result_true[0], result_true[1], result_pred[0], result_pred[1]
    ):
        result_true_dict = build_list2dict(len(word_true_list), word_true_list, tag_true_list, typ='true')
        result_pred_dict = build_list2dict(len(word_pred_list), word_pred_list, tag_pred_list, typ='pred')
        result_true_lists.append(result_true_dict)
        result_pred_lists.append(result_pred_dict)

    return result_true_lists, result_pred_lists


def build_list2dict(_len, _word_list, _tag_list, typ):
    ps_list = list()
    result_dict = {
        'content': ''.join(_word_list),
        'amount_of_cooperation': set(),
        'project_name': set(),
        'state': set(),
        'company_identification_Party_A': set(),
        'company_identification_Party_B': set(),
        'project_cycle': set(),
        'project_status': set()
    }
    # tag_dict = {
    #     'amount_of_cooperation': '合作金额',
    #     'project_name': '项目名称',
    #     'state': '国家',
    #     'company_identification_Party_A': '企业识别甲方',
    #     'company_identification_Party_B': '企业识别乙方',
    #     'project_cycle': '项目周期',
    #     'project_status': '项目状态'
    # }
    for index, word, tag in zip(range(_len), _word_list, _tag_list):
        start_pos = index
        end_pos = index + 1
        label_type = tag[2:]
        if tag[0] == 'B' and end_pos != _len:
            # two !=
            while _tag_list[end_pos][0] == 'I' and _tag_list[end_pos][2:] == label_type and end_pos + 1 != _len:
                end_pos += 1
            if _tag_list[end_pos][0] == 'E':
                chunk = ''.join(_word_list[start_pos: end_pos + 1])
                if label_type == 'project_status' and typ == 'pred':
                    ps_list.append(chunk)
                else:
                    result_dict[label_type].add(chunk)
    if typ == 'pred' and len(ps_list) > 0:
        result_dict['project_status'] = [max(ps_list, key=ps_list.count)]

    return result_dict


def list2xlsx(xlsx_path=None, result_lists=None):
    # 创建工作簿
    workbook = xlsxwriter.Workbook(xlsx_path)
    # 创建工作表
    worksheet = workbook.add_worksheet('sheet1')
    # 按行写
    worksheet.write_row(
        0, 0, [
            '合同金额',
            '项目名称',
            '国家',
            '企业识别甲方',
            '企业识别乙方',
            '项目周期',
            '项目状态'
        ]
    )
    for index, result in enumerate(result_lists):
        worksheet.write_row(
            index + 1, 0, [
                ','.join(result['amount_of_cooperation']),
                ','.join(result['project_name']),
                ','.join(result['state']),
                ','.join(result['company_identification_Party_A']),
                ','.join(result['company_identification_Party_B']),
                ','.join(result['project_cycle']),
                ','.join(result['project_status'])
            ]
        )

    workbook.close()


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    config_path = '../config/config'
    data = Data()
    data.read_config(config_file=config_path)
    status = data.status.lower()
    print('Seed num:', seed_num)

    if status == 'train':
        print('MODEL: train')
        data_initialization(data)
        data.generate_instance('train')
        data.generate_instance('dev')
        data.generate_instance('test')
        data.build_pretrain_emb()
        train(data)

        print('\n\nMODEL: decode')
        data.load(data.dset_dir)
        decode_results = load_model_decode(data, 'test')
        data.write_decoded_results(decode_results, 'test')

    elif status == 'decode':
        print('MODEL: decode')
        data.load(data.dset_dir)
        data.read_config(config_file=config_path)
        print(data.test_dir)

        data.generate_instance('test')
        decode_results = load_model_decode(data, 'test')
        data.write_decoded_results(decode_results, 'test')
    else:
        print('Invalid argument! Please use valid arguments! (train/decode)')
