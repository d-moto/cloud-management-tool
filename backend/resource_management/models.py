from django.db import models

# Create your models here.

class VirtualMachine(models.Model):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)  # 'AWS' or 'Azure'
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)