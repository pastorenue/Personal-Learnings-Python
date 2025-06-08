from collections import defaultdict, ChainMap


def find(seq, target):
    for i,value in enumerate(seq):
        if value == target:
            break
    else:
        return -1
    return 1


def find_with_sentinel(seq, target):
    """Find element in list using Sentinel."""
    found = False
    for i,value in enumerate(seq):
        if value == target:
            found = True
            break
    if not found:
        return -1
    return 1


print("--------Using Zip-------------")
print(dict(zip(["a", "b"], [5, 8])))
print("----END-----\n")
print("---Using Dictionary items attribute---")

d = {"a": 1, "b": 2, "c": 3}
for i,v in d.items():
    print(i, "-->", v)
print("-----END----\n")
print("----Count Frequency of Items in a List------")

d = {}
l = [1,3,2,4,2,5,3,2,5,5,3,6,3,3,5,4,3,3,5,3,6,3,6,3,3,53,43,5,3,6,4,5]
for i in l:
    d[i] = d.get(i, 0) + 1
print(d)
# Or use defaultdict
print("--------DefaultDict--------")
d = defaultdict(int)
for i in l:
    d[i] += 1
print(d)
print("----END----\n")
print("-------Grouping Items in a list with Dictionaries---------")
ls = ["matheo", "liean", "man", "groupon", "feil"]
d = {}
for n in ls:
    key = len(n) # This can be anything e.g. first letter, names with number of e, or even exact value of name
    if key not in d:
        d[key] = []
    d[key].append(n)
print(d)
print("----END----")
print("--------Use setdefault-----")
ds = {}
for n in ls:
    key = len(n)
    ds.setdefault(key, []).append(n)
print(ds)
print("----END----")
print("-----Or Better still use the DefaultDict------")
dd = defaultdict(list)
for n in ls:
    key = len(n)
    dd[key].append(n)
print(dd)
print("----END-----")
print("----Doing loop without loop but recursive calls-----")


def find_with_counter(seq, target, counter = 0):
    """Find element in list using Recursive call with counter to keep track of index."""
    if counter < len(seq):
        if seq[counter] == target:
            return 1
        else:
            counter += 1
            return find_with_counter(seq, target, counter=counter)
    else:
        return -1

print(find_with_counter([1,2,3], 1))
print("---END-----")
print("--------Using ChainMap-------------")
a = {"a":1, "b":4} # default
b = {"c": 2, "d": 5} # medium priority
c = {"a": 7, "d": 12} # highest priority
cm = ChainMap(c, b, a)
print(cm)
print(dir(cm))
print("----END-----")
