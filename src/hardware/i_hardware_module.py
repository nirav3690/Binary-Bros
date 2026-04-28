from abc import ABC, abstractmethod

class IHardwareModule(ABC):

    @abstractmethod
    def attach(self): pass

    @abstractmethod
    def detach(self): pass

    @abstractmethod
    def get_status(self) -> str: pass

    @abstractmethod
    def get_name(self) -> str: pass