from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Menu,
    MenuItem,
    MenuItemAvailability
)

from apps.favorites.models import (
    FavoriteMenuItem
)


class MenuItemAvailabilityInline(
    admin.TabularInline
):

    model = MenuItemAvailability

    extra = 0

    readonly_fields = (
        "reserved_quantity",
    )


@admin.register(Menu)
class MenuAdmin(
    admin.ModelAdmin
):

    list_display = (
        "title",
        "cook",
        "status_badge",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "cook__user__username",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    actions = (
        "activate_menus",
        "deactivate_menus",
    )

    def status_badge(
        self,
        obj
    ):
        color = (
            "green"
            if obj.is_active
            else "red"
        )

        text = (
            "Active"
            if obj.is_active
            else "Inactive"
        )

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            text
        )

    status_badge.short_description = (
        "Status"
    )

    @admin.action(
        description=
        "Activate selected menus"
    )
    def activate_menus(
        self,
        request,
        queryset
    ):
        queryset.update(
            is_active=True
        )

    @admin.action(
        description=
        "Deactivate selected menus"
    )
    def deactivate_menus(
        self,
        request,
        queryset
    ):
        queryset.update(
            is_active=False
        )


@admin.register(MenuItem)
class MenuItemAdmin(
    admin.ModelAdmin
):

    list_display = (
        "name",
        "menu",
        "price",
        "status_badge",
        "favorites_count",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    inlines = [
        MenuItemAvailabilityInline
    ]

    actions = (
        "activate_items",
        "deactivate_items",
    )

    def status_badge(
        self,
        obj
    ):
        color = (
            "green"
            if obj.is_active
            else "red"
        )

        text = (
            "Active"
            if obj.is_active
            else "Inactive"
        )

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            text
        )

    status_badge.short_description = (
        "Status"
    )

    @admin.action(
        description=
        "Activate selected items"
    )
    def activate_items(
        self,
        request,
        queryset
    ):
        queryset.update(
            is_active=True
        )

    @admin.action(
        description=
        "Deactivate selected items"
    )
    def deactivate_items(
        self,
        request,
        queryset
    ):
        queryset.update(
            is_active=False
        )

    def favorites_count(
    self,
    obj
    ):
        return (
        FavoriteMenuItem.objects
        .filter(
            menu_item=obj
        )
        .count()
    )

    favorites_count.short_description = (
    "Favorites"
)


@admin.register(MenuItemAvailability)
class MenuItemAvailabilityAdmin(
    admin.ModelAdmin
):

    list_display = (
        "menu_item",
        "date",
        "max_quantity",
        "reserved_quantity",
        "remaining_quantity",
    )

    list_filter = (
        "date",
    )

    search_fields = (
        "menu_item__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "remaining_quantity",
    )

    def remaining_quantity(
        self,
        obj
    ):
        return (
            obj.max_quantity
            -
            obj.reserved_quantity
        )

    remaining_quantity.short_description = (
        "Remaining"
    )