import inspect

def get_frame(frame,event,args):
    if frame:
        print(inspect.getouterframes(frame))

    return get_frame

import sys

def foo(a,b):
    c = a+b
    print(c)

sys.settrace(get_frame(None,None,None))
foo(1,2)
