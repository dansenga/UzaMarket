import uuid
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """Commande passée par un client."""

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CONFIRMED = "confirmed", "Confirmée"
        PROCESSING = "processing", "En préparation"
        SHIPPED = "shipped", "Expédiée"
        DELIVERED = "delivered", "Livrée"
        CANCELLED = "cancelled", "Annulée"

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Acheteur",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Statut",
    )
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mobile_number = models.CharField(max_length=25, blank=True, verbose_name="Numéro Mobile Money")
    is_paid = models.BooleanField(default=False, verbose_name="Payée")
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="Méthode de paiement")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"UZA-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.order_number}"

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """Article d'une commande."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sold_items",
        verbose_name="Vendeur",
    )
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
