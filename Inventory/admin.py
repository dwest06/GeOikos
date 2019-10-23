from django.contrib import admin
from .models import (
    Category ,
    Equipment ,
    Atribute ,
    Atribute_Equipment ,
    Choices ,
    Group ,
    Request ,
    Request_Category ,
    Loan ,
    Repair ,
    EquipmentDebt ,
    Transaction 
)

admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Atribute)
admin.site.register(Atribute_Equipment)
admin.site.register(Choices)
admin.site.register(Group)
admin.site.register(Request)
admin.site.register(Request_Category)
admin.site.register(Loan)
admin.site.register(Repair)
admin.site.register(EquipmentDebt)
admin.site.register(Transaction)