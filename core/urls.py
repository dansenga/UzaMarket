from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # Administration
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/utilisateurs/", views.admin_users, name="admin_users"),
    path("admin-panel/utilisateurs/<int:user_id>/toggle/", views.admin_toggle_user, name="admin_toggle_user"),
    path("admin-panel/produits/", views.admin_products, name="admin_products"),
    path("admin-panel/produits/<int:product_id>/toggle/", views.admin_toggle_product, name="admin_toggle_product"),
    path("admin-panel/produits/<int:product_id>/supprimer/", views.admin_delete_product, name="admin_delete_product"),
    path("admin-panel/commandes/", views.admin_orders, name="admin_orders"),
]
