from typing import NewType
import inspect

UserID = NewType("UserID", int)


class A:
    a: int = 1
    b: str = "b"

    def __init__(self):
        print(self.a)

    def foo(self):
        print(self.a)


def get_user_name(user_id: UserID) -> str:
    ...

# some_id = UserID(1)
# get_user_name(some_id)
# print(
#     inspect.getmembers(A, inspect.isfunction)
# )
# print(
#     inspect.getmembers_static(A)
# )

print(
    inspect.markcoroutinefunction(get_user_name)
)