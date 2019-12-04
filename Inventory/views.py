from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import *
from .forms import *
from Users.models import User
from Users.permission import is_admin, is_gestor_usuario, is_cuarto_equipo, is_tesorero, is_activo, is_pasivo

######################
## VISTAS PRINCIPALES
######################
@login_required
def home_inventario_view(request):
    user = User.objects.get(pk=request.user.pk)

    # Deuda total
    deuda = Decimal(0)
    for i in user.transaction_set.all():
        deuda += i.transaction

    # Solicitudes

    context = {
        'deuda' : deuda,
        'grupo' : request.user.groups.all().first(),
        'solicitudes' : Request.objects.filter(user=user),
        'prestamos' : Loan.objects.filter(user=user)
    }
    return render(request, "Inventory/home.html", context)

@login_required
@is_tesorero
def home_tesorero_view(request):
    if request.method == "GET":
        context = {
            "trimestral" : Transaction.objects.filter(reason='T'),
            "pagos" : Transaction.objects.filter(reason='P'),
            "multas" : Transaction.objects.filter(reason='M')

        }
    return render(request, "Inventory/tesorero.html", context)

@login_required
@is_cuarto_equipo
def home_cuarto_equipo_view(request):
    if request.method == "GET":
        context = {
            "prestamos" : Loan.objects.all(),
            "solicitudes" : Request.objects.all(),
            "categorias" : Category.objects.all(),
            "equipos" : Equipment.objects.all(),
        }
    return render(request, "Inventory/cuarto_equipo.html", context)

@login_required
@is_admin
def create_category(request):
    if request.method == "POST":
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            category = cat_form.save()
            names = request.POST.getlist('att_name')
            types = request.POST.getlist('att_type')
            units = request.POST.getlist('unit')
            nulls = request.POST.getlist('nullity')
            for i in range(0,len(names)):
                att = Attribute(name=names[i],attribute_type=types[i],unit=units[i])
                if(nulls[i] == 'Opcional'):
                    att.nullity = True
                att.category = category
                att.save()
            messages.success(request, "Categoria añadida")
            return redirect("Inventory:create_category")
        else:
            messages.error(request, "Fallo al añadir categoria")
            return redirect("Inventory:home_inventory")
    else:
        category_form = CategoryForm()
        return render(request, "Inventory/create_category.html", {"categoryform" : category_form})

@login_required
@is_cuarto_equipo
def create_group(request):
    if request.method == "POST":
        gr_form = GroupForm(request.POST)
        if gr_form.is_valid():
            gr_form.save()
            messages.success(request, "Grupo añadido")
        else:
            messages.error(request, "Fallo al añadir grupo")
        return redirect("Inventory:home_inventory")
    else:
        gr_form = GroupForm()
        return render(request, "Inventory/create_group.html", {"form" : gr_form})

@login_required
@is_cuarto_equipo
def equip_cat_selection(request):
    if request.method == "POST":
        form = CatQueryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category'].pk
            return redirect("Inventory:create_equipment_value", cat=category)
        else:
            messages.error(request,"No existe esta categoría.")
            return redirect("Inventory:home_inventory")
    else:
        form = CatQueryForm()
        return render(request, "Inventory/create_equipment.html", {"form" : form })

