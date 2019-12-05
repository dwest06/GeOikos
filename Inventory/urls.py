from django.urls import path
from . import views

app_name = "Inventory"

urlpatterns = [
    path('', views.home_inventario_view, name='home_inventory'),
    path('create-category', views.create_category, name='create_category'),
    path('create-equipment', views.equip_cat_selection , name="create_equipment"),
    path('create-equipment-value/<int:cat>', views.create_equipment , name="create_equipment_value"),
    path('modify-equipment-value/<int:eq_id>', views.modify_equipment , name="modify_equipment_value"),
    path('select-cat', views.cat_query_view , name="select-cat"),
    path('select-atts/<int:category>', views.atts_query_view, name="select-atts"),
    path('create-group', views.create_group , name="create_group"),
    path('manage-users', views.manage_users, name="manage_users"),
    path('create-loan', views.loan_creation , name="create_loan"),
    path('show-equipment/<int:category>',views.show_equipment, name="show_equipment"),
    path('load-transaction', views.load_transaction, name="load_transaction"),
    path('create-request',views.create_request, name="create_request"),
    path('loan-devolution/<int:loan>' ,views.loan_devolution, name="loan_devolution"),
    path('show-request/<int:request_id>',views.show_request,name="show_request"),
    # VISTAS DE TESORERO
    path('tesorero', views.home_tesorero_view, name="tesorero"),
    # VISTAS DE CUARTO DE EQUIPO
    path('cuarto-equipo', views.home_cuarto_equipo_view, name="cuarto_equipo"),
]
