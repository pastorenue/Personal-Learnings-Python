from collections import namedtuple
from collections.abc import Generator, Iterable, Sequence, Callable, Awaitable, Sized
import math
import random
from typing import Any, ClassVar, Final, Generic, Never, NoReturn, Protocol, Self, TypeVar

# type aliasing
type Vector = list[int]
x: Vector = [1, 2, 3]
print(x)

type ConnectionOptions = dict[str, str]
type Address = tuple[str, int]
type Server = tuple[Address, ConnectionOptions]

OfferEventModel = namedtuple("OfferEventModel", ["id", "offer"])
# Something else
type OfferErrorMapping = tuple[OfferEventModel, Any]

def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    for server in servers:
        address, _ = server
        print(f"broadcasting {message} to {address}")

def test(callback: Callable[[], str]) -> None:
    print(f"callback returns {callback()}")

def async_query(on_success: Callable[[int], None], on_error: Callable[[int, Exception], None]) -> None:
    ... # body elided

# Callable cannot express complex signatures such as functions that take a variadic number of arguments,
# overloaded functions, or functions that have keyword-only parameters.
# However, these signatures can be expressed by defining a Protocol class with a __call__() method:
class SupportsCall(Protocol):
    def __call__(self, *vals: bytes, max_len: int | None = None) -> None:
        ...

def batch_proc(data: Iterable[bytes], processor: SupportsCall) -> None:
    ...

def good_call(*vals: bytes, max_len: int | None = None) -> None:
    ...

def bad_call(*vals: bytes, maxlen: int) -> None:
    ...

batch_proc([b"foo", b"bar"], good_call) # ok
# wrong signature:
# Argument 2 to "batch_proc" has incompatible type "Callable[[VarArg(bytes), NamedArg(int, 'maxlen')], None]";
# expected "SupportsCall"  [arg-type]
# batch_proc([b"foo", b"bar"], bad_call)

def scale(scalar: int, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

z = scale(2, x)
print(f"{z=}")


y: list[int] = [1, 2, 3]
print(y)

def data_processor() -> Generator[float, float, None]:
    """Process data with dynamic thresholds.
    Yields: current value
    Accepts: new threshold via send()
    """
    threshold = 1.0
    while True:
        value = (lambda : math.floor(random.random() * 10))()  # Imagine this gets data from somewhere
        print(f"Received value: {value}")
        if value > threshold:
            # Yield value and allow threshold adjustment
            new_threshold = yield value
            if new_threshold is not None:
                threshold = new_threshold

# Usage:
processor = data_processor()
for _ in range(15):
    value = next(processor)
    print(f"Processing {value}")
    if value > 7:
        # Adjust threshold if values are too high
        processor.send(value * 0.8)


# Using Sized to indicate that a function expects an object with a __len__ method:
class MyContainer(Sized):
    def __init__(self) -> None:
        self._items: list[int] = []

    def __len__(self) -> int:
        return len(self._items)
    
    def add[T](self, item: T) -> None:
        self._items.append(item)
    
    def mutate_by(self, n: int, operator: Callable[[int], int]) -> Self:
        self._items = [operator(item, n) for item in self._items if isinstance(item, int)]
        return self

def get_length(obj: Sized) -> int:
    return len(obj)

container = MyContainer()
container.add(1)
container.add("2")
container.add({'e': 4})
container = container.mutate_by(2, lambda x, n: x * n)

print(get_length(container))  # 0
print(container._items)  # [2, 4]

# Using ClassVar to declare a class variable:
class MyClass:
    x: int
    y: ClassVar[int] = 0

    def __init__(self, x: int) -> None:
        self.x = x

c = MyClass(1)
print(c.x)  # 1
print(c.y)  # 0
c.y = 20 # error: Cannot assign to class variable "y" via instance
# MyClass.y = 20 # ok
print(c.y)  # 20


# Using Final to indicate that a class variable should not be reassigned:
class Connection:
    host: Final[str] = "localhost"
    port: int = 80

class MyConnection(Connection):
    host: str = "localhost"  # error: Cannot override final attribute "host"
    port: int = 8080  # ok

my_conn = MyConnection()
print(my_conn.host)  # localhost
print(my_conn.port)  # 8080


# Using Never or NoReturn to indicate that a function never returns normally:
def fail() -> NoReturn:
    raise Exception("Failed")

def fail2(n: int) -> int | Never:
    if not n:
        raise Exception("Failed")
    return n

# annotation-def TYPE_CHECKING_func():
#     T = TypeVar("T")
#     def func(arg: T): ...
#     func.__type_params__ = (T,)
#     return func

# func = TYPE_CHECKING_func()

# using covariant, contra-variant, and invariant type variables
class Animal: pass
class Cat(Animal): pass
class Dog(Animal): pass

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class Container(Generic[T_co]):
    def __init__(self, value: T_co) -> None:
        self.value = value

c_o: Container[Animal] = Container(Animal())
c_1: Container[Cat] = Container(Cat())
ani: Container[Animal] = c_1
cat: Container[Cat] = c_o
dog: Container[Dog] = c_o  # error: Incompatible types (expression has type "Container[Animal]", variable has type "Container[Dog]")


# Use invariant when you need exact type matching. Also good for cases where you are both producing and consuming values.
# Use covariant when you're producing/returning values
# Use contravariant when you're consuming/accepting values
class Producer(Generic[T_co]):
    def get(self) -> T_co:
        ...

class Consumer(Generic[T_contra]):
    def put(self, value: T_contra) -> None:
        ...

class PubSub(Generic[T]):
    def get(self) -> T:
        ...
    
    def put(self, value: T) -> None:
        ...

