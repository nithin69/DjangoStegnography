from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Document(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title", null=True, blank=True )
    txtdata = models.TextField(verbose_name="Data to encrypt")
    document = models.FileField(upload_to='normalimg/', verbose_name="Image to encrypt")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, verbose_name="Uploaded By", on_delete=models.CASCADE)