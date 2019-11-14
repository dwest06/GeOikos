from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import (Category, Equipment, Attribute, Group, 
                    Request, Request_Category, Loan, Repair, 
					EquipmentDebt, Transaction, Attribute_Equipment)
from django.core.validators import MaxValueValidator

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		labels = {
			'name' : 'Nombre de Categoría'
		}

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
                'serial', 'name', 'entry_date', 
                'elaboration_date', 'notes', 'group'
            ]
        labels = {
            'serial' : 'Serial',
            'name' : 'Nombre del Equipo',
            'entry_date' : 'Fecha de Entrada',
            'elaboration_date' : 'Fecha de Elaboracion',
            'notes' : 'Notas',
            'group' : 'Grupo'
        }

AttributeFormset = modelformset_factory(
	Attribute,
	fields = ['name', 'attribute_type', 'unit', 'nullity'],
	extra = 1,
	labels = {
		'name' : 'Nombre de Atributo',
		'attribute_type' : 'Tipo de dato',
		'unit' : 'Unidad',
		'nullity' : '(No esencial)'
	}
)

class IntValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_int']
        labels = { 'value_int' : ''}

class TxtValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_txt']
        labels = { 'value_txt' : ''}

class StrValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_str']
        labels = { 'value_str' : ''}

class DateValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_date']
        labels = { 'value_date' : ''}

class BoolValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_bool']
        labels = { 'value_bool' : ''}

class ChoiceValueForm(forms.ModelForm):
    class Meta:
        model = Attribute_Equipment
        fields = ['value_cho']
        labels = { 'value_cho' : ''}


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['user', 'specs', 'equipment', 'category']

class Request_CatForm(forms.ModelForm):
    class Meta:
        model = Request_Category
        fields = ['request', 'category', 'quantity']

class LoanCreationForm(forms.ModelForm):
    class Meta:
        model = Loan 
        fields = ['equipment', 'user', 'hand_over_date']
        labels = {
            'equipment' : 'Equipo',
            'user' : 'Usuario',
            'hand_over_date' : 'Fecha'
        }

class LoanDevolutionForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['delivery_date', 'score', 'notes']
        labels = {
            'delivery_date' : 'Fecha',
            'score' : 'Puntaje',
            'notes' : 'Notas'
        }

class RepairCreationForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['equipment', 'notes']

class RepairHandOverForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['repairer', 'hand_over_date', 'notes']

class RepairDevolutionForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['return_date', 'notes']

class EquipmentDebtCreationForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['user', 'category', 'damage_date', 'specs']

class EquipmentDebtReturnForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['return_date', 'specs']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'transaction', 'reason']
        labels = {
            'user' : 'Usuario',
            'transaction'  : 'Monto',
            'reason' : 'Motivo'
        }

class CatQueryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

class CatReqForm(forms.Form):
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	quantity = forms.IntegerField(label="quantity", required=True, initial=1)

	def clean_quantity(self):
		quantity = self.cleaned_data['quantity']
		if quantity <= 0:
			raise forms.ValidationError("Debes especificar una cantidad positiva")
		return quantity

CatReqFormset = formset_factory(
	CatReqForm,
	extra = 1
)

class EqReqForm(forms.Form):
	equipment = forms.ModelChoiceField(queryset=Equipment.objects.all())

class CommentsReqForm(forms.Form):
	comments = forms.CharField(required=False, widget=forms.Textarea)

EqReqFormset = formset_factory(
	EqReqForm,
	extra = 1
)

class AttsQueryForm(forms.Form):

    def __init__(self, category, *args, **kwargs):
        
        super(AttsQueryForm, self).__init__(*args, **kwargs)

        for att in Attribute.objects.filter(category=category):
            if att.attribute_type == 'INT' or att.attribute_type == 'FLT':
                self.fields[att.name] = forms.IntegerField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'STR':
                self.fields[att.name] = forms.CharField(max_length=100, label=att.name, required=att.nullity)
            elif att.attribute_type == 'TXT':
                self.fields[att.name] = forms.CharField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'BOO':
                self.fields[att.name] = forms.BooleanField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'DAT':
                self.fields[att.name] = forms.DateField(label=att.name, required=att.nullity)
            elif att.attribute_type == 'CHO':
                CHOICES = [dic['option_name'] for dic in Choices.objects.filter(attribute=att).values('option_name')]
                self.fields[att.name] = forms.ChoiceField(choices=CHOICES, label=att.name, required=att.nullity)
    