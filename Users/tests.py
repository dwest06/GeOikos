from django.test import TestCase
from .models import User
from django.test import Client
from .views import (
    login_user,
    logout_user,
    create_user,
    modify_user,
    delete_user
)
