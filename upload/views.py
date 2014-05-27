#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-19 13:35
#  Descrip :    
# -----------------------------------------------------

from django.http import HttpResponse
from upload.forms import UploadFileForm
from upload.models import UploadFileModel
from hashlib import md5
from fileserver import conf
import base64
import json
from fileserver.nlogging import Logger
import logging

logger = logging.getLogger('upload')

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
def get_file_md5(fp):
    """
    use: 
        get file md5 
    params:
        fp: file object, such as fp = open('...', '...')
    return:
        file md5 upper
    """
    md5_obj = md5()
    md5_obj.update(fp.read())
    return md5_obj.hexdigest().upper()
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
def get_decode_base64_str(base64_str):
    """
    use: 
        decode base64 string
    params: 
        base64_str: base64 string
    return:
        None: base64 string error
        string: decode string
    """
    if base64_str:
        return base64.decodestring(base64_str)
    else:
        return None

def get_file_type(filename):
    filename_list = filename.split('_')
    if len(filename_list) > 2:
        return filename_list[1]
    else:
        return conf.DEFAULT_FILE_TYPE

def get_dev_file_info():
    return {}, {}

def check_params(model, path, request):
    result_code = ''
    path_list = get_decode_base64_str(path).split('/')
    file_md5 = get_file_md5(model.file)
    logger.debug(file_md5)

    if not check_path(path_list):
        result_code = '1003' # path error
    elif not check_md5(model.filemd5, file_md5):
        result_code = '1004' # file md5 different
    elif not check_file_size(model.file.size):
        result_code = '1001' # file size more than conf.MAX_FILE_SIZE
    elif not check_file_ext(model.file.name):
        result_code = '1007'
    else:
        model.devtype = path_list[0]
        model.devhash = path_list[2][path_list[2].index('-') + 1:].upper()
        model.deversion = path_list[1]
        model.devip = path_list[2].split('-')[0]
        model.filename = model.file.name
        model.filemd5 = file_md5
        model.filetype = get_file_type(model.file.name)
        model.clientip = get_client_ip(request)
        model.file.field.upload_to = "/".join((model.filetype, conf.DEFAULT_FILE_PATH))

        result_code = '1000'
    return result_code, model

def check_file_size(size):
    if size > conf.MAX_FILE_SIZE:
        return False
    else:
        return True

def check_file_ext(filename):
    ext = filename.split('.')[-1]
    if ext in conf.ALLOW_FILE_EXTS:
        return True
    else:
        return False

def check_path(path_list):
    if len(path_list) == 4: 
        return True
    else:
        return False

def check_md5(md5_1, md5_2):
    """
    use: 
        check the two md5 values are same or not
    params:
        md5_1, md5_2: the two md5 values
    return:
        True: same
        False: different
    """

    if md5_1 and md5_2:
        if not cmp(md5_1, md5_2):
            return True
        else:
            return False
    else:
         return False

def index(request):
    """
    use: return index upload view
    params: 
        request: the request from client
    return:
        HttpResponse: the result for upload file (json)
    """
    error_lang = conf.DEFAULT_ERROR_LANG

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            path = form.cleaned_data['path']
            error_lang = get_error_lang(form)

            result_code, model= check_params(model, path, request)
            if result_code == '1000':
                model.save()
                dev_info, file_info = get_dev_file_info()
                plugins_run(dev_info, file_info)
                logger.info('upload file success')
            else:
                return HttpResponse(json.dumps(get_error_info(error_lang, result_code)))

            return HttpResponse(json.dumps(get_error_info(error_lang, '1000')))
        else:
            return HttpResponse('form is not valid<br>' + str(form.errors))
    else:
        logger.debug('test log.')
        return HttpResponse(json.dumps(get_error_info(error_lang, '1006')))

def plugins_run(dev_info, file_info):
    plugin = None
    plugin_model = None
    for plugin_name in conf.INSTALL_PLUGINS:
        try:
            plugin_model = __import__("".join(('plugins.', plugin_name)), fromlist=[plugin_name])
            plugin = plugin_model.Plugin({}, {})
            if plugin.is_run():
                plugin.run()
        except Exception,e:
            print e
