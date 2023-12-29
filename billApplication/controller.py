from .model.dataRepresentation import FormData
from .model.dbHandler import DatabaseHandler
from .view.app import App

class Controller:
    def __init__(self) -> None:
        self.model = DatabaseHandler(controller = self)
        self.model.connectToDb(dbName=r"billApplication/bills.db")
        self.model.createTable()
        
        self.view = App(controller = self)

    def insertData(self, data: dict) -> bool:
        fData = FormData(**data)
        if fData.isDefault():
            return False
        
        # data is valid
        self.model.pushToDb(data=fData)
        return True
