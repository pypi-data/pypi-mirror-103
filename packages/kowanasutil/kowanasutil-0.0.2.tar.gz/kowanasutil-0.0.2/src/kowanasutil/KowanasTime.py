from datetime import datetime
from datetime import timedelta

class KowanasTime:
    @classmethod
    def getKST(self, setZeroSec = False, setZeroMin = False, setZeroHour = False):
        now = datetime.now()+timedelta(hours=9)
        if setZeroHour == True:
            now -= timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        elif setZeroMin == True:
            now -= timedelta(minutes=now.minute, seconds=now.second)
        elif setZeroSec == True:
            now -= timedelta(seconds=now.second)
        return now

    @classmethod
    def today(self):
        now = datetime.now()+timedelta(hours=9)
        return now.strftime('%Y%m%d')

    @classmethod
    def getTimeStamp(self):
        return datetime.now().timestamp