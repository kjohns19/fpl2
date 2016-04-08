import fpl.utils
import fpl.error
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
            raise fpl.error.Error('Invalid type: ' + classname)
        return cls.deserialize(args)

    @staticmethod
    def load(filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = f.read()
                return Value.deserialize(data)
        elif os.path.isdir(filename):
            obj = fpl.object.Object()
            obj.load(filename)
            return obj
        else:
            raise fpl.error.Error('Invalid filename: ' + filename)

    def save(self, filename):
        fpl.utils.clear_path(filename)
        with open(filename, 'w') as f:
            f.write(self.serialize())

    def apply(self, program):
        var = program.tmpdir.get_new()
        var.value = self
        var.save()
        program.stack.push(var)

    def print(self):
        print(self.value)

    def is_true(self):
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<' + type(self).__name__ + '>'

    def serialize(self):
        return type(self).__name__ + '\n' + str(self)
