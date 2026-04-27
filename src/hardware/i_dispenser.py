from abc import ABC, abstractmethod

class IDispenser(ABC):

    @abstractmethod
    def dispense(self, product_id: str) -> bool: pass

    @abstractmethod
    def is_ready(self) -> bool: pass