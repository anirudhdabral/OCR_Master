from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector as mysql
from PyQt5.uic import loadUi
import sys
import gui.ocr
from Menu import Menu

class Login(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\login.ui', self)
        self.setFixedSize(396, 277)
        self.con = self.createConnection()
        self.cursor = self.con.cursor()
        self.btnsubmit.clicked.connect(self.checkLogin)
        self.btnsignup.clicked.connect(self.signup)
        self.btnback.clicked.connect(self.back)
        self.btnabout.clicked.connect(self.about)
        self.btnproceed.clicked.connect(self.proceed)
        self.back()
        self.txtuserid_2.setPlaceholderText("username")
        self.txtuserpass_2.setPlaceholderText("password")
        self.txtcpass.setPlaceholderText("confirm password")
        self.txtuserid.setPlaceholderText("username")
        self.txtuserpass.setPlaceholderText("password")

    def checkLogin(self):
        self.uid = self.txtuserid.text()
        self.upass = self.txtuserpass.text()
        query1 = 'select * ' \
                 'from logindetails ' \
                 'where userid=%s and password=%s'
        self.cursor.execute(query1, (self.uid, self.upass,))
        self.data = self.cursor.fetchone()
        self.status = self.cursor.rowcount
        if self.uid == '' or self.upass == '':
            self.showDialog('Please enter your details')
        elif self.status > 0:
            self.logon = Menu()
            self.logon.show()
            self.close()
        else:
            self.showDialog('Incorrect username or password!!')

    def proceed(self):
        self.uid2 = self.txtuserid_2.text()
        self.upass2 = self.txtuserpass_2.text()
        self.cpass = self.txtcpass.text()
        self.skey = self.txtskey.text()
        if self.uid2 == '' or self.upass2 == '' or self.cpass == '':
            self.showDialog('Please enter your details')
        elif self.upass2 != self.cpass:
            self.showDialog('Password does not match!!')
        else:
            query1 = 'select * ' \
                     'from logindetails ' \
                     'where userid=%s'
            self.cursor.execute(query1, (self.uid2,))
            self.data = self.cursor.fetchone()
            self.status = self.cursor.rowcount
            if self.status > 0:
                self.showDialog('ID already exists!')
            elif self.skey != "Admin00":
                self.showDialog('Wrong Security key!!')
            else:
                strinsert = 'insert into logindetails(userid, password) ' \
                            'values (%s,%s)'
                self.cursor.execute(strinsert, (self.uid2, self.upass2,))
                self.con.commit()
                self.showDialog('ID created!')
                self.back()

    def signup(self):
        self.txtskey.setVisible(True)
        self.txtuserid_2.setVisible(True)
        self.txtuserpass_2.setVisible(True)
        self.txtcpass.setVisible(True)
        self.label_3.setVisible(False)
        self.label.setVisible(False)
        self.label_4.setVisible(True)
        self.txtuserid.setVisible(False)
        self.txtuserpass.setVisible(False)
        self.btnback.setVisible(True)
        self.btnproceed.setVisible(True)
        self.btnsubmit.setVisible(False)
        
    def back(self):
        self.label_2.setVisible(False)
        self.txtskey.setPlaceholderText("admin security key")
        self.txtskey.setVisible(False)
        self.btnback.setVisible(False)
        self.btnproceed.setVisible(False)
        self.label_3.setVisible(True)
        self.label.setVisible(True)
        self.label_4.setVisible(False)
        self.txtuserid.setVisible(True)
        self.txtuserpass.setVisible(True)
        self.txtuserid_2.setVisible(False)
        self.txtuserpass_2.setVisible(False)
        self.txtcpass.setVisible(False)
        self.btnsubmit.setVisible(True)
        self.txtuserid_2.setText('')
        self.txtuserpass_2.setText('')
        self.txtcpass.setText('')
        self.txtskey.setText('')

    def about(self):
        self.showDialog('Under the supervision of Assistant Professor Anika Bisht,\n' \
                        'this project is made by:-\n' \
                        '1. Abhinav Sisodia\n' \
                        '2. Anirudh Dabral\n' \
                        '3. Ariba Khan\n' \
                        '4. Devansh Gupta')

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

    def questionDialog(self,title, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(txt)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btnstatus = msg.exec_()
        return btnstatus


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    app.exec_()