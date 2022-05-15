from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
import os
from PIL import Image
from pyparsing import Word
import gui.ocr
from detect_word import Detect_Word
from detect_digit import Digit


class Word_pred(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\WD.ui',self)
        self.rbtnAccu.setChecked(True)
        self.btnSubmit.setVisible(True)
        self.btnSubmit_2.setVisible(False)
        self.rbtnAccu.toggled.connect(self.check)
        self.rbtnSword.toggled.connect(self.check)
        self.check()
        self.btnSubmit.clicked.connect(self.submit)
        self.labelD.setVisible(False)
        self.labelW.setVisible(True)
        self.setFixedSize(578, 435)

    def submit(self):
        self.txtResults.clear()
        self.file = self.txtPath.text()
        if self.rbtnSword.isChecked():
            if self.file == "":
                self.showDialog("Please enter path first")
                return
            try:
                self.res, self.accuracy = Detect_Word.predict(self.file)
                self.txtResults.setText(self.res)
            except:
                self.showDialog('No file found')
            # print(self.res,self.accuracy)            
        elif self.rbtnAccu.isChecked():
            self.total_accuracy = 0.0
            count = 0
            for filename in os.listdir('images\word'):
                f = os.path.join('images\word', filename)
                # checking if it is a file
                if os.path.isfile(f):
                    self.read_file = f
                    self.res, self.accuracy = Detect_Word.predict(self.read_file)
                    print(self.res,self.accuracy)
                    self.total_accuracy += float(self.accuracy)
                    count +=1
            self.result = "Accuracy = " + "{:.2f}".format(self.total_accuracy/count) + "%"
            self.txtResults.setText(str(self.result))
                    
    def showDialog(self,txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def check(self):
        if self.rbtnAccu.isChecked():
            self.txtPath.setPlaceholderText("Add folder path here...")
            self.txtResults.setPlaceholderText("Accuracy results will be displayed here...")
        elif self.rbtnSword.isChecked():
            self.txtPath.setPlaceholderText("Add your file path here...")
            self.txtResults.setPlaceholderText("OCR results will be displayed here...")


class Digit_pred(Word_pred):
    def __init__(self):
        super().__init__()
        self.labelD.setVisible(True)
        self.labelW.setVisible(False)
        self.check()
        self.btnSubmit.setVisible(False)
        self.btnSubmit_2.setVisible(True)
        self.btnSubmit_2.clicked.connect(self.submit2)
        
    def submit2(self):
        self.txtResults.clear()
        self.file = self.txtPath.text()
        if self.rbtnSword.isChecked():
            if self.file == "":
                self.showDialog("Please enter path first")
                return
            try:
                self.res, self.accuracy = Digit.predict(self.file)
                self.txtResults.setText(str(self.res))
            except:
                self.showDialog('No file found')
            # print(self.res)
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
            self.result = "Accuracy = " + "{:.2f}".format((self.total_accuracy/count)*100) + "%"
            self.txtResults.setText(str(self.result))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # edit = Word_pred()
    edit = Digit_pred()
    edit.show()
    app.exec_()