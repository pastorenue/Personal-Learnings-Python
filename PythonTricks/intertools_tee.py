# itertools_tee.py
from itertools import tee
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
count = 0
for x in tee(a, 25):
    count += 1
    print(x)
print(count)