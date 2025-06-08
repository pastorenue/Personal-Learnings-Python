import pickle
with open("operators.pickle", "rb") as f:
    ops = pickle.load(f)

print(ops)

def perform_operation(operator, a, b):
    return ops[operator](a, b)

print(perform_operation("+", 4, 5))
# built-in operators > operators > lambda operators