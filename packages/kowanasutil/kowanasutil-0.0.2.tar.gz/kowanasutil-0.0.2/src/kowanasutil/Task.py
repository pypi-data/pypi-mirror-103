from datetime import datetime
from datetime import timedelta

class Task:
    def __init__(self, name, handler, args, schedule=None):
        self.name = name
        self.__handler = handler
        self.__args = args
        self.schedule = schedule

    def run(self):
        self.__handler(self.__args)