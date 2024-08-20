import sqlite3
from typing import List
from .dataRepresentation import Bill

class DatabaseHandler():
    def __init__(self) -> None:
        self._tableName = "bills"
        
    def connectToDb(self, dbName: str) -> None:
        '''connects to a database and creates a cursor'''
        self.con = sqlite3.connect(dbName, check_same_thread=False)
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

    
    def _execute(self, command: str, args: tuple) -> None:
        '''excecutes a given command'''
        self.cursor.execute(command, args)
        self.con.commit()

    def pushToDb(self, bill: Bill) -> None:
        '''inserts data to the table '''
        command = """INSERT INTO bills 
        ("date", "price", "company", "tags", "img")
        VALUES (?,?,?,?,?)"""
        self._execute(command, bill.toTuple())

    def returnMetaData(self):
        command = """SELECT date, price, company, tags FROM bills """
        self._execute(command, ())
        rows = self.cursor.fetchall()
        return rows
    
    def companyNames(self) -> list:
        command = """SELECT DISTINCT company FROM bills"""
        self._execute(command, ())
        data = self.cursor.fetchall()
        return [x[0] for x in data]

    @property
    def column_names(self) -> list:
        '''returns all the column names from the used table'''
        return ("date", "price", "company", "tags")
    

if __name__ == '__main__':
    pass





