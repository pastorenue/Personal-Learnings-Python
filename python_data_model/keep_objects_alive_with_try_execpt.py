import sys
import weakref

def function_that_raises():
    global x
    x = [1, 2, 3]  # This list will be referenced in the stack frame
    raise Exception("An error occurred")

def main():
    try:
        function_that_raises()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"Exception caught: {e}")
        print(f"Traceback object: {exc_traceback}")
        print(f"Exception type: {exc_type}")
        print(f"Exception value: {exc_value}")

        # Weak reference to check if the list is still alive
        frame_f = exc_traceback.tb_frame.f_back.f_locals["function_that_raises"]
        print(f"The attributes of the frame: {frame_f.__code__.co_varnames}")
        # x = frame.f_locals['x']
        # x_ref = weakref.ref(x)
        # print(f"References to the list inside the except block: {sys.getrefcount(x)}")
        return

# Run the main function and get the weak reference to the list
x_ref = main()

# Check if the list is still referenced
print(f"Is the list still alive after except block? {x_ref() is not None}")

# Deleting the exception information to allow garbage collection
del x_ref
del sys.exc_info

print(f"Is the list still alive after deleting exception info? {x_ref() is not None}")
