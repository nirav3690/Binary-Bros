from src.registry.central_registry import CentralRegistry
from src.hardware.spiral_dispenser import SpiralDispenser
from src.inventory.product import Product
from src.inventory.product_bundle import ProductBundle
from src.inventory.inventory_manager import InventoryManager
from src.payment.credit_card_gateway import CreditCardGateway
from src.payment.credit_card_adapter import CreditCardAdapter
from src.kiosks.food_kiosk import FoodKiosk

def main():
    print("=" * 48)
    print("  AURA RETAIL OS — Subtask 2 Simulation")
    print("=" * 48)

    print("\n[1] Singleton — CentralRegistry")
    r1 = CentralRegistry()
    r2 = CentralRegistry()
    print(f"  Location      : {r1.get('kioskLocation')}")
    print(f"  Same instance : {r1 is r2}")   

    print("\n[2] Composite — ProductBundle")
    water   = Product("P001", "Water Bottle",  20.0, 10)
    bandage = Product("P002", "Bandage Roll",  30.0,  5)

    kit = ProductBundle("B001", "Basic Kit")
    kit.add(water)
    kit.add(bandage)

    print(f"  Bundle price  : ₹{kit.get_price()}")
    print(f"  Bundle stock  : {kit.get_available_stock()}")
    print(f"  Available?    : {kit.is_available()}")

    print("\n[3] Adapter — CreditCardAdapter wrapping CreditCardGateway")
    inventory = InventoryManager()
    inventory.add_item(water)
    inventory.add_item(bandage)

    payment  = CreditCardAdapter(CreditCardGateway())
    dispenser = SpiralDispenser()
    kiosk    = FoodKiosk(dispenser, inventory, payment)

    kiosk.print_config()
    inventory.print_inventory()

    print("\n-- Purchase 1: valid product --")
    kiosk.purchase_item("P001", "user_nirav")

    print("\n-- Purchase 2: valid product --")
    kiosk.purchase_item("P002", "user_akshay")

    print("\n-- Purchase 3: product does not exist --")
    kiosk.purchase_item("P999", "user_nirav")

    print("\n" + "=" * 48)
    print("  Simulation complete — Subtask 2")
    print("=" * 48)

if __name__ == "__main__":
    main()