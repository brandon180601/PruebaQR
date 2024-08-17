from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.user.ID_persona.ID_rol.nombre_rol
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('Acceso')  # Redirige a una vista de acceso denegado
        return _wrapped_view
    return decorator