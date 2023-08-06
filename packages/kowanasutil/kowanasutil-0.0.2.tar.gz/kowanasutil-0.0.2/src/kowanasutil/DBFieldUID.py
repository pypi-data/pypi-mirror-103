from .DBField import DBField

class DBFieldUID(DBField):
    def __init__(self, dtype, length, autoIncrement = ''):
        super().__init__('uid', dtype, length, autoIncrement = autoIncrement)