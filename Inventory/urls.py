from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path('select-cat', views.CatQueryView , name="select-cat"),
    path('select-atts/<int:category>', views.AttsQueryView, name="select-atts")
]
