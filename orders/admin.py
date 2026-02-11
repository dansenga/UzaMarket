from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "seller", "product_name", "product_price", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "buyer", "status", "total_amount", "is_paid", "created_at"]
    list_filter = ["status", "is_paid", "created_at"]
    search_fields = ["order_number", "buyer__username"]
    readonly_fields = ["order_number", "total_amount"]
    inlines = [OrderItemInline]
