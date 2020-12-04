from django.db import models
from datetime import datetime 
# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=200)
    email =  models.CharField(max_length=200)
    password =  models.CharField(max_length=200)
    date_joined = models.DateTimeField(blank=True)