from django.urls import path

from .views import (
    MyMenuAPIView,
    MenuItemCreateAPIView,
    MenuItemListAPIView,
    MenuItemDetailAPIView,
    MenuItemUpdateAPIView,
    MenuItemDeleteAPIView,
    AvailabilityCreateAPIView,
    AvailabilityListAPIView,
    AvailabilityUpdateAPIView,
    AvailabilityDeleteAPIView,
    PublicMenuAPIView,
    PublicMenuItemListAPIView,
    PublicMenuItemDetailAPIView

)

urlpatterns = [

    path(
        "my-menu/",
        MyMenuAPIView.as_view(),
        name="my-menu"
    ),

    path(
        "items/",
        MenuItemListAPIView.as_view(),
        name="menu-item-list"
    ),

    path(
        "items/create/",
        MenuItemCreateAPIView.as_view(),
        name="menu-item-create"
    ),

    path(
        "items/<uuid:pk>/",
        MenuItemDetailAPIView.as_view(),
        name="menu-item-update"
    ),

    path(
        "items/<uuid:pk>/delete/",
        MenuItemDeleteAPIView.as_view(),
        name="menu-item-delete"
    ),

    path(
    "availabilities/",
    AvailabilityListAPIView.as_view(),
    name="availability-list"
    ),
    
    path(
    "availabilities/create/",
    AvailabilityCreateAPIView.as_view(),
    name="availability-create"
    ),
    
    path(
    "availabilities/<uuid:pk>/",
    AvailabilityUpdateAPIView.as_view(),
    name="availability-update"
    ),
    
    path(
    "availabilities/<uuid:pk>/delete/",
    AvailabilityDeleteAPIView.as_view(),
    name="availability-delete"
    ),

    path(
    "public/cooks/<uuid:cook_id>/menu/",
    PublicMenuAPIView.as_view(),
    name="public-menu"
    ),
    
    path(
    "public/cooks/<uuid:cook_id>/menu/items/",
    PublicMenuItemListAPIView.as_view(),
    name="public-menu-items"
    ),
    
    path(
    "public/menu-items/<uuid:pk>/",
    PublicMenuItemDetailAPIView.as_view(),
    name="public-menu-item-detail"
    ),
]