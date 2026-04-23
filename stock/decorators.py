from functools import wraps
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
