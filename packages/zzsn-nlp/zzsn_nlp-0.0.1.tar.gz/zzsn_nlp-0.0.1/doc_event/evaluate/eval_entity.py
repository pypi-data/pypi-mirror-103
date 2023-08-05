#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : eval_entity
# @Author   : LiuYan
# @Time     : 2021/1/15 18:02


def eval_entity(true_lists, pred_lists):
    TP, FN, FP = 0, 0, 0
    for true_dict, pred_dict in zip(true_lists, pred_lists):
        tp, fn, fp = compute_entity(true_dict, pred_dict)
        TP += tp
        FN += fn
        FP += fp

    p = TP / (TP + FP) if (TP + FP) != 0 else 0
    r = TP / (TP + FN) if (TP + FN) != 0 else 0
    f1 = (2 * p * r) / (p + r) if (p + r) != 0 else 0
    return p, r, f1


def compute_entity(true_dict, pred_dict):
    content_true, content_pred = true_dict['content'], pred_dict['content']
    amount_of_cooperation_true, amount_of_cooperation_pred = true_dict['amount_of_cooperation'], pred_dict['amount_of_cooperation']
    project_name_true, project_name_pred = true_dict['project_name'], pred_dict['project_name']
    state_true, state_pred = true_dict['state'], pred_dict['state']
    company_identification_Party_A_true, company_identification_Party_A_pred = true_dict['company_identification_Party_A'], pred_dict['company_identification_Party_A']
    company_identification_Party_B_true, company_identification_Party_B_pred = true_dict['company_identification_Party_B'], pred_dict['company_identification_Party_B']
    project_cycle_true, project_cycle_pred = true_dict['project_cycle'], pred_dict['project_cycle']
    project_status_true, project_status_pred = true_dict['project_status'], pred_dict['project_status']

    TP, FP = 0, 0
    # compute TP + FN
    TP_FN = len(amount_of_cooperation_true) + len(project_name_true) + len(state_true) + len(
        company_identification_Party_A_true
    ) + len(company_identification_Party_B_true) + len(project_cycle_true) + len(
        project_status_true
    )

    for aof_pred in amount_of_cooperation_pred:
        if judge_exist(aof_pred, amount_of_cooperation_true):
            TP += 1
        else:
            FP += 1

    for pn_pred in project_name_pred:
        if judge_exist(pn_pred, project_name_true):
            TP += 1
        else:
            FP += 1

    for s_pred in state_pred:
        if judge_exist(s_pred, state_true):
            TP += 1
        else:
            FP += 1

    for ciPA_pred in company_identification_Party_A_pred:
        if judge_exist(ciPA_pred, company_identification_Party_A_true):
            TP += 1
        else:
            FP += 1

    for ciPB_pred in company_identification_Party_B_pred:
        if judge_exist(ciPB_pred, company_identification_Party_B_true):
            TP += 1
        else:
            FP += 1

    for pc_pred in project_cycle_pred:
        if judge_exist(pc_pred, project_cycle_true):
            TP += 1
        else:
            FP += 1

    for ps_pred in project_status_pred:
        if judge_exist(ps_pred, project_status_true):
            TP += 1
        else:
            FP += 1

    return TP, TP_FN - TP, FP


def judge_exist(pred, true_list):
    for true in true_list:
        if pred == true:
            return True

    return False