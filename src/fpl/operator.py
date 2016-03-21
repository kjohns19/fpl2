import fpl.value

class Operator(fpl.value.Value):
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
        self.symbol = symbol;
        self.func = func

    def __str__(self):
        return self.symbol

fpl.value.Value.register_type('Operator', Operator)