@login_required
@is_cuarto_equipo
def create_equipment(request, cat):    
    if request.method == "POST":
        print(request.POST)
        equip_form = EquipmentForm(request.POST)
        if equip_form.is_valid():
            
            equipment = equip_form.save(commit=False)
            equipment.category = Category.objects.get(pk=cat)
            equipment.save()
            for group in request.POST.getlist('group'):
                if group != '':
                    g = Group.objects.get(name=group)
                    equipment.group.add(g)

            cat_attributes = list(Attribute.objects.filter(category=cat))
            
            idxs = [0,0,0,0,0,0,0]
            lists = [
                request.POST.getlist('value_int'),
                request.POST.getlist('value_txt'),
                request.POST.getlist('value_str'),
                request.POST.getlist('value_bool'),
                request.POST.getlist('value_date'),
                request.POST.getlist('value_cho'),
                request.POST.getlist('value_float')
            ]

            for att in cat_attributes:
                att_val = AttributeEquipmet()
                if att.attribute_type=='INT': #0
                    att_val.value_int = lists[0][idxs[0]]
                    idxs[0]+=1
                elif att.attribute_type=='TXT': #1
                    att_val.value_txt = lists[1][idxs[1]]
                    idxs[1]+=1
                elif att.attribute_type=='STR': #2
                    att_val.value_str = lists[2][idxs[2]]
                    idxs[2]+=1
                elif att.attribute_type=='BOO': #3
                    att_val.value_bool = lists[3][idxs[3]]
                    idxs[3]+=1
                elif att.attribute_type=='DAT': #4
                    att_val.value_date = lists[4][idxs[4]]
                    idxs[4]+=1
                elif att.attribute_type=='CHO': #5
                    att_val.value_cho = lists[5][idxs[5]]
                    idxs[5]+=1
                elif att.attribute_type=='FLT': #6
                    att_val.value_float = lists[6][idxs[6]]
                    idxs[6]+=1
                att_val.equipment = equipment
                att_val.attribute = att
                att_val.save()
            messages.success(request, "Equipo Agregado")
            return redirect("Inventory:home_inventory")
        else:                
            messages.error(request, "Fallo al agregar equipo")
            return render(request, "Inventory:ḧome_inventory")
    else:
        equip_form = EquipmentForm()
        catAttributes = list(Attribute.objects.filter(category=cat))
        att_forms=[]
        for att in cat_attributes:
            att_name = att.name
            att_null = not att.nullity
            if att.attribute_type=='INT':
                form = IntValueForm(att_null)
            elif att.attribute_type=='TXT':
                form = TxtValueForm(att_null)
            elif att.attribute_type=='STR':
                form = StrValueForm(att_null)
            elif att.attribute_type=='BOO':
                form = BoolValueForm(att_null)
            elif att.attribute_type=='DAT':
                form = DateValueForm(att_null)
            elif att.attribute_type=='CHO':
                form = ChoiceValueForm(att_null)
            elif att.attribute_type=='FLT':
                form = FltValueForm(att_null)
            att_forms.append((form,att_name,att_null))
        groups = Group.objects.all()
        return render(request, "Inventory/create_equipment_value.html", context = {
            "equipform" : equip_form, "attforms" : att_forms, 'groups':groups, 'page_title': 'Crear Equipo'
            })

@login_required
@is_activo
def create_request(request):
    if request.method == "POST":
                             
        cat_list = request.POST.getlist('cat_value')
        q_list = request.POST.getlist('cat_q')

        if(len(cat_list)!=len(q_list)):
            messages.error(request,"Solicitud incorrecta")
            return redirect("Inventory:create_request")

        if(any(int(q)<=0 for q in q_list) or 
           not all(Category.objects.filter(name=cat).exists() for cat in cat_list)):
           messages.error(request,"Solicitud incorrecta")
           return redirect("Inventory:create_request")

        request_obj = Request.objects.create(user=request.user,specs=request.POST['comments'])

        for i in range(0,len(cat_list)):
            quantity = int(q_list[i])
            category = Category.objects.get(name=cat_list[i])
            request_cat = RequestCategory.objects.create(
                                                        request=request_obj,
                                                        category=category,
                                                        quantity=quantity
                                                        )
            request_cat.save()
        
        messages.success(request,"Solicitud enviada")
        return redirect("Inventory:create_request")

    else:
        categories = Category.objects.all()
        return render(request, "Inventory/create_request.html", {'categories':categories})

@login_required
@is_pasivo
def cat_query_view(request):
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
def atts_query_view(request, category):
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
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_int=value).values()]
                elif att_type == 'STR':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_str=value).values()]
                elif att_type == 'TXT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_txt=value).values()]
                elif att_type == 'BOO':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_boo=value).values()]
                elif att_type == 'DAT':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_dat=value).values()]
                elif att_type == 'CHO':
                    equipment_ids = [val['equipment_id'] for val in AttributeEquipmet.objects.filter(attribute=att_id, value_cho=value).values()]
                query = query.filter(id__in=equipment_ids)              
            return render(request, "Inventory/table.html", {'table':query})
        else:
            messages.error(request,"Error: Valores no permitidos")
        return redirect("Inventory:home_inventory")
    else:
        form = AttsQueryForm(category)
        return render(request, "Inventory/search.html", {"form":form})

# VISTAS DE GESTOR DE USUARIOS
@login_required
@is_gestor_usuario
def manage_users(request, *args, **kwargs):
    return render(request, 'Inventory/manage_user.html', {'users': User.objects.all()})

