import fpl.utils
import importlib
import os.path

class Value:
    __types = {}
    @classmethod
    def register_type(cls, name, type):
        cls.__types[name] = type
    @staticmethod
    def deserialize(data):
        classname, args = data.split('\n', 1)
        cls = Value.__types.get(classname)
        if cls is None:
            #TODO error
            print('Invalid type: ' + classname)
            return None
        return cls.deserialize(args)

    @staticmethod
    def load(filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = f.read()
                return Value.deserialize(data)
        elif os.path.isdir(filename):
            #TODO create object
            pass
        else:
            print('Invalid filename: ' + filename)
            return None

    def save(self, filename):
        fpl.utils.clear_path(filename)
        with open(filename, 'w') as f:
            f.write(self.serialize())

    def apply(self, program):
        var = program.tmpdir.get_new()
        var.value = self
        var.save()
        program.stack.push(var)

    def is_true(self):
        return True

    def __repr__(self):
        return str(self)

    def serialize(self):
        return type(self).__name__ + '\n' + str(self)
