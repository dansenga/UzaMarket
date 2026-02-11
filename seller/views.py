from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F
from accounts.decorators import seller_required
from products.models import Product
from orders.models import Order, OrderItem
from .forms import ProductForm


@seller_required
def dashboard(request):
    """Tableau de bord vendeur."""
    products = Product.objects.filter(seller=request.user)
    total_products = products.count()
    active_products = products.filter(is_active=True).count()

    # Commandes reçues par le vendeur
    order_items = OrderItem.objects.filter(seller=request.user)
    total_sales = order_items.aggregate(
        total=Sum(F("product_price") * F("quantity"))
    )["total"] or 0
    total_orders = order_items.values("order").distinct().count()

    recent_orders = (
        Order.objects.filter(items__seller=request.user)
        .distinct()
        .order_by("-created_at")[:5]
    )

    context = {
        "total_products": total_products,
        "active_products": active_products,
        "total_sales": total_sales,
        "total_orders": total_orders,
        "recent_orders": recent_orders,
        "products": products[:5],
    }
    return render(request, "seller/dashboard.html", context)


@seller_required
def product_list(request):
    """Liste des produits du vendeur."""
    products = Product.objects.filter(seller=request.user)
    return render(request, "seller/product_list.html", {"products": products})


@seller_required
def product_create(request):
    """Ajouter un produit."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"Produit « {product.name} » créé avec succès !")
            return redirect("seller:products")
    else:
        form = ProductForm()
    return render(request, "seller/product_form.html", {"form": form, "title": "Ajouter un produit"})


@seller_required
def product_edit(request, pk):
    """Modifier un produit."""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produit « {product.name} » mis à jour.")
            return redirect("seller:products")
    else:
        form = ProductForm(instance=product)
    return render(request, "seller/product_form.html", {"form": form, "title": "Modifier le produit", "product": product})


@seller_required
def product_delete(request, pk):
    """Supprimer un produit."""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"Produit « {name} » supprimé.")
        return redirect("seller:products")
    return render(request, "seller/product_confirm_delete.html", {"product": product})


@seller_required
def order_list(request):
    """Commandes reçues par le vendeur."""
    orders = (
        Order.objects.filter(items__seller=request.user)
        .distinct()
        .order_by("-created_at")
    )
    return render(request, "seller/order_list.html", {"orders": orders})


@seller_required
def order_detail(request, order_number):
    """Détail d'une commande reçue."""
    order = get_object_or_404(Order, order_number=order_number)
    # Vérifier que le vendeur a des articles dans cette commande
    seller_items = order.items.filter(seller=request.user)
    if not seller_items.exists():
        messages.error(request, "Vous n'avez pas accès à cette commande.")
        return redirect("seller:orders")
    return render(request, "seller/order_detail.html", {"order": order, "seller_items": seller_items})


@seller_required
def order_update_status(request, order_number):
    """Mettre à jour le statut d'une commande."""
    order = get_object_or_404(Order, order_number=order_number)
    if not order.items.filter(seller=request.user).exists():
        messages.error(request, "Vous n'avez pas accès à cette commande.")
        return redirect("seller:orders")

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()
            messages.success(request, f"Statut de la commande mis à jour : {order.get_status_display()}")
        else:
            messages.error(request, "Statut invalide.")

    return redirect("seller:order_detail", order_number=order_number)
