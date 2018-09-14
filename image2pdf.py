from PIL import Image
from fpdf import FPDF
from array import array
import os

def convert(imagepath):
    pdf = FPDF('L', 'in', (26.46, 37.4))

    pdf.add_page()
    pdf.image(imagepath, 0, 0, 37.4, 26.46)
    pdf.output(imagepath[:-4] + ".pdf", "F")
