#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : test
# @Author   : LiuYan
# @Time     : 2021/4/22 11:26

from base.app.base_app import *

test_1 = Blueprint('test_1', __name__)


@test_1.route('/test', methods=['GET'])
def test():
    # Default route
    app.logger.debug('this is a test -> success DEBUG message')         # no

    app.logger.info('this is a test -> success INFO message')           # yes
    app.logger.warning('this is a test -> success WARNING message')     # yes
    app.logger.error('this is a test -> success ERROR message')         # yes
    app.logger.critical('this is a test -> success CRITICAL message')   # yes
    logger.info('test -> success!')
    return 'test -> success!'
