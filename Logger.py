import os
from threading import Lock
import Utils


class Logger:
    # ***************** singleton ****************
    _instance = None

    def __new__(cls, *args, **kw):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def __init__(self, path):
        self.path = path
        logPath = os.path.join(self.path, self.logName)
        self.file = open(logPath, mode='a+', encoding='utf-8')

    def __del__(self):
        if self.file is not None:
            self.file.close()

    # ******************* feature field *****************
    logName = 'log'
    path = None
    file = None
    lock = Lock()
    MES_TYPE = {'ERROR': '[ERROR]', 'WARNING ': '[WARNING] ', 'INFO': '[INFO]'}

    # ******************* method field *****************
    def fileLog(self, mesType, *mes):
        con = [].append(Utils.getDateStr(), mesType, mes)
        con = con + '\n'
        self.lock.acquire()
        self.file.writelines(con)
        self.lock.release()

    def consoleLog(self, mesType, *mes):
        con = [].append(Utils.getDateStr(), mesType, mes)
        con = con + '\n'
        print(con)

    def logging(self, mesType, *mes):
        self.fileLog(type, mes)
        self.consoleLog(type, mes)


