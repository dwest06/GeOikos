from django import forms
from django.forms import formset_factory, modelformset_factory, widgets
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError 
from .models import (Category, Equipment, Attribute, Group, 
                    Request, RequestCategory, Loan, Repair, 
                    EquipmentDebt, Transaction, AttributeEquipmet)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name' : 'Nombre de la categoria'
        }
        error_messages = {
            'name' : {
                'required' : 'Campo obligatorio'
            }
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
                'serial', 'name', 'entry_date', 
                'elaboration_date', 'notes'
            ]
        labels = {
            'serial' : 'Serial',
            'name' : 'Nombre del Equipo',
            'entry_date' : 'Fecha de entrada a Oikos',
            'elaboration_date' : 'Fecha de Elaboracion',
            'notes' : 'Notas',
        }
        error_messages = {
            'serial' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
            },
            'name' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido',
            },
            'entry_date' : {
                'invalid' : 'Fecha inválida',
            },
            'elaboration_date' : {
                'invalid' : 'Fecha inválida',
            }
        }
    def clean_serial(self):
        serial = self.cleaned_data['serial']
        if serial is None:
            return None
        if serial < 0:
            raise forms.ValidationError("Debes especificar una cantidad positiva")
        return serial
        
class IntValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_int']
        labels = { 'value_int' : ''}

        error_messages = {
            'value_int' : {
                'invalid' : 'Entrada inválida'
            }
        }

        widgets = {
            'value_int' : widgets.NumberInput(attrs={'class' : 'form-control ', 'placeholder' : 'Inserte un entero aquí'})
        }

    def __init__(self, required, *args, **kwargs):
        super(IntValueForm, self).__init__(*args, **kwargs)
        self.fields['value_int'].required=required

class FltValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_float']
        labels = { 'value_float' : ''}

        error_messages = {
            'value_float' : {
                'invalid' : 'Entrada inválida'
            }
        }

    def __init__(self, required, *args, **kwargs):
        super(FltValueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['value_float'].required=required
        
class TxtValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_txt']
        labels = { 'value_txt' : ''}

        error_messages = {
            'value_txt' : {
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

        widgets = {
            'value_txt' : widgets.Textarea(attrs={'class' : 'form-control ', 'placeholder' : 'Inserte texto aquí'})
        }

    def __init__(self, required, *args, **kwargs):
        super(TxtValueForm, self).__init__(*args, **kwargs)
        self.fields['value_txt'].required=required

class StrValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_str']
        labels = { 'value_str' : ''}

        error_messages = {
            'value_str' : {
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

    def __init__(self, required, *args, **kwargs):
        super(StrValueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['value_str'].required=required

class DateValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_date']
        labels = { 'value_date' : ''}

        error_messages = {
            'value_date' : {
                'invalid' : 'Fecha inválida',
            }
        }

        widgets = {
            'value_date' : widgets.DateInput(attrs={'type':'date', 'class':'form-control', 'placeholder':'MM/DD/YYYY'})
        }

    def __init__(self, required, *args, **kwargs):
        super(DateValueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['type'] = 'date'
            visible.field.widget.attrs['placeholder'] = "mm/dd/yyyy"
        self.fields['value_date'].required=required
    
class BoolValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_bool']
        labels = { 'value_bool' : ''}
        
        widgets = {
            'value_bool' : widgets.Select(attrs={'class':'form-control custom-select'}, choices=[(True,'Verdadero'),(False,'Falso')])
        }

    def __init__(self, required, *args, **kwargs):
        super(BoolValueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if not required:
                visible.field.widget.choices = [(None,'-----'),(True,'Verdadero'),(False,'Falso')]
        self.fields['value_bool'].required=required
        

class ChoiceValueForm(forms.ModelForm):
    class Meta:
        model = AttributeEquipmet
        fields = ['value_cho']
        labels = { 'value_cho' : ''}

    def __init__(self, required, *args, **kwargs):
        super(ChoiceValueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['value_cho'].required=required


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = { 'name' : 'Nombre'}
        error_messages = {
            'name' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class LoanCreationForm(forms.ModelForm):
    class Meta:
        model = Loan 
        fields = ['equipment', 'user', 'hand_over_date']
        labels = {
            'equipment' : 'Equipo',
            'user' : 'Usuario',
            'hand_over_date' : 'Fecha'
        }

        error_messages = {
            'equipment' : {
                'required' : 'Campo obligatorio',
            },
            'user' : {
                'required' : 'Campo obligatorio',
            },
            'hand_over_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            }
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

        error_messages = {
            'delivery_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'score' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairCreationForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['equipment', 'notes']

        error_messages = {
            'equipment' : {
                'required' : 'Campo obligatorio',
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairHandOverForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['repairer', 'hand_over_date', 'notes']

        error_messages = {
            'repairer' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            },
            'hand_over_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class RepairDevolutionForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['return_date', 'notes']

        error_messages = {
            'return_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'notes' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class EquipmentDebtCreationForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['user', 'category', 'damage_date', 'specs']

        error_messages = {
            'user' : {
                'required' : 'Campo obligatorio',
            },
            'category' : {
                'required' : 'Campo obligatorio',
            },
            'damage_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'specs' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class EquipmentDebtReturnForm(forms.ModelForm):
    class Meta:
        model = EquipmentDebt
        fields = ['return_date', 'specs']

        error_messages = {
            'return_date' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Fecha inválida'
            },
            'specs' : {
                'required' : 'Campo obligatorio',
                'max_length' : 'Máximo de caracteres excedido'
            }
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        
        model = Transaction
        fields = ['user', 'transaction', 'reason']
        labels = {
            'user' : 'Usuario: ',
            'transaction'  : 'Monto: ',
            'reason' : 'Motivo: '
        }
        error_messages = {
            'user' : {
                'required' : "Campo obligatorio"
            },
            'transaction' : {
                'required' : 'Campo obligatorio',
                'invalid' : 'Entrada inválida',
                'max_digits' : 'Máximo de 7 dígitos',
                'max_decimals' : 'Máximo de 2 decimales'
            }
        }

class CatReqForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Categoría")
    quantity = forms.IntegerField(label="Cantidad", required=True, initial=1)

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        notAvEq = Equipment.notAvEquipment()
        avCat = {x.category.id for x in Equipment.objects.exclude(id__in=notAvEq)}
        self.fields['category'].queryset = Category.objects.filter(id__not_Fin=avCat)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Debes especificar una cantidad positiva")
        return quantity

class CatQueryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Categoría: ')
    
CatReqFormset = formset_factory(
    CatReqForm,
    extra = 1
)

class EqReqForm(forms.Form):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label="Equipo"
    )

    def __init__(self, *a, **kw):
        super().__init__(a, kw)
        self.fields['equipment'].queryset=Equipment.objects.exclude(id__in=Equipment.notAvEquipment())        
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
    
class DateForm(forms.Form):
    date = forms.DateField()