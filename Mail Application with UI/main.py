import typing
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mailGUI.ui", self)
        self.show()
        
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.attach_sth)
        self.pushButton_3.clicked.connect(self.send_mail)
        
    
    def login(self):
        try:
            self.server = smtplib.SMTP(self.lineEdit_3.text(), self.lineEdit_4.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.lineEdit.text(), self.lineEdit_2.text())
            
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.pushButton.setEnabled(False)
            
            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            
            self.msg = MIMEMultipart()
            
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Login Info!")
            message_box.exec()
            
        except:
             message_box = QMessageBox()
             message_box.setText("Login Failed!")
             message_box.exec()
            
    
    def attach_sth(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                attachment = open(filename, 'rb')
                filename = filename[filename.rfind("/") + 1: ]
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachment; filename = {filename}")
                self.msg.attach(p)
                if not self.label_8.text().endswith(":"):
                    self.label_8.setText(self.label_8.text() + ",")
                self.label_8.setText(self.label_8.text() + " " + filename)
                
                
    
    def send_mail(self):
        dialog  = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole) # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole) # 1
        
        if dialog.exec() == 0:
            try:
                self.msg['From'] = "Bhavya"
                self.msg['To'] = self.lineEdit_5.text()
                self.msg['Subject'] = self.lineEdit_6.text()
                self.msg.attach(MIMEText(self.textEdit.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.lineEdit.text(), self.lineEdit_5.text(), text)
                
                message_box = QMessageBox()
                message_box.setText("Mail sent!")
                message_box.exec()
                
            except: 
                message_box = QMessageBox()
                message_box.setText("Sending Mail Failed!")
                message_box.exec()
                
    
app = QApplication([])
window = MyGUI()
app.exec_()