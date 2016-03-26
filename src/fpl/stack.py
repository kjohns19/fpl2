import fpl.storage
import fpl.variable
import fpl.pointer
import os
import os.path
import sys

class Stack:
    def __init__(self, path):
        self.storage = fpl.storage.Storage(path)

    def pop(self, do_load=True):
        size = self.storage.counter()
        if size.value.value == 0:
            print('ERROR: Trying to pop from empty stack!', file=sys.stderr)
            return None

        size.value.value -= 1
        size.save()

        pointer = self.storage.get_at(size.value.value)
        pointer.load()
        pointer.delete()

        path = pointer.value.value
        val = fpl.variable.Variable(path)
        if do_load:
            val.load()
        #TODO better check for this
        if '_tmp' in val.path:
            val.delete()
        
        return val

    def push(self, variable):
        size = self.storage.counter()

        pointer = self.storage.get_at(size.value.value)
        pointer.value = fpl.pointer.Pointer(variable.path)
        pointer.save()

        size.value.value += 1
        size.save()

    def debug(self):
        size = self.storage.counter()
        print([ self.storage.get_at(i).load() for i in range(0, size.value.value) ])
