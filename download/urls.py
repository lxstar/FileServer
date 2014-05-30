#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    urls.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download app's urls
# -----------------------------------------------------

from django.conf.urls import patterns, include, url

urlpatterns = patterns('download.views',
            (r'^$', 'index'),
)