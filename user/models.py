
from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
