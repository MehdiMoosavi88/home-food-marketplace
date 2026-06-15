from django.contrib import admin

from .models import CookProfile


@admin.register(CookProfile)
class CookProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "city",
        "phone",
    )

    search_fields = (
        "user__username",
        "user__email",
        "city",
        "phone",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    list_per_page = 25