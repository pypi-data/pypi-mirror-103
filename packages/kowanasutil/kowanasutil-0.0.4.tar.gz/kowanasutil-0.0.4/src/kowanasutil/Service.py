import time
import threading
from datetime import datetime
from datetime import timedelta

from abc import ABCMeta
from .Log import Log
from .Task import Task
from .KowanasTime import KowanasTime

class Service(metaclass=ABCMeta):
    _name = ''
    _tasks = {}
    def __init__(self, name):
        self._name = name
        self.__log = Log()

    def _addTask(self, task):
        self._tasks[task.name] = task

    def run(self):
        threading.Thread(target=self.__run).start()

    def __run(self):
        while True:
            nextSchedule = None
            for task in list(self._tasks.values()):
                expectSchedule = task.schedule.getNext()
                if expectSchedule < KowanasTime.getKST():
                    task.schedule.clearNext()
                    task.run()
                    expectSchedule = task.schedule.getNext()
                if nextSchedule == None or expectSchedule < nextSchedule:
                    nextSchedule = expectSchedule
            self._waitUntil(nextSchedule)        

    def _handle(self):
        pass

    def _wait(self, duration):
        time.sleep(duration)

    def _waitUntil(self, until):
#        self.__log.d('current time '+KowanasTime.getKST().strftime('%Y-%m-%d %H:%M:%S'))
#        self.__log.d('wait until '+until.strftime('%Y-%m-%d %H:%M:%S'))
        now = KowanasTime.getKST()
        if now < until:
            remained = until - now
            self.__log.d('waiting for '+str(remained.total_seconds())+' seconds')
            time.sleep(remained.total_seconds())