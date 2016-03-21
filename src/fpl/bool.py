import fpl.value

class Bool(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        if data == 'False':
            return Bool.false_value()
        return Bool.true_value()
    
    __true = None
    __false = None
    @classmethod
    def true_value(cls):
        if cls.__true is None:
            cls.__true = Bool(True)
        return cls.__true
    @classmethod
    def false_value(cls):
        if cls.__false is None:
            cls.__false = Bool(False)
        return cls.__false

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
