from functools import wraps
from django.http import HttpResponseForbidden

def hospital_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
                                    # Check if user is authenticated and has 'is_hospital_admin' attribute set True
        if not request.user.is_authenticated or not getattr(request.user, 'is_hospital_admin', False):
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def ticket_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
                                       # Check if user is authenticated and has 'is_ticket_admin' attribute set True
        if not request.user.is_authenticated or not getattr(request.user, 'is_ticket_admin', False):
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
