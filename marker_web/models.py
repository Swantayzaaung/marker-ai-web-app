from django.db import models

# Create your models here.
class DownloadedPaper(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='downloads/')
