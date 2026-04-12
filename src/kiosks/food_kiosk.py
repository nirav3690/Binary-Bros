from src.kiosks.abstract_kiosk import AbstractKiosk

class FoodKiosk(AbstractKiosk):

    def purchase_item(self, product_id: str, user_id: str) -> bool:
        print(f"\n  [FoodKiosk] Purchase by: {user_id}")

        if not self._inventory.is_available(product_id):
            print("  [FoodKiosk] FAILED — product not available.")
            return False

        item = self._inventory.get_item(product_id)
        paid = self._payment.process_payment(item.get_price(), user_id)

        if not paid:
            print("  [FoodKiosk] FAILED — payment unsuccessful.")
            return False

        self._inventory.deduct_stock(product_id)
        self._dispenser.dispense(product_id)
        print(f"  [FoodKiosk] Purchase complete.")
        return True