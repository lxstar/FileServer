FileServer
==========

upload and download file by django.







curl test:
    curl -X POST -F file=@filepath -F path=dstpath -F md5=filemd5 -F lang=en -F params=dsadsadsadsdsadsa



curl -X POST -F file=@/home/lxstar/tmp/uploadfile.zip -F filemd5=7cdbfa42e65a0cb19ce11836526ecf73 -F path=d2FmLzEuMi4zNC8xOTIuMTYuMS4yMjItYWFhYS1iYmJiLWRkZGQtc2RzYS90ZXN0X3dhZmxvZ19zc3NzLnRhci5nego= 127.0.0.1:8000/upload/



curl -X POST -F path=d2FmLzEuMi4zNC8xOTIuMTYuMS4yMjItYWFhYS1iYmJiLWRkZGQtc2RzYS90ZXN0X3dhZmxvZ19zc3NzLnRhci5nego= filemd5=7cdbfa42e65a0cb19ce11836526ecf73 127.0.0.1:8000/download/