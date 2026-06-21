from django.contrib import admin

from .models import (
    FavoriteCook,
    FavoriteMenuItem
)


@admin.register(
    FavoriteCook
)
class FavoriteCookAdmin(
    admin.ModelAdmin
):

    list_display = (
        "customer",
        "cook",
        "cook_username",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "cook__user__username",
    )

    autocomplete_fields = (
        "customer",
        "cook",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    def cook_username(
        self,
        obj
    ):
        return (
            obj.cook.user.username
        )

    cook_username.short_description = (
        "Cook Username"
    )


@admin.register(
    FavoriteMenuItem
)
class FavoriteMenuItemAdmin(
    admin.ModelAdmin
):

    list_display = (
        "customer",
        "menu_item",
        "menu_item_name",
        "menu_owner",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "menu_item__name",
    )

    autocomplete_fields = (
        "customer",
        "menu_item",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    def menu_item_name(
        self,
        obj
    ):
        return (
            obj.menu_item.name
        )

    menu_item_name.short_description = (
        "Menu Item"
    )

    def menu_owner(
        self,
        obj
    ):
        return (
            obj.menu_item
            .menu
            .cook
            .user
            .username
        )

    menu_owner.short_description = (
        "Cook"
    )
