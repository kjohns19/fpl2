import importlib

class Value:
    @staticmethod
    def deserialize(data):
        classname, args = data.split('\n', 1)
        module = importlib.import_module('value')
        cls = getattr(module, classname)
        return cls.deserialize(args)

    def apply(self, program):
        program.stack.push(self)

    def serialize(self):
        return type(self).__name__ + '\n' + str(self)
