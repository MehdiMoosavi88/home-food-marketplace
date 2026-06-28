from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CookProfile

from .serializers import (
    CookProfileSerializer
)

from .permissions import (
    IsCook
)

from drf_yasg.utils import (
    swagger_auto_schema
)

from drf_yasg import openapi

from django.db.models import (
    Avg,
    Count
)

from django_filters.rest_framework import (
    DjangoFilterBackend
)

from rest_framework.filters import (
    SearchFilter,
)

from core.filters import (
    CookProfileFilter,
    CookOrderingFilter
)

class CookMeAPIView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        CookProfileSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_object(self):
        return self.request.user.cook_profile

    @swagger_auto_schema(
        tags=["Cook Profile"]
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

    @swagger_auto_schema(
        tags=["Cook Profile"]
    )
    def patch(
        self,
        request,
        *args,
        **kwargs
    ):
        return super().patch(
            request,
            *args,
            **kwargs
        )
    
class PublicCookListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        CookProfileSerializer
    )

    permission_classes = [
        AllowAny
    ]

    queryset = (
    CookProfile.objects
    .select_related("user")
    .order_by(
        "user__username"
    )
    )

    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    CookOrderingFilter,
    ]

    filterset_class = (
        CookProfileFilter
    )

    search_fields = [
        "user__username",
        "city",
        "bio",
    ]

    ordering_fields = [
    "favorites_count",
    "average_rating",
    "reviews_count",
    "created_at",
    ]

    ordering = [
    "-favorites_count",
    "-average_rating",
    "-reviews_count",
    "created_at",
    ]

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                CookProfile.objects.none()
            )

        queryset = (
            CookProfile.objects
            .select_related("user")
        )

        popular = (
            self.request.query_params.get(
                "popular"
            )
        )

        ordering = (
            self.request.query_params.get(
                "ordering"
            )
        )

        if (
            popular == "true"
            and
            not ordering
        ):

            queryset = queryset.order_by(
                "-favorites_count",
                "-average_rating",
                "-reviews_count",
            )

        return queryset

    @swagger_auto_schema(
    manual_parameters=[

        openapi.Parameter(
            "city",
            openapi.IN_QUERY,
            description=
            "Filter by city",
            type=
            openapi.TYPE_STRING
        ),

        openapi.Parameter(
            "min_rating",
            openapi.IN_QUERY,
            description=
            "Minimum rating",
            type=
            openapi.TYPE_NUMBER
        ),

        openapi.Parameter(
    "popular",
    openapi.IN_QUERY,
    description=(
        "Return cooks ordered by popularity "
        "(favorites, rating and reviews). "
        "Accepted value: true"
    ),
    type=openapi.TYPE_BOOLEAN,
    ),
    ],
    tags=["Public Cooks"]
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