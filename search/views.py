#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.search
#  Date    :    2014-05-28 14:07
#  Descrip :    fileserver.views
# -----------------------------------------------------

from django.http import HttpResponse
from search.forms import FindFileForm
from fileserver import conf, settings
from search.forms import FindFileForm
from upload.models import UploadFileModel

import logging
import json
import os

# logger named 'search'
# define in logging.cfg's [logger_search]
logger = logging.getLogger('search')

def get_error_lang(form):
    """
    use: 
        get language for error's messages
        define in conf.ERRORS's key
    params: 
        form: upload file form from brower
    return:
        user lang: if the choice lang we have
        default lang: we have not this language
                      define at conf.DEFAULT_ERROR_LANG
    """
    if form.cleaned_data['lang'] in conf.ERRORS:
        return form.cleaned_data['lang']
    else:
        return conf.DEFAULT_ERROR_LANG

def get_error_info(lang, result_code):
    """
    use: 
        get error msgs by lang and result code(conf.ERRORS)
    params: 
        lang: error language
        result_code: error code
    return:
        error_info: the error info
    """
    if lang not in conf.ERRORS:
        lang = conf.DEFAULT
    errors = conf.ERRORS[lang]
    error_info = {
        'result': result_code,
        'msgs': errors[result_code],
    }
    return error_info

def get_file_md5(dstpath, filemd5=None):
    """
    use:
        get file md5 from database with dstpath or filemd5
        also make sure the file is exist
        if dstpath and filemd both have:
            filemd5 worked
    params:
        dstpath: the path from client path params
                 not filepath in fileserver nfs !!!
        filemd5: file's md5 from client
    return:
        db_file_md5: can find in database
        None: can not find in database
    """
    upload_obj = None

    if filemd5:
        upload_obj = UploadFileModel.objects.filter(filemd5=filemd5).only('id', 'filemd5', 'file').order_by('-id')
    else:
        upload_obj = UploadFileModel.objects.filter(path=dstpath).only('id', 'file', 'filemd5').order_by('-id')
    
    if upload_obj:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(upload_obj[0].file))):
            return upload_obj[0].filemd5 
    else:
        return ''

def find_file(request):
    """
    use:
        fild file with md5 or path(not real path)
    params:
        request: views.request
    return:
        file streaming: find file right
        error_info: not find file
                    {
                        'result_code': (string),
                        'msgs': (string),
                        'filemd5': (file'md5 or ''),
                    }
    """
    error_lang = conf.DEFAULT_ERROR_LANG
    result_code = ''
    db_filemd5 = ''

    form = FindFileForm(request.REQUEST)
    if form.is_valid():
        error_lang = get_error_lang(form)

        dstpath = form.cleaned_data['path']
        filemd5 = form.cleaned_data['filemd5'].upper()
        db_filemd5 = get_file_md5(dstpath, filemd5)
        if db_filemd5:
            result_code = '1000'
        else:
            result_code = '1002'
    else:
        # '1008': 'upload form insufficient parameters'
        result_code = '1008'  

    error_info = get_error_info(error_lang, result_code)
    error_info['filemd5'] = db_filemd5
    return HttpResponse(json.dumps(error_info)) 