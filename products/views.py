from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    """Liste des produits avec filtrage."""
    products = Product.objects.filter(is_active=True, quantity__gt=0)
    categories = Category.objects.all()

    # Filtrage par catégorie
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Filtrage par état
    condition = request.GET.get("condition")
    if condition:
        products = products.filter(condition=condition)

    # Filtrage par prix
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Recherche
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Tri
    sort = request.GET.get("sort", "-created_at")
    if sort in ["price", "-price", "-created_at", "created_at", "name"]:
        products = products.order_by(sort)

    context = {
        "products": products,
        "categories": categories,
        "current_category": category_slug,
        "current_condition": condition,
        "current_sort": sort,
        "query": query or "",
    }

    # Support HTMX : renvoyer uniquement la grille de produits
    if request.headers.get("HX-Request"):
        return render(request, "products/includes/product_grid.html", context)

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    """Détail d'un produit."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)[:4]
    )
    return render(request, "products/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })
