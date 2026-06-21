from django.contrib import admin

from .models import Notification

from django import forms

class NotificationAdminForm(
    forms.ModelForm
):

    class Meta:

        model = Notification

        fields = "__all__"

    def clean(self):

        cleaned_data = super().clean()

        user = cleaned_data.get(
            "user"
        )

        is_global = cleaned_data.get(
            "is_global"
        )

        if is_global and user:

            raise forms.ValidationError(
                "Global notification cannot have a user."
            )

        if (
            not is_global
            and
            not user
        ):

            raise forms.ValidationError(
                "User notification requires a user."
            )

        return cleaned_data

@admin.register(
    Notification
)
class NotificationAdmin(
    admin.ModelAdmin
):
    
    form = (
        NotificationAdminForm
    )

    list_display = (
        "user",
        "title",
        "is_read",
        "is_global",
        "created_at",
    )

    list_filter = (
        "is_global",
        "is_read",
        "created_at",
    )

    search_fields = (
        "user__username",
        "title",
        "message",
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