#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    forms.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-16 14:07
#  Descrip :    
# -----------------------------------------------------

from django import forms
from upload.models import UploadFileModel

class UploadFileForm(forms.ModelForm):
    path = forms.CharField()
    filemd5 = forms.CharField()
    lang = forms.CharField(required=False)
    params = forms.CharField(required=False)

    class Meta:
        model = UploadFileModel
        fields = ['file']

