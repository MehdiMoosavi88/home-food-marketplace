from rest_framework import serializers

from .models import (
    Menu,
    MenuItem,
    MenuItemAvailability
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
            "favorites_count",
            "orders_count",
            "average_rating",
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
    
class MenuItemAvailabilitySerializer(
    serializers.ModelSerializer
):

    id = serializers.UUIDField(
        read_only=True
    )

    remaining_quantity = (
        serializers.SerializerMethodField()
    )

    class Meta:

        model = MenuItemAvailability

        fields = (
            "id",
            "menu_item",
            "date",
            "max_quantity",
            "reserved_quantity",
            "remaining_quantity",
        )

        read_only_fields = (
            "id",
            "reserved_quantity",
            "remaining_quantity",
        )

        validators = []

    def get_remaining_quantity(
        self,
        obj
    ):
        return (
            obj.max_quantity -
            obj.reserved_quantity
        )

    def validate(self, attrs):

        menu_item = attrs.get(
            "menu_item",
            self.instance.menu_item
            if self.instance else None
        )

        date = attrs.get(
            "date",
            self.instance.date
            if self.instance else None
        )

        queryset = (
            MenuItemAvailability.objects
            .filter(
                menu_item=menu_item,
                date=date
            )
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Capacity for this food and date already exists."
                    ]
                }
            )

        return attrs