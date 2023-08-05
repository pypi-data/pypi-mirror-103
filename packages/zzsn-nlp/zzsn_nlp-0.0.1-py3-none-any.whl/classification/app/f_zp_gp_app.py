#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : f_zp_gp_app
# @Author   : LiuYan
# @Time     : 2021/4/20 20:51

from base.app.base_app import *
from classification.runner.runner_fast_text import FastTextRunner

classification_f_zp_gp = Blueprint('/classification/f_zp_gp', __name__)

ft_config_path = '../classification/config/fast_text_config.yml'
runner = FastTextRunner(config_path=ft_config_path)


@classification_f_zp_gp.route('/test', methods=('GET', 'POST'))
def test():
    logger.info('test -> classify -> f_zp_gp success!')
    return 'test -> classify -> f_zp_gp success!'


@classification_f_zp_gp.route('/classify/', methods=['POST'])
def classify():
    """
    -> data:
    :return:
    """
    data = request.get_json()
    id = data['id']
    title = data['title']
    content = data['content']
    result_dict = runner.pred(
        id=id,
        title=title,
        content=content,
    )
    # logger.info(result_dict)
    app.logger.info(result_dict)

    return json.dumps(result_dict, ensure_ascii=False)
