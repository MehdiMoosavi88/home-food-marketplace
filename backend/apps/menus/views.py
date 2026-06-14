from rest_framework import generics

from drf_yasg.utils import (
    swagger_auto_schema
)

from .models import (
    Menu,
    MenuItem,
    MenuItemAvailability
)

from .serializers import (
    MenuSerializer,
    MenuItemSerializer,
    MenuItemAvailabilitySerializer
)

from apps.cooks.permissions import (
    IsCook
)

from .permissions import IsMenuOwner

from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)

class MyMenuAPIView(
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
    
class MenuItemCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    permission_classes = [
        IsCook
    ]

    @swagger_auto_schema(
        tags=["Menu Items"],
        operation_summary="Create Menu Item"
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

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            menu=
            self.request.user
            .cook_profile
            .menu
        )

class MenuItemListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        IsCook
    ]

    @swagger_auto_schema(
        tags=["Menu Items"]
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
                MenuItem.objects
                .none()
            )

        return (
            MenuItem.objects
            .filter(
                menu=
                self.request.user
                .cook_profile
                .menu
            )
            .order_by("name")
        )
    
class MenuItemDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        IsCook,
        IsMenuOwner
    ]

    queryset = (
        MenuItem.objects.all()
    )

    @swagger_auto_schema(
        tags=["Menu Items"]
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
        tags=["Menu Items"]
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

    @swagger_auto_schema(
        tags=["Menu Items"]
    )
    def delete(
        self,
        request,
        *args,
        **kwargs
    ):
        return super().delete(
            request,
            *args,
            **kwargs
        )
    
class MenuItemUpdateAPIView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        IsCook
    ]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @swagger_auto_schema(
        operation_summary=
        "Update Menu Item"
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

    def get_queryset(self):

        cook_profile = (
            self.request.user
            .cook_profile
        )

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItem
                .objects
                .none()
            )

        return MenuItem.objects.filter(
            menu=cook_profile.menu
        )
    
class MenuItemDeleteAPIView(
    generics.DestroyAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        cook_profile = (
            self.request.user
            .cook_profile
        )

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItem
                .objects
                .none()
            )

        return MenuItem.objects.filter(
            menu=cook_profile.menu
        )
    
class AvailabilityCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        MenuItemAvailabilitySerializer
    )

    permission_classes = [
        IsCook
    ]

    def perform_create(
        self,
        serializer
    ):

        menu_item = serializer.validated_data[
            "menu_item"
        ]

        if (
            menu_item.menu.cook.user
            != self.request.user
        ):
            raise PermissionDenied(
                "Not your menu item."
            )

        serializer.save()

class AvailabilityListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MenuItemAvailabilitySerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        cook_profile = (
            self.request.user
            .cook_profile
        )

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItemAvailability
                .objects
                .none()
            )

        return (
            MenuItemAvailability
            .objects
            .filter(
                menu_item__menu__cook=
                cook_profile
            )
            .order_by(
                "date"
            )
        )
    
class AvailabilityUpdateAPIView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        MenuItemAvailabilitySerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        cook_profile = (
            self.request.user
            .cook_profile
        )

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItemAvailability
                .objects
                .none()
            )

        return (
            MenuItemAvailability
            .objects
            .filter(
                menu_item__menu__cook=
                cook_profile
            )
        )
    
    def perform_update(
            self,
            serializer
        ):
        serializer.is_valid(
        raise_exception=True
    )
        serializer.save()
    
class AvailabilityDeleteAPIView(
    generics.DestroyAPIView
):

    serializer_class = (
        MenuItemAvailabilitySerializer
    )

    permission_classes = [
        IsCook
    ]

    def get_queryset(self):

        cook_profile = (
            self.request.user
            .cook_profile
        )

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItemAvailability
                .objects
                .none()
            )

        return (
            MenuItemAvailability
            .objects
            .filter(
                menu_item__menu__cook=
                cook_profile
            )
        )