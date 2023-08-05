#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : doc_sim_app
# @Author   : LiuYan
# @Time     : 2021/4/20 20:50

from base.app.base_app import *
from doc_similarity.data.compare import *

doc_sim = Blueprint('/doc_sim', __name__)


@doc_sim.route('/test', methods=('GET', 'POST'))
def test():
    app.logger.info('test -> doc_sim_app success!')
    # logger.info('test -> doc_sim_app success!')
    return 'test -> doc_sim_app success!'


@doc_sim.route('/similarity/', methods=['POST'])
def similarity():
    """
    -> data:
    :return:
    """
    data = request.get_json()
    article_list = data['article_list']
    title_sim_name = data['title_sim_name']
    content_sim_name = data['content_sim_name']
    result_dict = compare_single(
        article_list=article_list,
        title_sim_name=title_sim_name,
        content_sim_name=content_sim_name
    )
    # logger.info(result_dict)
    app.logger.info(result_dict)

    return json.dumps(result_dict, ensure_ascii=False)


@doc_sim.route('/similarity_list/', methods=['POST'])
def similarity_list():
    """
    -> data:
    :return:
    """
    data = request.get_json()
    article_list = data['article_list']
    title_sim_name = data['title_sim_name']
    content_sim_name = data['content_sim_name']
    result_dict = compare_many(
        article_list=article_list,
        title_sim_name=title_sim_name,
        content_sim_name=content_sim_name
    )
    # logger.info(result_dict)
    app.logger.info(result_dict)

    return json.dumps(result_dict, ensure_ascii=False)
