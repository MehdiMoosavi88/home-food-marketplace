from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Reservation,
    ReservationItem
)


class ReservationItemInline(
    admin.TabularInline
):

    model = ReservationItem

    extra = 0

    can_delete = False

    readonly_fields = (
        "menu_item",
        "date",
        "quantity",
        "unit_price",
    )


@admin.register(Reservation)
class ReservationAdmin(
    admin.ModelAdmin
):

    list_display = (
        "short_id",
        "customer",
        "status_badge",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "total_price",
    )

    inlines = [
        ReservationItemInline
    ]

    actions = (
        "mark_confirmed",
        "mark_cancelled",
        "mark_completed",
    )

    list_per_page = 25

    def short_id(
        self,
        obj
    ):
        return str(obj.id)[:8]

    short_id.short_description = (
        "ID"
    )

    def status_badge(
        self,
        obj
    ):

        colors = {
            "pending": "#f39c12",
            "confirmed": "#27ae60",
            "cancelled": "#e74c3c",
            "completed": "#3498db",
        }

        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(
                obj.status,
                "black"
            ),
            obj.get_status_display()
        )

    status_badge.short_description = (
        "Status"
    )

    @admin.action(
        description=
        "Mark selected reservations as Confirmed"
    )
    def mark_confirmed(
        self,
        request,
        queryset
    ):
        queryset.update(
            status=
            Reservation.Status.CONFIRMED
        )

    @admin.action(
        description=
        "Mark selected reservations as Cancelled"
    )
    def mark_cancelled(
        self,
        request,
        queryset
    ):
        queryset.update(
            status=
            Reservation.Status.CANCELLED
        )

    @admin.action(
        description=
        "Mark selected reservations as Completed"
    )
    def mark_completed(
        self,
        request,
        queryset
    ):
        queryset.update(
            status=
            Reservation.Status.COMPLETED
        )


@admin.register(ReservationItem)
class ReservationItemAdmin(
    admin.ModelAdmin
):

    list_display = (
        "reservation",
        "menu_item",
        "quantity",
        "unit_price",
        "date",
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
    )