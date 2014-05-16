#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    models.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-15 17:53
#  Descrip :    
# -----------------------------------------------------

from django.db import models

class uploadlist(models.Model):
    devtype = models.CharField(max_length=20)
    devhash = models.CharField(max_length=20)
    deversion = models.CharField(max_length=10)
