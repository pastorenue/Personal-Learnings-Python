# blue.py
from colors.base import BaseColor

class Blue(BaseColor):
    variant: str = '\033[94m'
    point_value: int = 1

    def paint(self) -> str:
        return f"painting {self.variant} on {self.__class__.__name__}"

    def draw(self) -> str:
        return f"drawing {self.variant} on {self.__class__.__name__}"
    
    def is_clean(self) -> bool:
        return True
    

class Foo:
    def bar(self, value: str) -> str:
        d: dict = {}
        d.get(None)
        return f"bar is {value }"
