from datetime import datetime, timedelta
from .KowanasTime import KowanasTime

class Scheduler:
    TERM_DAY = 'day'
    TERM_HOUR = 'hour'
    TERM_MIN = 'min'
    TERM_SECOND = 'second'

    def __init__(self, every=None, term=None, begin=None):
        self.schedule = [] 
        self.every = every
        self.term = term
        self.begin = begin

    def setNext(self):
        if len(self.schedule) <= 0:
            self.setBeginTime()

    def setBeginTime(self, plus = 0):
        currentTime = KowanasTime.getKST()
        if self.term == Scheduler.TERM_DAY: 
            beginTime = datetime(year=currentTime.year, month=currentTime.month, day=currentTime.day, hour=0, minute=0, second=0) + timedelta(days=plus)
        elif self.term == Scheduler.TERM_HOUR:
            beginTime = datetime(year=currentTime.year, month=currentTime.month, day=currentTime.day, hour=currentTime.hour, minute=0, second=0) + timedelta(hours=plus)
        elif self.term == Scheduler.TERM_MIN:
            beginTime = datetime(year=currentTime.year, month=currentTime.month, day=currentTime.day, hour=currentTime.hour, minute=currentTime.minute, second=0) + timedelta(minutes=plus)
        elif self.term == Scheduler.TERM_SECOND:
            beginTime = datetime(year=currentTime.year, month=currentTime.month, day=currentTime.day, hour=currentTime.hour, minute=currentTime.minute, second=currentTime.second) + timedelta(seconds=plus)
        self.schedule = [beginTime + every for every in self.every]
        removeCount = 0
        for schedule in self.schedule:
            if schedule < currentTime: removeCount+=1
        self.schedule = self.schedule[removeCount:]
        if len(self.schedule) <= 0: self.setBeginTime(plus=1)

    def getNext(self):
        self.setNext()
        nextTime = self.schedule[0]
        if self.begin != None:
            begin = self.begin
            self.begin = None
            return begin
        return nextTime

    def clearNext(self):
        self.schedule.remove(self.schedule[0])

    @classmethod
    def everysec(self, s):
        return [timedelta(seconds=x) for x in range(0, 60, s)]

    @classmethod
    def everymin(self, m):
        return [timedelta(minutes=x) for x in range(0, 60, m)]