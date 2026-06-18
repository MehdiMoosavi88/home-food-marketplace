from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status

from rest_framework.response import Response

from rest_framework.exceptions import (
    ValidationError
)

from rest_framework import generics

from django.shortcuts import (
    get_object_or_404
)

from .models import (
    Reservation,
    ReservationItem
)

from .serializers import (
    ReservationCreateSerializer,
    ReservationSerializer,
    CookReservationSerializer
)

from apps.menus.models import (
    MenuItemAvailability
)

from core.permissions.roles import (
    IsCustomer,
    IsCook,
    IsAdmin
)

from drf_yasg.utils import (
    swagger_auto_schema
)

from drf_yasg import openapi

class ReservationCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        ReservationCreateSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        serializer = (
            self.get_serializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        reservation = (
            self.perform_create(
                serializer
            )
        )

        response_serializer = (
            ReservationSerializer(
                reservation
            )
        )

        return Response(
            response_serializer.data,
            status=201
        )

    @transaction.atomic
    def perform_create(
        self,
        serializer
    ):

        reservation = (
            Reservation.objects.create(
                customer=
                self.request.user
            )
        )

        total_price = 0

        for item_data in serializer.validated_data[
            "items"
        ]:

            availability = (
                MenuItemAvailability.objects
                .select_for_update()
                .get(
                    menu_item_id=
                    item_data[
                        "menu_item"
                    ],
                    date=
                    item_data[
                        "date"
                    ]
                )
            )

            quantity = (
                item_data[
                    "quantity"
                ]
            )

            remaining = (
                availability.max_quantity
                -
                availability.reserved_quantity
            )

            if quantity > remaining:

                raise ValidationError(
                    "Not enough capacity."
                )

            menu_item = (
                availability.menu_item
            )

            if (
        menu_item.menu.cook.user
        == self.request.user
        ):
                raise ValidationError(
        "You cannot reserve your own food."
        )

            ReservationItem.objects.create(
                reservation=
                reservation,

                menu_item=
                menu_item,

                date=
                item_data["date"],

                quantity=
                quantity,

                unit_price=
                menu_item.price
            )

            availability.reserved_quantity += (
                quantity
            )

            availability.save()

            total_price += (
                menu_item.price *
                quantity
            )

        reservation.total_price = (
            total_price
        )

        reservation.save()

        return reservation
    
class MyReservationListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        ReservationSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Reservation.objects
                .none()
            )

        return (
            Reservation.objects
            .filter(
                customer=
                self.request.user
            )
            .prefetch_related(
                "items",
                "items__menu_item"
            )
            .order_by(
                "-created_at"
            )
        )
    
class ReservationDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        ReservationSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Reservation.objects
                .none()
            )

        return (
            Reservation.objects
            .filter(
                customer=
                self.request.user
            )
            .prefetch_related(
                "items",
                "items__menu_item"
            )
        )
    
class ReservationCancelAPIView(
    APIView
):
    
    permission_classes = [
        IsCustomer
    ]

    @transaction.atomic
    def patch(
        self,
        request,
        pk
    ):

        reservation = (
            get_object_or_404(
                Reservation.objects
                .prefetch_related(
                    "items"
                ),
                pk=pk,
                customer=request.user
            )
        )

        if (
            reservation.status
            != Reservation.Status.PENDING
        ):
            raise ValidationError(
                "Only pending reservations can be cancelled."
            )

        for item in (
            reservation.items.all()
        ):

            availability = (
                MenuItemAvailability.objects
                .select_for_update()
                .get(
                    menu_item=item.menu_item,
                    date=item.date
                )
            )

            availability.reserved_quantity -= (
                item.quantity
            )

            availability.save(
                update_fields=[
                    "reserved_quantity"
                ]
            )

        reservation.status = (
            Reservation.Status.CANCELLED
        )

        reservation.save(
            update_fields=[
                "status"
            ]
        )

        return Response(
            {
                "detail":
                "Reservation cancelled successfully."
            },
            status=status.HTTP_200_OK
        )
    
class CookReservationListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CookReservationSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
            Reservation.objects
            .none()
        )

        cook_profile = (
        self.request.user
        .cook_profile
        )

        queryset = (
        Reservation.objects
        .filter(
            items__menu_item__menu__cook=
            cook_profile
        )
        .prefetch_related(
            "items",
            "items__menu_item"
        )
        .distinct()
        .order_by(
            "-created_at"
        )
    )

        status = (
        self.request.query_params.get(
            "status"
        )
    )

        if status:

            valid_statuses = [
            choice[0]
            for choice in
            Reservation.Status.choices
        ]

            if status not in valid_statuses:

                raise ValidationError(
                {
                    "status":
                    (
                        "Invalid status. "
                        f"Allowed values: "
                        f"{', '.join(valid_statuses)}"
                    )
                }
            )

            queryset = queryset.filter(
            status=status
        )

        return queryset
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
            "status",
            openapi.IN_QUERY,
            description=(
                "Filter by reservation status"
            ),
            type=openapi.TYPE_STRING,
            enum=[
                "pending",
                "confirmed",
                "completed",
                "cancelled",
            ]
        )
    ],
    tags=["Cook Reservations"]
)
    def get(
    self,
    request,
    *args,
    **kwargs
):
        return super().get(
        request,
        *args,
        **kwargs
    )
    
class CookReservationDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        ReservationSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Reservation.objects
                .none()
            )

        cook_profile = (
            self.request.user
            .cook_profile
        )

        return (
            Reservation.objects
            .filter(
                items__menu_item__menu__cook=
                cook_profile
            )
            .prefetch_related(
        "items",
        "items__menu_item"
    )
            .distinct()
        )
    
class ReservationConfirmAPIView(
    generics.UpdateAPIView
):

    serializer_class = (
        ReservationSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Reservation.objects
                .none()
            )

        cook_profile = (
            self.request.user
            .cook_profile
        )

        return (
            Reservation.objects
            .filter(
                items__menu_item__menu__cook=
                cook_profile,
                status=
                Reservation.Status.PENDING
            )
            .distinct()
        )

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        reservation = (
            self.get_object()
        )

        reservation.status = (
            Reservation.Status.CONFIRMED
        )

        reservation.save(
            update_fields=[
                "status"
            ]
        )

        return Response(
            ReservationSerializer(
                reservation
            ).data
        )
    
class ReservationCompleteAPIView(
    generics.UpdateAPIView
):

    serializer_class = (
        ReservationSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Reservation.objects
                .none()
            )

        cook_profile = (
            self.request.user
            .cook_profile
        )

        return (
            Reservation.objects
            .filter(
                items__menu_item__menu__cook=
                cook_profile,
                status=
                Reservation.Status.CONFIRMED
            )
            .distinct()
        )

    def patch(
        self,
        request,
        *args,
        **kwargs
    ):

        reservation = (
            self.get_object()
        )

        reservation.status = (
            Reservation.Status.COMPLETED
        )

        reservation.save(
            update_fields=[
                "status"
            ]
        )

        return Response(
            ReservationSerializer(
                reservation
            ).data
        )