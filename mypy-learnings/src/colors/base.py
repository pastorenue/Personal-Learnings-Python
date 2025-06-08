from abc import ABC, abstractmethod


class BaseColor(ABC):
    variant: str
    point_value: int

    @abstractmethod
    def paint(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> str:
        raise NotImplementedError
        
    def __str__(self) -> str:
        return self.variant

    def __repr__(self) -> str:
        return f"<self.__class__.__name__: {self.variant}, {self.point_value}>"
    
    def __call__(self):
        print("Add changes")