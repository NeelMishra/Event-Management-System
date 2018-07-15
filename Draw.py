
from PyQt5.QtGui import QFontMetrics
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdb

def paint(canvas, location , size, font, text):
    try:
        canvas.setFont(font, size)
        canvas.drawString(location[0],location[1], text)
        canvas.showPage()
    except Exception as e:
        print(e)

def pdf(text, font, coordinate, pdf_name):

##    pdb.set_trace()
    w,h = A4
    font_metrics = QFontMetrics(font)
    n_loc = (coordinate[0], coordinate[1])
    n_size = font_metrics.height()//2
    n_font = font.family()

    try:
        pdfmetrics.registerFont(TTFont(n_font, n_font + ".ttf"))
           
    except:
        pass
    
    existing_pdf = PdfFileReader(open(pdf_name, "rb"))
    
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    
    #Itreative section, Here is where the magic occurs, abstractly.
    
    for detail in text:
        paint(can, n_loc, n_size, n_font, detail[0]) 
    #Itreative portion ends
    
    class temp_pdf():
        
        def get_page(self,page_no):
            self.outputStream.close()
            self.reader = PdfFileReader(self.name+'.pdf', 'rb')
            page = self.reader.getPage(page_no + 1)
            self.outputStream = open(self.name, 'wb')
            return page
        
        def d_page(self,page):
            self.output.addPage(page)
            self.output.write(self.outputStream)
        
        def __init__(self,filename):
            self.name = filename
            self.outputStream = open(self.name + '.pdf', "wb")
            self.output = PdfFileWriter()
            self.output.addBlankPage(h,w)
            self.output.write(self.outputStream)
            
    
    can.save()
    
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    
    output = PdfFileWriter()
    
    a = temp_pdf('temp')
    # add the "watermark" (which is the new pdf) on the existing page
    
    page = existing_pdf.getPage(0)
    a.d_page(page)
    
    i = 0
    for pages in new_pdf.pages:    
        
        dpage = a.get_page(0)
        dpage.mergePage(new_pdf.getPage(i))
        output.addPage(dpage)
        del(dpage)
        i += 1
        print('Step Complete')
        

    outputStream = open("destination.pdf", "wb")
    
    print("Certificates created and merged = ", i )
    
    output.write(outputStream)
    outputStream.close()
