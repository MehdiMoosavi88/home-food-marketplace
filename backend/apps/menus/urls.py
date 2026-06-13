from django.urls import path

from .views import (
    MyMenuAPIView,
    MenuItemCreateAPIView,
    MenuItemListAPIView,
    MenuItemDetailAPIView,
    MenuItemUpdateAPIView,
    MenuItemDeleteAPIView,
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
]