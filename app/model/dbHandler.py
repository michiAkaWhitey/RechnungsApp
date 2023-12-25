import sqlite3
from app.model.dataRepresentation import FormData

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


    def _execute(self, command: str, args: tuple) -> None:
        '''excecutes a given command'''
        self.cursor.execute(command, args)
        self.con.commit()




