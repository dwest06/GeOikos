from django.urls import path
from . import views

app_name = "Inventory"

urlpatterns = [
    path('', views.homeInventarioView, name='home_inventory'),
    path('create-category', views.createCategory, name='create_category'),
    path('create-equipment', views.EquipCatSelection , name="create_equipment"),
    path('create-equipment-value/<int:cat>', views.createEquipment , name="create_equipment_value"),
    path('select-cat', views.CatQueryView , name="select-cat"),
    path('select-atts/<int:category>', views.AttsQueryView, name="select-atts"),
    path('create-group', views.createGroup , name="create_group"),
    path('manage-users', views.manage_users, name="manage_users"),
    path('create-loan', views.LoanCreation , name="create_loan"),
    path('show-equipment/<int:category>',views.ShowEquipment, name="show_equipment"),
    path('load-transaction', views.loadTransaction, name="load_transaction"),
    path('create-request',views.createRequest, name="create_request")
]
