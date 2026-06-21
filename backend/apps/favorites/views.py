from django.shortcuts import (
    get_object_or_404
)

from rest_framework import (
    generics,
    status
)

from rest_framework.response import (
    Response
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.exceptions import (
    ValidationError
)

from core.permissions.roles import (
    IsCustomer
)

from apps.cooks.models import (
    CookProfile
)
from apps.menus.models import (
    MenuItem
)

from .models import (
    FavoriteCook,
    FavoriteMenuItem
)

from .serializers import (
    FavoriteCookSerializer,
    FavoriteMenuItemSerializer
)

from drf_yasg.utils import swagger_auto_schema

class FavoriteCookCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        FavoriteCookSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary="Add Cook To Favorites"
    )
    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        return super().post(
            request,
            *args,
            **kwargs
        )

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        cook_id = request.data.get(
            "cook"
        )

        if not cook_id:

            raise ValidationError(
                {
                    "cook":
                    "Cook id is required."
                }
            )

        cook = get_object_or_404(
            CookProfile,
            pk=cook_id
        )

        favorite, created = (
            FavoriteCook.objects
            .get_or_create(
                customer=request.user,
                cook=cook
            )
        )

        if not created:

            raise ValidationError(
                "Cook already in favorites."
            )

        serializer = (
            self.get_serializer(
                favorite
            )
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class FavoriteCookDeleteAPIView(
    generics.DestroyAPIView
):

    permission_classes = [
        IsCustomer
    ]

    lookup_url_kwarg = (
        "cook_id"
    )

    def get_object(self):

        return get_object_or_404(
            FavoriteCook,
            customer=
            self.request.user,
            cook_id=
            self.kwargs[
                "cook_id"
            ]
        )
    
    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary="Remove Cook From Favorites"
    )

    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        favorite = (
            self.get_object()
        )

        favorite.delete()

        return Response(
            {
                "detail":
                "Cook removed from favorites."
            },
            status=status.HTTP_200_OK
        )
    
class FavoriteMenuItemCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        FavoriteMenuItemSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary=
        "Add Menu Item To Favorites"
    )
    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        return self.create(
            request,
            *args,
            **kwargs
        )

    def create(
        self,
        request,
        *args,
        **kwargs
    ):

        menu_item_id = (
            request.data.get(
                "menu_item"
            )
        )

        if not menu_item_id:

            raise ValidationError(
                {
                    "menu_item":
                    "Menu item id is required."
                }
            )

        menu_item = (
            get_object_or_404(
                MenuItem,
                pk=menu_item_id,
                is_active=True
            )
        )

        favorite, created = (
            FavoriteMenuItem.objects
            .get_or_create(
                customer=
                request.user,
                menu_item=
                menu_item
            )
        )

        if not created:

            raise ValidationError(
                "Menu item already in favorites."
            )

        serializer = (
            self.get_serializer(
                favorite
            )
        )

        return Response(
            serializer.data,
            status=
            status.HTTP_201_CREATED
        )
    
class FavoriteMenuItemDeleteAPIView(
    generics.DestroyAPIView
):

    permission_classes = [
        IsCustomer
    ]

    lookup_url_kwarg = (
        "menu_item_id"
    )

    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary=
        "Remove Menu Item From Favorites"
    )
    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        favorite = (
            get_object_or_404(
                FavoriteMenuItem,
                customer=
                request.user,
                menu_item_id=
                kwargs[
                    "menu_item_id"
                ]
            )
        )

        favorite.delete()

        return Response(
            {
                "detail":
                (
                    "Menu item removed "
                    "from favorites."
                )
            },
            status=
            status.HTTP_200_OK
        )
    

class FavoriteCookListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        FavoriteCookSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary=
        "My Favorite Cooks"
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

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                FavoriteCook.objects
                .none()
            )

        return (
            FavoriteCook.objects
            .filter(
                customer=
                self.request.user
            )
            .select_related(
                "cook",
                "cook__user"
            )
            .order_by(
                "-created_at"
            )
        )
    
class FavoriteMenuItemListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        FavoriteMenuItemSerializer
    )

    permission_classes = [
        IsCustomer
    ]

    @swagger_auto_schema(
        tags=["Favorites"],
        operation_summary=
        "My Favorite Menu Items"
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

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                FavoriteMenuItem.objects
                .none()
            )

        return (
            FavoriteMenuItem.objects
            .filter(
                customer=
                self.request.user
            )
            .select_related(
                "menu_item"
            )
            .order_by(
                "-created_at"
            )
        )