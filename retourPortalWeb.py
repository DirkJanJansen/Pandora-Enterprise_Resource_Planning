from login import hoofdMenu
from bestelOrder import artKeuze
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                            QDialog, QMessageBox
from PyQt5.QtGui import  QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                                create_engine)
from sqlalchemy.sql import select

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def foutEmail():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Incorrect e-mail address!')
    msg.setWindowTitle('Incorrect email address')
    msg.exec_()

def zoekEmailadres(m_email, klmail):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Web articles return items.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Email = QLabel()
            emailEdit = QLineEdit()
            emailEdit.setFixedWidth(220)
            emailEdit.setFont(QFont("Arial",10))
            emailEdit.textChanged.connect(self.emailChanged)
                                        
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
    
            grid.addWidget(QLabel('Email address customer\nor Customer number'), 1, 0)
            grid.addWidget(emailEdit, 1, 1)
           
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(closeBtn, 2, 1)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100) 
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro") 
     
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
                  
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
    
        def emailChanged(self, text):
            self.Email.setText(text)
    
        def returnEmail(self):
            return self.Email.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnEmail()]
       
    window = Widget()
    data = window.getData()
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String))
  
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if data[0] and '@' in data[0]:
        klmail = data[0]
        s = select([accounts]).where(accounts.c.email == klmail)
        rp = conn.execute(s).first()
    elif data[0][0] == '1' and len(data[0]) == 9:
        klantnr = data[0]
        s = select([accounts]).where(accounts.c.accountID == klantnr)
        rp = conn.execute(s).first()
        klmail = rp[1]
    else:
        klmail = '' 
        foutEmail()
        zoekEmailadres(m_email, klmail)
          
    if rp:
        artKeuze(m_email, 1, klmail)
    zoekEmailadres(m_email, klmail)