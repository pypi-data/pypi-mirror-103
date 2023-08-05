#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : digital_recognition_app
# @Author   : LiuYan
# @Time     : 2021/4/20 21:00

from base.app.base_app import *
from sequence.model.model_pyltp import LTP
from sequence.regular.regular_digital_recognition import RDR

seq_digital_recognition = Blueprint('/sequence/digital_recognition', __name__)

# model_path = '/data/zutnlp/model/pyltp/ltp_data_v3.4.0'
model_path = '/home/zzsn/liuyan/model/ltp/ltp_data_v3.4.0'
ltp = LTP(model_path=model_path)
rdr = RDR()


@seq_digital_recognition.route('/test', methods=('GET', 'POST'))
def test():
    app.logger.info('test -> sequence -> digital_recognition success!')
    # logger.info('test -> sequence -> digital_recognition success!')
    return 'test -> sequence -> digital_recognition success!'


@seq_digital_recognition.route('/dr/', methods=['POST'])
def digital_recognition():
    data = request.get_json()
    sentence = data['title'] + data['article']
    word_list, tag_list = ltp.pos(sentence=sentence)
    number_list, money_list = rdr.digital_sorting(word_list=word_list, tag_list=tag_list)
    print('\n数字个数为: {} \n分别是: {}'.format(len(number_list), ' '.join(number_list)))
    print('\n金额个数为: {} \n分别是: {}'.format(len(money_list), ' '.join(money_list)))
    result_dict = {
        # 'title': data['title'],
        # 'article': data['article'],
        'number_sum': len(number_list),
        'number_list': number_list,
        'money_sum': len(money_list),
        'money_list': money_list
    }
    app.logger.info(result_dict)

    return json.dumps(result_dict, ensure_ascii=False)


@seq_digital_recognition.route('/release/', methods=('GET', 'POST'))
def release():
    ltp.release()
    app.logger.info('Success release model!')
    return 'Success release model!'
