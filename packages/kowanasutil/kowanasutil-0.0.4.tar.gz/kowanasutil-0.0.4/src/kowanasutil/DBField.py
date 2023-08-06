class DBField:
    AutoIncrement = 'AUTO_INCREMENT'
    def __init__(self, key, dtype, length, autoIncrement = ''):
        self.key = key
        self.type = dtype
        self.length = length
        self.autoIncrement = autoIncrement