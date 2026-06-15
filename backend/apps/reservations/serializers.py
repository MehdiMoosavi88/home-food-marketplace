from rest_framework import serializers

from .models import (
    Reservation,
    ReservationItem
)

from apps.menus.models import (
    MenuItem,
    MenuItemAvailability
)

class ReservationItemCreateSerializer(
    serializers.Serializer
):

    menu_item = (
        serializers.UUIDField()
    )

    date = (
        serializers.DateField()
    )

    quantity = (
        serializers.IntegerField(
            min_value=1
        )
    )

class ReservationCreateSerializer(
    serializers.Serializer
):

    items = (
        ReservationItemCreateSerializer(
            many=True
        )
    )

    def validate(
        self,
        attrs
    ):

        items = attrs["items"]

        if not items:

            raise serializers.ValidationError(
                "At least one item is required."
            )

        # جلوگیری از آیتم‌های تکراری در یک رزرو
        seen = set()

        for item in items:

            menu_item_id = item[
                "menu_item"
            ]

            date = item[
                "date"
            ]

            quantity = item[
                "quantity"
            ]

            key = (
                str(menu_item_id),
                date
            )

            if key in seen:

                raise serializers.ValidationError(
                    f"Duplicate menu item "
                    f"'{menu_item_id}' "
                    f"for date {date}."
                )

            seen.add(key)

            try:

                availability = (
                    MenuItemAvailability.objects
                    .select_related(
                        "menu_item"
                    )
                    .get(
                        menu_item_id=
                        menu_item_id,
                        date=date
                    )
                )

            except (
                MenuItemAvailability
                .DoesNotExist
            ):

                raise serializers.ValidationError(
                    f"No capacity found for "
                    f"menu item "
                    f"{menu_item_id}"
                )

            remaining = (
                availability.max_quantity
                -
                availability.reserved_quantity
            )

            if quantity > remaining:

                raise serializers.ValidationError(
                    f"Only {remaining} portions "
                    f"available."
                )

        return attrs
    
class ReservationItemSerializer(
    serializers.ModelSerializer
):

    menu_item_name = (
        serializers.CharField(
            source=
            "menu_item.name",
            read_only=True
        )
    )

    class Meta:

        model = ReservationItem

        fields = (
            "id",
            "menu_item",
            "menu_item_name",
            "date",
            "quantity",
            "unit_price",
        )

        read_only_fields = (
            "id",
            "unit_price",
        )

class ReservationSerializer(
    serializers.ModelSerializer
):

    items = (
        ReservationItemSerializer(
            many=True,
            read_only=True
        )
    )

    class Meta:

        model = Reservation

        fields = (
            "id",
            "status",
            "total_price",
            "items",
            "created_at",
        )

        read_only_fields = (
            "id",
            "status",
            "total_price",
            "created_at",
        )
    
class CookReservationSerializer(
    serializers.ModelSerializer
):

    customer_username = (
        serializers.CharField(
            source="customer.username",
            read_only=True
        )
    )

    class Meta:

        model = Reservation

        fields = (
            "id",
            "customer_username",
            "status",
            "total_price",
            "created_at",
        )