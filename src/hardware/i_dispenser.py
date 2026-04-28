from abc import ABC, abstractmethod

class IDispenser(ABC):

    @abstractmethod
    def dispense(self, product_id: str) -> bool: pass

    @abstractmethod
    def is_ready(self) -> bool: pass

    @abstractmethod
    def recalibrate(self): pass

    @abstractmethod
    def get_type(self) -> str: pass