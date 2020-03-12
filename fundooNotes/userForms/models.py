from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    takeNote = models.TextField()
    archive = models.BooleanField(default=False)
    