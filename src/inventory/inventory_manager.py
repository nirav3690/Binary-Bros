from src.inventory.product import Product

class InventoryManager:

    def __init__(self):
        self._items = {}

    def add_item(self, item):
        self._items[item.get_id()] = item

    def get_item(self, item_id):
        return self._items.get(item_id)

    def is_available(self, item_id) -> bool:
        item = self._items.get(item_id)
        return item is not None and item.is_available()

    def deduct_stock(self, item_id):
        item = self._items.get(item_id)
        if isinstance(item, Product):
            item.deduct()

    def print_inventory(self):
        print("\n  --- Inventory ---")
        for item in self._items.values():
            print(f"  {item.get_name():<20} "
                  f"Price: ₹{item.get_price():.2f}  "
                  f"Stock: {item.get_available_stock()}")
        print("  -----------------")