import os
import sqlite3
import pyodbc
from sqlite3 import Error


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class dc_database:
    def select_sql(self, sql):
        self.conn = self.create_dc_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_sql_dict(self, sql):
        self.conn = self.create_dc_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)

        desc = self.cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in self.cur.fetchall()]
        return data

    def execute_sql(self, sql):
        self.conn = self.create_dc_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def create_dc_connection(self):
        try:
            conn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={server}; database={database}; \
                                   trusted_connection=no;UID={uid};PWD={pwd}".format(server="10.96.101.10",
                                                                                     database="DC_Dev",
                                                                                     uid="noah_dev",
                                                                                     pwd="noah_dev"))
            return conn
        except Error as e:
            print(e)

        return None


class sqlite_database:
    def execute_sql(self, sql):
        self.conn = self.create_sqlite_connection(BASE_DIR + "\\db.sqlite3")
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def select_sql_dict(self, sql):
        self.conn = self.create_sqlite_connection(BASE_DIR + "\\db.sqlite3")
        self.cur = self.conn.cursor()
        self.cur.execute(sql)

        desc = self.cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in self.cur.fetchall()]
        return data

    def create_sqlite_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)

            return conn
        except Error as e:
            print(e)

        return None