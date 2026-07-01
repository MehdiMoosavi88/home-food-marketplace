from apps.notifications.services import (
    create_notification,
)


def send_payment_success_notification(
    payment,
):

    create_notification(
        user=payment.customer,
        title="Payment Successful",
        message=(
            "Your payment was completed successfully. "
            "Your reservation is awaiting confirmation by the cook."
        ),
    )