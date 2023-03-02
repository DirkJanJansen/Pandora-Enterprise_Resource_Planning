from login import hoofdMenu
from sys import platform
import os
from PyQt5.QtCore  import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMessageBox,\
                            QComboBox, QPushButton, QLineEdit
 
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def geenMenu():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen bestandsnaam gekozen!')
    msg.setWindowTitle('Geen keuze')
    msg.exec_()
        
def printFile(filename, m_email, path):
    if platform == 'win32':
        os.startfile(path+filename, "print")
    else:
        os.system("lpr "+path+filename)
        
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Printen diverse formulieren')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
    
def fileList(m_email, path):
    filelist = []
    for file in os.listdir(path):
        if file[-4:] == '.txt':
            filelist.append(file)
    class combo(QDialog):
        def __init__(self, parent=None):
              super(combo, self).__init__(parent)
              self.setWindowTitle("Printen van lijsten")
              self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
              self.setFont(QFont("Arial", 10))
              grid = QGridLayout()
              grid.setSpacing(20)
            
              logo = QLabel()
              pixmap = QPixmap('./images/logos/logo.jpg')
              logo.setPixmap(pixmap)
              grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
              
              plbl = QLabel()
              plbl = QLabel('Printen\nLijsten')
              plbl.setStyleSheet("color:rgba(45, 83, 115, 255); font: 20pt Comic Sans MS")
              grid.addWidget(plbl, 0, 1)
                    
              lbl = QLabel()
              pixmap = QPixmap('./images/logos/verbinding.jpg')
              lbl.setPixmap(pixmap)
              grid.addWidget(lbl, 0, 0, 1, 1)
              
              self.Keuze = QLabel()          
              self.cb = QComboBox()
              self.cb.setFixedWidth(420)
              self.cb.setFont(QFont("Arial",10))
              self.cb.setStyleSheet("color: black;  background-color: #F8F7EE")
              self.cb.addItem('                                 Kies bestand')
              grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
              
              for item in range(len(filelist)):
                  self.cb.addItem(filelist[item])
                  self.cb.model().sort(0)
                  grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
                  
              self.cb.activated[str].connect(self.cbChanged)
              
              self.aantal = QLabel()
              aantalEdit = QLineEdit('1')
              aantalEdit.setStyleSheet("background: #F8F7EE")
              aantalEdit.setFixedWidth(30)
              aantalEdit.setFont(QFont("Arial",10))
              aantalEdit.textChanged.connect(self.aantalChanged)
              reg_ex = QRegExp("^[0-9]{1,2}$")
              input_validator = QRegExpValidator(reg_ex, aantalEdit)
              aantalEdit.setValidator(input_validator)
              
              grid.addWidget(QLabel('Aantal kopieën te printen'), 3, 1, 1, 2)
              grid.addWidget(aantalEdit, 3, 2, 1, 1, Qt.AlignRight)
              
              plbl = QLabel()
              pmap = QPixmap('./images/thumbs/MG3650.jpg')
              plbl.setPixmap(pmap)
              grid.addWidget(plbl , 3, 0, 2, 1, Qt.AlignCenter)
                    
              cancelBtn = QPushButton('Sluiten')
              cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))  
                
              grid.addWidget(cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
              cancelBtn.setFont(QFont("Arial",10))
              cancelBtn.setFixedWidth(90)
              cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
              printBtn = QPushButton('Printen')
              printBtn.clicked.connect(self.accept)  
                
              grid.addWidget(printBtn,  4, 2)
              printBtn.setFont(QFont("Arial",10))
              printBtn.setFixedWidth(90)
              printBtn.setStyleSheet("color: black;  background-color: gainsboro")    
                  
              grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
                
              self.setLayout(grid)
              self.setGeometry(550, 300, 150, 150)
          
        def cbChanged(self, text):
              self.Keuze.setText(text)
              
        def aantalChanged(self, text):
             self.aantal.setText(text)
             
        def returncb(self):
             return self.Keuze.text()
          
        def returnaant(self):
            return self.aantal.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = combo(parent)
            dialog.exec_()
            return [dialog.returncb(), dialog.returnaant()]
           
    win = combo()
    data = win.getData()
    if data[0] == '' or data[0][0] == ' ':
        geenMenu()
        fileList(m_email, path)
    elif data[0]:
        if data[1]:
            mhoev = data[1] 
        else:
            mhoev = '1'
        filename = data[0]
        for x in range(0, int(mhoev)):
            printFile(filename, m_email, path)
        printing()
        fileList(m_email, path)
    else:
        fileList(m_email, path)            