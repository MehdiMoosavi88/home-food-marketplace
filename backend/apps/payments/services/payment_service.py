from django.utils import timezone

from ..models import Payment

from ..exceptions import PaymentVerificationFailed

from .notifications import send_payment_success_notification


class PaymentService:

    def __init__(
        self,
        gateway,
    ):
        self.gateway = gateway

    def create_payment(
        self,
        payment,
    ):
        """
        Start a payment.
        """

        return (
            self.gateway.create_payment(
                payment
            )
        )

    def verify_payment(
        self,
        payment,
    ):

        result = self.gateway.verify_payment(
            payment
        )

        if not result["success"]:

            payment.status = (
                Payment.Status.FAILED
            )

            payment.save(
                update_fields=[
                    "status",
                ]
            )

            raise PaymentVerificationFailed()

        payment.status = (
            Payment.Status.SUCCESS
        )

        payment.ref_id = (
            result["ref_id"]
        )

        payment.paid_at = (
            timezone.now()
        )

        payment.save(
            update_fields=[
                "status",
                "ref_id",
                "paid_at",
            ]
        )

        payment.reservation.mark_as_paid()

        send_payment_success_notification(
        payment
        )

        return payment
    
    def create_payment_record(
        self,
        reservation,
        customer,
    ):

        return Payment.objects.create(
            reservation=reservation,
            customer=customer,
            amount=reservation.total_price,
        )