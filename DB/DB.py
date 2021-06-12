import os
import pymysql
from DB.query_engine import Query_engine


class DB(Query_engine):
    __cnx = None
    __cursor = None
    __error = None
    __instance = None

    def __init__(self, host=None, username=None, password=None, dbname=None):
        self.__host = host or os.getenv('DB_HOST')
        self.__username = username or os.getenv('DB_USERNAME')
        self.__password = password or os.getenv('DB_PASSWORD')
        self.__dbname = dbname or os.getenv('DB_DBNAME')
        self.__cnx = pymysql.connect(
            host=self.__host,
            user=self.__username,
            password=self.__password,
            database=self.__dbname,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__cnx.autocommit = True

    @classmethod
    def get_instance(cls, host=None, username=None, password=None, dbname=None):
        if cls.__instance is None:
            cls.__instance = cls(host=host, username=username, password=password, dbname=dbname)
        return cls.__instance

    def query(self, sql: str, values: dict):
        self.__cursor = self.__cnx.cursor()
        try:
            self.__cursor.execute(sql, values)
        except (pymysql.Error, pymysql.Warning) as e:
            self.__error = e

    def insert(self, table: str):
        self._table = table
        self._action = "INSERT INTO"
        return self

    def select(self, table: str):
        self._table = table
        self._action = "SELECT"
        return self

    def update(self, table: str):
        self._table = table
        self._action = "UPDATE"
        return self

    def delete(self, table: str):
        self._table = table
        self._action = "DELETE"
        return self

    def exec(self):
        self.__error = None
        self._set_query()
        self.query(self._qb_query, self._qb_values)
        self._reset()
        return self

    def results(self):
        return self.__cursor.fetchall()

    def first(self):
        return self.__cursor.fetchone()

    def error(self):
        return self.__error
