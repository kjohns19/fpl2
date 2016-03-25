import fpl.value
import fpl.utils
import os.path
import sys

class Variable:
    def __init__(self, path, default=None, value=None, do_load=False, do_save=False):
        self.path = path
        loaded = False
        self.value = value
        if not value and os.path.exists(path):
            if do_load:
                self.load()
                loaded = True
        elif default:
            self.value = default

        if not loaded and self.value and do_save:
            self.save()

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
            self.value.save(self.path)

    def delete(self):
        fpl.utils.clear_path(self.path)
