#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    urls.py
#  Author  :    liuxing2@
#  Project :    fileserver.search
#  Date    :    2014-05-28 14:07
#  Descrip :    fileserver.urls
# -----------------------------------------------------

from django.conf.urls import patterns, include, url

urlpatterns = patterns('search.views',
            (r'^findfile/$', 'find_file'),
)