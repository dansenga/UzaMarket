from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem


def _get_cart(request):
    """Récupère ou crée le panier de l'utilisateur/session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Fusionner panier de session si existant
        session_key = request.session.session_key
        if session_key:
            try:
                session_cart = Cart.objects.get(session_key=session_key, user=None)
                for item in session_cart.items.all():
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart, product=item.product,
                        defaults={"quantity": item.quantity},
                    )
                    if not created:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart


def cart_view(request):
    """Affiche le panier."""
    cart = _get_cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


@require_POST
def add_to_cart(request, product_id):
    """Ajoute un produit au panier."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > product.quantity:
        messages.error(request, "Quantité demandée non disponible.")
        return redirect("products:detail", slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={"quantity": quantity},
    )
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.quantity:
            cart_item.quantity = product.quantity
        cart_item.save()

    messages.success(request, f"« {product.name} » ajouté au panier.")

    if request.headers.get("HX-Request"):
        return render(request, "cart/includes/cart_badge.html", {"cart": cart})

    return redirect("cart:view")


@require_POST
def update_cart_item(request, item_id):
    """Met à jour la quantité d'un article."""
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get("quantity", 1))

    if quantity < 1:
        item.delete()
        messages.info(request, "Article supprimé du panier.")
    elif quantity > item.product.quantity:
        messages.error(request, "Quantité non disponible.")
    else:
        item.quantity = quantity
        item.save()

    if request.headers.get("HX-Request"):
        return render(request, "cart/cart.html", {"cart": cart})

    return redirect("cart:view")


@require_POST
def remove_from_cart(request, item_id):
    """Supprime un article du panier."""
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.product.name
    item.delete()
    messages.info(request, f"« {product_name} » retiré du panier.")

    if request.headers.get("HX-Request"):
        return render(request, "cart/cart.html", {"cart": cart})

    return redirect("cart:view")
