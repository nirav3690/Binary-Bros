from src.commands.i_command import ICommand
from src.inventory.product import Product

class RestockCommand(ICommand):

    def __init__(self, product_id, quantity, inventory):
        self._product_id = product_id
        self._quantity   = quantity
        self._inventory  = inventory

    def execute(self) -> bool:
        item = self._inventory.get_item(self._product_id)
        if isinstance(item, Product):
            item.restock(self._quantity)
            self._inventory.save()
            return True
        return False

    def undo(self):
        item = self._inventory.get_item(self._product_id)
        if isinstance(item, Product):
            item._stock = max(0, item._stock - self._quantity)
            self._inventory.save()

    def log(self):
        print(f"[RestockCommand] Restocked {self._product_id} by {self._quantity}")