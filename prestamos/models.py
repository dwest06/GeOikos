from django.db import models
from usuarios.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class Equipment(models.Model):
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	elaboration_date = models.DateField(null=True)
	entry_date = models.DateField(null=True)
	discontinued = models.BooleanField(default=False)
	discontinued_date = models.DateField(null=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		return 'Equipment of ' + self.category

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

	def __str__(self):
		return self.name

class Value(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)

	class Meta:
		abstract = True

class IntValue(Value):
	value = models.IntegerField(null=True)

	def __str__(self):
		return 'Int ' + str(self.value)

class LstValue(Value):
	value =models.TextField(null=True)

	def __str__(self):
		return 'Lst ' + str(self.value)

class SstValue(Value):
	value = models.CharField(max_length=140, null=True)

	def __str__(self):
		return 'Sst ' + str(self.value)

class BooValue(Value):
	value = models.BooleanField(null=True)

	def __str__(self):
		return 'Bool ' + str(self.value)

class FltValue(Value):
	value = models.IntegerField(null=True) #Esto se dividira entre 100 para tener puntos decimales
	def __str__(self):
		return 'Flt ' + str(self.value)

class DatValue(Value):
	value = models.DateField(null=True)

	def __str__(self):
		return 'Date ' + str(self.value)

#Opciones para un atributo de multiples opciones
class Options(models.Model):
	atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)
	option = models.CharField(max_length=100)

	def __str__(self):
		return self.option

#Escoger entre las opciones
class ChoValue(Value):
	value = models.ForeignKey(Options,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return 'Cho ' + str(self.value)

class Group(models.Model):
	name = models.CharField(max_length=120)
	equipment = models.ManyToManyField(Equipment)

	def __str__(self):
		return self.name

class Request(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Request of ' + str(self.user)

class RequestedItem(models.Model):
	request = models.ForeignKey(Request,on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	specs = models.TextField(blank=True)

	def __str__(self):
		return 'RequestItem of ' + str(self.request)

class EquipmentLoan(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	hand_over_date = models.DateField()
	return_date = models.DateField(null=True)
	score = models.PositiveIntegerField(
		validators=[MaxValueValidator(500)] #Esto se dividira entre 100 para tener puntos decimales
		)
	request = models.ForeignKey(Request,on_delete=models.CASCADE,null=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		return 'Equipment Loan of ' + str(self.equipment) + ' to ' + str(self.user)

class Repair(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	repairer = models.CharField(max_length=100,null=True)
	hand_over_date = models.DateField(null=True)
	return_date = models.DateField(null=True)
	notes = models.TextField(blank=True)
	def __str__(self):
		return 'Repair of ' + str(self.equipment)

class EquipmentDebt(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	damage_date = models.DateField(null=True)
	return_date = models.DateField(null=True)
	specs = models.TextField(blank=True)

	def __str__(self):
		return 'Equipment Debt of ' + str(self.equipment)

class Balance(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
	balance = models.IntegerField(default=0)

	def __str__(self):
		return 'Equipment Loan of ' + str(self.equipment)

class Transaction(models.Model):
	REASON_OPTIONS = [
		('P','Payment'),
		('F','Fine'),
		('T','Membership'),
	]
	user = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
	transaction = models.IntegerField()
	reason = models.CharField(max_length=1,choices=REASON_OPTIONS)

	def __str__(self):
		return 'Transaction of ' + str(self.user)
