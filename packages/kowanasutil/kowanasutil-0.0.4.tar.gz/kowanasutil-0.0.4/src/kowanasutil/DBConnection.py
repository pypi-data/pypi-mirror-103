import pymysql
from .Config import Config

class DBConnection:
    db = None
    dbname = ''
    cursor = None
    def __init__(self, dbname, config):
        self.dbname = dbname
        self.__config = config

    def connect(self):
        config = self.__config
        self.db = pymysql.connect(user=config.get('DB_USER'), passwd=config.get('DB_PASSWORD'), host=config.get('DB_HOST'), db=self.dbname, charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def disconnect(self):
        self.db.close()

    def commit(self):
        self.db.commit()
