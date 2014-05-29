#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-28 13:35
#  Descrip :    
# -----------------------------------------------------

from django.http import HttpResponse
from download.forms import DownloadFileForm
from download.models import DownloadFileModel
from upload.models import UploadFileModel
from fileserver import conf

import traceback
import json

import logging

logger = logging.getLogger('download')


def get_client_ip(request):
    """
    use: 
        get client ip from request
    params:
        request: the request from view
    return:
        client ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
        'msgs': errors[result_code]    
    }
    return error_info

def get_file_path(dstpath):
    pass

def index(request):
    """
    use:
        return index download view
    params:
        request: the request from client
    return:
        HttpResponse: the file download 
    """
    error_lang = conf.DEFAULT_ERROR_LANG
    result_code = ''

    if request.method == 'POST':
        form = DownloadFileForm(request.POST)

        if form.is_valid():
            error_lang = get_error_lang(form)
            model = form.save(commit=False)
            dstpath = form.cleaned_data['path']
            params = form.cleaned_data['params']
            filepath = plugins_run(dstpath, params)
            logger.debug('download view run_plugin function')

            if not filepath:
                filepath = get_file_path(dstpath)
            model.clientip = get_client_ip(request)
            model.filepath = filepath
            model.save()

            result_code = '1000'
        else:
            # '1008': 'upload form insufficient parameters'
            result_code = '1008'
    else:
        # '1006': 'request method error, must be POST'
        result_code = '1006'
    return  HttpResponse(json.dumps(get_error_info(error_lang, result_code)))

def plugins_run(dstpath, params):
    """
    use:
        run download plugins in conf.INSTALL_DOWNLOAD_PLUGINS
    params:
        dstpath: path from form(base64)
    return:
        None
    """
    plugin = None
    plugin_model = None

    for plugin_name in conf.INSTALL_DOWNLOAD_PLUGINS:
        try:
            plugin_model = __import__("".join(('plugins.download.', plugin_name)), fromlist=[plugin_name])
            plugin = plugin_model.Plugin(dstpath, params)
            if plugin.is_run():
                dstpath = plugin.run()
                return dstpath
        except:
            logger.error('fileserver upload plugin run error, plugin name=%s'%plugin_name)
            logger.error(traceback.format_exc())
    return None