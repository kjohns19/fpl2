import fpl.utils
import fpl.error
import glob
import os
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
            obj = Object()
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


class Function(Value):
    @staticmethod
    def deserialize(data):
        split = data.split('\n')
        args = list(reversed(split[0].split()))
        code_start = int(split[1])
        return Function(args, code_start)

    def __init__(self, args, code_start):
        self.args = args
        self.code_start = code_start

    def call(self, program):
        stack = program.stack
        arguments = [stack.pop().value for i in range(len(self.args))]
        program.jump_change_dir('_', self.code_start)
        for arg, name in zip(arguments, self.args):
            var = fpl.variable.Variable(name, arg)
            var.save()

    def print(self):
        print('<function>')

    def __str__(self):
        return ' '.join(reversed(self.args)) + '\n' + str(self.code_start)
Value.register_type('Function', Function)


class NoneType(Value):
    @staticmethod
    def deserialize(data):
        return NoneType.singleton()

    __singleton = None
    @classmethod
    def singleton(cls):
        if cls.__singleton is None:
            cls.__singleton = NoneType()
        return cls.__singleton

    def __init__(self):
        self.value = None

    def print(self):
        print('<none>')

    def is_true(self):
        return False

    def __str__(self):
        return ''
Value.register_type('NoneType', NoneType)


class Number(Value):
    @staticmethod
    def deserialize(data):
        if data == 'False':
            value = 0
        elif data == 'True':
            value = 1
        else:
            value = int(data)
        return Number(value)

    def __init__(self, value):
        self.value = value

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)
Value.register_type('Number', Number)


class Object(Value):
    def __init__(self):
        self.value = {}

    def load(self, path):
        self.value = {path: None for path in glob.glob(os.path.join(path, '*'))}

    def load_all(self):
        for path in self.value.keys():
            value = Value.load(path)
            if isinstance(value, Object):
                value.load_all()
            self.value[path] = value

    def save(self, filename):
        fpl.utils.clear_path(filename)
        os.mkdir(filename)
        for path, value in self.value.items():
            newpath = os.path.join(filename, os.path.basename(path))
            value = value or Value.load(path)
            value.save(newpath)

    def __str__(self):
        return 'obj'

    def print(self):
        print('<object>')
Value.register_type('Object', Object)


class Operator(Value):
    __operators = {}
    @classmethod
    def add_operator(cls, name, func):
        cls.__operators[name] = Operator(name, func)

    @classmethod
    def get_operator(cls, name):
        return cls.__operators.get(name)

    @classmethod
    def deserialize(cls, data):
        return cls.__operators[data]

    def apply(self, program):
        self.func(program)

    def __init__(self, symbol, func):
        self.symbol = symbol
        self.func = func

    def __str__(self):
        return self.symbol
Value.register_type('Operator', Operator)


class Pointer(Value):
    @staticmethod
    def deserialize(data):
        return Pointer(data)

    def __init__(self, value):
        self.value = os.path.abspath(value)

    def __str__(self):
        return self.value
Value.register_type('Pointer', Pointer)


class String(Value):
    @staticmethod
    def deserialize(data):
        return String(data)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
Value.register_type('String', String)


class Symbol(Value):
    @staticmethod
    def deserialize(data):
        return Symbol(data)

    def __init__(self, value):
        self.value = value

    def apply(self, program):
        var = fpl.variable.Variable(self.value)
        program.stack.push(var)

    def __str__(self):
        return self.value
Value.register_type('Symbol', Symbol)

