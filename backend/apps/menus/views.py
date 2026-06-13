from rest_framework import generics

from drf_yasg.utils import (
    swagger_auto_schema
)

from .models import Menu

from .serializers import (
    MenuSerializer
)

from apps.cooks.permissions import (
    IsCook
)

class CookMenuAPIView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        MenuSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_object(self):

        return (
            self.request.user
            .cook_profile
            .menu
        )

    @swagger_auto_schema(
        tags=["Cook Menu"]
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
        tags=["Cook Menu"]
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