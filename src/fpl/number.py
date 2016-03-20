import fpl.value

class Number(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        return Number(int(data))

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
