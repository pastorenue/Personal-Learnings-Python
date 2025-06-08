import abc
from abc import ABC, abstractmethod

class BaseColor(ABC, metaclass=abc.ABCMeta):
    variant: str
    point_value: int
    @abstractmethod
    def paint(self) -> str: ...
    @abstractmethod
    def draw(self) -> str: ...
