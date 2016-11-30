from django.db import models

class GRDS(models.Model):
    governor=models.CharField(max_length=200)
    rds=models.CharField(max_length=55555)
