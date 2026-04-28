from src.payment.i_payment_processor import IPaymentProcessor

class _UPIProvider:
    def pay(self, vpa, amount):
        print(f"  [UPIProvider] Sending ₹{amount} to {vpa}")
        return True
    def refund(self, ref):
        print(f"  [UPIProvider] Refunding {ref}")
        return True

class UPIAdapter(IPaymentProcessor):
    def __init__(self): self._p = _UPIProvider()
    def process_payment(self, amount, user_id):
        return self._p.pay(f"{user_id}@upi", amount)
    def refund_payment(self, txn_id):
        return self._p.refund(txn_id)
    def get_name(self): return "UPI"