from colors.base import BaseColor as BaseColor

class Blue(BaseColor):
    variant: str
    point_value: int
    def paint(self) -> str: ...
    def draw(self) -> str: ...
