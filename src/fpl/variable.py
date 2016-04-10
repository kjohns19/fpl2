import fpl.value
import fpl.utils
import fpl.error
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
        self.value = fpl.value.Value.load(self.path)
        return self.value

    def save(self):
        if self.value:
            self.value.save(self.path)

    def delete(self):
        fpl.utils.clear_path(self.path)

    def is_tmp(self):
        return '/_tmp/' in self.path
