from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Users(AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=255)
    # password=models.BinaryField(max_length=255)
    date_joined = models.DateTimeField(blank=True)
    products_recommend = models.TextField(max_length=255)

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name
