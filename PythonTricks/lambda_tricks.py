# lambda_tricks.py
from functools import reduce

# print(help(reduce))
print(reduce(lambda x,b: x+b, [1, 2, 3, 4]))
print(list(filter(lambda x: x%2==0, [1, 2, 3, 4])))
print(list(map(lambda x: x**2, [1, 2, 3, 4])))