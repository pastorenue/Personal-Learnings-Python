import locale
import string

locale.setlocale(category=locale.LC_ALL, locale="fr_FR.UTF-8")

c: int = 10000000
d: float = 3.14

print(f"{c:,d}")

print(f"{c:_}")
print(locale.format_string("%.2f", d, grouping=True))

print(string.ascii_letters)
print(string.ascii_lowercase)
print(string.ascii_uppercase)
print(string.ascii_letters + string.digits)
print(string.ascii_letters + string.ascii_lowercase + string.digits)

print(string.punctuation)
print(string.digits)
print(string.hexdigits)
print(string.octdigits)

msg = ("disk failure", 32)
print('error: %s' % (msg,))
print(rf"me")
print(f"abc { 65 } def")

class A(str):
    pass

    def __format__(self, format_spec: str) -> str:
        fmt = format_spec.format(self)
        if format_spec == ".":
            print("format_spec == .")
            return f"{self:{fmt}}"
        return fmt.replace("_", format_spec)

class MyString:
    def __init__(self, value: int) -> None:
        self.value = value

    def __format__(self, format_spec: str) -> str:
        assert isinstance(self.value, int)
        fmt = f"{self.value:_}"
        return fmt.replace("_", format_spec)



from typing import ClassVar
from dataclasses import dataclass

class Key:
    stats: ClassVar[dict[str, int]] = {}
    value: int
    in_use: bool

    def __init__(self, value: int, in_use: bool) -> None:
        self.value = value
        self.in_use = in_use


some_key = Key(2, True)
some_key.stats = {'safe': 1, 'dangerous': 2}
print(some_key.stats)


from datetime import datetime

now = datetime.now()
print(f"{now:%d.%m.%y}")