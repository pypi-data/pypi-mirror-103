import pymysql
from .Config import Config

class DBConnection:
    db = None
    dbname = ''
    cursor = None
    def __init__(self, dbname):
        self.dbname = dbname

    def connect(self):
        config = Config()
        self.db = pymysql.connect(user=config.get('DB_USER'), passwd=config.get('DB_PASSWORD'), host=config.get('DB_HOST'), db=self.dbname, charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def disconnect(self):
        self.db.close()

    def commit(self):
        self.db.commit()
