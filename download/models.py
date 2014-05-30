#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    models.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download object model
# -----------------------------------------------------

from django.db import models

class DownloadFileModel(models.Model):
    """
    use:
        save data to database from DownloadFileForm
    """
    filetime = models.DateTimeField(auto_now_add=True)
    filepath = models.CharField(max_length=500)
    clientip = models.IPAddressField()