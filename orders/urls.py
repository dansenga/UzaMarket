from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<str:order_number>/", views.order_confirmation, name="confirmation"),
    path("historique/", views.order_history, name="history"),
    # Moneroo payment
    path("paiement/retour/<str:order_number>/", views.payment_return, name="payment_return"),
    path("paiement/reessayer/<str:order_number>/", views.retry_payment, name="retry_payment"),
    path("webhook/moneroo/", views.moneroo_webhook, name="moneroo_webhook"),
    # Detail (doit rester en dernier car capture <str>)
    path("<str:order_number>/", views.order_detail, name="detail"),
]
