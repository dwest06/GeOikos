from django.urls import path
from .views import login_user, logout_user, create_user, modify_user, delete_user, change_password_user
from . import views

app_name = "Users"

urlpatterns = [
    path('create-user', create_user, name="create_user"),
    path('modify-user/<int:pk>', modify_user, name="modify_user"),
    path('delete-user', delete_user, name="delete_user"),
    path('login', login_user, name="login"),
    path('logout', logout_user, name="logout"),
]
