#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    upload_plugin_template.py
#  Author  :    liuxing2@
#  Project :    fileserver.plugins
#  Date    :    2014-05-28 14:07
#  Descrip :    upload plugin template
# -----------------------------------------------------
from fileserver import conf

import redis
import logging
logger = logging.getLogger('plugins')

"""
upload plugin template

1. class name must be 'Plugin'
2. function is_run and run must
"""


class Plugin(object):

    __name = "upload plugin template"
    __version = "0.1"

    def __init__(self, dev_info, file_info, params):
        self.dev_info = dev_info
        self.file_info = file_info
        self.params = params

    def is_run(self):

        if self.dev_info.get('devhash') == 'AAAA-BBBB-CCCC-SDDD':
            return True
        else:
            return False

    def run(self):

        self.push_redis('fileserver_test', self.file_info.get('filepath'))
        return True

    def push_redis(self, queue_name, queue_value):

        logger.debug(self.params)
        r = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)
        r.lpush(queue_name, queue_value)

        """
        you can get data in other server use:
            r.rpop('.......')
        """