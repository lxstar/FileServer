# FileServer


##### 概述
* 使用Django框架 记录存储使用MySQL
* 使用HTTP协议上传，利于横向拓展
* 使用logging模块，利于记录日志
* 实现了插件模块，使上传和下载可以自定义
* 不适合：大文件传输，很高稳定性的传输等



#####上传模块
* 使用POST请求，将文件的信息通过HTTP FILE和POST参数传递给FileServer
* FileServer接收到数据之后，会对其进行数据的准确性的校验，从而返回处理的结果
* 数据校验正确后，会将记录写入MySQL中，同时将文件写入到配置的文件目录下

* 参数说明：

        URL：/upload/
        类型： POST
        参数：
            file:       上传的文件流      必须
            filemd5:    上传文件的MD5值   必须
            path:       上传的目标路径    必须
            lang:       返回码信息的语言  非必须
            params:     传递给插件的参数  非必须
        返回值：
            JSON格式的返回信息：
                {
                    result: (返回码),
                    msgs:   (返回信息)
                }
        具体说明：
            1. filemd5 在linux下可以通过md5sum工具获得
            2. path 必须遵循格式：设备类型/设备版本/设备IP-设备HASH值/文件名称
                 文件名称 必须遵循格式：xxxx_文件类型_xxxx_xxxx_.xxx
                         即必须在有两个以上的下划线，第二段中必须是文件类型，否则归为other类型
                 例如：WAF/5.0/192.168.55.2-AAAA-BBBB-CCCC-DDDD/192.168.1.1_waflog_0530.zip
            3. path 必须为base64编码后的参数 linux下可使用 echo path|base64 获取到base64的加密串

        curl实例：
            (path=WAF/5.0/192.168.55.2-AAAA-BBBB-CCCC-DDDD/192.168.1.1_waflog_0530.zip)
            
            curl -X POST -F file=@/tmp/192.168.1.1_waflog_0530.zip -F path=V0FGLzUuMC8xOTIuMTY4LjU1LjItQUFBQS1CQkJCLUNDQ0MtRERERC8xOTIuMTY4LjEuMV93YWZsb2dfMDUzMC56aXAK -F filemd5=189e725f4587b679740f0f7783745056 -F lang=en -F params=upload_log xxx.xxx.xxx.xxx/upload/
            
    


#####下载模块

* 下载模块通过客户端传来的参数，在数据库中找到真实的路径返回文件流或错误码给客户端

* 参数说明:

        URL：/download/
        类型: POST/GET
        参数：
            path：      base64的目标路径，同upload的规范    必须
            filemd5:    文件的md5值                       非必须
            lang:       返回码信息的语言  非必须
            params:     传递给插件的参数  非必须
        返回值：
            正常情况下返回文件流
            错误的情况下返回错误的信息，同上传的JSON信息结构
        具体说明：
            1. 当path和filemd5同时存在时，只使用md5值去寻找文件，path不使用
            2. path同样需要base64编码，格式和upload中的path一致
            3. lang和params与upload中用法一致
            4. 可以使用GET的参数形式访问
            
        curl实例:
            (path=WAF/5.0/192.168.55.2-AAAA-BBBB-CCCC-DDDD/192.168.1.1_waflog_0530.zip)
        
            curl -F path=V0FGLzUuMC8xOTIuMTY4LjU1LjItQUFBQS1CQkJCLUNDQ0MtRERERC8xOTIuMTY4LjEuMV93YWZsb2dfMDUzMC56aXAK -F filemd5=189e725f4587b679740f0f7783745056 -F lang=en -F params=download_log xxx.xxx.xxx.xxx/download/
            

#####查询模块

* 通过文件的目标路径或文件md5确定文件是否存在

* 参数说明
        
        URL: /search/findfile/
        类型: POST/GET
        参数:
            path：      base64的目标路径，同upload的规范    必须
            filemd5:    文件的md5值                       非必须
            lang:       返回码信息的语言  非必须
            params:     传递给插件的参数  非必须
        返回值:
            
            JSON格式的返回信息：
                {
                    result: (返回码),
                    msgs:   (返回信息),
                    filemd5:(文件md5，如果没有找到则为空)
                }
        具体说明:
            1. 当path和filemd5同时存在时，只使用md5值去寻找文件，path不使用
            2. path同样需要base64编码，格式和upload中的path一致
            3. lang和params与upload中用法一致
            4. 可以使用GET的参数形式访问

         curl实例:
            (path=WAF/5.0/192.168.55.2-AAAA-BBBB-CCCC-DDDD/192.168.1.1_waflog_0530.zip)
        
            curl -F path=V0FGLzUuMC8xOTIuMTY4LjU1LjItQUFBQS1CQkJCLUNDQ0MtRERERC8xOTIuMTY4LjEuMV93YWZsb2dfMDUzMC56aXAK -F filemd5=189e725f4587b679740f0f7783745056 -F lang=en -F params=download_log xxx.xxx.xxx.xxx/search/findfile/
       
#####错误码解释
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

#####插件编写
* 在plugins文件夹下有upload、download两个文件夹，分别放着上传和下载使用的插件
* 插件的命名方式:upload_plugin_xxxxx.py 或 download_plugin_xxxx.py分别放在对应的文件夹下面
* 插件需要实现is_run()函数判断此插件需要执行否，判断条件尽量严谨，避免误判断
* 插件需要实现run()函数进行插件的逻辑处理函数
* 上传插件返回无返回值
* 下载插件无返回值时，系统自动根据参数寻找文件，返回路径时，系统根据插件返回的路径直接找文件返回

#####部署说明（runserver形式）

* 需要安装包: Python-2.6/2.7 Django-1.4/1.5 MySQLdb-1.2.2/1.2.3

* 具体配置：
    1. 在settings中配置数据库
    2. MEDIA_ROOT为FileServer文件上传的根目录
    3. 如果需要使用插件，需要在conf.py中添加插件文件名在INSTALL_UPLOAD_PLUGINS或INSTALL_DOWNLOAD_PLUGINS中
    4. 配置允许的文件大小和路径等信息，都在conf.py中

#####FAQ

1. 上传插件怎么不执行？
    * 查看在文件是否放在upload或download文件夹下。
    * 查看插件的文件名称（比如test.py 插件名称为test）是否写入了conf.py的INSTALL_DOWNLOAD_PLUGINS或INSTALL_UPLOAD_PLUGINS中
    * 查看is_run()函数的判断参数是否正确

2. 下载插件怎么不返回文件流?
    * 查看是否把要下载的文件后缀名在ALLOW_FILE_EXTS中写入
    * 查看是否把自定义路径放入ALLOW_SAVE_PATHS中
    * 查看文件的大小是否超过了MAX_FILE_SIZE



----------------------
lxstar01@gmail.com
2014-06-03







