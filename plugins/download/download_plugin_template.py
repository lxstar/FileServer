#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    download_plugin_template.py
#  Author  :    liuxing2@
#  Project :    fileserver.plugins
#  Date    :    2014-05-28 14:07
#  Descrip :    download plugin template
# -----------------------------------------------------
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
	
        if self.params == 'nsfocus':
            return True
        else:
            return False

    def run(self):

        return '/tmp/testfile.tar.gz'
