import fpl.value
import os.path
import sys

class Variable:
    def __init__(self, path, value=None):
        self.path = path
        self.value = value

    def load(self):
        if os.path.exists(self.path):
            self.value = fpl.value.Value.load(self.path)
        else:
            #TODO maybe throw something here
            print('ERROR: Path ' + self.path + ' does not exist', file=sys.stderr)
            self.value = None
        return self.value

    def save(self):
        if self.value:
            self.value.save()
