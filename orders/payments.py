"""
Service d'intégration Moneroo — passerelle de paiement Mobile Money.
https://docs.moneroo.io/payments/standard-integration
"""

import hashlib
import hmac
import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

MONEROO_API_URL = getattr(settings, "MONEROO_API_URL", "https://api.moneroo.io/v1")
MONEROO_SECRET_KEY = getattr(settings, "MONEROO_SECRET_KEY", "")


def _headers():
    """En-têtes communs pour l'API Moneroo."""
    return {
        "Authorization": f"Bearer {MONEROO_SECRET_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _is_sandbox_mode():
    """Vérifie si on est en mode sandbox local (clé non configurée)."""
    return (
        not MONEROO_SECRET_KEY
        or MONEROO_SECRET_KEY == "YOUR_MONEROO_SECRET_KEY"
    )


def initialize_payment(order, return_url):
    """
    Initialise un paiement Moneroo et retourne l'URL de checkout.

    En mode sandbox local (clé non configurée), simule le paiement
    en redirigeant directement vers le return_url avec succès.

    Args:
        order: instance Order (avec buyer, total_amount, order_number)
        return_url: URL de retour après paiement

    Returns:
        dict: {"payment_id": str, "checkout_url": str} ou None si erreur
    """
    # ── Mode sandbox local : simuler le paiement ──
    if _is_sandbox_mode():
        import uuid
        fake_id = f"sandbox_{uuid.uuid4().hex[:12]}"
        # Ajouter les query params que Moneroo enverrait
        separator = "&" if "?" in return_url else "?"
        checkout_url = f"{return_url}{separator}paymentId={fake_id}&paymentStatus=success"
        logger.info(
            "[SANDBOX] Paiement simulé pour %s → %s", order.order_number, fake_id
        )
        return {"payment_id": fake_id, "checkout_url": checkout_url}

    # ── Mode production : appel API Moneroo ──
    payload = {
        "amount": int(order.total_amount),  # Moneroo attend un entier
        "currency": getattr(settings, "MONEROO_CURRENCY", "CDF"),
        "description": f"Commande {order.order_number} - UzaMarket",
        "customer": {
            "email": order.buyer.email or f"{order.buyer.username}@uzamarket.cd",
            "first_name": order.buyer.first_name or order.buyer.username,
            "last_name": order.buyer.last_name or "",
        },
        "return_url": return_url,
        "metadata": {
            "order_id": str(order.id),
            "order_number": order.order_number,
        },
    }

    try:
        response = requests.post(
            f"{MONEROO_API_URL}/payments/initialize",
            headers=_headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        payment_id = data["data"]["id"]
        checkout_url = data["data"]["checkout_url"]

        logger.info(
            "Moneroo payment initialized: %s → %s", order.order_number, payment_id
        )
        return {"payment_id": payment_id, "checkout_url": checkout_url}

    except requests.exceptions.RequestException as e:
        logger.error("Moneroo initialize_payment error: %s", e)
        return None
    except (KeyError, TypeError) as e:
        logger.error("Moneroo unexpected response: %s", e)
        return None


def verify_payment(payment_id):
    """
    Vérifie le statut d'un paiement Moneroo.

    Args:
        payment_id: ID du paiement retourné par Moneroo

    Returns:
        dict: {"status": str, "amount": int, "currency": str, ...} ou None
    """
    # Mode sandbox local
    if _is_sandbox_mode() or (payment_id and payment_id.startswith("sandbox_")):
        logger.info("[SANDBOX] Vérification simulée pour %s → success", payment_id)
        return {"status": "success", "id": payment_id}
    try:
        response = requests.get(
            f"{MONEROO_API_URL}/payments/{payment_id}/verify",
            headers=_headers(),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data")

    except requests.exceptions.RequestException as e:
        logger.error("Moneroo verify_payment error: %s", e)
        return None
    except (KeyError, TypeError) as e:
        logger.error("Moneroo verify unexpected response: %s", e)
        return None


def verify_webhook_signature(payload_body, signature_header):
    """
    Vérifie la signature d'un webhook Moneroo (HMAC-SHA256).

    Args:
        payload_body: corps brut de la requête (bytes)
        signature_header: valeur du header X-Moneroo-Signature

    Returns:
        bool: True si la signature est valide
    """
    webhook_secret = getattr(settings, "MONEROO_WEBHOOK_SECRET", "")
    if not webhook_secret:
        logger.warning("MONEROO_WEBHOOK_SECRET non configuré — webhook non vérifié.")
        return True  # En dev, on accepte

    computed = hmac.new(
        webhook_secret.encode("utf-8"),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed, signature_header or "")
