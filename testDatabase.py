from database.dbHandler import DatabaseHandler

db = DatabaseHandler()
db.connectToDb(dbName='database/bills.db')
print(db.companyNames())
db.close()