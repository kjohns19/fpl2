import fpl.variable
import fpl.number
import os
import os.path
import sys

class Storage:
    def __init__(self, path):
        self.path = path
        os.makedirs(path)
        self.counter()

    def counter(self):
        counter = fpl.variable.Variable(
            os.path.join(self.path, 'counter'),
            default=fpl.number.Number(0),
            do_load=True, do_save=True)
        return counter

    def get(self, count):
        varpath = os.path.join(self.path, str(count))
        var = fpl.variable.Variable(varpath)
        return var
