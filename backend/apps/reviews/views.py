from rest_framework import generics

from .models import Review, Comment

from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer,
    CommentCreateSerializer,
    CommentSerializer
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
    
class CommentCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        CommentCreateSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            customer=
            self.request.user
        )

class CookCommentListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CommentSerializer
    )

    permission_classes = []

    def get_queryset(
        self
    ):

        return (
            Comment.objects
            .filter(
                cook_id=
                self.kwargs[
                    "cook_id"
                ],
                is_active=True
            )
            .select_related(
                "customer"
            )
        )
    
class MenuCommentListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CommentSerializer
    )

    permission_classes = []

    def get_queryset(
        self
    ):

        return (
            Comment.objects
            .filter(
                menu_id=
                self.kwargs[
                    "menu_id"
                ],
                is_active=True
            )
            .select_related(
                "customer"
            )
        )
    
class MenuItemCommentListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CommentSerializer
    )

    permission_classes = []

    def get_queryset(
        self
    ):

        return (
            Comment.objects
            .filter(
                menu_item_id=
                self.kwargs[
                    "menu_item_id"
                ],
                is_active=True
            )
            .select_related(
                "customer"
            )
        )
