from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                            QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import  QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                             create_engine, func)
from sqlalchemy.sql import select

def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Foutieve postcode ingevoerd!')
    msg.setWindowTitle('Postcode')
    msg.exec_()

def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Niet (alle) vereiste gegevens ingevuld!')
    msg.setWindowTitle('Gegevens!')
    msg.exec_()
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def fout_email():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('ongeldig email adres!')
    msg.setWindowTitle('e-mailadres!')
    msg.exec_()

def foutTelnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('geen 10 cijfers!')
    msg.setWindowTitle('Telefoonnummer!')
    msg.exec_()

def dontMatch():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Wachtwoord niet identiek\nen/of minder dan 8 tekens!')
    msg.setWindowTitle('Wachtwoord!')
    msg.exec_()
 
def leverancierBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Leverancier is al aanweizg!')
    msg.setWindowTitle('Account')
    msg.exec_()

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11 % 10
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalLeverancier(m_email):
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    try:
        mlevnr=(conn.execute(select([func.max(leveranciers.c.leverancierID,\
            type_=Integer)])).scalar())
        mlevnr=int(maak11proef(mlevnr))
        conn.close
    except:
        mlevnr = 300000005
    invLeverancier(mlevnr, m_email)
   
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt!')
    msg.setWindowTitle('Leveranciergegevens')
    msg.exec_()

