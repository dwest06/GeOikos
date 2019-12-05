from django.contrib import admin
from .models import (
    Category ,
    Equipment ,
    Attribute ,
    AttributeEquipmet ,
    Choices ,
    Group ,
    Request ,
    RequestCategory ,
    Loan ,
    Repair ,
    EquipmentDebt ,
    Transaction ,
    Quarterly
)

admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Attribute)
admin.site.register(AttributeEquipmet)
admin.site.register(Choices)
admin.site.register(Group)
admin.site.register(Request)
admin.site.register(RequestCategory)
admin.site.register(Loan)
admin.site.register(Repair)
admin.site.register(EquipmentDebt)
admin.site.register(Transaction)
admin.site.register(Quarterly)