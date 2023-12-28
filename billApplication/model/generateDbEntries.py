from billApplication.model.dbHandler import DatabaseHandler
from billApplication.model.dataRepresentation import FormData
import cv2
import random

hand = DatabaseHandler()
hand.connectToDb(dbName=r"app/bills.db")
hand.createTable()

filename = "data/hervis.jpg"
img = cv2.imread(filename)
if img is None: 
    print("Img is None")
    exit()

for i in range(50):
    p = FormData(
        date="22.12.23",
        price=random.uniform(10.00, 200.00),
        company=random.choice(["Hervis", "Obi", "Billa","Spar", "Hofer","Edeka"]),
        tags=random.choices(["Sport", "Weihnachten","Elektronik","sonst","tanken","div"],k=2),
        img=img)
    print(f"Inserted to db = {p}")
    hand.insertData(data=p)
print("Success")