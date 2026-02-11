from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from products.models import Product, Category
from accounts.decorators import admin_required


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


# ── Administration ────────────────────────────────
@admin_required
def admin_dashboard(request):
    from accounts.models import User
    from orders.models import Order, OrderItem

    context = {
        "total_users": User.objects.count(),
        "total_sellers": User.objects.filter(role="seller").count(),
        "total_clients": User.objects.filter(role="client").count(),
        "total_products": Product.objects.count(),
        "active_products": Product.objects.filter(is_active=True).count(),
        "total_orders": Order.objects.count(),
        "total_revenue": OrderItem.objects.aggregate(
            total=Sum(F("product_price") * F("quantity"))
        )["total"] or 0,
        "recent_orders": Order.objects.order_by("-created_at")[:10],
        "recent_users": User.objects.order_by("-date_joined")[:10],
        "pending_orders": Order.objects.filter(status="pending").count(),
    }
    return render(request, "admin_panel/dashboard.html", context)


@admin_required
def admin_users(request):
    from accounts.models import User

    users = User.objects.all().order_by("-date_joined")
    role_filter = request.GET.get("role", "")
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, "admin_panel/users.html", {"users": users, "current_role": role_filter})


@admin_required
def admin_toggle_user(request, user_id):
    from accounts.models import User

    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.is_active = not user.is_active
        user.save()
        status = "activé" if user.is_active else "désactivé"
        messages.success(request, f"Utilisateur {user.username} {status}.")
    return redirect("core:admin_users")


@admin_required
def admin_products(request):
    products = Product.objects.select_related("seller", "category").order_by("-created_at")
    return render(request, "admin_panel/products.html", {"products": products})


@admin_required
def admin_toggle_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.is_active = not product.is_active
        product.save()
        status = "activé" if product.is_active else "désactivé"
        messages.success(request, f"Produit « {product.name} » {status}.")
    return redirect("core:admin_products")


@admin_required
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"Produit « {name} » supprimé.")
    return redirect("core:admin_products")


@admin_required
def admin_orders(request):
    from orders.models import Order

    orders = Order.objects.select_related("buyer").order_by("-created_at")
    status_filter = request.GET.get("status", "")
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, "admin_panel/orders.html", {"orders": orders, "current_status": status_filter})
