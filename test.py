from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
import os
from PIL import Image
import pytesseract
from translate import Translator
import gui.ocr
# from detect_word import Detect_Word
# from digit import Digit

'''
include the following:
pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
'''
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Main(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\main.ui',self)
        # self.txtPath.setPlaceholderText("Add your file path here...")
        self.txtResults.setPlaceholderText("  OCR results will be displayed here...")
        self.txtTranslate.setPlaceholderText("  Translated text will be displayed\n  here...")
        self.rbtnFull.setChecked(True)
        self.rbtnSword.setChecked(True)
        self.rbtnFull.toggled.connect(self.check)
        self.rbtnWord.toggled.connect(self.check)
        self.rbtnDigit.toggled.connect(self.check)
        self.rbtnAccu.toggled.connect(self.check)
        self.rbtnSword.toggled.connect(self.check)
        self.check()
        self.btnSubmit.clicked.connect(self.submit)
        self.btnTranslate.clicked.connect(self.translate_text)
        self.setFixedSize(952, 609)
        # self.digit_predict()

    def submit(self):
        if self.rbtnFull.isChecked():
            self.full_ocr()
        elif self.rbtnWord.isChecked():
            self.word_predict()
        elif self.rbtnDigit.isChecked():
            self.digit_predict()

    def translate_text(self):
        self.selected_lang = self.comboBox.currentText()
        if self.selected_lang == "Select Language":
            self.showDialog("Please select language first")
            return
        elif self.selected_lang == "Hindi":
            self.lang = "hi"
        elif self.selected_lang == "French":
            self.lang = "fr"
        elif self.selected_lang == "Spanish":
            self.lang = "es"
        elif self.selected_lang == "German":
            self.lang = "de"
        else:
            self.lang = "en"
        self.text=self.txtResults.toPlainText()
        if self.text == "":
            self.showDialog("Enjcnvdfv")
        else:
            tr = Translator(to_lang = self.lang)
            self.txtTranslate.setText(tr.translate(self.text))

    def full_ocr(self):
        self.file = self.txtPath.text()
        try:
            # target = pytesseract.image_to_string(self.file, lang='eng', config='--oem 3 ')
            self.txtResults.setText("target")
        except:
            self.showDialog('No file found')

    def word_predict(self):
        self.txtResults.clear()
        self.file = self.txtPath.text()
        if self.rbtnSword.isChecked():
            try:
                self.res, self.accuracy = Detect_Word.predict(self.file)
            except:
                self.showDialog('No file found')
            # print(self.res,self.accuracy)
            self.txtResults.setText(self.res)
        elif self.rbtnAccu.isChecked():
            self.total_accuracy = 0.0
            count = 0
            for filename in os.listdir('images\word'):
                f = os.path.join('images\word', filename)
                # checking if it is a file
                if os.path.isfile(f):
                    self.read_file = f.split("\\")[-1]
                    self.res, self.accuracy = Detect_Word.predict(self.read_file)
                    print(self.res,self.accuracy)
                    self.total_accuracy += float(self.accuracy)
                    count +=1
            self.txtResults.setText(self.total_accuracy/count)
                    

    def digit_predict(self):
        self.txtResults.clear()
        self.file = self.txtPath.text()
        if self.rbtnSword.isChecked():
            try:
                self.res, self.accuracy = Digit.predict(self.file)
            except:
                self.showDialog('No file found')
            # print(self.res)
            self.txtResults.setText(str(self.res))
        elif self.rbtnAccu.isChecked():
            self.total_accuracy = 0.0
            count = 0
            for filename in os.listdir('images\digit'):
                f = os.path.join('images\digit', filename)
                # checking if it is a file
                if os.path.isfile(f):
                    self.read_file = f
                    print(f)
                    self.res, self.accuracy = Digit.predict(self.read_file)
                    print(self.res,self.accuracy)
                    self.total_accuracy += float(self.accuracy)
                    count +=1
            self.result = "{:.2f}".format((self.total_accuracy/count)*100)
            self.txtResults.setText(str(self.result))

    def showDialog(self,txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def check(self):
        if self.rbtnFull.isChecked():
            self.txtPath.setPlaceholderText("  Add your file path here...")
            self.labelDoc.setVisible(True)
            self.rbtnAccu.setHidden(True)
            self.rbtnSword.setHidden(True)
        elif self.rbtnWord.isChecked() or self.rbtnDigit.isChecked():
            self.labelDoc.setVisible(False)
            self.rbtnAccu.setHidden(False)
            self.rbtnSword.setHidden(False)
            if self.rbtnAccu.isChecked():
                self.txtPath.setPlaceholderText("  Add folder path here...")
            elif self.rbtnSword.isChecked():
                self.txtPath.setPlaceholderText("  Add your file path here...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = Main()
    edit.show()
    app.exec_()