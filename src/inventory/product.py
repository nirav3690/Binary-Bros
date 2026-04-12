from src.inventory.i_inventory_item import IInventoryItem

class Product(IInventoryItem):

    def __init__(self, product_id, name, price, stock):
        self._id    = product_id
        self._name  = name
        self._price = price
        self._stock = stock

    def get_id(self)              -> str:   return self._id
    def get_name(self)            -> str:   return self._name
    def get_price(self)           -> float: return self._price
    def get_available_stock(self) -> int:   return self._stock
    def is_available(self)        -> bool:  return self._stock > 0

    def deduct(self):
        self._stock -= 1
        print(f"  [Inventory] Stock deducted for: {self._name}")