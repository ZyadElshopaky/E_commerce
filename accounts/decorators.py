from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def seller_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in.")
                return redirect("login")
            if not request.user.is_seller :
                messages.error(request, "You are not a seller")
                return redirect("home")
            
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator