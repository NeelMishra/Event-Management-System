import sys


from Draw import pdf
from excel import return_excel_info
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QFontDialog

class Window(QMainWindow):

    excel_file = None
    excel_path = ''
    design_path = ''
    design_pix_map = None
    font_style = None
    extracted_excel_data = None
    
    def __init__(self):

        super(Window, self).__init__()
        loadUi('Design.ui', self)
        self.show()

        self.add_excel_button.triggered.connect(self.excel_file_browse)
        self.add_design_button.triggered.connect(self.design_path_browse)
        self.set_font_button.triggered.connect(self.select_font)
        self.generate_pdf_button.triggered.connect(self.generate_pdf)


    def excel_file_browse(self):

        self.excel_path, _ = QFileDialog.getOpenFileName(self, 'Select excel path')

        if(self.excel_path == None):
            return

        self.extracted_excel_data = return_excel_info(self.excel_path)



    def design_path_browse(self):

        self.design_path, _ = QFileDialog.getOpenFileName(self, 'Select certificate design.')

        if(self.design_path == None):
            return

        self.design_pix_map = QPixmap(self.design_path)
        #print(self.Image)
        self.Image.setPixmap(self.design_pix_map)
        #print(self.design_pix_map.width(),self.design_pix_map.height())


    def select_font(self):
            
        self.font_style, valid = QFontDialog.getFont()

    def generate_pdf(self):
        pass
        #pdf(self.extracted_excel_data)

        
        
app = QApplication(sys.argv)

GUI = Window()

sys.exit(app.exec_())
