class Stack[T]:
    def __init__(self) -> None:
        self.stack: list[T] = []

    def push(self, item: T) -> None:
        """
        Add an item to the stack.

        :param item: the item to add to the stack
        """
        self.stack.append(item)

    def pop(self) -> T:
        """
        Remove and return the last item from the stack.

        Raises:
            IndexError: if the stack is empty
        """
        return self.stack.pop()

    def peek(self) -> T:
        """
        Return the last item from the stack without removing it.

        Raises:
            IndexError: if the stack is empty
        """
        return self.stack[-1]