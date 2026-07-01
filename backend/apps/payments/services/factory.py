from apps.payments.gateways.fake import FakeGateway

from .payment_service import (
    PaymentService,
)


def get_payment_service():

    return PaymentService(
        gateway=FakeGateway(),
    )