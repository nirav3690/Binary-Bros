import json, os, time
from src.commands.i_command import ICommand

class RefundCommand(ICommand):

    def __init__(self, txn_id, payment):
        self._txn_id = txn_id
        self._payment = payment

    def execute(self) -> bool:
        result = self._payment.refund_payment(self._txn_id)
        if result:
            self.log()
        return result

    def undo(self): pass

    def log(self):
        path = "data/transactions.json"
        if not os.path.exists(path):
            return
        with open(path) as f:
            txns = json.load(f)
        for t in txns:
            if t["txn_id"] == self._txn_id:
                t["status"] = "REFUNDED"
        with open(path, "w") as f:
            json.dump(txns, f, indent=2)
        