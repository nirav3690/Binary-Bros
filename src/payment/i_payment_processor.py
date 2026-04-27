from abc import ABC, abstractmethod

class IPaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float, user_id: str) -> bool: pass

    @abstractmethod
    def refund_payment(self, transaction_id: str) -> bool: pass