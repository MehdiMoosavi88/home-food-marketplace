from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "reservation",
        "amount",
        "status",
        "gateway",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "status",
        "gateway",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "reservation__id",
        "authority",
        "ref_id",
    )

    readonly_fields = (
        "authority",
        "ref_id",
        "paid_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "customer",
        "reservation",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 25

    def has_change_permission(
    self,
    request,
    obj=None,
    ):
        if (
        obj
        and
        obj.status == Payment.Status.SUCCESS
        ):
            return False

        return super().has_change_permission(
        request,
        obj,
        )
