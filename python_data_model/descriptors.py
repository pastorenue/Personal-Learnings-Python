class PositiveInteger:
    """Positive integer descriptor"""

    def __init__(
        self,
        verbose: str = None,
        name: str = None,
        locale: str = "en_US",
        default: int = 0,
        description: str = None,
    ):
        self.verbose = verbose
        self.name = name
        self.locale = locale
        self.default = default
        self.description = description

    def __set_name__(self, owner, name):
        if self.name:
            self.name = name
        if self.verbose:
            self.var_name = self.verbose
        else:
            self.var_name = f"_{name}"

    def __get__(self, instance, objtype=None):
        print(instance, objtype)
        if instance is None:
            return self
        return getattr(instance, self.var_name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Only positive values are allowed")
        setattr(instance, self.var_name, value)


class Person:
    """Person implementation of a descriptor"""
    age = PositiveInteger(
        verbose="Age",
        name="age",
        locale="en_US",
        default=1,
        description="Person's age"
    )

    def __init__(self, age=0):
        self.age = age

if __name__ == "__main__":
    person = Person(age=10)

    print(person.age)
