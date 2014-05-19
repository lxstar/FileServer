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
    path_list = path.split('/')
    if len(path_list) == 4:
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

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            path = form.cleaned_data['path']
            model_save(model, path, request)
            run_plugins(None, None)

            return HttpResponse('success')
        else:
            return HttpResponse('form is not valid<br>' + str(form.errors))
    else:
        return HttpResponse("<form method='post' enctype='multipart/form-data'>\
                                path:<input name='path' type='text'>\
                                md5:<input name='filemd5' type='text'>\
                                params:<input name='params' type='text'>\
                                lang: <input name='lang' type='text'>\
                                <input name='file' type='file'>\
                                <input type='submit'>\
                            </form>")


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
