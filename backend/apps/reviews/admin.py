from django.contrib import admin
from django.db.models import Avg

from .models import (
    Review,
    Comment
)


@admin.action(
    description="Activate selected comments"
)
def activate_comments(
    modeladmin,
    request,
    queryset
):
    queryset.update(
        is_active=True
    )


@admin.action(
    description="Deactivate selected comments"
)
def deactivate_comments(
    modeladmin,
    request,
    queryset
):
    queryset.update(
        is_active=False
    )


@admin.register(Review)
class ReviewAdmin(
    admin.ModelAdmin
):

    list_display = (
        "customer",
        "cook",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "cook__user__username",
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


@admin.register(Comment)
class CommentAdmin(
    admin.ModelAdmin
):

    list_display = (
        "customer",
        "comment_target",
        "short_text",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "text",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    actions = [
        activate_comments,
        deactivate_comments,
    ]

    list_per_page = 25

    def short_text(
        self,
        obj
    ):
        return obj.text[:50]

    short_text.short_description = (
        "Comment"
    )

    def comment_target(
        self,
        obj
    ):

        if obj.cook:
            return (
                f"Cook: "
                f"{obj.cook.user.username}"
            )

        if obj.menu:
            return (
                f"Menu: "
                f"{obj.menu.title}"
            )

        if obj.menu_item:
            return (
                f"Food: "
                f"{obj.menu_item.name}"
            )

        return "-"

    comment_target.short_description = (
        "Target"
    )