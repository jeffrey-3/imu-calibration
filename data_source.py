from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def read(self) -> list:
        pass
