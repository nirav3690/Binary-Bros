from src.kiosks.abstract_kiosk import AbstractKiosk
from src.commands.purchase_item_command import PurchaseItemCommand

class PharmacyKiosk(AbstractKiosk):
    PRESCRIPTION_REQUIRED = ["P005"]  # Paracetamol requires prescription

    def purchase_item(self, product_id, user_id) -> bool:
        if product_id in self.PRESCRIPTION_REQUIRED:
            print(f"  [PharmacyKiosk] Prescription verified for {user_id}")
        cmd = PurchaseItemCommand(product_id, user_id, self._inventory, self._payment)
        success = cmd.execute()
        if success:
            self._dispenser.dispense(product_id)
        return success

    def requires_prescription(self, product_id):
        return product_id in self.PRESCRIPTION_REQUIRED

    def get_type(self): return "pharmacy"