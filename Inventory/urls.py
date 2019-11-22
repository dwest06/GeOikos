from django.urls import path
from . import views

app_name = "Inventory"

urlpatterns = [
    path('', views.home_inventario_view, name='home_inventory'),
    path('create-category', views.create_category, name='create_category'),
    path('create-equipment', views.equip_cat_selection , name="create_equipment"),
    path('create-equipment-value/<int:cat>', views.create_equipment , name="create_equipment_value"),
    path('select-cat', views.cat_query_view , name="select-cat"),
    path('select-atts/<int:category>', views.atts_query_view, name="select-atts"),
    path('create-group', views.create_group , name="create_group"),
    path('manage-users', views.manage_users, name="manage_users"),
    path('create-loan', views.loan_creation , name="create_loan"),
    path('show-equipment/<int:category>',views.show_equipment, name="show_equipment"),
    path('load-transaction', views.load_transaction, name="load_transaction"),
    path('create-request',views.create_request, name="create_request")
]
