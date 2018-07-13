
info = [["Neel Mishra"], ["IndarJeet Singh"],]

def pdf(info):

    from PyPDF2 import PdfFileWriter, PdfFileReader
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter,A4
    
    w,h = A4
    
    n_loc = (430,342)
    n_size = 36
    n_font = 'Courier'
    
    d_loc = (120, 311.5)
    d_size = None
    d_font = 'Courier'
    
    e_loc = (120, 282)
    e_size = None
    e_font = 'Courier'
    
    s_loc = (w,2)
    s_size = None
    s_font = 'Courier'
    
    
    
    def paint(canvas, location , size, font, text):
        canvas.setFont(font, size)
        canvas.drawString(location[0],location[1], text)
        canvas.showPage()
    
    existing_pdf = PdfFileReader(open("design.pdf", "rb"))
    
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    
    #Itreative section
    
    for detail in info:
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