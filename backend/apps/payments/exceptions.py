from rest_framework.exceptions import APIException


class PaymentVerificationFailed(
    APIException
):

    status_code = 400

    default_detail = (
        "Payment verification failed."
    )