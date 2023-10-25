from django.urls import path
from . import views


urlpatterns = [
    # order URLs
    path("checkout", views.checkout, name="checkout"),
    path("complete-order", views.complete_order, name="complete-order"),
    # payment URLs
    path("payment-success", views.payment_success, name="payment-success"),
    path("payment-failed", views.payment_failed, name="payment-failed"),
    # liqpay
]
