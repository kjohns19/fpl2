import fpl.value

class NoneType(fpl.value.Value):
    @staticmethod
    def deserialize(data):
        return NoneType.value()

    __singleton = None
    @classmethod
    def value(cls):
        if cls.__singleton is None:
            cls.__singleton = NoneType()
        return cls.__singleton

    def __init__(self):
        pass

    def __str__(self):
        return ''