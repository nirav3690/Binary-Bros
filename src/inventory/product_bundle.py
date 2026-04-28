from src.inventory.i_inventory_item import IInventoryItem

class ProductBundle(IInventoryItem):
    def __init__(self, bundle_id, name):
        self._id       = bundle_id
        self._name     = name
        self._children = []

    def add(self, item): self._children.append(item)

    def get_id(self)   -> str:   return self._id
    def get_name(self) -> str:   return self._name

    def get_price(self) -> float:
        return sum(c.get_price() for c in self._children)

    def get_available_stock(self) -> int:
        if not self._children: return 0
        return min(c.get_available_stock() for c in self._children)

    def is_available(self) -> bool:
        return all(c.is_available() for c in self._children)