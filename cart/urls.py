from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="view"),
    path("ajouter/<int:product_id>/", views.add_to_cart, name="add"),
    path("modifier/<int:item_id>/", views.update_cart_item, name="update"),
    path("supprimer/<int:item_id>/", views.remove_from_cart, name="remove"),
]
