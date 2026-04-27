from abc import ABC, abstractmethod

class ICommand(ABC):

    @abstractmethod
    def execute(self) -> bool: pass

    @abstractmethod
    def undo(self): pass

    @abstractmethod
    def log(self): pass