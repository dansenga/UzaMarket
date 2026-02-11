from django.shortcuts import render
from products.models import Product, Category


def home(request):
    """Page d'accueil."""
    featured_products = Product.objects.filter(is_active=True, quantity__gt=0)[:8]
    categories = Category.objects.all()[:6]
    return render(request, "core/home.html", {
        "featured_products": featured_products,
        "categories": categories,
    })


def about(request):
    """Page À propos."""
    return render(request, "core/about.html")


def contact(request):
    """Page Contact."""
    return render(request, "core/contact.html")
