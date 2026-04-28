from src.kiosks.abstract_kiosk import AbstractKiosk
from src.commands.purchase_item_command import PurchaseItemCommand

class EmergencyReliefKiosk(AbstractKiosk):
    def __init__(self, dispenser, inventory, payment):
        super().__init__(dispenser, inventory, payment)
        self._user_counts = {}

    def purchase_item(self, product_id, user_id) -> bool:
        max_qty = int(self._registry.get("maxEmergencyQty"))
        count   = self._user_counts.get(user_id, 0)
        if count >= max_qty:
            print(f"  [EmergencyKiosk] BLOCKED — {user_id} reached limit of {max_qty}")
            return False
        cmd = PurchaseItemCommand(product_id, user_id, self._inventory, self._payment)
        success = cmd.execute()
        if success:
            self._dispenser.dispense(product_id)
            self._user_counts[user_id] = count + 1
        return success

    def get_type(self): return "emergency"