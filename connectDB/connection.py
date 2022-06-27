import mysql.connector
from mysql.connector import Error


class Connect:
    __host = "localhost"
    __user = "root"
    __password = ""
    __port = 3306
    __database = "hotel"

    def getconnect(self):
        try:
            connect = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                port=self.__port,
                database=self.__database
            )
            return connect
        except Error as e:
            print(e)
