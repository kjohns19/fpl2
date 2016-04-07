import fpl.value

class String(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        return String(data)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

fpl.value.Value.register_type('String', String)
