import sqlite3
from typing import List
from billApplication.model.dataRepresentation import FormData

class DatabaseHandler():
    def __init__(self) -> None:
        self._tableName = "bills"
        
    def connectToDb(self, dbName: str) -> None:
        '''connects to a database and creates a cursor'''
        self.con = sqlite3.connect(dbName)
        self.cursor = self.con.cursor()

    def close(self) -> None:
        '''closes the cursor and connection'''
        self.cursor.close()
        self.con.close()

    def createTable(self) -> None:
        '''creates a table with all necessary datatypes'''
        command = """CREATE TABLE IF NOT EXISTS bills
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date TEXT, price NUMERIC, company TEXT, tags TEXT, img BLOB)"""
        self._execute(command, ())

    def insertData(self, data: FormData) -> None:
        '''inserts data to the table '''
        command = """INSERT INTO bills 
        ("date", "price", "company", "tags", "img")
        VALUES (?,?,?,?,?)"""

        self._execute(command, data.toTuple())

    def getColumnNames(self) -> list:
        '''returns all the column names from the used table'''
        return ("date", "price", "company", "tags")
    
    def returnMetaData(self):
        command = """SELECT date, price, company, tags FROM bills """
        self._execute(command, ())
        rows = self.cursor.fetchall()
        return rows
    
    def _execute(self, command: str, args: tuple) -> None:
        '''excecutes a given command'''
        self.cursor.execute(command, args)
        self.con.commit()




