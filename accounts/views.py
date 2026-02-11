from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, SellerRegisterForm, LoginForm, ProfileForm


def register_view(request):
    """Inscription client."""
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue sur UzaShop.")
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def seller_register_view(request):
    """Inscription vendeur."""
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription vendeur réussie ! Bienvenue sur UzaShop.")
            return redirect("seller:dashboard")
    else:
        form = SellerRegisterForm()
    return render(request, "accounts/seller_register.html", {"form": form})


def login_view(request):
    """Connexion."""
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} !")
            next_url = request.GET.get("next", "core:home")
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Déconnexion."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("core:home")


@login_required
def profile_view(request):
    """Profil utilisateur."""
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
