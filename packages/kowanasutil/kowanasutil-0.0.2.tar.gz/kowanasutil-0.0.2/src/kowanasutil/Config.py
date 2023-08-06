from .Singleton import Singleton

class Config(metaclass=Singleton):
    configs = None

    def __init__(self, file='/home/ubuntu/workspace/.config'):
        with open(file) as f:
            self.configs = self._parse(f.read())

    def _parse(self, data):
        configs = {}
        lines = data.split('\n')
        for line in lines:
            if '=' not in line: continue
            line = line.replace(' ', '')
            seperated = line.split('=')
            key = seperated[0]
            value = seperated[1]
            configs[key] = value
        return configs

    def get(self, key):
        return self.configs[key]
