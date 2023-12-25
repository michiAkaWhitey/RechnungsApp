from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

import cv2
from PIL import Image
from .app.model.dataRepresentation import FormData

filename = "../data/hervis.jpg"
img = cv2.imread(filename)
if img is None: print("Img is None")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
im_pil = Image.fromarray(img)


p = FormData(
    date="",
    price=26.98,
    company="Hervis",
    tags=["Sport", "Weihnachten2023"],
    img=img,
    imgFilename=filename
)

# thermopaper has normal 80mm
billWidthReal = 80 # mm

w, h = im_pil.size # pixel
billWidthPixel = billWidthReal * mm # pixel
billHeightPixel = billWidthPixel * h/w

billHeightPixel = billHeightPixel/ mm

print(f"Rechnung (w x h) = {billWidthReal} x {billHeightPixel}mm")

canvas = Canvas('output.pdf', pagesize=A4)
canvas.drawString(100,100,"Hello World")
canvas.drawInlineImage(image=im_pil,x=10,y=10, width=billWidthPixel, height= billHeightPixel)
canvas.showPage()
canvas.save()