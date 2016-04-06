import fpl.value
import fpl.utils
import glob
import os

class Object(fpl.value.Value):
    def __init__(self):
        self.value = {}

    def load(self, path):
        self.value = {path: None for path in glob.glob(os.path.join(path, '*'))}

    def save(self, filename):
        fpl.utils.clear_path(filename)
        os.mkdir(filename)
        for path, value in self.value.items():
            newpath = os.path.join(filename, os.path.basename(path))
            value = fpl.value.Value.load(path)
            value.save(newpath)

    def print(self):
        print('<object>')

fpl.value.Value.register_type('Object', Object)
