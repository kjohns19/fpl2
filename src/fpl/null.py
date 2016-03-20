import fpl.value

class Null(fpl.value.Value):
    __singleton = None
    @classmethod
    def deserialize(cls, data):
        if cls._singleton is None:
            cls._singleton = Null()
        return cls._singleton

    def __init__(self):
        pass

    def __str__(self):
        return ''
