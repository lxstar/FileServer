#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    conf.py
#  Author  :    liuxing2@
#  Project :    
#  Date    :    2014-05-15 16:53
#  Descrip :    
# -----------------------------------------------------


# uplaod plugins install
INSTALL_UPLOAD_PLUGINS = [
    "upload_plugin_template"
]

# download plugins install
INSTALL_DOWNLOAD_PLUGINS = [
    'download_plugin_template'
]

# errors define
ERRORS = {
    'en': {
        '1000': 'normal',
        '1001': 'file size exceeds limit',
        '1002': 'file is not exist',
        '1003': 'file path error',
        '1004': 'file md5 error',
        '1005': 'language error',
        '1006': 'request method error, must be POST',
        '1007': 'file ext not allow',
        '1008': 'upload form insufficient parameters',
        '1404': 'unknown error',
    },
    'cn': {
        '1000': '正常返回值',
        '1001': '文件大小超过上限',
        '1002': '文件不存在',
        '1003': '文件目标路径错误',
        '1004': '文件MD5值不一致',
        '1005': '返回值语言不存在',
        '1006': '请求类型错误，必须是POST',
        '1007': '文件类型不允许',
        '1008': '上传文件参数不足',
        '1404': '未知错误',
    }
}

# default error language
DEFAULT_ERROR_LANG = 'en'

# max size limit 
MAX_FILE_SIZE = 104857600 # 100MB 

# allow file ext
ALLOW_FILE_EXTS = ['zip', '.log', 'tar.gz'] 

# default filetype
DEFAULT_FILE_TYPE = "other"

# default file save path
DEFAULT_FILE_PATH = "%Y/%m/%d/%H/%M/%S"

# redis conf
REDIS_HOST = '10.7.201.130'
REDIS_PORT = '6379'

# allow save file path
ALLOW_SAVE_PATHS = [
    '/tmp/fileserver/',    
]