from src.payment.i_payment_processor import IPaymentProcessor
from src.payment.credit_card_gateway import CreditCardGateway

class CreditCardAdapter(IPaymentProcessor):
    def __init__(self, gateway):
        self._gateway = gateway
    def process_payment(self, amount, user_id):
        txn = self._gateway.initiate_charge(amount, user_id)
        return txn is not None
    def refund_payment(self, txn_id):
        return self._gateway.reverse_charge(txn_id)
    def get_name(self): return "Credit Card"