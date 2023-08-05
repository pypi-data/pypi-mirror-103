#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : app_run
# @Author   : LiuYan
# @Time     : 2021/4/20 20:11

import sys
import logging

sys.path.append('../')
from base.app.base_app import *
from classification.app.f_zp_gp_app import classification_f_zp_gp
from doc_event.app.the_belt_and_road_app import doc_event_br
from doc_similarity.app.doc_sim_app import doc_sim
from sequence.app.digital_recognition_app import seq_digital_recognition

HOST = '0.0.0.0'
PORT = 7000
DEBUG = False

# classification
app.register_blueprint(classification_f_zp_gp, url_prefix='/classification/f_zp_gp')
# doc_event
app.register_blueprint(doc_event_br, url_prefix='/doc_event/br')
# doc_sim
app.register_blueprint(doc_sim, url_prefix='/doc_sim')
# sequence
app.register_blueprint(seq_digital_recognition, url_prefix='/sequence/digital_recognition')


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
