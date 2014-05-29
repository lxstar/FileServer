#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    plugin_template.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-19 13:35
#  Descrip :    
# ------------------------------------------------------
from fileserver import conf

import logging
logger = logging.getLogger('plugins')

"""
download plugin template

1. class name must be 'Plugin'
2. function is_run and run must
"""


class Plugin(object):

    __name = "download plugin template"
    __version = "0.1"

    def __init__(self, dstpath, params):
        self.dstpath = dstpath
        self.params = params

    def is_run(self):

        logger.debug('download plugin is_run function')
        if True:
            return True
        else:
            return False

    def run(self):
        logger.debug('download plugin run function')
        return 12345677