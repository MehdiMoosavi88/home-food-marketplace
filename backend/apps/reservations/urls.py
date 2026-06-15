from django.urls import path

from .views import (
    ReservationCreateAPIView,
    MyReservationListAPIView,
    ReservationDetailAPIView,
    ReservationCancelAPIView,
    CookReservationListAPIView,
    CookReservationDetailAPIView,
    ReservationConfirmAPIView,
    ReservationCompleteAPIView
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

    path(
    "cook/reservations/",
    CookReservationListAPIView.as_view(),
    name="cook-reservation-list"
    ),

    path(
    "cook/reservations/<uuid:pk>/",
    CookReservationDetailAPIView.as_view(),
    name="cook-reservation-detail"
    ),

    path(
    "cook/reservations/<uuid:pk>/confirm/",
    ReservationConfirmAPIView.as_view(),
    name="reservation-confirm"
    ),

    path(
    "cook/reservations/<uuid:pk>/complete/",
    ReservationCompleteAPIView.as_view(),
    name="reservation-complete"
    ),
]