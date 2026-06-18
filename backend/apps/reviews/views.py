from rest_framework import generics

from .models import Review

from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer
)

from core.permissions.roles import (
    IsCustomer
)

class ReviewCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        ReviewCreateSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    def perform_create(
        self,
        serializer
    ):

        reservation = (
            serializer.validated_data[
                "reservation_obj"
            ]
        )

        first_item = (
            reservation.items
            .select_related(
                "menu_item__menu__cook"
            )
            .first()
        )

        cook = (
            first_item
            .menu_item
            .menu
            .cook
        )

        Review.objects.create(
            customer=
            self.request.user,

            reservation=
            reservation,

            cook=cook,

            rating=
            serializer.validated_data[
                "rating"
            ],

            comment=
            serializer.validated_data.get(
                "comment",
                ""
            )
        )
