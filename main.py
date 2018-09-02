import sys
import os

from Draw import pdf, paint
from excel import return_excel_info
from image2pdf import convert


from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QFontMetrics
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QFontDialog
from PyQt5 import QtCore

class FontBox(QDialog):


    def __init__(self,justForFun):
        super(FontBox, self).__init__()
        loadUi('blah.ui', self)
        print(justForFun)

    def __del__(self):
        del(self)
    



class Window(QMainWindow):
    image_ratio = None
    current_image_size = None
    excel_file = None
    excel_path = ''
    design_path = ''
    design_pix_map = None
    font_style = None
    extracted_excel_data = None
    x = None
    y = None
    font_metrics = None
    #Heading of the excel sheet are used as fields
    #A dictionary is created, which has keys as the heading of excel
    #The value is the location, font_size, color, etc as an entire dictionary.
    fields = {}
    
    
    def __init__(self):


        ##Setting up appropriate flags for different fields
        ##  that will be inserted by user.



        #initializing different GUI elements!
        super(Window, self).__init__()
        loadUi('Design.ui', self)
        self.show()
        self.progress.hide()
        #self.progress.setValue(20)
        #self.progress.show()
        #self.flag_spacer.changeSize(0)

        


        
        self.red_pix_map = QPixmap("Icons/red.jpg")
        self.green_pix_map = QPixmap("Icons/green.jpg")
        print(self.green_pix_map)
        self.design_signal.setPixmap(self.red_pix_map)
        self.excel_signal.setPixmap(self.green_pix_map)
        self.font_signal.setPixmap(self.red_pix_map)
        self.fields_signal.setPixmap(self.green_pix_map)


        
        self.Image.mousePressEvent = self.getPos
        self.add_excel_button.triggered.connect(self.excel_file_browse)
        self.add_design_button.triggered.connect(self.design_path_browse)
        self.set_font_button.triggered.connect(self.select_font)
        self.generate_pdf_button.triggered.connect(self.generate_pdf)
        self.preview_certificate_button.triggered.connect(self.preview_pdf)
        self.setting_button.triggered.connect(self.dropdown)


    def dropdown(self):
        self.dialog = FontBox("Neel Mishra")
        self.dialog.show()

    def getPos(self , event):
        try:
            if( int((event.pos().x()) * self.image_ratio[0] + 23) <1260):
                 self.x = int((event.pos().x()) * self.image_ratio[0] + 3)
                 self.y = int((self.current_image_size[1] - event.pos().y()) * self.image_ratio[1] + 9)
                 print(self.x,self.y)
                 return
            self.x = int((event.pos().x()) * self.image_ratio[0] + 23)
            self.y = int((self.current_image_size[1] - event.pos().y()) * self.image_ratio[1] + 9)
            print(self.x,self.y)
        except Exception as e:
            print(e)


    def excel_file_browse(self):

        self.excel_path, _ = QFileDialog.getOpenFileName(self, 'Select excel path')

        if(self.excel_path == None):
            return

        self.extracted_excel_data, self.headings = return_excel_info(self.excel_path)#Get excel data

        for heading in self.headings:
            fields[heading] = {'coordinates' : None,
                               'font_color' : None,
                               'font_size' : None,
                               'font_family' : None,
                               }


    def design_path_browse(self):

        self.design_path, _ = QFileDialog.getOpenFileName(self, 'Select certificate design.')

        if(self.design_path == None):
            return

        self.design_pix_map = QPixmap(self.design_path)
        #print(self.Image)
        self.design_pix_map = self.design_pix_map.scaled(2204, 908, QtCore.Qt.KeepAspectRatio)
        self.Image.setPixmap(self.design_pix_map)
        self.current_image_size = [self.design_pix_map.width(), self.design_pix_map.height()]

        try:
            self.image_ratio = [b/a for b,a in zip([2664, 1896],self.current_image_size)]
            convert(self.design_path)
        except Exception as e:
            print(e)
        
        print(str(self.design_pix_map.height())+ "  " + str(self.design_pix_map.width()) )
        #print(self.image_ratio)
        #print(self.current_image_size)
        #print(A4)

    def select_font(self):
        try:
            self.font_style, valid = QFontDialog.getFont()
            print(self.font_style)
            print(valid)
            #self.font_metrics = QFontMetrics(self.font_style)
            #print(type(self.font_style.family()))
        except Exception as e:
            print(e)

    def generate_pdf(self):

        try:
            convert(self.design_path)
            pdf(self.extracted_excel_data,self.font_style, [self.x,self.y], self.design_path[0:-4] + ".pdf", self.progress)
        except Exception as e:
            print(e)

        os.startfile('destination.pdf')

    def preview_pdf(self):

        data = ['Test','Test',]

        try:
            convert(self.design_path)
            pdf(data,self.font_style, [self.x,self.y], self.design_path[0:-4] + ".pdf", self.progress)
        except Exception as e:
            print(e)

        os.startfile('destination.pdf')
        
        
app = QApplication(sys.argv)

GUI = Window()

sys.exit(app.exec_())
