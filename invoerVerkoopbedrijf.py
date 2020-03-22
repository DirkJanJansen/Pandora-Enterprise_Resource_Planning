from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
           QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import  QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                             create_engine, func)
from sqlalchemy.sql import select

def foutBtwnr(): 
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Foutief BTW nummer!')
    msg.setWindowTitle('Gegevens!')
    msg.exec_()
    
def foutKvknr(): 
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Foutief KVK nummer!')
    msg.setWindowTitle('Gegevens!')
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
 
def koperBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Bedrijf-Verkoop is al aanweizg!')
    msg.setWindowTitle('Bedrijf-Verkoop')
    msg.exec_()

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalKoper():
    metadata = MetaData()
    kopers = Table('kopers', metadata,
        Column('koperID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    mkopernr=(conn.execute(select([func.max(kopers.c.koperID, type_=Integer)\
                                   .label('mkopernr')])).scalar())
    mkopernr=int(maak11proef(mkopernr))
    conn.close
    return(mkopernr)
   
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt!')
    msg.setWindowTitle('Bedrijven Verkoop')
    msg.exec_()

def invBedrijf(m_email):                                 
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Invoer Bedrijf Verkoop")
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
            
            self.Afdeling = QLabel()
            q14Edit = QLineEdit()
            q14Edit.setFixedWidth(540)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.textChanged.connect(self.q14Changed)
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q14Edit)
            q14Edit.setValidator(input_validator)
            
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
            
            self.Bedrijfsnummer =  QLabel()
            q13Edit = QLineEdit()
            q13Edit.setText(str(bepaalKoper()))
            q13Edit.setAlignment(Qt.AlignRight)
            q13Edit.setStyleSheet("color: black")
            q13Edit.setFixedWidth(110)
            q13Edit.setDisabled(True)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.textChanged.connect(self.q13Changed)
            
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
            grid.addWidget(QLabel('Nieuwe Bedrijf-Verkoop invoeren'), 0, 1, 1, 2,Qt.AlignCenter)
                        
            grid.addWidget(QLabel('                              *'), 1, 0) 
            grid.addWidget(QLabel('Verplichte velden'), 1, 1)   
                         
            grid.addWidget(QLabel('Bedrijfsnaam           *'), 2, 0)
            grid.addWidget(q3Edit, 2, 1, 1, 3) 
            
            grid.addWidget(QLabel('Afdelingsnaam/Kamer/\nKontaktpersoon'), 3, 0)
            grid.addWidget(q14Edit, 3, 1, 1, 3)  
                 
            grid.addWidget(QLabel('Rechtsvorm             *'), 4, 0)
            grid.addWidget(q5Edit, 4, 1) 
            
            grid.addWidget(QLabel('BTWnummer   *'), 4, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q2Edit, 4, 2) 
            
            grid.addWidget(QLabel('KvKnummer            *'), 5, 0)
            grid.addWidget(q4Edit, 5, 1) 
                 
            grid.addWidget(QLabel('Postcode    *'), 5, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q6Edit, 5, 2)
     
            grid.addWidget(QLabel('Huisnummer           *'), 6, 0)
            grid.addWidget(q7Edit, 6, 1)
    
            grid.addWidget(QLabel('Toevoeging'), 6, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 6, 2)
     
            grid.addWidget(QLabel('Telefoonnummer     *'), 7, 0)
            grid.addWidget(q12Edit, 7, 1) 
            
            grid.addWidget(QLabel('Bedrijf-Verkoopnummer'), 8, 0)
            grid.addWidget(q13Edit, 8, 1) 
                                
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 1)
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
            
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 8, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 7, 2, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
         
        def q3Changed(self, text):
            self.Bedrijfsnaam.setText(text)
            
        def q14Changed(self, text):
            self.Afdeling.setText(text)
                    
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
            
        def q13Changed(self, text):
            self.Bedrijfsnummer.setText(text)
                
        def returnBedrijfsnaam(self):
            return self.Bedrijfsnaam.text()
        
        def returnAfdeling(self):
            return self.Afdeling.text()
        
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
    
        def returnBedrijfsnummer(self):
            return self.Bedrijfsnummer.text() 
       
         
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnBedrijfsnaam(), dialog.returnRechtsvorm(),\
                    dialog.returnBTWnummer(), dialog.returnKvKnummer(),\
                    dialog.returnPostcode(), dialog.returnHuisnummer(),\
                    dialog.returnToevoeging(), dialog.returnTelefoonnummer(),\
                    dialog.returnBedrijfsnummer(),dialog.returnAfdeling()]
                    
    window = Widget()
    data = window.getData()
    mbedrijfsnaam = (data[0]).title()
    mrechtsvorm = (data[1]).upper()
    if data[2] and len(data[2]) == 14:
        mbtwnr = data[2].upper()
    else:
        foutBtwnr()
        invBedrijf(m_email)
    if data[3] and len(data[3]) == 8:
        mkvknr = data[3]
    else:
        foutKvknr()
        invBedrijf(m_email)
    mpostcode = (data[4]).upper()
    mhuisnr = data[5]
    if not (mbedrijfsnaam and mrechtsvorm and mpostcode and mhuisnr):
        geenGegevens()
        invBedrijf(m_email)
    mhuisnr = int(mhuisnr)
    mtoev = (data[6])
    if mtoev:
        mtoev = '-'+mtoev
    mtelnr = (data[7])
    if data[7]:
        if len(mtelnr) < 10:
            foutTelnr()
            invBedrijf(m_email)
    else:
            geenGegevens()
            invBedrijf(m_email)
    mkopernr = (data[8])
    if data[9]:
        mafd = data[9]
    else:
        mafd = ''
    import postcode
    if postcode.checkpostcode(mpostcode,mhuisnr):
        metadata = MetaData()

        kopers = Table('kopers', metadata,
            Column('koperID', Integer(), primary_key=True),
            Column('bedrijfsnaam', String),
            Column('rechtsvorm', String),
            Column('btwnummer', String),
            Column('kvknummer', String),
            Column('telnr', String(10)),
            Column('huisnummer', String(5), nullable=False),
            Column('postcode', String(6), nullable=False),       
            Column('toevoeging', String),
            Column('afdeling', String))
                        
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        
        mkopernr=bepaalKoper()
                                 
        conn = engine.connect()
        s = select([kopers.c.koperID]).\
                where(kopers.c.koperID == mkopernr)
        result = conn.execute(s).first()
        
        if result:
            conn.close()
            koperBestaat()
            invBedrijf(m_email)
        else:
            inskop = kopers.insert().values(
            koperID=mkopernr,  
            bedrijfsnaam=mbedrijfsnaam,
            rechtsvorm=mrechtsvorm,
            btwnummer=mbtwnr,
            kvknummer=mkvknr,
            postcode=mpostcode,
            huisnummer=mhuisnr,
            toevoeging=mtoev,
            telnr=mtelnr,
            afdeling = mafd)
            conn.execute(inskop)
            conn.close()
            Invoer()
    else:
            postcode.foutPostc()  
            invBedrijf(m_email)