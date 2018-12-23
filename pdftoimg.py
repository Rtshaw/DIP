# -*- coding: utf-8 -*-

import sys
from wand.image import Image


pdffile=sys.argv[1]
pdf = Image(filename=pdffile, resolution=300)
pdfImage = pdf.convert("png")

c = 1
for img in pdfImage.sequence:
    page = Image(image=img)
    page.save(filename="./images/"+str(c)+".png")
    c += 1



