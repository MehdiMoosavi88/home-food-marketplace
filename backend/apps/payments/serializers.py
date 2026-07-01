from rest_framework import serializers

from .models import Payment


class PaymentSerializer(
    serializers.ModelSerializer
):

    reservation_id = (
        serializers.UUIDField(
            source="reservation.id",
            read_only=True,
        )
    )

    customer = (
        serializers.CharField(
            source="customer.username",
            read_only=True,
        )
    )

    class Meta:

        model = Payment

        fields = (
            "id",
            "reservation_id",
            "customer",
            "amount",
            "status",
            "gateway",
            "authority",
            "ref_id",
            "paid_at",
            "created_at",
        )

        read_only_fields = fields


class PaymentStartSerializer(
    serializers.Serializer
):

    payment_id = (
        serializers.UUIDField()
    )

    authority = (
        serializers.CharField()
    )

    payment_url = (
        serializers.CharField()
    )

class PaymentHistorySerializer(
    serializers.ModelSerializer
):

    reservation = serializers.UUIDField(
        source="reservation.id",
        read_only=True,
    )

    class Meta:

        model = Payment

        fields = (
            "id",
            "reservation",
            "amount",
            "status",
            "authority",
            "ref_id",
            "paid_at",
            "created_at",
        )

        read_only_fields = fields