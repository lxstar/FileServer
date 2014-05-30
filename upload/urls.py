#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.urls
#  Date    :    2014-05-28 14:07
#  Descrip :    upload.urls
# -----------------------------------------------------

from django.conf.urls import patterns, include, url

urlpatterns = patterns('upload.views',
            (r'^$', 'index'),
)
