from rest_framework import serializers

from .models import (
    Menu,
    MenuItem
)

class MenuSerializer(
    serializers.ModelSerializer
):
    id = serializers.UUIDField(
        read_only=True
    )

    class Meta:

        model = Menu

        fields = (
            "id",
            "title",
            "description",
        )
        read_only_fields = (
            "id",
        )

class MenuItemSerializer(
    serializers.ModelSerializer
):
    id = serializers.UUIDField(
        read_only=True
    )
    image_url = serializers.SerializerMethodField()
    class Meta:

        model = MenuItem

        fields = (
            "id",
            "name",
            "description",
            "price",
            "image",
            "image_url",
            "is_active",
        )
        read_only_fields = (
            "id",
            "image_url",
        )
    def get_image_url(self, obj):

        request = self.context.get("request")

        if obj.image and request:
            return request.build_absolute_uri(
                obj.image.url
            )

        return None