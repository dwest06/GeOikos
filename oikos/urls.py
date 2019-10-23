from django.urls import path
from .views import home

app_name = "oikos"

urlpatterns = [
    path('', home, name="home")
]
