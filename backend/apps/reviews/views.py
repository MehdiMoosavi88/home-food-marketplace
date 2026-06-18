from rest_framework import generics

from .models import Review

from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer
)

from core.permissions.roles import (
    IsCustomer
)

from rest_framework.permissions import (
    AllowAny
)

from drf_yasg.utils import (
    swagger_auto_schema
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

class MyReviewListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        ReviewSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    @swagger_auto_schema(
        tags=["Reviews"]
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

    def get_queryset(
        self
    ):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Review.objects
                .none()
            )

        return (
            Review.objects
            .filter(
                customer=
                self.request.user
            )
            .select_related(
                "cook",
                "reservation"
            )
            .order_by(
                "-created_at"
            )
        )
    
class PublicCookReviewListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        ReviewSerializer
    )

    permission_classes = [AllowAny]

    @swagger_auto_schema(
    tags=["Public Reviews"]
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

    def get_queryset(
        self
    ):

        cook_id = (
            self.kwargs[
                "cook_id"
            ]
        )

        return (
            Review.objects
            .filter(
                cook_id=cook_id
            )
            .select_related(
                "customer"
            )
            .order_by(
                "-created_at"
            )
        )
