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


def get_client_ip(request):
    """
    use: get client ip from request
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
    use: get file md5 
    params:
        fp: file object, such as fp = open('...', '...')
    return:
        file md5 upper
    """
    md5_obj = md5()
    md5_obj.update(fp.read())
    return md5_obj.hexdigest().upper()

def check_md5(md5_1, md5_2):
    """
    use: check the two md5 values are same or not
    params:
        md5_1, md5_2: the two md5 values
    return:
        True: same
        False: different
    """
    if md5_1 and md5_2:
        if cmp(md5_1, md5_2):
            return True
        else:
            return False
    else:
         return False

def model_save(model, path, request):
    """
    use: resolve paths params to model and save to db
    params:
        model: create from form
        path:  form field path
               like 'waf/12/192.168.1.1-AAAA-BBBB-CCCC-DDDD/xxxxx_filetype_xxxx_xxx_x.xx'
        request: the request from view
    return:
        True: path all right
        False: path has error
    """
    path_list = decode_base64(path).split('/')
    if len(path_list) == 4:
        print model.file.size
        model.devtype = path_list[0]
        model.devhash = path_list[2][path_list[2].index('-') + 1:].upper()
        model.deversion = path_list[1]
        model.devip = path_list[2].split('-')[0]
        model.filename = model.file.name
        model.filemd5 = get_file_md5(model.file)
        model.filetype = path_list[3].split('_')[1]
        model.clientip = get_client_ip(request)
        model.save()
        return True
    else:
        return False

def decode_base64(base64_str):
    """
    use: decode base64 string
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

def get_error_lang(form):
    if form.cleaned_data['lang'] in conf.ERRORS:
        return form.cleaned_data['lang']
    else:
        return conf.DEFAULT_ERROR_LANG

def get_error_info(lang, result_code):
    if lang not in conf.ERRORS:
        lang = conf.DEFAULT
    errors = conf.ERRORS[lang]
    error_info = {
        'result': result_code,
        'msgs': errors[result_code]    
    }
    return error_info


def index(request):
    error_lang = conf.DEFAULT_ERROR_LANG

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            path = form.cleaned_data['path']
            model_save(model, path, request)
            error_lang = get_error_lang(form)

            run_plugins(None, None)

            return HttpResponse(json.dumps(get_error_info(error_lang, '1000')))
        else:
            return HttpResponse('form is not valid<br>' + str(form.errors))
    else:
        return HttpResponse(json.dumps(get_error_info(error_lang, '1006')))

def run_plugins(dev_info, file_info):
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
