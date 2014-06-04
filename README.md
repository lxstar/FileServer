# FileServer
---

##### 概述
* 使用Django框架 记录存储使用MySQL
* 使用HTTP协议上传，利于横向拓展
* 使用logging模块，利于记录日志
* 实现了插件模块，使上传和下载可以自定义
* 不适合：大文件传输，很高稳定性的传输等

-------

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
            
            curl -X POST -F file=@/tmp/192.168.1.1_waflog_0530.zip -F path=V0FGLzUuMC8xOTIuMTY4LjU1LjItQUFBQS1CQkJCLUNDQ0MtRERERC8xOTIuMTY4LjEuMV93YWZsb2dfMDUzMC56aXAK -F filemd5=189e725f4587b679740f0f7783745056 -F lang=en -F params=upload_log
            
    
------

#####下载模块

* 下载模块通过客户端传来的参数，在数据库中找到真实的路径返回文件流或错误码给客户端

* 参数说明
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
            2. 
