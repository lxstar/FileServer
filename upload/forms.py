#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    forms.py
#  Author  :    liuxing2@
#  Project :    fileserver.upload
#  Date    :    2014-05-16 14:07
#  Descrip :    upload.forms
# -----------------------------------------------------

from django import forms
from upload.models import UploadFileModel

class UploadFileForm(forms.ModelForm):
    lang = forms.CharField(required=False)
    params = forms.CharField(required=False)

    class Meta:

        # modelForm form UploadFielModel
        model = UploadFileModel
        # fields is the field same in model and form
        fields = ['file', 'filemd5', 'path']