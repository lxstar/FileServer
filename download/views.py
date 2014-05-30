#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download app's views
# -----------------------------------------------------

from django.http import HttpResponse
from download.forms import DownloadFileForm
from download.models import DownloadFileModel
from upload.models import UploadFileModel
from fileserver import conf, settings

import traceback
import json
import os
import logging

# logger named 'download'
# define in logging.cfg's [logger_download]
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

def get_file_path(dstpath, filemd5=None):
    """
    use:
        get file real path from database with dstpath or filemd5
        if dstpath and filemd both have:
            filemd5 worked
    params:
        dstpath: the path from client path params
                 not filepath in fileserver nfs !!!
        filemd5: file's md5 from client
    return:
        realpath: can find in database
        None: can not find in database
    """
    upload_obj = None

    if filemd5:
        upload_obj = UploadFileModel.objects.filter(filemd5=filemd5).only('id', 'filemd5', 'file').order_by('-id')
    else:
        upload_obj = UploadFileModel.objects.filter(path=dstpath).only('id', 'file').order_by('-id')
    if upload_obj:
        return os.path.join(settings.MEDIA_ROOT, str(upload_obj[0].file))
    else:
        return None

def get_file_response(filepath):
    """
    use:
        get HttpResponse object for download file streaming
    params:
        filepath: file real path on fileserver
    return:
        FileHttpResponse: realpath right and file is exist
        None: realpath failed or file isn't exist
    """
    if filepath and os.path.isfile(str(filepath)):
        try:
            fp = open(str(filepath), 'rb')
            data = fp.read()
            fp.close()
        except:
            logger.error('download read file error.')
            logger.error(traceback.format_exc())

        filename = filepath.split('/')[-1]

        response = HttpResponse(data)
        response['mimetype'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s'%filename
        return response
    else:
        return None

def check_file_path(filepath):
    """
    use:
        check file path is or isn't in conf.ALLOW_SAVE_PATHS
    params:
        filepath: file real path
    return:
        True or False
    """
    if filepath:
        for start in conf.ALLOW_SAVE_PATHS:
            if filepath.startswith(start):
                return True
    return False

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
    file_response = None

    form = DownloadFileForm(request.REQUEST)

    if form.is_valid():
        error_lang = get_error_lang(form)
        
        dstpath = form.cleaned_data['path']
        params = form.cleaned_data['params']
        filemd5 = form.cleaned_data['filemd5'].upper()
        filepath = plugins_run(dstpath, params)

        if not filepath:
            filepath = get_file_path(dstpath, filemd5)
            
        if filepath and os.path.isfile(str(filepath)) \
                    and check_file_path(str(filepath)):
            file_response = get_file_response(filepath)

        if file_response:
            model = form.save(commit=False)
            model.clientip = get_client_ip(request)
            model.filepath = filepath
            model.save()
        else:
            # '1002': 'file is not exist'
            result_code = '1002'                
    else:
        # '1008': 'upload form insufficient parameters'
        result_code = '1008'

    if file_response:
        return file_response
    else:
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