from util import Singleton

class SingletonClass(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name;    