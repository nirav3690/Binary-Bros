from abc import ABC, abstractmethod

class IInventoryItem(ABC):

    @abstractmethod
    def get_id(self) -> str: pass

    @abstractmethod
    def get_name(self) -> str: pass

    @abstractmethod
    def get_price(self) -> float: pass

    @abstractmethod
    def get_available_stock(self) -> int: pass

    @abstractmethod
    def is_available(self) -> bool: pass