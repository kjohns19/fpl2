import fpl.value

class NoneType(fpl.value.Value):
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

    def is_true(self):
        return False

    def __str__(self):
        return ''

fpl.value.Value.register_type('NoneType', NoneType)
