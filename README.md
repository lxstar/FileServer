FileServer
==========

upload and download file by django.


curl test:
    curl -X POST -F file=@filepath -F path=dstpath -F md5=filemd5 -F lang=en -F params=dsadsadsadsdsadsa



curl -X POST -F file=@/tmp/uploadfile.zip -F filemd5=4B01524E288A37D59758FA9D3EA15F00 -F path=d2FmLzUuMC8xOTIuMTY5LjEuMS1hYWFhLWJiYmItY2NjYy1zZGRkLzExMjNfYXBwX3Nkc2QudGFyLmd6 127.0.0.1:8000/upload/

