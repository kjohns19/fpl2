import fpl.storage
import fpl.variable
import fpl.number
import os
import os.path
import sys

class Stack:
    def __init__(self, path):
        self.storage = fpl.storage.Storage(path)

    def pop(self):
        size = self.storage.counter()
        if size.value.value == 0:
            print('ERROR: Trying to pop from empty stack!', file=sys.stderr)
            return None

        size.value.value -= 1
        size.save()

        val = self.storage.get(size.value.value)
        val.load()
        val.delete()
        
        return val.value

    def push(self, value):
        size = self.storage.counter()

        val = self.storage.get(size.value.value)
        val.value = value
        val.save()

        size.value.value += 1
        size.save()

    def debug(self):
        size = self.storage.counter()
        print([ self.storage.get(i).load() for i in range(0, size.value.value) ])
