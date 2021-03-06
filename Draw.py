
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
        pdfmetrics.registerFont(TTFont(font, font + ".ttf"))
        canvas.setFont(font, int(size))
        canvas.drawString(int(location[0]),int(location[1]), text)
        canvas.showPage() #New page
    except Exception as e:
        print("Exception from paint" , e)

def pdf(progress, fields, pdf_name):#,progress):
##    text = text[1:]
##    total_length = len(text)
##    print(total_length)
##    pdb.set_trace()
   ## n_font = font.family()
    w,h = A4
    try:
        pdfmetrics.registerFont(TTFont(n_font, n_font + ".ttf"))
           
    except:
        pass
    
    existing_pdf = PdfFileReader(open(pdf_name, "rb"))
    
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    
    #Itreative section, Here is where the magic occurs, abstractly.

    i = 0
    length = (len(fields[list(fields.keys())[0]]['content']))
    j = 1
    while(i != length):
        ratio = (j / length) * 100
        for heading in fields:

            n_loc = fields[heading]['coordinates']
            n_size = fields[heading]['font_size']
            n_font = fields[heading]['font_family']
            n_color = fields[heading]['font_color']      
            location = n_loc

            if (n_loc == None):
                continue
            if (fields[heading]['content'] == None):
                continue

            else:
                #draw[i]
                pdfmetrics.registerFont(TTFont(n_font, n_font + ".ttf"))
                can.setFont(n_font, int(n_size))
                can.drawString(int(location[0]),int(location[1]),
                               fields[heading]['content'][i])
        
        i += 1
        j += 1
        progress.setValue(int(ratio))
        progress.show()
        can.showPage()

    progress.hide()





##    for heading in fields:
##
##        
##        n_loc = fields[heading]['coordinates']
##        if(n_loc == None):
##            continue
##        n_size = fields[heading]['font_size']
##        n_font = fields[heading]['font_family']
##        n_color = fields[heading]['font_color']
##
##        i += 1
##        #RATIO = i / total_length
##        #print(i)
##        ##print(total_length)
##        ##print(RATIO)
##
##        for value in fields[heading]['content']:
##            print(value)
##            paint(can, n_loc, n_size, n_font, value) #Print names
##
##
##        #progress.show()
##        #progress.setValue(int(RATIO * 100))
##    

#progress.hide()
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
