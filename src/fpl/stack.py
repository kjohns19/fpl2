import fpl.variable
import fpl.number
import os
import os.path
import sys

class Stack:
    def __init__(self, path):
        self.path = path
        os.makedirs(path)
        self.__size()

    def __size(self):
        size = fpl.variable.Variable(
                os.path.join(self.path, 'size'),
                default=fpl.number.Number(0),
                do_load=True, do_save=True)
        return size

    def pop(self):
        size = self.__size()
        if size.value.value == 0:
            print('ERROR: Trying to pop from empty stack!', file=sys.stderr)
            return None

        size.value.value -= 1
        size.save()

        valpath = os.path.join(self.path, str(size.value.value))
        val = fpl.variable.Variable(valpath, do_load=True)
        val.delete()
        
        return val.value

    def push(self, value):
        size = self.__size()

        valpath = os.path.join(self.path, str(size.value.value))
        val = fpl.variable.Variable(valpath, value=value, do_save=True)

        size.value.value += 1
        size.save()

    def __str__(self):
        return ''
