#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : the_belt_and_road_app
# @Author   : LiuYan
# @Time     : 2021/4/20 20:49

from base.app.base_app import *

doc_event_br = Blueprint('/doc_event/br', __name__)


@doc_event_br.route('/test', methods=('GET', 'POST'))
def test():
    app.logger.info('test -> doc_event -> the_belt_and_road_app success!')
    logger.info('test -> doc_event -> the_belt_and_road_app success!')
    return 'test -> doc_event -> the_belt_and_road_app success!'
