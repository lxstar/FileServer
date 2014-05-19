#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    plugin_test.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-19 13:35
#  Descrip :    
# -----------------------------------------------------


class Plugin(object):

    __name = "test plugin"
    __version = "0.0.1"

    def __init__(self, dev_info, file_info):
        self.dev_info = dev_info
        self.file_info = file_info

    def is_run(self):
        print "waf plugin isrun"
        return True

    def run(self):
        print "waf plugin run"
        return True
