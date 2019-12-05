from django.db import models
from Users.models import User
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=120, unique=True)
        
    def __str__(self):
        return self.name


class Equipment(models.Model):
    serial = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    entry_date = models.DateField(blank=True, null=True)
    elaboration_date = models.DateField(blank=True, null=True)
    discontinued = models.BooleanField(default=False)
    discontinued_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    group = models.ManyToManyField(Group,blank=True)

    def __str__(self):
        return self.name+ ': equipo de ' + self.category.name

    def discontinuedEq():
        return Equipment.objects.filter(discontinued=True).values('id')

    def notAvEquipment():
        borrowed = Loan.borrowedEq()
        notAv = Equipment.discontinuedEq().union(borrowed)
        notAvEq = [ x['id'] for x in notAv ]
        return notAvEq
    
    def avEquipment():
        notAvEq = Equipment.notAvEquipment()
        avEq = Equipment.objects.exclude(id__in=notAvEq)
        return avEq

class Attribute(models.Model):
    TYPE_CHOICES = [
        ('INT', 'Entero'),
        ('TXT', 'Texto'),
        ('STR', 'String'),
        ('BOO', 'Booleano'),
        ('FLT', 'Decimal'),
        ('DAT', 'Fecha'),
        ('CHO', 'Selección'),
    ]
    name = models.CharField(max_length=50)
    attribute_type = models.CharField(max_length=3,choices=TYPE_CHOICES)
    unit = models.CharField(max_length=20,blank=True,default="")
    nullity = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def isBlank(attribute):
        return Attribute.objects.filter(pk=attribute).nullity
    
# Opciones para un atributo de multiples opciones
class Choices(models.Model):
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
    option_name = models.CharField(max_length=100)

    def __str__(self):
        return self.option_name

class AttributeEquipmet(models.Model):

    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)   
    value_str = models.CharField(max_length=100,null=True)
    value_txt = models.TextField(null=True)
    value_int = models.IntegerField(null=True)
    value_date = models.DateField(null=True)
    value_float = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    value_bool = models.BooleanField(null=True)
    value_cho  = models.ForeignKey(Choices,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.attribute.name + " de " + self.equipment.name
    
    

class Request(models.Model):
    date = models.DateField(auto_now_add=True)
    specs = models.TextField(blank=True,default="")
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='requesting_user')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='equipment_user',null=True)
    category = models.ManyToManyField(Category,through='RequestCategory')
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Solicitud de ' + str(self.user1)

class RequestCategory(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Loan(models.Model):
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='loan_user')
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator_user')
    hand_over_date = models.DateField()
    deadline = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    score = models.IntegerField(null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return 'Prestamo de equipo de ' + str(self.user)

    def borrowedEq():
        return Loan.objects.filter(delivery_date__isnull=True).values('equipment')

class Repair(models.Model):
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
    repairer = models.CharField(max_length=100,null=True)
    hand_over_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return 'Reparacion de ' + str(self.equipment)

class EquipmentDebt(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    damage_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    specs = models.TextField(blank=True)

    def __str__(self):
        return 'Deuda de equipo de ' + str(self.user)

class Transaction(models.Model):
    REASON_OPTIONS = [
        ('P','Pago'),
        ('M','Multa'),
        ('T','Trimestralidad'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction = models.DecimalField(max_digits=7, decimal_places=2)
    reason = models.CharField(max_length=1,choices=REASON_OPTIONS)
    
    def __str__(self):
        return 'Transaccion de ' + str(self.user) + ', ' + str(self.transaction) + ', ' + str(self.reason) 

class Quarterly(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
