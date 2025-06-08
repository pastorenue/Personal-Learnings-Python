class AutoInit(type):
    def __new__(cls: type, name: str, bases: tuple, attrs: dict) -> type:
        """Automatically initialize attributes.

        Args:
            cls (type): Also can be named `meta`. The metaclass of the class. In this case, AutoInit.
            name (str): The name of the class to be initialized.
            bases (tuple): The base or super classes of the class to be initialized.
            attrs (dict): The attributes of the class to be initialized.

        Returns:
            type: The initialized class.
        """
        fields = [
            k for k, v in attrs.items() if not callable(v) and not k.startswith("_")
        ]

        for field in fields:
            attrs[field] = field

        return type.__new__(cls, name, bases, attrs)

class MyClass(metaclass=AutoInit):
    z: str
    __t: int = 1
    x: int = 1
    y: tuple = 2,


c = MyClass()
print(c.x)