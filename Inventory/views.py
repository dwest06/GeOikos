from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
<<<<<<< HEAD
from .forms import (
    CategoryForm, AttributeFormset, CatQueryForm, EquipmentForm, 
    IntValueForm, TxtValueForm, StrValueForm, DateValueForm, 
    BoolValueForm, ChoiceValueForm, AttsQueryForm, GroupForm
)
from Users.models import User
=======
from .forms import *
>>>>>>> payments
from Users.permission import is_admin, is_gestor_usuario, is_cuarto_equipo, is_tesorero, is_activo, is_pasivo

@login_required
def homeInventarioView(request):
    context = {
        'deuda' : 0.00,
        'grupo' : request.user.groups.all().first()
    }
    return render(request, "Inventory/home.html", context)

@login_required
@is_admin
def createCategory(request):
    if request.method == "POST":
        catForm = CategoryForm(request.POST)
        attFormset = AttributeFormset(request.POST)
        if catForm.is_valid() and attFormset.is_valid():
            category = catForm.save()
            for attform in attFormset:
                attribute = attform.save(commit=False)
                attribute.category = category
                attribute.save()
            messages.success(request, "Categoria añadida")
            return redirect("Inventory:create_category")
        else:
            messages.error(request, "Fallo al añadir categoria")
            return redirect("Inventory:home_inventory")
    else:
        categoryForm = CategoryForm()
        attFormset = AttributeFormset(queryset=Attribute.objects.none())
        return render(request, "Inventory/create_category.html", {"categoryform" : categoryForm, "formset" : attFormset})

@login_required
@is_cuarto_equipo
def createGroup(request):
    if request.method == "POST":
        grForm = GroupForm(request.POST)
        if grForm.is_valid():
            grForm.save()
            messages.success(request, "Grupo añadido")
        else:
            messages.error(request, "Fallo al añadir grupo")
        return redirect("Inventory:home_inventory")
    else:
        grForm = GroupForm()
        return render(request, "Inventory/create_group.html", {"form" : grForm})

@login_required
@is_pasivo
def EquipCatSelection(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:create_equipment_value", cat=category)
        else:
            messages.error(request,"No existe esta categoria.")
        return redirect("Inventory:home_inventory")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/create_equipment.html", {"form" : form})

@login_required
@is_cuarto_equipo
def createEquipment(request, cat):
    if request.method == "POST":
        equipForm = EquipmentForm(request.POST)
        catAttributes = list(Attribute.objects.filter(category=cat))
        attForms=[]
        for att in catAttributes:
            if att.attribute_type=='INT' or att.attribute_type=='FLT':
                attForms.append(IntValueForm(request.POST))
            elif att.attribute_type=='TXT':
                attForms.append(TxtValueForm(request.POST))
            elif att.attribute_type=='STR':
                attForms.append(StrValueForm(request.POST))
            elif att.attribute_type=='BOO':
                attForms.append(BoolValueForm(request.POST))
            elif att.attribute_type=='DAT':
                attForms.append(DateValueForm(request.POST))
            elif att.attribute_type=='CHO':
                attForms.append(ChoiceValueForm(request.POST))
        if equipForm.is_valid() and all(attForm.is_valid() for attForm in attForms):
            equipment= equipForm.save(commit=False)
            equipment.category = Category.objects.get(pk=cat)
            equipment.save()
            i=0
            for attForm in attForms:
                value = attForm.save(commit=False)
                value.equipment = equipment
                value.attribute = catAttributes[i]
                value.save()
                i+=1
            messages.success(request, "Equipo Agregado")
        else:
            messages.error(request, "Fallo al agregar equipo")
        return redirect("Inventory:home_inventory")
    else:
        equipForm = EquipmentForm()
        catAttributes = list(Attribute.objects.filter(category=cat))
        attForms=[]
        for att in catAttributes:
            attName = att.name
            if att.attribute_type=='INT' or att.attribute_type=='FLT':
                attForms.append((IntValueForm(),attName))
            elif att.attribute_type=='TXT':
                attForms.append((TxtValueForm(),attName))
            elif att.attribute_type=='STR':
                attForms.append((StrValueForm(),attName))
            elif att.attribute_type=='BOO':
                attForms.append((BoolValueForm(),attName))
            elif att.attribute_type=='DAT':
                attForms.append((DateValueForm(),attName))
            elif att.attribute_type=='CHO':
                attForms.append((ChoiceValueForm(),attName))

        return render(request, "Inventory/create_equipment_value.html", {"equipform" : equipForm, "attforms" : attForms})

@login_required
@is_activo
def createRequest(request):
    if request.method == "POST":
        catformset = CatReqFormset(request.POST)
        eqformset  = EqReqFormset(request.POST)
        comments   = CommentsReqForm(request.POST)
       
        if catformset.is_valid() and eqformset.is_valid() and comments.is_valid():
            requestObj = Request.objects.create(user=request.user)
            requestObj.specs = comments.cleaned_data['comments']
            
            for form in catformset: 
                try:
                    category = form.cleaned_data['category'].pk              
                    quantity = form.cleaned_data['quantity']
                except KeyError:
                    continue
                requestcat =  Request_Category.objects.create(
                                category=Category.objects.get(pk=category),
                                request=requestObj,
                                quantity=form.cleaned_data['quantity']
                              )
                requestcat.save()
            
            requestObj.save()

            for form in eqformset:
                try:
                    equipment = form.cleaned_data['equipment'].pk
                except KeyError:
                    continue
                requestObj.equipment.add(Equipment.objects.get(pk=equipment))
        
        else:
            messages.error(request,"Form Inválido. Ingrese una cantidad positiva")
            return redirect("Inventory:create_request")
        
        messages.success(request,"")
        return render(request,"oikos/home.html")

    else:
        catform = CatReqFormset()
        eqform = EqReqFormset()
        comments = CommentsReqForm()
        return render(request, "Inventory/create_request.html", 
                      {"catformset" : catform, "eqformset" : eqform, "comments" : comments})

<<<<<<< HEAD
=======
@login_required
@is_pasivo
>>>>>>> payments
def CatQueryView(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:show_equipment", category=category)
        else:
            messages.error(request,"No existe esta categoria.")
        return redirect("Inventory:home_inventory")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/search.html", {"form" : form})

@login_required
@is_pasivo
def AttsQueryView(request, category):
    if request.method == "POST":
        form = AttsQueryForm(category,request.POST)
        if form.is_valid():
            user_atts = form.cleaned_data
            query = Equipment.objects.filter(category=category)
            for att in Attribute.objects.filter(category=category).values():
                att_id   = att['id']
                att_name = att['name']
                att_type = att['attribute_type']
                try:
                    value = user_atts[att_name]
                    assert(value)
                except (KeyError, AssertionError):
                    continue
                if att_type == 'INT' or att_type == 'FLT':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_int=value).values()]
                elif att_type == 'STR':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_str=value).values()]
                elif att_type == 'TXT':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_txt=value).values()]
                elif att_type == 'BOO':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_boo=value).values()]
                elif att_type == 'DAT':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_dat=value).values()]
                elif att_type == 'CHO':
                    equipment_ids = [val['equipment_id'] for val in Attribute_Equipment.objects.filter(attribute=att_id, value_cho=value).values()]
                query = query.filter(id__in=equipment_ids)              
            return render(request, "Inventory/table.html", {'table':query})
        else:
            messages.error(request,"Error: Valores no permitidos")
        return redirect("Inventory:home_inventory")
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

