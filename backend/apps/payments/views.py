from django.shortcuts import (
    get_object_or_404,
)

from drf_yasg.utils import (
    swagger_auto_schema,
)

from drf_yasg import (
    openapi,
)

from rest_framework import (
    generics,
    status,
)

from rest_framework.response import (
    Response,
)

from rest_framework.exceptions import (
    ValidationError,
)

from rest_framework.filters import OrderingFilter

from apps.reservations.models import (
    Reservation,
)

from core.permissions.roles import (
    IsCustomer,
)

from .models import (
    Payment,
)

from .serializers import (
    PaymentStartSerializer,
    PaymentSerializer,
    PaymentHistorySerializer
)

from .gateways.fake import (
    FakeGateway,
)

from .services.factory import (
    get_payment_service,
)

from core.serializers import (
    ErrorSerializer,
)

class StartPaymentAPIView(
    generics.GenericAPIView
):

    permission_classes = [
        IsCustomer,
    ]

    serializer_class = (
        PaymentStartSerializer
    )

    def _get_reservation(
        self,
        request,
        reservation_id,
    ):

        return get_object_or_404(
            Reservation.objects.select_related(
                "customer",
            ),
            id=reservation_id,
            customer=request.user,
        )

    @swagger_auto_schema(
        tags=["Payments"],
        responses={
        201: PaymentStartSerializer,
        400: ErrorSerializer,
        404: ErrorSerializer,
    }
    )

    def post(
        self,
        request,
        reservation_id,
    ):

        reservation = self._get_reservation(
            request,
            reservation_id,
        )

        self._validate_reservation(
            reservation
            )

        service = get_payment_service()
  
        payment = (
    service.create_payment_record(
        reservation=reservation,
        customer=request.user,
        )
        )
        result = (
    service.create_payment(
        payment,
        )
        )

        response_data = {
    "payment_id": payment.id,
    "authority": result["authority"],
    "payment_url": result["payment_url"],
    }
        
        serializer = self.get_serializer(
    response_data
    )
        return Response(
    serializer.data,
    status=status.HTTP_201_CREATED,
    )
    
    def _validate_reservation(
    self,
    reservation,
    ):
        if (
        reservation.status
        !=
        Reservation.Status.PENDING
        ):
            raise ValidationError(
            {
                "reservation":
                (
                    "Only pending reservations "
                    "can be paid."
                )
            }
            )
        if (
        Payment.objects.filter(
            reservation=reservation,
        ).exists()
        ):
            raise ValidationError(
            {
                "payment":
                (
                    "A payment already exists "
                    "for this reservation."
                )
            }
        )
        if (
        reservation.total_price <= 0
        ):
            raise ValidationError(
            {
                "amount":
                (
                    "Reservation amount "
                    "must be greater than zero."
                )
            }
        )


class VerifyPaymentAPIView(
    generics.GenericAPIView
):

    permission_classes = [
        IsCustomer,
    ]

    serializer_class = (
        PaymentSerializer
    )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "authority",
                openapi.IN_PATH,
                description=(
                    "Payment authority returned by "
                    "the Start Payment API."
                ),
                type=openapi.TYPE_STRING,
            )
        ],
        operation_summary="Verify payment",
        operation_description=(
            "Verifies a pending payment. "
            "If successful, the payment is marked "
            "as successful and the reservation is "
            "marked as paid."
        ),
        responses={
            200: PaymentSerializer,
            400: ErrorSerializer,
            404: ErrorSerializer,
        },
        tags=["Payments"],
    )

    def post(
    self,
    request,
    authority,
    *args,
    **kwargs,
    ):

        payment = self.get_payment()

        service = get_payment_service()

        payment = service.verify_payment(
        payment
    )

        serializer = self.get_serializer(
        payment
    )

        return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )

    def get_payment(
    self,
    ):
        return get_object_or_404(
        Payment.objects.select_related(
            "reservation",
            "customer",
        ),
        authority=self.kwargs["authority"],
        customer=self.request.user,
    )

class PaymentHistoryAPIView(
    generics.ListAPIView
):

    serializer_class = (
        PaymentHistorySerializer
    )

    permission_classes = [
        IsCustomer
    ]

    filter_backends = [
    OrderingFilter,
    ]

    ordering_fields = [
    "created_at",
    "amount",
    "status",
    ]

    ordering = [
    "-created_at",
    ]

    @swagger_auto_schema(
    operation_summary="Payment history",
    operation_description=(
        "Returns the authenticated customer's "
        "payment history."
    ),
    manual_parameters=[
        openapi.Parameter(
            "ordering",
            openapi.IN_QUERY,
            description=(
                "Ordering options:\n"
                "- created_at\n"
                "- -created_at\n"
                "- amount\n"
                "- -amount\n"
                "- status\n"
                "- -status"
            ),
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: PaymentHistorySerializer(many=True),
        401: ErrorSerializer,
    },
    tags=["Payments"],
    )
    
    def get(
    self,
    request,
    *args,
    **kwargs,
    ):
        
        return super().get(
        request,
        *args,
        **kwargs,
    )

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return (
                Payment.objects.none()
            )

        return (
    Payment.objects
    .select_related(
        "reservation",
        )
        .filter(
        customer=self.request.user
        )
        .order_by(
            "-created_at"
        )
        )
    
