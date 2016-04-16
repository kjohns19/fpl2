import fpl.variable
import fpl.value
import os
import os.path
import sys

class Storage:
    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.counter()

    def counter(self):
        counter = fpl.variable.Variable(
            os.path.join(self.path, 'counter'),
            default=fpl.value.Number(0),
            do_load=True, do_save=True)
        return counter

    def get_at(self, count):
        varpath = os.path.join(self.path, str(count))
        var = fpl.variable.Variable(varpath)
        return var

    def get_new(self):
        counter = self.counter()
        var = self.get_at(counter.value.value)
        counter.value.value += 1
        counter.save()
        return var
