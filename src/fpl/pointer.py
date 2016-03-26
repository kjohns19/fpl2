import fpl.value

class Pointer(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        return Pointer(data)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

fpl.value.Value.register_type('Pointer', Pointer)