@login_required
@is_cuarto_equipo
def loan_creation(request):
    if request.method == "POST":
        lc_form = LoanCreationForm(request.POST)
        if lc_form.is_valid():
            lc_form.save()
            messages.success(request, "Prestamo cargado")
        else:
            messages.error(request, "Fallo al cargar prestamo")
        return redirect("Inventory:home_inventory")
    else:
        lc_form = LoanCreationForm()
        return render(request, "Inventory/create_loan.html", {"form" : lc_form})

@login_required
@is_cuarto_equipo
def loan_devolution(request,loan):
    if request.method == "POST":
        instance = Loan.objects.get(pk=loan)
        form = LoanDevolutionForm(request.POST)
        if form.is_valid():
            delivery_date= form.cleaned_data.get("delivery_date")
            score= form.cleaned_data.get("score")
            notes= form.cleaned_data.get("notes")
            instance.delivery_date=delivery_date
            instance.score=score
            instance.notes=notes
            instance.save()
            messages.success(request, "Devolución cargada")
        else:
            messages.error(request, "Fallo al cargar devolución")
        return redirect("Inventory:home_inventory")
    else: 
        form = LoanDevolutionForm()
        return render(request, "Inventory/loan_devolution.html", {"form" : form})

        

@login_required
@is_pasivo
def show_equipment(request,category):

    atts = Attribute.objects.filter(category=category)
    equip = Equipment.objects.filter(category=category)
    catname = Category.objects.get(id=category).name
    borrowedEq = [ x['equipment'] for x in Loan.borrowedEq() ]
    discontinuedEq = [ x['id'] for x in Equipment.discontinuedEq() ]
    rows = []
    for eq in equip:

        available = 'Disponible'
        if(eq.id in borrowedEq):
            available = 'Prestado'
        elif(eq.id in discontinuedEq):
            available = 'Discontinuado'
        
        vals = [eq.serial, eq.name]
        name = eq.name
        for att in atts:
            att_type=att.attribute_type
            val=AttributeEquipmet.objects.get(attribute=att,equipment=eq)
            if att_type == 'INT':
                vals.append(val.value_int)
            elif att_type == 'STR':
                vals.append(val.value_str)
            elif att_type == 'TXT':
                vals.append(val.value_txt)
            elif att_type == 'BOO':
                vals.append(val.value_boo)
            elif att_type == 'DAT':
                vals.append(val.value_dat)
            elif att_type == 'FLT':
                vals.append(val.value_float)
            elif att_type == 'CHO':
                vals.append(val.value_cho)

        info = [ 
            {'name':'Fecha de elaboración','value':eq.elaboration_date}, 
            {'name':'Fecha de llegada a Oikos', 'value':eq.entry_date},
            {'name':'Fecha de descontinuación', 'value':eq.discontinued_date}, 
            {'name':'Notas sobre el equipo', 'value':eq.notes}
            ]
        groups = [group for group in eq.group.all()]
        rows.append({'name':name, 'vals':vals, 'av':available, 'info':info, 'groups':groups})

    return render(request, "Inventory/equipment_table.html", {'attributes': atts, 
                                                              'rows' : rows,
                                                              'name' : catname                                                
                                                              })

@login_required
@is_tesorero
def load_transaction(request):
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
        return redirect("Inventory:tesorero")
    form = TransactionForm()
    return render(request, "Inventory/load_transaction.html", {"form" : form, "heading": "Cargar Transacciones"})


@login_required
@is_cuarto_equipo
def devolution_deadline_global(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            date= form.cleaned_data.get("date")
            activeloans = Loan.objects.filter(delivery_date__isnull=True).filter(deadline__isnull=True, deadline__gte=date)
            activeloans.deadline=date
            activeloans.save()
            messages.success(request, "Fecha de entrega cargada")
        else:
            messages.success(request, "Fecha inválida")
        return redirect("Inventory:cuarto_equipo")
    else:
        form = DateForm()
        ###### CREAR TEMMPLATE
        return redirect("Inventory:cuarto_equipo")

@login_required
@is_cuarto_equipo
def devolution_deadline_single(request,pk):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            date= form.cleaned_data.get("date")
            loan = Loan.objects.get(pk=pk)
            loan.deadline=date
            loan.save()
            messages.success(request, "Fecha de entrega cargada")
        else:
            messages.success(request, "Fecha inválida")
        return redirect("Inventory:cuarto_equipo")
    else:
        form = DateForm()
        ###### CREAR TEMMPLATE
        return redirect("Inventory:cuarto_equipo")