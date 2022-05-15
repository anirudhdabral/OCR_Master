from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
from translate import Translator
import gui.ocr

class Translate(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\Translator.ui',self)
        # self.txtPath.setPlaceholderText("Add your file path here...")
        self.txtTranslate.setPlaceholderText("  Translated text will be displayed\n  here...")
        self.btnTranslate.clicked.connect(self.translate_text)
        self.setFixedSize(853, 411)

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
        self.text=self.txtSource.toPlainText()
        if self.text == "":
            self.showDialog("Please enter text to be translated!")
        else:
            tr = Translator(to_lang = self.lang)
            self.txtTranslate.setText(tr.translate(self.text))

    def showDialog(self,txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = Translate()
    edit.show()
    app.exec_()