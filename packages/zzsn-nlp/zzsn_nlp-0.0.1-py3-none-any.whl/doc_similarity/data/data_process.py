#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : data_process
# @Author   : LiuYan
# @Time     : 2021/4/9 15:01

import xlrd
import xlsxwriter


def xlsx2list(xlsx_path: str) -> list:
    wb = xlrd.open_workbook(xlsx_path)
    sh = wb.sheet_by_name('Sheet1')
    total_list = list()
    for i in range(sh.nrows):
        if i < 3:
            continue
        row = sh.row_values(i)
        total_list.append({
            'id': int(row[0]),
            'title': row[1].replace('\n', '').replace('\r', '').replace('\t', ''),
            'content': row[2].replace('\n', '').replace('\r', '').replace('\t', '')
        })
        # row = sh.row_values(i)
        # total_list.append({
        #     'id': i,
        #     'title': row[0].replace('\n', '').replace('\r', '').replace('\t', ''),
        #     'content': row[1].replace('\n', '').replace('\r', '').replace('\t', '')
        # })
    return total_list


def list2xlsx(xlsx_path=None, result_lists=None):
    workbook = xlsxwriter.Workbook(xlsx_path)
    worksheet = workbook.add_worksheet('result')
    worksheet.write_row(
        0, 0, [
            'content_id_x', 'content_id_y',
            'cos_sim', 'jac_sim', 'lev_sim',
            'min_hash', 'old_sim_hash', 'new_sim_hash',
            'ctt_sim',
            'cos_sim', 'jac_sim', 'lev_sim',
            'min_hash', 'old_sim_hash', 'new_sim_hash',
            'ctt_sim',
        ]
    )
    for index, result in enumerate(result_lists):
        worksheet.write_row(
            index + 1, 0, [
                result[0],
                result[1],
                result[2]['result_cos_sim'],
                result[2]['result_jac_sim'],
                result[2]['result_lev_sim'],
                result[2]['result_min_hash_sim'],
                result[2]['result_old_sim_hash_sim'],
                result[2]['result_new_sim_hash_sim'],
                result[2]['result_sim_tx'],
                result[3]['result_cos_sim'],
                result[3]['result_jac_sim'],
                result[3]['result_lev_sim'],
                result[3]['result_min_hash_sim'],
                result[3]['result_old_sim_hash_sim'],
                result[3]['result_new_sim_hash_sim'],
                result[3]['result_sim_tx'],
            ]
        )

    workbook.close()


if __name__ == '__main__':
    xlsx_path = '../data/total_datasets.xlsx'
    total_list = xlsx2list(xlsx_path=xlsx_path)
    pass
