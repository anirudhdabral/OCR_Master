from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import mysql.connector as mysql
import sys
import os
from PIL import Image
import pytesseract
import gui.ocr
from Translate import Translate
from Notes import Notes
from Word_Digit import Word_pred, Digit_pred


'''
include the following:
pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
'''
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui\Menu.ui',self)
        self.setFixedSize(698, 588)
        self.con = self.createConnection()
        self.cursor = self.con.cursor()
        self.txtPath.setPlaceholderText("Add your file path here...")
        self.txtResults.setPlaceholderText("OCR results will be displayed here...")
        self.btnSubmit.clicked.connect(self.submit)
        self.btnClear.clicked.connect(self.reset)
        self.btnSave.clicked.connect(self.save_note)
        self.actionTranslator.triggered.connect(lambda: self.loadFrame(self.actionTranslator))
        self.actionWord.triggered.connect(lambda: self.loadFrame(self.actionWord))
        self.actionDigit.triggered.connect(lambda: self.loadFrame(self.actionDigit))
        self.actionNotes.triggered.connect(lambda: self.loadFrame(self.actionNotes))
        self.actionLogout.triggered.connect(lambda: self.loadFrame(self.actionLogout))
        self.reset()

    def loadFrame(self,item):
        caption = item.text()
        if caption == 'Translator':
            self.load = Translate()
        elif caption == 'Logout':
            return exit(0)
        elif caption == 'Word':
            self.load = Word_pred()
        elif caption == 'Digit':
            self.load = Digit_pred()
        elif caption == 'Notes':
            self.load = Notes()
        else:
            return
        self.load.show()
    
    def save_note(self):
        self.content = self.txtResults.toPlainText()
        if self.content == "":
            self.showDialog("Nothing to Save")
            return
        btn = self.questionDialog('Confirmation', 'Are you sure you want to save the note?')
        if btn == QMessageBox.Yes:
            strinsert = 'insert into notes values (%s,%s)'
            self.cursor.execute(strinsert,
                                (int(self.newid), self.content,))
            self.con.commit()
            self.showDialog('Notes saved successfully.')
        self.getId()

    def submit(self):
        self.txtResults.clear()
        self.file = self.txtPath.text()
        if self.file == "":
            self.showDialog("Please enter path first!")
            return
        try:
            target = pytesseract.image_to_string(self.file, lang='eng', config='--oem 3 ')
            self.txtResults.setText(target)
        except:
            self.showDialog('No file found')
    
    def getId(self):
        strsql = 'select max(note_id) ' \
                 'from notes'
        self.cursor.execute(strsql)
        self.rowdata = self.cursor.fetchone()
        if self.rowdata[0] == None:
            self.newid = 1
        else:
            self.newid = self.rowdata[0] + 1
        self.txtId.setText(str(self.newid))

    def showDialog(self,txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def questionDialog(self,title, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btnstatus = msg.exec_()
        return btnstatus
    
    def createConnection(self):
        con = mysql.connect(host='localhost', database='ocr', user='root', password='')
        return con
    
    def reset(self):
        self.txtResults.clear()
        self.txtPath.setText("")
        self.getId()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = Menu()
    edit.show()
    app.exec_()