def invLeverancier(mlevnr, m_email):                                 
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Invoer leverancier")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                  
            self.Bedrijfsnaam = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setFixedWidth(540)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Rechtsvorm = QLabel()
            q5Edit = QLineEdit()
            q5Edit.setFixedWidth(200)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp("^.{1,30}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            self.BTWnummer =  QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(170)
            q2Edit.setText("")
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed)
            reg_ex = QRegExp("^[NLnl]{2}[0-9]{9}[Bb]{1}[0-9]{2}$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
            
            self.KvKnummer =  QLabel()
            q4Edit = QLineEdit()
            q4Edit.setFixedWidth(120)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
       
            self.Postcode = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setFixedWidth(80)
            font = QFont("Arial",10)
            font.setCapitalization(QFont.AllUppercase)
            q6Edit.setFont(font)
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
            
            self.Huisnummer = QLabel()
            q7Edit = QLineEdit()
            q7Edit.setFixedWidth(60)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[0-9]{1,5}$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
    
            self.Toevoeging = QLabel()
            q8Edit = QLineEdit()
            q8Edit.setFixedWidth(80)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            reg_ex = QRegExp("^[A-Za-z0-9-]{0,10}")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
               
            self.Telefoonnr = QLabel()
            q12Edit = QLineEdit()
            q12Edit.setFixedWidth(120)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed)
            reg_ex = QRegExp("^[0]{1}[0-9]{9}$")
            input_validator = QRegExpValidator(reg_ex, q12Edit)
            q12Edit.setValidator(input_validator)
            
            self.Leveranciernummer =  QLabel()
            q13Edit = QLineEdit(str(mlevnr))
            q13Edit.setFixedWidth(110)
            q13Edit.setStyleSheet("color: black")
            q13Edit.setAlignment(Qt.AlignRight)
            q13Edit.setDisabled(True)
            q13Edit.setFont(QFont("Arial",10))
             
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 2, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Nieuwe leverancier invoeren'), 0, 1, 1, 2,Qt.AlignCenter)
                        
            grid.addWidget(QLabel('                              *'), 1, 0) 
            grid.addWidget(QLabel('Verplichte velden'), 1, 1)   
                         
            grid.addWidget(QLabel('Bedrijfsnaam           *'), 2, 0)
            grid.addWidget(q3Edit, 2, 1, 1, 3)  
                 
            grid.addWidget(QLabel('Rechtsvorm             *'), 3, 0)
            grid.addWidget(q5Edit, 3, 1) 
            
            grid.addWidget(QLabel('BTWnummer   *'), 3, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q2Edit, 3, 2) 
            
            grid.addWidget(QLabel('KvKnummer             *'), 4, 0)
            grid.addWidget(q4Edit, 4, 1) 
                 
            grid.addWidget(QLabel('Postcode  *'), 4, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q6Edit, 4, 2)
     
            grid.addWidget(QLabel('Huisnummer            *'), 5, 0)
            grid.addWidget(q7Edit, 5, 1)
    
            grid.addWidget(QLabel('Toevoeging'), 5, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 5, 2)
      
            grid.addWidget(QLabel('Telefoonnummer      *'), 6, 0)
            grid.addWidget(q12Edit, 6, 1) 
            
            grid.addWidget(QLabel('Leveranciernummer'), 7, 0)
            grid.addWidget(q13Edit, 7, 1) 
                                
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 1)
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
            
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 7, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 6, 2, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
          
        def q3Changed(self, text):
            self.Bedrijfsnaam.setText(text)
                    
        def q5Changed(self, text):
            self.Rechtsvorm.setText(text)
            
        def q2Changed(self, text):
            self.BTWnummer.setText(text)      
            
        def q4Changed(self, text):
            self.KvKnummer.setText(text)
    
        def q6Changed(self, text):
            self.Postcode.setText(text)
                  
        def q7Changed(self, text):
            self.Huisnummer.setText(text)
    
        def q8Changed(self, text):
            self.Toevoeging.setText(text)
        
        def q12Changed(self, text):
            self.Telefoonnr.setText(text)
            
        def returnBedrijfsnaam(self):
            return self.Bedrijfsnaam.text()
        
        def returnRechtsvorm(self):
            return self.Rechtsvorm.text()
    
        def returnBTWnummer(self):
            return self.BTWnummer.text()
        
        def returnKvKnummer(self):
            return self.KvKnummer.text()
    
        def returnPostcode(self):
            return self.Postcode.text()
        
        def returnHuisnummer(self):
            return self.Huisnummer.text()
    
        def returnToevoeging(self):
            return self.Toevoeging.text()
        
        def returnTelefoonnummer(self):
            return self.Telefoonnr.text()   
    
         
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnBedrijfsnaam(), dialog.returnRechtsvorm(),\
                    dialog.returnBTWnummer(), dialog.returnKvKnummer(),\
                    dialog.returnPostcode(), dialog.returnHuisnummer(),\
                    dialog.returnToevoeging(), dialog.returnTelefoonnummer()]
               
    window = Widget()
    data = window.getData()
    mbedrijfsnaam = (data[0]).title()
    mrechtsvorm = (data[1]).upper()
    mbtwnr = data[2].upper()
    mkvknr = data[3]
    mpostcode = (data[4]).upper()
    mhuisnr = data[5]
    if not (mbedrijfsnaam and mrechtsvorm and mpostcode and mhuisnr):
        geenGegevens()
        bepaalLeverancier(m_email)
    mhuisnr = int(mhuisnr)
    mtoev = (data[6])
    if mtoev:
        mtoev = '-'+mtoev
    mtelnr = (data[7])
    if data[7]:
        if len(mtelnr) < 10:
            foutTelnr()
            bepaalLeverancier(m_email)
    else:
            geenGegevens()
            bepaalLeverancier(m_email)
    import postcode
    if postcode.checkpostcode(mpostcode,mhuisnr)[0]:
        metadata = MetaData()

        leveranciers = Table('leveranciers', metadata,
            Column('leverancierID', Integer(), primary_key=True),
            Column('bedrijfsnaam', String),
            Column('rechtsvorm', String),
            Column('btwnummer', String),
            Column('kvknummer', String),
            Column('telnr', String(10)),
            Column('huisnummer', String(5), nullable=False),
            Column('postcode', String(6), nullable=False),       
            Column('toevoeging', String))
                        
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
                                             
        conn = engine.connect()
        s = select([leveranciers.c.leverancierID]).\
                where(leveranciers.c.leverancierID == mlevnr)
        result = conn.execute(s).first()
        
        if result:
            conn.close()
            leverancierBestaat()
            bepaalLeverancier(m_email)
        else:
            inslev = leveranciers.insert().values(
            leverancierID=mlevnr,  
            bedrijfsnaam=mbedrijfsnaam,
            rechtsvorm=mrechtsvorm,
            btwnummer=mbtwnr,
            kvknummer=mkvknr,
            postcode=mpostcode,
            huisnummer=mhuisnr,
            toevoeging=mtoev,
            telnr=mtelnr)
            result = conn.execute(inslev)
            inslev.bind = engine
            result.inserted_primary_key
            conn.close()
            Invoer()
    else:
           foutPostcode()
    bepaalLeverancier(m_email)