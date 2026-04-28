from abc import ABC, abstractmethod
from src.registry.central_registry import CentralRegistry

class AbstractKiosk(ABC):
    def __init__(self, dispenser, inventory, payment):
        self._dispenser = dispenser
        self._inventory = inventory
        self._payment   = payment
        self._registry  = CentralRegistry()

    @abstractmethod
    def purchase_item(self, product_id, user_id) -> bool: pass

    def get_type(self) -> str: return "base"