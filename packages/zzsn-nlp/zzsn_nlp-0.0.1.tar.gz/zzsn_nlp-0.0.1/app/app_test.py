#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : app_test
# @Author   : LiuYan
# @Time     : 2021/4/22 9:59

import sys
import logging

sys.path.append('../')
from app.test import test_1
from base.app.base_app import *

HOST = '0.0.0.0'
PORT = 7001
DEBUG = False

app.register_blueprint(test_1, url_prefix='/test_1')


@app.route('/')
def hello_world():
    app.logger.info('Hello World!')
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # gunicorn --workers=2 --bind=0.0.0.0:8000 --log-level=debug gunicorn_log:app

# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     logging.basicConfig(level=gunicorn_logger.level, handlers=gunicorn_logger.handlers)
#     app.logger.handlers = gunicorn_logger.handlers
