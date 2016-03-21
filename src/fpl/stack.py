class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)

    def __str__(self):
        return str(self.stack)
