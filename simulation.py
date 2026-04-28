from src.registry.central_registry import CentralRegistry
from src.hardware.spiral_dispenser import SpiralDispenser
from src.inventory.product import Product
from src.inventory.product_bundle import ProductBundle
from src.inventory.inventory_manager import InventoryManager
from src.payment.credit_card_gateway import CreditCardGateway
from src.payment.credit_card_adapter import CreditCardAdapter
from src.kiosks.food_kiosk import FoodKiosk

transaction_log = []

class LoggedFoodKiosk(FoodKiosk):
    def purchase_item(self, product_id, user_id):
        item = self._inventory.get_item(product_id)
        success = super().purchase_item(product_id, user_id)
        if success and item:
            transaction_log.append({
                "user":    user_id,
                "product": item.get_name(),
                "amount":  item.get_price(),
                "status":  "SUCCESS"
            })
        else:
            transaction_log.append({
                "user":    user_id,
                "product": product_id,
                "amount":  0,
                "status":  "FAILED"
            })
        return success

def admin_menu(inventory, registry):
    ADMIN_PASSWORD = "admin123"

    password = input("\n  Enter admin password: ").strip()
    if password != ADMIN_PASSWORD:
        print("  Wrong password. Access denied.")
        return

    while True:
        print("\n  ==== Admin Panel ====")
        print("  1. View Inventory")
        print("  2. Restock a Product")
        print("  3. View Transaction History")
        print("  4. View Payment Summary")
        print("  5. Change Kiosk Location")
        print("  6. Exit Admin Panel")
        print("  ====================")

        choice = input("  Enter choice (1-6): ").strip()

        if choice == "1":
            inventory.print_inventory()

        elif choice == "2":
            print("\n  Which product to restock?")
            print("  1. Water Bottle (P001)")
            print("  2. Biscuit Pack (P002)")
            print("  3. Bandage Roll (P003)")
            p = input("  Enter choice: ").strip()
            qty = input("  Enter quantity to add: ").strip()

            if not qty.isdigit():
                print("  Invalid quantity.")
                continue

            qty = int(qty)
            id_map = {"1": "P001", "2": "P002", "3": "P003"}
            item_id = id_map.get(p)

            if item_id:
                item = inventory.get_item(item_id)
                if isinstance(item, Product):
                    item._stock += qty
                    print(f"  Restocked {item.get_name()} by {qty}."
                          f" New stock: {item.get_available_stock()}")
            else:
                print("  Invalid choice.")

        elif choice == "3":
            print("\n  ---- Transaction History ----")
            if not transaction_log:
                print("  No transactions yet.")
            else:
                for i, txn in enumerate(transaction_log, 1):
                    print(f"  {i}. User: {txn['user']:<15} "
                          f"Product: {txn['product']:<20} "
                          f"Amount: ₹{txn['amount']:<8} "
                          f"Status: {txn['status']}")
            print("  ----------------------------")

        elif choice == "4":
            print("\n  ---- Payment Summary ----")
            total     = sum(t["amount"] for t in transaction_log if t["status"] == "SUCCESS")
            success   = sum(1 for t in transaction_log if t["status"] == "SUCCESS")
            failed    = sum(1 for t in transaction_log if t["status"] == "FAILED")
            print(f"  Total transactions : {len(transaction_log)}")
            print(f"  Successful         : {success}")
            print(f"  Failed             : {failed}")
            print(f"  Total revenue      : ₹{total:.2f}")
            print("  -------------------------")

        elif choice == "5":
            new_loc = input("  Enter new kiosk location: ").strip()
            if new_loc:
                registry.set("kioskLocation", new_loc)
                print(f"  Location updated to: {new_loc}")

        elif choice == "6":
            print("  Exiting admin panel.")
            break

        else:
            print("  Invalid choice.")


def main():
    print("=" * 48)
    print("  AURA RETAIL OS — Interactive Simulation")
    print("=" * 48)

    registry  = CentralRegistry()
    water     = Product("P001", "Water Bottle",  20.0, 10)
    biscuit   = Product("P002", "Biscuit Pack",  15.0,  5)
    bandage   = Product("P003", "Bandage Roll",  30.0,  8)

    inventory = InventoryManager()
    inventory.add_item(water)
    inventory.add_item(biscuit)
    inventory.add_item(bandage)

    payment   = CreditCardAdapter(CreditCardGateway())
    dispenser = SpiralDispenser()
    kiosk     = LoggedFoodKiosk(dispenser, inventory, payment)

    while True:
        print(f"\n  Location : {registry.get('kioskLocation')}")
        print(f"  Currency : {registry.get('currency')}")
        print("\n  ---- Login ----")
        print("  1. User")
        print("  2. Admin")
        print("  3. Exit System")
        print("  ---------------")

        role = input("  Who are you? (1/2/3): ").strip()

        if role == "1":
            user_id = input("  Enter your name: ").strip()
            if not user_id:
                user_id = "guest"

            while True:
                print(f"\n  Welcome, {user_id}!")
                inventory.print_inventory()
                print("\n  ---- Menu ----")
                print("  1. Buy Water Bottle  (₹20)")
                print("  2. Buy Biscuit Pack  (₹15)")
                print("  3. Buy Bandage Roll  (₹30)")
                print("  4. View Inventory")
                print("  5. Logout")
                print("  --------------")

                choice = input("  Enter choice (1-5): ").strip()

                if choice == "1":
                    kiosk.purchase_item("P001", user_id)
                elif choice == "2":
                    kiosk.purchase_item("P002", user_id)
                elif choice == "3":
                    kiosk.purchase_item("P003", user_id)
                elif choice == "4":
                    inventory.print_inventory()
                elif choice == "5":
                    print(f"  Goodbye, {user_id}!")
                    break
                else:
                    print("  Invalid choice.")

        elif role == "2":
            admin_menu(inventory, registry)

        elif role == "3":
            print("\n  Shutting down Aura Retail OS. Goodbye!")
            break

        else:
            print("  Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()