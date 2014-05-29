from django.db import models
from fileserver import conf

class UploadFileModel(models.Model):

    devtype = models.CharField(max_length=20)
    devhash = models.CharField(max_length=20)
    deversion = models.CharField(max_length=10)
    devip = models.IPAddressField()
    file = models.FileField(upload_to=conf.DEFAULT_FILE_PATH)
    filename = models.CharField(max_length=50)
    filetime = models.DateTimeField(auto_now_add=True)
    filemd5 = models.CharField(max_length=32)
    filetype = models.CharField(max_length=20)
    path = models.CharField(max_length=500)
    clientip = models.IPAddressField()