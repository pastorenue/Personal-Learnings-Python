# python_operators.py
import operator


# print(operator.add(4,5)) # 4+5
# print(operator.__add__(4,5)) # 4+5
# print(operator.truediv(5,2)) # 5/2
# print(operator.ge(5,2)) # 5>=2
# print(operator.eq(5,2)) # 5==2
# print(operator.not_(5<4)) # 5<4
# print(operator.is_(5,2)) # 5==2
# print(bin(operator.and_(0b101, 0b110)))
operators = {
    "-": operator.sub,
    "+": operator.add,
    "*": operator.mul,
    "/": operator.truediv
}

def perform_operation(operator, a, b):
    return operators[operator](a, b)

# print(perform_operation("%", 4, 5))

# import pickle
# with open("operators.pickle", "wb") as f:
#     pickle.dump(operators, f)

# with open("operators.pickle", "rb") as f:
#     ops = pickle.load(f)

musician_dicts = [
    {"id": 1, "fname": "Brian", "lname": "Wilson", "group": "Beach Boys"},
    {"id": 2, "fname": "Carl", "lname": "Wilson", "group": "Beach Boys"},
    {"id": 3, "fname": "Dennis", "lname": "Wilson", "group": "Beach Boys"},
    {"id": 4, "fname": "Bruce", "lname": "Johnston", "group": "Beach Boys"},
    {"id": 5, "fname": "Hank", "lname": "Marvin", "group": "Shadows"},
    {"id": 6, "fname": "Bruce", "lname": "Welch", "group": "Shadows"},
    {"id": 7, "fname": "Brian", "lname": "Bennett", "group": "Shadows"},
]

# get_element_four = operator.itemgetter(4)
# print(get_element_four(musician_dicts))
# get_elements_one_three_five = operator.itemgetter(1, 3, 5)
# print(get_elements_one_three_five(musician_dicts))

# get_names = operator.itemgetter("fname", "lname")
# for m in get_elements_one_three_five(musician_dicts):
#     print(get_names(m))
musician_lists = [
    [1, "Brian", "Wilson", "Beach Boys"],
    [2, "Carl", "Wilson", "Beach Boys"],
    [3, "Dennis", "Wilson", "Beach Boys"],
    [4, "Bruce", "Johnston", "Beach Boys"],
    [5, "Hank", "Marvin", "Shadows"],
    [6, "Bruce", "Welch", "Shadows"],
    [7, "Brian", "Bennett", "Shadows"],
]

get_id = operator.itemgetter(0)
get_elements_two_one = operator.itemgetter(2,1)
get_lname = operator.itemgetter("lname")
get_names = operator.itemgetter("fname", "lname")
# print(min(musician_lists, key=get_id))
# print(max(musician_lists, key=get_id))
# print(min(musician_dicts, key=get_lname))
# # print(max(musician_dicts, key=get_lname))

# print(sorted(musician_lists, key=get_id, reverse=True))
# print("---")
# print(sorted(musician_lists, key=get_elements_two_one, reverse=True))
# print("---")
# print(sorted(musician_dicts, key=get_names, reverse=True))

# Using attrgetter
from dataclasses import dataclass

@dataclass
class Musician:
    id: int
    fname: str
    lname: str
    group: str

    def get_full_name(self, last_name_first=False):
        if last_name_first:
            return f"{self.lname}, {self.fname}"
        return f"{self.fname} {self.lname}"


group_members = [Musician(*musician) for musician in musician_lists]
get_fname = operator.attrgetter("fname")
get_id_name = operator.attrgetter("id", "fname")
get_id = operator.attrgetter("id")
first_last = operator.methodcaller("get_full_name")
last_first = operator.methodcaller("get_full_name", True)

# for person in group_members:
#     print(get_id_name(person))

# for musician in sorted(group_members, key=get_id, reverse=True):
#     print(musician)
for musician in group_members:
    print(last_first(musician))
