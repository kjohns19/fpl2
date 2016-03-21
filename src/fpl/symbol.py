import fpl.value

class Symbol(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        return Symbol(data)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

fpl.value.Value.register_type('Symbol', Symbol)
