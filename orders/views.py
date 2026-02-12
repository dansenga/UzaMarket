import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from .payments import initialize_payment, verify_payment, verify_webhook_signature

logger = logging.getLogger(__name__)


@login_required
def checkout(request):
    """Passage de commande — crée la commande puis redirige vers Moneroo si paiement mobile."""
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
            payment_method = form.cleaned_data["payment_method"]

            with transaction.atomic():
                order = Order.objects.create(
                    buyer=request.user,
                    shipping_address=form.cleaned_data["shipping_address"],
                    phone=form.cleaned_data["phone"],
                    payment_method=payment_method,
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

            # ──── Paiement Mobile Money via Moneroo ────
            if payment_method == "mobile_money":
                return_url = request.build_absolute_uri(
                    f"/commandes/paiement/retour/{order.order_number}/"
                )
                result = initialize_payment(order, return_url)

                if result:
                    order.moneroo_payment_id = result["payment_id"]
                    order.moneroo_checkout_url = result["checkout_url"]
                    order.status = Order.Status.AWAITING_PAYMENT
                    order.save()
                    # Rediriger vers la page de paiement Moneroo
                    return redirect(result["checkout_url"])
                else:
                    messages.error(
                        request,
                        "Impossible d'initialiser le paiement. Veuillez réessayer.",
                    )
                    return redirect("orders:detail", order_number=order.order_number)

            # ──── Paiement à la livraison ────
            messages.success(
                request,
                f"Commande {order.order_number} passée avec succès !",
            )
            return redirect("orders:confirmation", order_number=order.order_number)
    else:
        form = CheckoutForm(
            initial={
                "shipping_address": request.user.address,
                "phone": request.user.phone,
            }
        )

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def payment_return(request, order_number):
    """
    Retour depuis Moneroo après paiement.
    Moneroo ajoute ?paymentId=...&paymentStatus=... à l'URL de retour.
    """
    order = get_object_or_404(Order, order_number=order_number, buyer=request.user)

    payment_id = request.GET.get("paymentId", order.moneroo_payment_id)
    payment_status = request.GET.get("paymentStatus", "")

    if payment_id:
        # Toujours re-vérifier côté serveur
        verification = verify_payment(payment_id)
        if verification and verification.get("status") == "success":
            order.is_paid = True
            order.status = Order.Status.CONFIRMED
            order.save()
            messages.success(request, "Paiement reçu ! Votre commande est confirmée.")
            return redirect("orders:confirmation", order_number=order.order_number)

    # Paiement échoué ou en attente
    if payment_status == "failed":
        messages.error(request, "Le paiement a échoué. Vous pouvez réessayer.")
    else:
        messages.info(request, "Paiement en cours de traitement…")

    return redirect("orders:detail", order_number=order.order_number)


@csrf_exempt
@require_POST
def moneroo_webhook(request):
    """
    Webhook Moneroo — reçoit les notifications de paiement.
    Events : payment.success, payment.failed
    """
    # Vérifier la signature
    signature = request.headers.get("X-Moneroo-Signature", "")
    if not verify_webhook_signature(request.body, signature):
        logger.warning("Webhook Moneroo : signature invalide.")
        return JsonResponse({"error": "Invalid signature"}, status=403)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    event = payload.get("event", "")
    data = payload.get("data", {})
    payment_id = data.get("id", "")

    logger.info("Moneroo webhook: event=%s, payment_id=%s", event, payment_id)

    if not payment_id:
        return JsonResponse({"status": "ignored"})

    try:
        order = Order.objects.get(moneroo_payment_id=payment_id)
    except Order.DoesNotExist:
        logger.warning("Webhook Moneroo : commande introuvable pour payment_id=%s", payment_id)
        return JsonResponse({"status": "not_found"})

    if event == "payment.success":
        # Double vérification via l'API
        verification = verify_payment(payment_id)
        if verification and verification.get("status") == "success":
            order.is_paid = True
            order.status = Order.Status.CONFIRMED
            order.save()
            logger.info("Commande %s confirmée via webhook.", order.order_number)

    elif event == "payment.failed":
        logger.info("Paiement échoué pour la commande %s.", order.order_number)

    return JsonResponse({"status": "ok"})


@login_required
def retry_payment(request, order_number):
    """Réinitialiser le paiement Moneroo pour une commande non payée."""
    order = get_object_or_404(Order, order_number=order_number, buyer=request.user)

    if order.is_paid:
        messages.info(request, "Cette commande est déjà payée.")
        return redirect("orders:detail", order_number=order.order_number)

    if order.payment_method != "mobile_money":
        messages.warning(request, "Ce mode de paiement ne supporte pas le paiement en ligne.")
        return redirect("orders:detail", order_number=order.order_number)

    return_url = request.build_absolute_uri(
        f"/commandes/paiement/retour/{order.order_number}/"
    )
    result = initialize_payment(order, return_url)

    if result:
        order.moneroo_payment_id = result["payment_id"]
        order.moneroo_checkout_url = result["checkout_url"]
        order.status = Order.Status.AWAITING_PAYMENT
        order.save()
        return redirect(result["checkout_url"])

    messages.error(request, "Impossible d'initialiser le paiement. Veuillez réessayer.")
    return redirect("orders:detail", order_number=order.order_number)


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
