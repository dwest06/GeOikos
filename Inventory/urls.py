from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "Inventory"

urlpatterns = [
    path('', views.createCategory, name='create_category'),
    path('create-equipment', views.EquipCatSelection , name="create_equipment"),
    path('create-equipment-value/<int:cat>', views.createEquipment , name="create_equipment_value"),
]
