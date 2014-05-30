#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    forms.py
#  Author  :    liuxing2@
#  Project :    fileserver.search
#  Date    :    2014-05-28 14:07
#  Descrip :    handle form form client
# -----------------------------------------------------

from django import forms

class FindFileForm(forms.Form):
    """
    use:
        model for search find file
    """
    filemd5 = forms.CharField(required=False)
    path = forms.CharField()
    lang = forms.CharField(required=False)
    params = forms.CharField(required=False)