import uuid

from .base import BaseGateway

from django.conf import settings


class FakeGateway(BaseGateway):

    def _generate_reference(self):

        return str(
            uuid.uuid4()
        )

    def create_payment(
        self,
        payment,
    ):
        """
        Simulate creating a payment session.
        """

        authority = (
            self._generate_reference()
        )

        payment.authority = authority

        payment.save(
            update_fields=[
                "authority",
            ]
        )

        return {
            "authority": authority,
            "payment_url": (
                f"/payments/fake/"
                f"{authority}/"
            ),
        }

    def verify_payment(
    self,
    payment,
    ):
        
        return {
        "success": settings.FAKE_PAYMENT_SUCCESS,
        "ref_id": (
            str(uuid.uuid4())
        ),
    }