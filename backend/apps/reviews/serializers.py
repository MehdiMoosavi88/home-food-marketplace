from rest_framework import serializers

from .models import Review, Comment

from apps.reservations.models import (
    Reservation
)


class ReviewCreateSerializer(
    serializers.ModelSerializer
):

    reservation = (
        serializers.UUIDField()
    )

    class Meta:

        model = Review

        fields = (
            "reservation",
            "rating",
            "comment",
        )

    def validate_rating(
        self,
        value
    ):

        if value < 1 or value > 5:

            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value

    def validate(
        self,
        attrs
    ):

        request = self.context[
            "request"
        ]

        reservation_id = attrs[
            "reservation"
        ]

        try:

            reservation = (
                Reservation.objects
                .select_related(
                    "customer"
                )
                .get(
                    pk=reservation_id
                )
            )

        except Reservation.DoesNotExist:

            raise serializers.ValidationError(
                "Reservation not found."
            )

        if (
            reservation.customer
            != request.user
        ):

            raise serializers.ValidationError(
                "This reservation does not belong to you."
            )

        if (
            reservation.status
            != Reservation.Status.COMPLETED
        ):

            raise serializers.ValidationError(
                "Only completed reservations can be reviewed."
            )

        if hasattr(
            reservation,
            "review"
        ):

            raise serializers.ValidationError(
                "Review already exists."
            )

        attrs[
            "reservation_obj"
        ] = reservation

        return attrs
    
class ReviewSerializer(
    serializers.ModelSerializer
):

    customer_username = (
        serializers.CharField(
            source=
            "customer.username",
            read_only=True
        )
    )

    class Meta:

        model = Review

        fields = (
            "id",
            "customer_username",
            "rating",
            "comment",
            "created_at",
        )

class CommentCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Comment

        fields = (
            "cook",
            "menu",
            "menu_item",
            "text",
        )

    def validate(
        self,
        attrs
    ):

        targets = [

            attrs.get("cook"),

            attrs.get("menu"),

            attrs.get("menu_item")
        ]

        selected = len(
            [
                item
                for item in targets
                if item is not None
            ]
        )

        if selected != 1:

            raise serializers.ValidationError(
                "Select exactly one target."
            )

        return attrs
    
class CommentSerializer(
    serializers.ModelSerializer
):

    customer_username = (
        serializers.CharField(
            source=
            "customer.username",
            read_only=True
        )
    )

    class Meta:

        model = Comment

        fields = (
            "id",
            "customer_username",
            "text",
            "created_at",
        )