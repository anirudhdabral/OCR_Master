from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import mysql.connector as mysql
import sys
from pyparsing import Word
import gui.ocr

class Notes(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\OCR_Notes.ui', self)
        self.setFixedSize(911, 436)
        self.con = self.createConnection()
        self.cursor = self.con.cursor()
        self.tablesize()
        self.show_notes()
        self.populateCombo()
        self.btnShow.clicked.connect(self.show_details)

    def show_notes(self):
        query = 'select note_id, content from notes'
        self.cursor.execute(query)
        self.dataset = self.cursor.fetchall()
        rowcount = len(self.dataset)
        self.table1.setRowCount(rowcount)
        rownum = 0
        for row in self.dataset:
            for column in range(len(row)):
                self.table1.setItem(rownum, column, QTableWidgetItem(str(row[column])))
            rownum = rownum + 1
    
    def show_details(self):
        self.note_id = self.cmb.currentText()
        query1 = 'select content from notes where note_id=%s'
        self.cursor.execute(query1, (int(self.note_id),))
        self.modelset = self.cursor.fetchone()
        self.txtShow.setText(self.modelset[0])
    
    def populateCombo(self):
        strsql = 'select note_id from notes'
        self.cursor.execute(strsql)
        self.dataset = self.cursor.fetchall()
        for data in self.dataset:
            self.cmb.addItem(str(data[0]))

    def createConnection(self):
        con = mysql.connect(host='localhost', database='ocr', user='root', password='')
        return con

    def showDialog(self,txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Message.')
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def tablesize(self):
        self.table1.setColumnWidth(0, 125)
        self.table1.setColumnWidth(1, 350)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes = Notes()
    notes.show()
    app.exec_()