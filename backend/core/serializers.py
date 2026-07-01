from rest_framework import serializers


class ErrorSerializer(
    serializers.Serializer
):

    detail = serializers.CharField(
        help_text="Human-readable error message."
    )

    code = serializers.CharField(
        required=False,
        help_text="Optional machine-readable error code."
    )