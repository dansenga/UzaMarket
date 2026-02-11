from django.urls import path
from . import views

app_name = "seller"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("produits/", views.product_list, name="products"),
    path("produits/ajouter/", views.product_create, name="product_create"),
    path("produits/<int:pk>/modifier/", views.product_edit, name="product_edit"),
    path("produits/<int:pk>/supprimer/", views.product_delete, name="product_delete"),
    path("commandes/", views.order_list, name="orders"),
    path("commandes/<str:order_number>/", views.order_detail, name="order_detail"),
    path("commandes/<str:order_number>/statut/", views.order_update_status, name="order_update_status"),
]
