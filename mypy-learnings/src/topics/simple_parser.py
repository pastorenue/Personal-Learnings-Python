import libcst as cst

code = """
def add(a, b):
    return a + b
"""

tree = cst.parse_module(code)
print(tree)