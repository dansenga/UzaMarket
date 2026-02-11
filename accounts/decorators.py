from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def seller_required(view_func):
    """Décorateur : accès réservé aux vendeurs."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_seller:
            messages.error(request, "Accès réservé aux vendeurs.")
            return redirect("core:home")
        return view_func(request, *args, **kwargs)

    return _wrapped


def admin_required(view_func):
    """Décorateur : accès réservé aux administrateurs."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_admin_user:
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect("core:home")
        return view_func(request, *args, **kwargs)

    return _wrapped
