from rest_framework import generics

from drf_yasg.utils import (
    swagger_auto_schema
)

from drf_yasg import openapi

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

from apps.cooks.models import (
    CookProfile
)

from .permissions import IsMenuOwner

from rest_framework.permissions import AllowAny

from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)

from django_filters.rest_framework import (
    DjangoFilterBackend
)

from rest_framework.filters import (
    SearchFilter,
)

from core.filters import (
    MenuItemOrderingFilter,
    MenuItemFilter
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

        cook_profile = (
            self.request.user
            .cook_profile
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

        cook_profile = (
            self.request.user
            .cook_profile
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

        cook_profile = (
            self.request.user
            .cook_profile
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

        cook_profile = (
            self.request.user
            .cook_profile
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

        cook_profile = (
            self.request.user
            .cook_profile
        )

        return (
            MenuItemAvailability
            .objects
            .filter(
                menu_item__menu__cook=
                cook_profile
            )
        )
    
class PublicMenuAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        MenuSerializer
    )

    permission_classes = [AllowAny]

    lookup_url_kwarg = (
        "cook_id"
    )

    def get_object(self):

        cook = (
            CookProfile.objects
            .select_related("menu")
            .get(
                pk=self.kwargs[
                    "cook_id"
                ]
            )
        )

        return cook.menu
    
class PublicMenuItemListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        AllowAny
    ]

    @swagger_auto_schema(
    tags=["Public Menu"],
    operation_summary=
    "Search Menu Items"
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

    filter_backends = [
        SearchFilter
    ]

    search_fields = [
        "name",
        "description",
        "menu__title",
        "menu__cook__user__username",
    ]

    def get_queryset(self):

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
            .select_related(
                "menu",
                "menu__cook",
                "menu__cook__user",
            )
            .filter(
                is_active=True,
                menu__is_active=True,
            )
            .order_by(
                "name"
            )
        )
    
class PublicMenuItemDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [AllowAny]

    queryset = (
        MenuItem.objects
        .filter(
            is_active=True,
            menu__is_active=True
        )
    )

class PublicMenuItemSearchAPIView(
    generics.ListAPIView
):

    serializer_class = (
        MenuItemSerializer
    )

    permission_classes = [
        AllowAny
    ]

    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    MenuItemOrderingFilter,
    ]

    filterset_class = (
    MenuItemFilter
    )

    search_fields = [
        "name",
        "description",
        "menu__title",
        "menu__cook__user__username",
    ]

    ordering_fields = [

    "price",

    "created_at",

    "favorites_count",

    "orders_count",

    "average_rating",

    "name",
    ]

    ordering = [
    "name"
    ]

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            "min_price",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Minimum price"
        ),
        openapi.Parameter(
            "max_price",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Maximum price"
        ),
    ],
    tags=["Public Menu"]
)

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                MenuItem.objects.none()
            )

        return (
            MenuItem.objects
            .select_related(
                "menu",
                "menu__cook",
                "menu__cook__user",
            )
            .filter(
                is_active=True,
                menu__is_active=True,
            )
            .order_by(
                "name"
            )
        )