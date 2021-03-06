from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICES = [
        ('AC', 'Miembro Activo'),
        ('AS', 'Aspirante Estrella'),
        ('IN', 'Inactivo'),
        ('EX', 'Ex-miembro')
    ]
    USERNAME_FIELD = 'email'
    email = models.EmailField('email-address', unique=True)
    usb_id = models.IntegerField(null=True)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,null=True, default='IN')
    pic = models.ImageField(upload_to = 'img/Users', default = 'img/Users/None/default.png', blank=True)
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.username + ')'