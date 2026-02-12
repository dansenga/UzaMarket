from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "seller", "product_name", "product_price", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "buyer", "status", "payment_method", "total_amount", "is_paid", "created_at"]
    list_filter = ["status", "is_paid", "payment_method", "created_at"]
    search_fields = ["order_number", "buyer__username", "moneroo_payment_id"]
    readonly_fields = ["order_number", "total_amount", "moneroo_payment_id", "moneroo_checkout_url"]
    inlines = [OrderItemInline]
    fieldsets = (
        ("Commande", {"fields": ("order_number", "buyer", "status", "total_amount")}),
        ("Livraison", {"fields": ("shipping_address", "phone", "notes")}),
        ("Paiement", {"fields": ("payment_method", "mobile_number", "is_paid", "moneroo_payment_id", "moneroo_checkout_url")}),
    )
