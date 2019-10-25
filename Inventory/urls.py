from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homeInventarioView, name='home_inventory'),
    path('create-category', views.createCategory, name='create_category')
]
