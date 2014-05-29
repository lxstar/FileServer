#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    forms.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-28 14:07
#  Descrip :    
# -----------------------------------------------------

from django import forms
from download.models import DownloadFileModel

class DownloadFileForm(forms.ModelForm):
    filemd5 = forms.CharField(required=False)
    path = forms.CharField()
    lang = forms.CharField(required=False)
    params = forms.CharField(required=False)

    class Meta:
    	model = DownloadFileModel
    	fields = []	