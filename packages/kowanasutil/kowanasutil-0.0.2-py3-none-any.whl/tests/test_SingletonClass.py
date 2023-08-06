from .SingletonClass import SingletonClass
from threading import Thread

def run(name, result):
    singleton = SingletonClass(name)
    result[0] = str(singleton)

def test_Singleton():
    resultA = ['A']
    resultB = ['B']
    processa = Thread(target=run, args=('ACLASS', resultA))
    processb = Thread(target=run, args=('BCLASS', resultB))
    processa.start()
    processb.start()
    assert(resultA[0] == resultB[0])