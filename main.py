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
    def __init__(self,dictionary, flag):
        super(FontBox, self).__init__()
        loadUi('blah.ui', self)
        for header in dictionary.keys():
            self.pointer.addItem(header)
        #self.pointer.addItem(dictionary[
        #print(flag)
        self.ok_button.clicked.connect(lambda: self.button_click(dictionary,flag))
        self.cancel_button.clicked.connect(self.closing_logic)
        self.show()

    def closing_logic(self):
        self.close()

    def button_click(self, dictionary, flag):
        try:
            #print(flag)
            flag[0] = self.pointer.currentText()
            r = self.R.text()
            g = self.G.text()
            b = self.B.text()
            dictionary[flag[0]]['font_size'] = self.size.text()
            dictionary[flag[0]]['font_color'] = (r,g,b)
            dictionary[flag[0]]['font_family'] = self.font.currentText()
            print(flag)
            self.close()

        except Exception as e:
            print("Exception from button_click" + e)
        




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
    flag = []
    
    
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
        #self.set_font_button.triggered.connect(self.select_font)
        self.generate_pdf_button.triggered.connect(self.generate_pdf)
        self.preview_certificate_button.triggered.connect(self.preview_pdf)
        self.setting_button.triggered.connect(self.dropdown)


    def dropdown(self):
        try:
            if(len(self.fields) == 0):
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.about(self, "Excel file not set!", "Please set an excel file path, via the excel button.")
                return
            self.dialog = FontBox(self.fields,self.flag)
            self.dialog.show()
            print(self.flag)
        except Exception as e:
            print("exception from dropdown" ,e)

    def getPos(self , event):
        try:
            #print(self.fields[self.flag])
            if( int((event.pos().x()) * self.image_ratio[0] + 23) <1260):
                 self.x = int((event.pos().x()) * self.image_ratio[0] + 3)
                 self.y = int((self.current_image_size[1] - event.pos().y()) * self.image_ratio[1] + 9)
                 self.fields[self.flag[0]]['coordinates'] = (self.x, self.y)
                 print(self.fields[self.flag[0]]['coordinates'], self.flag, '\n', self.fields)
                 return
            self.x = int((event.pos().x()) * self.image_ratio[0] + 23)
            self.y = int((self.current_image_size[1] - event.pos().y()) * self.image_ratio[1] + 9)
            self.fields[self.flag[0]]['coordinates'] = (self.x, self.y)
            print(self.fields[self.flag[0]]['coordinates'], self.flag, '\n', self.fields)
        except Exception as e:
            print("Exception from getPos" ,e)


    def excel_file_browse(self):
        try:
            self.excel_path, _ = QFileDialog.getOpenFileName(self, 'Select excel path')

            if(self.excel_path == None):
                return

            self.extracted_excel_data, self.headings = return_excel_info(self.excel_path)#Get excel data
            #print(self.extracted_excel_data)
            i = 0
            for heading in self.headings:
                
                self.fields[heading] = {'coordinates' : None,
                                   'font_color' : None,
                                   'font_size' : None,
                                   'font_family' : None,
                                   }

                temp_list = []
                for values in self.extracted_excel_data[1:]:
                    temp_list.append(values[i])
                self.fields[heading]['content'] = temp_list
                i += 1
                
            self.flag = [list(self.fields.keys())[0]]
            print(self.fields)
        except Exception as e:
            print("Exception from excel_file_browse", e)
            


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
            print("Exception from design_path_browse", e)
        
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
            print("Exception from select_font[Important]")

    def generate_pdf(self):

        if(len(self.fields) == 0):
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.about(self, "Excel file not set!", "Please set an excel file path, via the excel button.")
            return


        if(len(self.design_path) == 0):
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.about(self, "Design not set!", "Please set a design image path, via the design button.")
            return
            
            
        #try:
        convert(self.design_path)
        pdf(self.fields,self.design_path[0:-4] + ".pdf",)# self.progress)
        #except Exception as e:
        #    print("Exception from generate_pdf", e)

        os.startfile('destination.pdf')

    def preview_pdf(self):

        data = ['Test','Test',]

        try:
            convert(self.design_path)
            pdf(data,self.font_style, [self.x,self.y], self.design_path[0:-4] + ".pdf", self.progress)
        except Exception as e:
            print("Exception from preview_pdf", e)

        os.startfile('destination.pdf')
        
        
app = QApplication(sys.argv)

GUI = Window()

sys.exit(app.exec_())
