from abc import ABC, abstractmethod
import os


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name
    
    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)
    
    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value!r} to be one of {self.options!r}")


class Number(Validator):

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f'Expected {value} to be at least {self.min_value}')

        if self.max_value is not None and value > self.max_value:
            raise ValueError(f'Expected {value} to be at most {self.max_value}')


class String(Validator):

    def __init__(self, min_length=None, max_length=None, predicate=None):
        self.min_length = min_length
        self.max_length = max_length
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f'Expected {value!r} to be a string')

        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f'Expected {value!r} to be at least {self.min_length} characters')

        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f'Expected {value!r} to be at most {self.max_length} characters')

        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {value!r} to be match {self.predicate}')


class DataDescriptor:
    def __init__(self, value):
        self.value = value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"Retrieving value: {self.value} from {obj} through {objtype}")
        return self.value

    def __set__(self, obj, value):
        self.value = value


class TestDesc:

    def __init__(self, value):
        self.value = value


class Coordinate:
    def __get__(self, obj, owner):
        print('__get__ called')

    def __set__(self, obj, value):
        print('__set__ called')


class Point:
    x = Coordinate()
    y = Coordinate()

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Component:
    name = String(min_length=3, max_length=10, predicate=None)
    size = Number(min_value=1, max_value=100)
    quantity = Number(min_value=1)
    status = OneOf('new', 'used', 'refurbished')
    test = TestDesc('test')
    d1 = DataDescriptor(10)


    def __init__(self, name, size, quantity, status):
        self.name = name
        self.size = size
        self.quantity = quantity
        self.status = status


class Ten:
    """A descriptor that returns 10"""

    def __get__(self, obj, objtype=None):
        return 10

class Example:
    x = 5
    y = Ten()


class DynamicSize:
    def __get__(self, obj, objtype=None):
        return len(os.listdir(obj.dirname))


class Directory:
    size = DynamicSize()
 
    def __init__(self, dirname):
        self.dirname = dirname

class LoggedAgeAccess:
    def __get__(self, obj, objtype=None):
        value = obj._age
        print(f'Accessing {value!r}')
        return value

    def __set__(self, obj, value):
        print(f'Updating {value!r}')
        obj._age = value


class Person:
    age = LoggedAgeAccess()

    def __init__(self, name, age):
        self.age = age
        self.name = name


class Property:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.getter(obj)


class ClassMethod:
    def __init__(self, method):
        self.method = method

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.method
        return lambda *args, **kwargs: self.method(obj, *args, **kwargs)


class StaticMethod:
    def __init__(self, method):
        self.method = method

    def __get__(self, obj, objtype=None):
        return self.method



if __name__ == '__main__':
    mary = Person('Mary', 30)
    dave = Person('Dave', 40)
    print(vars(mary))
    print(vars(dave))

    # Test the Component class
    c = Component('screw', 10, 100, 'new')
    print(vars(c))
    print(Component.__getattribute__(c, 'name'))
    print(c.test.__dict__)
    print(c.d1)
    print(Component.d1)
    
    # Test the Point class
    print("Point class")
    p = Point(2, 3)
    print(vars(p))
    print("Point.__dict__: ", Point.__dict__)
    print("Point.__getattribute__ for x", Point.__getattribute__(p, 'x'))
    print("Point.__getattribute__ for y", Point.__getattribute__(p, 'y'))
    print(p.x)
    print(p.y)
