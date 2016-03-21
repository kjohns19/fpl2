import importlib

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

    def apply(self, program):
        program.stack.push(self)

    def __repr__(self):
        return str(self)

    def serialize(self):
        return type(self).__name__ + '\n' + str(self)
