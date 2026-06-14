from django.urls import path

from .views import (
    ReservationCreateAPIView,
    MyReservationListAPIView,
    ReservationDetailAPIView,
    ReservationCancelAPIView,
)

urlpatterns = [

    path(
        "create/",
        ReservationCreateAPIView.as_view(),
        name="reservation-create"
    ),
    path(
    "my/",
    MyReservationListAPIView.as_view(),
    name="my-reservations"
    ),

    path(
    "<uuid:pk>/",
    ReservationDetailAPIView.as_view(),
    name="reservation-detail"
    ),

    path(
    "<uuid:pk>/cancel/",
    ReservationCancelAPIView.as_view(),
    name="reservation-cancel"
),
]