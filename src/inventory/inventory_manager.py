import json, os
from src.inventory.product import Product

class InventoryManager:
    def __init__(self):
        self._items = {}

    def load(self):
        path = "data/inventory.json"
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            for item in data:
                self._items[item["id"]] = Product(
                    item["id"], item["name"], item["price"], item["stock"])

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open("data/inventory.json", "w") as f:
            json.dump([i.to_dict() for i in self._items.values()
                       if isinstance(i, Product)], f, indent=2)

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
            self.save()

    def all_items(self):
        return list(self._items.values())