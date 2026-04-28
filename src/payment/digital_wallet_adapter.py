from src.payment.i_payment_processor import IPaymentProcessor

class _WalletProvider:
    def debit(self, wallet_id, amount):
        print(f"  [WalletProvider] Debiting ₹{amount} from wallet: {wallet_id}")
        return True
    def credit(self, wallet_id, amount):
        print(f"  [WalletProvider] Crediting ₹{amount} to wallet: {wallet_id}")
        return True

class DigitalWalletAdapter(IPaymentProcessor):
    def __init__(self): self._p = _WalletProvider()
    def process_payment(self, amount, user_id):
        return self._p.debit(f"wallet_{user_id}", amount)
    def refund_payment(self, txn_id):
        import json, os
        amount = 0
        path = "data/transactions.json"
        if os.path.exists(path):
            with open(path) as f:
                txns = json.load(f)
            for t in txns:
                if t["txn_id"] == txn_id:
                    amount = t["amount"]
                    break
        return self._p.credit(txn_id, amount)
    def get_name(self): return "Digital Wallet"