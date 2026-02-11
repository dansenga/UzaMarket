from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """Passage de commande (authentification obligatoire)."""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, "Votre panier est vide.")
        return redirect("cart:view")

    if not cart.items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect("cart:view")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    buyer=request.user,
                    shipping_address=form.cleaned_data["shipping_address"],
                    phone=form.cleaned_data["phone"],
                    payment_method=form.cleaned_data["payment_method"],
                    mobile_number=form.cleaned_data.get("mobile_number", ""),
                    notes=form.cleaned_data.get("notes", ""),
                    total_amount=cart.total,
                )

                for cart_item in cart.items.select_related("product"):
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        seller=cart_item.product.seller,
                        product_name=cart_item.product.name,
                        product_price=cart_item.product.price,
                        quantity=cart_item.quantity,
                    )
                    # Décrémenter le stock
                    cart_item.product.quantity -= cart_item.quantity
                    cart_item.product.save()

                # Vider le panier
                cart.items.all().delete()

            messages.success(request, f"Commande {order.order_number} passée avec succès !")
            return redirect("orders:confirmation", order_number=order.order_number)
    else:
        form = CheckoutForm(initial={
            "shipping_address": request.user.address,
            "phone": request.user.phone,
        })

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def order_confirmation(request, order_number):
    """Page de confirmation de commande."""
    order = get_object_or_404(Order, order_number=order_number, buyer=request.user)
    return render(request, "orders/confirmation.html", {"order": order})


@login_required
def order_history(request):
    """Historique des commandes du client."""
    orders = Order.objects.filter(buyer=request.user)
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    """Détail d'une commande."""
    order = get_object_or_404(Order, order_number=order_number, buyer=request.user)
    return render(request, "orders/detail.html", {"order": order})
