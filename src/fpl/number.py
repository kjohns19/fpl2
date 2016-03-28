import fpl.value

class Number(fpl.value.Value):
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

fpl.value.Value.register_type('Number', Number)
