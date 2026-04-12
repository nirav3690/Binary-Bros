from src.payment.i_payment_processor import IPaymentProcessor
from src.payment.credit_card_gateway import CreditCardGateway

class CreditCardAdapter(IPaymentProcessor):

    def __init__(self, gateway: CreditCardGateway):
        self._gateway = gateway

    def process_payment(self, amount: float, user_id: str) -> bool:
        txn = self._gateway.initiate_charge(amount, user_id)
        print(f"  [CreditCardAdapter] Payment successful. Ref: {txn}")
        return txn is not None

    def refund_payment(self, transaction_id: str) -> bool:
        return self._gateway.reverse_charge(transaction_id)