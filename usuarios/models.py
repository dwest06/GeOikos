from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=100, verbose_name='Nombre de Usuario')
    REQUIRED_FIELDS = ['username'] 
