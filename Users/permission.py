from geoikos.settings import LOGIN_URL
from django.db.models import Q
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def test(test_func):
    """
    Aux function for decorators
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            messages.error(request, "Acceso denegado, No tienes permisos para realizar esta accion.")
            return redirect("Inventory:home_inventory")
        return _wrapped_view
    return decorator



def is_admin(function=None):
    """
    Decorator for check if user is admin.
    """
    actual_decorator = test(lambda user: user.groups.filter(name='admin').exists())
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_gestor_usuario(function=None,):
    """
    Decorator for check if user is gestor de usuarios.
    """
    actual_decorator = test(
        lambda user: user.groups.filter(Q(name='admin') | Q(name='gestor_usuarios')).exists()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_tesorero(function=None,):
    """
    Decorator for check if user is tesorero.
    """
    actual_decorator = test(
        lambda user: user.groups.filter(Q(name='admin') | Q(name='tesorero')).exists()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_cuarto_equipo(function=None,):
    """
    Decorator for check if user is cuarto de equipo.
    """
    actual_decorator = test(
        lambda user: user.groups.filter(Q(name='admin') | Q(name='cuarto_equipo')).exists()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_activo(function=None,):
    """
    Decorator for check if user is miembro activo.
    """
    actual_decorator = test(
        lambda user: user.groups.filter(
            Q(name='admin') |
            Q(name='cuarto_equipo') |
            Q(name='gestor_usuarios') |
            Q(name='tesorero') |
            Q(name='activo')
        ).exists()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_pasivo(function=None,):
    """
    Decorator for check if user is miembro pasivo.
    """
    actual_decorator = test(
        lambda user: user.groups.filter(
            Q(name='admin') |
            Q(name='cuarto_equipo') |
            Q(name='gestor_usuarios') |
            Q(name='tesorero') |
            Q(name='activo') |
            Q(name='pasivo')
        ).exists()
    )
    if function:
        return actual_decorator(function)
    return actual_decorator