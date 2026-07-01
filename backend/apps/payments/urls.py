from django.urls import path

from .views import (
    StartPaymentAPIView,
    VerifyPaymentAPIView,
    PaymentHistoryAPIView
)

urlpatterns = [

    path(
        "start/<uuid:reservation_id>/",
        StartPaymentAPIView.as_view(),
        name="payment-start",
    ),

    path(
        "verify/<uuid:authority>/",
        VerifyPaymentAPIView.as_view(),
        name="payment-verify",
    ),

     path(
        "",
        PaymentHistoryAPIView.as_view(),
        name="payment-history",
    ),

]