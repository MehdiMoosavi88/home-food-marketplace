from django.urls import path

from .views import (
    FavoriteCookCreateAPIView,
    FavoriteCookDeleteAPIView,
    FavoriteCookListAPIView,

    FavoriteMenuItemCreateAPIView,
    FavoriteMenuItemDeleteAPIView,
    FavoriteMenuItemListAPIView,
)

urlpatterns = [

    # Cook Favorites

    path(
        "cooks/",
        FavoriteCookListAPIView.as_view(),
        name="favorite-cook-list"
    ),

    path(
        "cooks/add/",
        FavoriteCookCreateAPIView.as_view(),
        name="favorite-cook-create"
    ),

    path(
        "cooks/<uuid:cook_id>/",
        FavoriteCookDeleteAPIView.as_view(),
        name="favorite-cook-delete"
    ),

    # Menu Item Favorites

    path(
        "menu-items/",
        FavoriteMenuItemListAPIView.as_view(),
        name="favorite-menu-item-list"
    ),

    path(
        "menu-items/add/",
        FavoriteMenuItemCreateAPIView.as_view(),
        name="favorite-menu-item-create"
    ),

    path(
        "menu-items/<uuid:menu_item_id>/",
        FavoriteMenuItemDeleteAPIView.as_view(),
        name="favorite-menu-item-delete"
    ),
]