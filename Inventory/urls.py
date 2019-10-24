from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path('search', views.search , name="search")
]
