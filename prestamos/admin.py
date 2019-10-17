from django.contrib import admin
from .models import (
    Category ,
    Equipment ,
    Atribute ,
    Options ,
    Group ,
    Request ,
    RequestedItem ,
    EquipmentLoan ,
    Repair ,
    EquipmentDebt ,
    Balance ,
    Transaction 
)

admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Atribute)
admin.site.register(Options)
admin.site.register(Group)
admin.site.register(Request)
admin.site.register(RequestedItem)
admin.site.register(EquipmentLoan)
admin.site.register(Repair)
admin.site.register(EquipmentDebt)
admin.site.register(Balance)
admin.site.register(Transaction)