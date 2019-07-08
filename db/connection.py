""" Mysql Module """
from mysql.connector import connect
from .config import Config


class Database:
    def __init__(self):
        config = Config()
        self.host = config.host
        self.user = config.user
        self.password = config.password
        self.database = config.database

    def get_connection(self):
        connection = connect(host=self.host, user=self.user,
                             passwd=self.password, database=self.database)

        return connection

    def get_all_data(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
