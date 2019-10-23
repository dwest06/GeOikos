from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICES = [
        ('AC', 'Activo'),
        ('AS', 'Aspirante Estrella'),
        ('IN', 'Inactivo'),
        ('EX', 'Ex-miembro')
    ]
    USERNAME_FIELD = 'email'
    id_number = models.IntegerField(unique=True,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    usb_id = models.IntegerField(null=True)
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=100, verbose_name='Nombre de Usuario')
    balance = models.IntegerField(null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,null=True)
    REQUIRED_FIELDS = ['username'] 
