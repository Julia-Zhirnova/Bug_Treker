import os
import sqlite3
from sqlite3 import Error


class Database(object):
    def __init__(self, connection):
        super(Database, self).__init__()
        self.connect = connection
        self.db_direction = os.path.join(os.getcwd(), 'db', 'data_file.db')

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_direction)
            self.connect = conn
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, create_table_sql):
        try:
            conn = self.connect
            c = conn.cursor()
            c.execute(create_table_sql)
            return c
        except Error as e:
            print(e)
