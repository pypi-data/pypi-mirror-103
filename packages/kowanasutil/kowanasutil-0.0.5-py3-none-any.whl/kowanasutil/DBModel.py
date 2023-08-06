from abc import ABCMeta

class DBModel(metaclass=ABCMeta):
    __dbConnection = None
    __tablename = None
    __fields = None
    __foreignkeys = None
    _records = {}

    AUTO_INCREMENT = -1
    NO_RECORD = "NO_RECORD"

    String = "VARCHAR"
    Int = "INT"
    Float = "FLOAT"
    Long = "BIGINT"

    def __init__(self, dbConnection, tablename, fields=None, foreignkeys=[], debug=False):
        self.__dbConnection = dbConnection
        self.__tableName = tablename
        self.__foreignkeys = foreignkeys
        self.__debug = debug
        if fields != None:
            self.__fields = fields
            self.__createTable()

    def __createTable(self):
        sql = 'CREATE TABLE if not exists '+self.__tableName+' ('
        for field in self.__fields:
            sql += field.key + ' ' + field.type + '(' + str(field.length) + ') NOT NULL ' + field.autoIncrement + ', '
        sql += 'PRIMARY KEY ('+ self.__fields[0].key +')'
        for foreignkey in self.__foreignkeys:
            sql += ', FOREIGN KEY ('+foreignkey[0]+') REFERENCES '+foreignkey[1]
        sql += ') ENGINE=InnoDB, charset=utf8;'
        return self.__query(sql)

    def __query(self, sql):
        if self.__debug == True:
            print (sql)
        try:
            self.__dbConnection.cursor.execute(sql)
        except Exception as e:
            print (str(e))
            return False
        return True

    def __fetch(self):
        return self.__dbConnection.cursor.fetchall()    

    def commit(self):
        try:
            self.__dbConnection.commit()
        except Exception as e:
            print (e)
            return False
        return True

    def __columnsToString(self, columns):
        sqlcolumns = ''
        if columns != None:
            sqlcolumns = '('+columns+')'
        return sqlcolumns    

    def __whereToString(self, where):
        sqlwhere = ''
        keys= list(where.keys())
        values = list(where.values())
        for key, value in zip(keys, values):
            sqlwhere = sqlwhere + key + '='
            if type(value) is not str:
                value = str(value)
            sqlwhere = sqlwhere + value

    def _insert(self, values, columns = None):
        sqlcolumns = self.__columnsToString(columns)
        sqlvalues = '('+values+')'
        sql = 'INSERT INTO '+self.__tableName+' '+sqlcolumns+' VALUES '+sqlvalues+';'
        return self.__query(sql)

    def _update(self, values, where = None):
        sql = 'UPDATE '+self.__tableName+' SET '+values+' WHERE '+where+';'
#        sql = 'REPLACE INTO '+self.__tableName+' SET '+values+';'
        return self.__query(sql)

    def _select(self, where = None):
        sql = 'SELECT * FROM '+self.__tableName
        if where != None: sql += ' WHERE '+where+';'
        else: sql += ';'
        if self.__query(sql) == False: return []
        return self.__fetch()

    def _delete(self, where):
        sql = 'DELETE FROM '+self.__tableName+' WHERE '+where+';'
        if self.__query(sql) == False: return False
        return True

    # clear table
    def clear(self):
        sql = 'truncate table '+self.__tableName+';'
        self.__query(sql)
        result = self.__dbConnection.cursor.fetchall()
        return result

    def __getStringByFieldType(self, data, field):
        if field.type == DBModel.String:
            return '\"'+data+'\"'
        if field.type == DBModel.Int or field.type == DBModel.Float or field.type == DBModel.Long:
            return str(data)

    # get query string for query
    def _getInsertQuery(self, data):
        if data[0] == DBModel.AUTO_INCREMENT: sql = 'NULL'
        else: sql = self.__getStringByFieldType(data[0], self.__fields[0])
        for index in range(1, len(data)):
            sql += ', ' + self.__getStringByFieldType(data[index], self.__fields[index])
        return sql

    def _getUpdateQuery(self, data):
        sql = ''
        for field, value in zip(self.__fields[1:], data[1:]):
            if field.type == DBModel.String:
                sql += field.key + '=\'' + str(value) + '\','
            else:
                sql += field.key + '=' + str(value) + ','
        return sql[:-1]

    # compare between 2 data
    def equal(self, a, b):
        pass

    # verify data
    def _verify(self, data):
        return True

    # get data from row
    def _fromRow(self, row):
        if len(row) > 0:
            return [row[field.key] for field in self.__fields]
        else: return []

    # convert data to json
    def toJson(self, data):
        return json.dumps(_records)

    # add data to table
    def add(self, data = None, columns = None):
        if self._verify(data) == False: return False
        if self._insert(self._getInsertQuery(data), columns = columns) == False: 
            return False
        return True

    # update record in table
    def update(self, uid, data):
        if self._verify(data) == False: return False
        where = 'uid = \''+str(uid)+'\''
        if self._update(self._getUpdateQuery(data), where = where) == False: 
            return False
        return True

    # read data from table
    def read(self, uid):
        where = 'uid = \''+str(uid)+'\''
        rows = self._select(where)
        if len(rows) <= 0: return False
        return self._fromRow(rows[0])

    def cache(self):
        self._records = self.readAll()

    # read all data from table
    def readAll(self):
        rows = self._select()
        records = []
        for row in rows:
            record = self._fromRow(row)
            records.append(record)
#            records[record[0]] = record
        return records

    def readAllToDict(self):
        rows = self._select()
        records = {}
        for row in rows:
            record = self._fromRow(row)
            records[record[0]] = record
        return records

    # delete record in table
    def delete(self, uid):
        where = 'uid = '+str(uid)
        return self._delete(where)
