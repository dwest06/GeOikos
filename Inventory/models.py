from django.db import models
from Users.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class Equipment(models.Model):
	serial = models.IntegerField(unique=True)
	name = models.CharField(max_length=100)
	entry_date = models.DateField(null=True)
	elaboration_date = models.DateField(null=True)
	discontinued = models.BooleanField(default=False)
	discontinued_date = models.DateField(null=True)
	notes = models.TextField(blank=True)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)

	def __str__(self):
		return self.name+ ': equipment of ' + self.category

class Attribute(models.Model):
	TYPE_CHOICES = [
		('INT', 'Integer'),
		('TXT', 'Text'),
		('STR', 'String'),
		('BOO', 'Boolean'),
		('FLT', 'Float'),
		('DAT', 'Date'),
		('CHO', 'Choice'),
	]
	name = models.CharField(max_length=50)
	attribute_type = models.CharField(max_length=3,choices=TYPE_CHOICES)
	unit = models.CharField(max_length=20, null=True, blank=True)
	nullity = models.BooleanField(default=False)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

# Opciones para un atributo de multiples opciones
class Choices(models.Model):
	attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
	option_name = models.CharField(max_length=100)

	def __str__(self):
		return self.option_name

class Attribute_Equipment(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
	value_str = models.CharField(max_length=100,null=True)
	value_txt = models.TextField(null=True)
	value_int = models.IntegerField(null=True)
	value_date = models.DateField(null=True)
	value_bool = models.BooleanField(null=True)
	value_cho  = models.ForeignKey(Choices,null=True,on_delete=models.CASCADE)

class Group(models.Model):
	name = models.CharField(max_length=120)
	equipment = models.ManyToManyField(Equipment)

	def __str__(self):
		return self.name

class Request(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	specs = models.TextField(null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	equipment = models.ManyToManyField(Equipment)
	category = models.ManyToManyField(Category,through='Request_Category' )

	def __str__(self):
		return 'Request of ' + str(self.user)

class Request_Category(models.Model):
	request = models.ForeignKey(Request, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

class Loan(models.Model):
	equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	hand_over_date = models.DateTimeField()
	deadline = models.DateTimeField(null=True)
	delivery_date = models.DateTimeField(null=True)
	score = models.IntegerField(null=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		return 'Equipment loan of ' + str(self.user)

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

class Transaction(models.Model):
	REASON_OPTIONS = [
		('P','Payment'),
		('F','Fine'),
		('T','Membership'),
	]
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	transaction = models.IntegerField()
	reason = models.CharField(max_length=1,choices=REASON_OPTIONS)
