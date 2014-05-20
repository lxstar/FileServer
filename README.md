FileServer
==========

upload and download file by django.


curl test:
    curl -X POST -F file=@filepath -F path=dstpath -F md5=filemd5 -F lang=en -F params=dsadsadsadsdsadsa



curl -X POST -F file=@/tmp/uploadfile.txt -F filemd5=85B0AE3A8A708B927BF1A30DFF3C6540 -F path=d2FmLzUuMC8xOTIuMTY5LjEuMS1hYWFhLWJiYmItY2NjYy1zZGRkLzExMjNfYXBwX3Nkc2QudGFyLmd6 127.0.0.1:9999/upload/


