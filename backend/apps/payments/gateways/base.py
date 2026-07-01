from abc import (
    ABC,
    abstractmethod,
)


class BaseGateway(ABC):

    @abstractmethod
    def create_payment(
        self,
        payment,
    ):
        """
        Create a payment session and return
        the payment URL.
        """
        raise NotImplementedError

    @abstractmethod
    def verify_payment(
        self,
        payment,
        data,
    ):
        """
        Verify the payment result received
        from the payment gateway.
        """
        raise NotImplementedError