<<<<<<< HEAD
# VISTAS DE GESTOR DE USUARIOS
@login_required
@is_gestor_usuario
def manage_users(request, *args, **kwargs):
    return render(request, 'Inventory/manage_user.html', {'users': User.objects.all()})
=======
@login_required
@is_cuarto_equipo
def LoanCreation(request):
    if request.method == "POST":
        lcForm = LoanCreationForm(request.POST)
        if lcForm.is_valid():
            lcForm.save()
            messages.success(request, "Prestamo cargado")
        else:
            messages.error(request, "Fallo al cargar prestamo")
        return redirect("Inventory:home_inventory")
    else:
        lcForm = LoanCreationForm()
        return render(request, "Inventory/create_loan.html", {"form" : lcForm})

@login_required
@is_pasivo
def ShowEquipment(request,category):
    atts = Attribute.objects.filter(category=category)
    equip = Equipment.objects.filter(category=category)
    vals = []
    for eq in equip:
        vals2 = [eq.name]
        for att in atts:
            att_type=att.attribute_type
            val=Attribute_Equipment.objects.get(attribute=att,equipment=eq)
            if att_type == 'INT' or att_type == 'FLT':
                vals2.append(val.value_int)
            elif att_type == 'STR':
                vals2.append(val.value_str)
            elif att_type == 'TXT':
                vals2.append(val.value_txt)
            elif att_type == 'BOO':
                vals2.append(val.value_boo)
            elif att_type == 'DAT':
                vals2.append(val.value_dat)
            elif att_type == 'CHO':
                vals2.append(val.value_cho)
        vals.append(vals2)
    return render(request, "Inventory/equipment_table.html", {'attributes': atts, 'values':vals})

@login_required
@is_tesorero
def loadTransaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid() and form.cleaned_data['transaction'] > 0.00:
            trans = form.save(commit = False)
            if trans.reason != 'P':
                trans.transaction *= -1
            trans.save()
            messages.success(request, "Transacción cargada")
        else:
            messages.error(request, "Fallo al cargar transacción")
        return redirect("Inventory:load_transaction")
    form = TransactionForm()
    return render(request, "Inventory/load_transaction.html", {"form" : form})
>>>>>>> payments
