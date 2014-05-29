from django.db import models

class DownloadFileModel(models.Model):

	filetime = models.DateTimeField(auto_now_add=True)
	filepath = models.IntegerField()
	clientip = models.IPAddressField()