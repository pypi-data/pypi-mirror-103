import pandas as pd
import pyodbc


class DatabaseConnection:
    def __init__(self, server, database, query):
        self.conn = None
        self.server = server
        self.database = database
        self.query = query

    def db_connect(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};\
                SERVER=' + self.server + ';\
                DATABASE=' + self.database + ';\
                trusted_connection=yes'
            )
            print("Database connection OK")
            return self.conn
        except:
            print("Problem in database connection")

    def db_query(self):
        try:
            self.result = pd.read_sql_query(self.query, self.conn)
            print("Query syntax OK")
            return self.result
        except:
            print("Problem with SQL query")

    def to_df(self):
        try:
            dataframe = pd.DataFrame(self.result)
            print("Dataframe conversion OK")
            return dataframe
        except:
            print("Problem with dataframe conversion")