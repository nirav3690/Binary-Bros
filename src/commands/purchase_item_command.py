import time, json, os
from src.commands.i_command import ICommand

# PATTERN: Command
class PurchaseItemCommand(ICommand):

    def __init__(self, product_id, user_id, inventory, payment):
        self._product_id = product_id
        self._user_id    = user_id
        self._inventory  = inventory
        self._payment    = payment
        self._executed   = False
        self._txn_id     = None
        self._amount     = 0

    def execute(self) -> bool:
        if not self._inventory.is_available(self._product_id):
            return False
        item = self._inventory.get_item(self._product_id)
        self._amount = item.get_price()
        paid = self._payment.process_payment(self._amount, self._user_id)
        if not paid:
            return False
        self._inventory.deduct_stock(self._product_id)
        self._txn_id   = f"TXN_{self._product_id}_{int(time.time())}"
        self._executed = True
        self.log()
        return True

    def undo(self):
        if self._executed:
            self._payment.refund_payment(self._txn_id)
            self._executed = False
            self._save_log("REFUNDED")

    def log(self):
        self._save_log("SUCCESS")

    def _save_log(self, status):
        os.makedirs("data", exist_ok=True)
        path = "data/transactions.json"
        txns = []
        if os.path.exists(path):
            with open(path) as f:
                txns = json.load(f)
        txns.append({
            "txn_id":     self._txn_id,
            "product_id": self._product_id,
            "user_id":    self._user_id,
            "amount":     self._amount,
            "status":     status,
            "timestamp":  time.strftime("%Y-%m-%d %H:%M:%S")
        })
        with open(path, "w") as f:
            json.dump(txns, f, indent=2)

    def get_txn_id(self):
        return self._txn_id