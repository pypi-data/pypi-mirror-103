import os
import threading
from datetime import datetime
from .Singleton import Singleton
from .KowanasTime import KowanasTime

class Log(metaclass=Singleton):
    __lock = threading.Lock()
    __logfile = None
    def __init__(self, logfile = None):
        self.__logfile = logfile
        if self.__logfile != None:
            print ('log' + self.__logfile)
            if os.path.exists(self.__logfile) == False:
                with open(self.__logfile, 'w') as f:
                    f.write('created at '+self.__getNow())

    def __getNow(self):
        return KowanasTime.getKST().strftime('%Y-%m-%d %H:%M:%S')

    def d(self, *log):
        strbuf = ''
        for l in log:
            strbuf += str(l)

        print (strbuf)
#        thread = threading.Thread(target=self.write, args=(log),)
#        thread.start()
        if self.__logfile != None: 
            self.__write(self.__getNow()+': '+strbuf+'\n')

    def __write(self, log):
        self.__lock.acquire()
        with open(self.__logfile, 'a') as f:
            f.write(log)
        self.__lock.release()