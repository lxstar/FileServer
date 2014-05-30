#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    log.py
#  Author  :    liuxing2@
#  Project :    fileserver.fileserver
#  Date    :    2014-05-28 14:07
#  Descrip :    log model for fileserver
# -----------------------------------------------------


"""
File used for loading project's logs.

"""


import os
import time
import threading
import logging
from logging.config import fileConfig

from django.conf import settings

class LogConfigWatcher(threading.Thread):
    """portal project's logging file handlers.
    This extends from threading.Thread class.

    """

    NAME = 'log.watcher'

    def __init__(self, cfg_file):
        """class LogConfigWatcher's __init__ method.

        Args:
            cfg_file: The logging configure file path.
        """
        threading.Thread.__init__(self, name=self.NAME)
        self.setDaemon(True)
        self.cfg_file = cfg_file
        
    def run(self):
        """LogConfigWatcher thread's entrance method.

        """
        last_mtime = 0
        while True:
            try:
                mtime = os.stat(self.cfg_file).st_mtime
                if mtime > last_mtime:
                    fileConfig(self.cfg_file)
                    last_mtime = mtime
                    logger = logging.getLogger('root')
                    logger.info("load logging configuration from %s",
                            self.cfg_file)
            except Exception, err_msg:
                logging.warn("fail to load logging config from %s, %s",
                        self.cfg_file, err_msg)
            time.sleep(5)


def init_log(cfg_file):
    """Using LogConfigWatcher to init logging's configures.

    Args:
        cfg_file: The logging configure file path.

    If the logging configure file path does not exists, all logs will be
    redirected into console.

    """
    for thrd in threading.enumerate():
        if thrd.getName() == LogConfigWatcher.NAME:
            return
    print cfg_file
    if os.path.isfile(cfg_file):
        LogConfigWatcher(cfg_file).start()
    else:
        logging.basicConfig(
                level=logging.DEBUG if settings.DEBUG else logging.WARN,
                format='%(asctime)s %(levelname)s %(message)s')
        logging.info("ouput logging to console")
