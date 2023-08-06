class Undefined:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __repr__(self):
        return '<undefined>'

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not isinstance(other, self.__class__)

    def __hash__(self):
        return hash(id(self))


undefined = Undefined()
__all__ = ('undefined',)
