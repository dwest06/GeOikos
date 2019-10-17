from django.db import models
from GeOikos.usuarios.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=60)

class Equipment(models.Model):
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	elaboration_date = models.DateField(null=True)
	entry_date = models.DateField(null=True)
	discontinued = models.BooleanField(default=False)
	discontinued_date = models.DateField(null=True)
	notes = models.TextField(blank=True)

class Atribute(models.Model):
	TYPE_CHOICES = [
		('INT', 'Integer'),
		('LST', 'LongString'),
		('SST', 'ShortString'),
		('BOO', 'Boolean'),
		('FLT', 'Float'),
		('DAT', 'Date'),
		('CHO', 'Choice'),
	]
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	atribute_type = models.CharField(max_length=3,choices=TYPE_CHOICES)
	unit = models.CharField(max_length=20)
	nullity = models.BooleanField()

class Value(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)

	class Meta:
		abstract = True

class IntValue(Value):
	value = models.IntegerField(null=True)

class LstValue(Value):
	value =models.TextField(null=True)

class SstValue(Value):
	value = models.CharField(max_length=140, null=True)

class BooValue(Value):
	value = models.BooleanField(null=True)

class FltValue(Value):
	value = models.IntegerField(null=True) #Esto se dividira entre 100 para tener puntos decimales

class DatValue(Value):
	value = models.DateField(null=True)

#Opciones para un atributo de multiples opciones
class Options(models.Model):
	atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)
	option = models.CharField(max_length=100)

#Escoger entre las opciones
class ChoValue(Value):
	value = models.ForeignKey(Options,on_delete=models.CASCADE,null=True)

class Group(models.Model):
	name = models.CharField(max_length=120)
	equipment = models.ManyToManyField(Equipment)

class Request(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

class RequestedItem(models.Model):
	request = models.ForeignKey(Request,on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	specs = models.TextField(blank=True)

class EquipmentLoan(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	hand_over_date = models.DateField()
	return_date = models.DateField(null=True)
	score = models.IntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(500)] #Esto se dividira entre 100 para tener puntos decimales
		)
	request = models.ForeignKey(Request,on_delete=models.CASCADE,null=True)
	notes = models.TextField(blank=True)


class Repair(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	repairer = models.CharField(max_length=100,null=True)
	hand_over_date = models.DateField(null=True)
	return_date = models.DateField(null=True)
	notes = models.TextField(blank=True)

class EquipmentDebt(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	damage_date = models.DateField(null=True)
	return_date = models.DateField(null=True)
	specs = models.TextField(blank=True)

class Balance(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
	balance = models.IntegerField(default=0)

class Transaction(models.Model):
	REASON_OPTIONS = [
		('P','Payment'),
		('F','Fine'),
		('T','Membership'),
	]
	user = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
	transaction = models.IntegerField()
	reason = models..CharField(max_length=1,choices=REASON_OPTIONS)
