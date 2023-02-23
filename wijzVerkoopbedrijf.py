from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                           QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                            create_engine, update)
from sqlalchemy.sql import select
  
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def wijzWindow(self, m_email):
    self.close()
    zoekKoper(m_email)
       
def foutTelnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('no 10 digits!')
    msg.setWindowTitle('Sales company')
    msg.exec_()
    
def foutKopernr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Company not found')
    msg.setWindowTitle('Sales company')
    msg.exec_()
         
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Your data has been adjusted!')
    msg.setWindowTitle('Sales company')
    msg.exec_()
           
def zoekKoper(m_email):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify sales company.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Bedrijfsnummer = QLabel()
            levEdit = QLineEdit()
            levEdit.setFixedWidth(100)
            levEdit.setFont(QFont("Arial",10))
            levEdit.textChanged.connect(self.levChanged)
            reg_ex = QRegExp('^[6]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            levEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)
         
            grid.addWidget(QLabel('Sales company'), 1, 1)
            grid.addWidget(levEdit, 1, 2)
       
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
    
        def levChanged(self, text):
            self.Bedrijfsnummer.setText(text)
    
        def returnBedrijfsnummer(self):
            return self.Bedrijfsnummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnBedrijfsnummer()]
       
    window = Widget()
    data = window.getData()
    if data[0]:
        mkopernr = int(data[0])
    else:
          mkopernr = 0
    
    metadata = MetaData()

    kopers = Table('kopers', metadata,
        Column('koperID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([kopers]).where(kopers.c.koperID == mkopernr)
    rpkop = conn.execute(s).first()
    
    if rpkop:
        updateKoper(m_email, mkopernr)
    else:
        foutKopernr()
        zoekKoper(m_email)
        
def updateKoper(m_email, mkopernr):
    metadata = MetaData()
    kopers= Table('kopers', metadata,
        Column('koperID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('btwnummer', String),
        Column('kvknummer', String),
        Column('telnr', String),
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('postcode', String),
        Column('afdeling', String))       
              
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([kopers]).where(kopers.c.koperID == mkopernr)
    rpkop = conn.execute(sel).first()
    if rpkop:
        mkopernr = rpkop[0]
        mbedrnaam = rpkop[1]
        mrechtsvorm = rpkop[2]
        mbtwnr = rpkop[3]
        mkvknr = rpkop[4]
        mtelnr = rpkop[5]
        mhuisnr = rpkop[6]
        mhuisnr = int(mhuisnr)
        mtoev = rpkop[7]
        mpostcode = rpkop[8]
        mafdeling = rpkop[9]
        import postcode
        mstrtplts = postcode.checkpostcode(mpostcode,mhuisnr)
        mstraat = mstrtplts[0]
        mplaats = mstrtplts[1]
                                
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify sales company")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                  
            self.Bedrijfsnaam = QLabel()
            q3Edit = QLineEdit(mbedrnaam)
            q3Edit.setText(mbedrnaam)
            q3Edit.setFixedWidth(540)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^[^0-9]{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Afdeling = QLabel()
            q16Edit = QLineEdit()
            q16Edit.setText(mafdeling)
            q16Edit.setFixedWidth(540)
            q16Edit.setFont(QFont("Arial",10))
            q16Edit.textChanged.connect(self.q16Changed)
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q16Edit)
            q16Edit.setValidator(input_validator)
                
            self.Rechtsvorm = QLabel()
            q5Edit = QLineEdit()
            q5Edit.setText(mrechtsvorm)
            q5Edit.setFixedWidth(100)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp("^[^0-9]{1,30}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            self.BTWnummer =  QLabel()
            q2Edit = QLineEdit()
            q2Edit.setText(str(mbtwnr))
            q2Edit.setDisabled(True)
            q2Edit.setFixedWidth(170)
            q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed)
            reg_ex = QRegExp("^[A-Za-z]{2}[0-9]{9}[Bb]{1}[0-9]{2}$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
            
            self.KvKnummer =  QLabel()
            q4Edit = QLineEdit()
            q4Edit.setText(str(mkvknr))
            q4Edit.setFixedWidth(110)
            q4Edit.setDisabled(True)
            q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.Straat =  QLabel()
            q1Edit = QLineEdit()
            q1Edit.setText(mstraat)
            q1Edit.setFixedWidth(540)
            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q1Edit.setDisabled(True)
    
            self.Huisnummer = QLabel()
            q7Edit = QLineEdit()
            q7Edit.setText(str(mhuisnr))
            q7Edit.setAlignment(Qt.AlignRight)
            q7Edit.setFixedWidth(60)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[0-9]{1,5}$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
        
            self.Toevoeging = QLabel()
            q8Edit = QLineEdit('')
            q8Edit.setFixedWidth(80)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            q8Edit.setText(mtoev)
            reg_ex = QRegExp("^[A-Za-z0-9-#]{0,10}")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
            
            self.Postcode = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setText(mpostcode)
            q6Edit.setFixedWidth(80)
            font = QFont("Arial",10)
            font.setCapitalization(QFont.AllUppercase)
            q6Edit.setFont(font)
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
               
            self.Woonplaats =  QLabel()
            q15Edit = QLineEdit()
            q15Edit.setText(mplaats)
            q15Edit.setFixedWidth(400)
            q15Edit.setDisabled(True)
            q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
               
            self.Telefoonnr = QLabel()
            q13Edit = QLineEdit('')
            q13Edit.setFixedWidth(120)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.textChanged.connect(self.q13Changed)
            q13Edit.setText(mtelnr)
            reg_ex = QRegExp("^[0]{1}[0-9]{9}$")
            input_validator = QRegExpValidator(reg_ex, q13Edit)
            q13Edit.setValidator(input_validator)
            
            self.Bedrijfverkoopnummer =  QLabel()
            q14Edit = QLineEdit()
            q14Edit.setText(str(mkopernr))
            q14Edit.setAlignment(Qt.AlignRight)
            q14Edit.setFixedWidth(120)
            q14Edit.setDisabled(True)
            q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.textChanged.connect(self.q14Changed)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)
   
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Modifications sales company'), 0, 1)
                        
            grid.addWidget(QLabel('                                  *'), 1, 0) 
            grid.addWidget(QLabel('Required fields'), 1, 1)   
                         
            grid.addWidget(QLabel('Company name           *'), 2, 0)
            grid.addWidget(q3Edit, 2, 1, 1, 3) 
            
            grid.addWidget(QLabel('Department name/Room/\nContact person'), 3, 0)
            grid.addWidget(q16Edit, 3, 1, 1, 3)  
                 
            grid.addWidget(QLabel('Legal status                *'), 4, 0)
            grid.addWidget(q5Edit, 4, 1) 
            
            grid.addWidget(QLabel('VATnumber   *'), 4, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q2Edit, 4, 2) 
            
            grid.addWidget(QLabel('KvKnumber                 *'), 5, 0)
            grid.addWidget(q4Edit, 5, 1) 
            
            grid.addWidget(QLabel('Street'),6, 0)
            grid.addWidget(q1Edit, 6, 1, 1, 3)
     
            grid.addWidget(QLabel('Housenumber             *'), 7, 0)
            grid.addWidget(q7Edit, 7, 1)
    
            grid.addWidget(QLabel('Suffix'), 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 7, 2)
            
            grid.addWidget(QLabel('Zipcode Residence     *'), 8, 0)
            grid.addWidget(q6Edit, 8, 1)
            
            grid.addWidget(q15Edit, 8, 1, 1, 2, Qt.AlignRight) 
     
            grid.addWidget(QLabel('Telephonenumber       *'), 9, 0)
            grid.addWidget(q13Edit, 9, 1) 
            
            grid.addWidget(QLabel('SalesCompanynumber'), 10, 0)
            grid.addWidget(q14Edit, 10, 1) 
                                
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 1)
              
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: wijzWindow(self,m_email))
            
            applyBtn = QPushButton('Modify')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 10, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 9, 2, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
               
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
          
        def q3Changed(self, text):
            self.Bedrijfsnaam.setText(text)
            
        def q16Changed(self, text):
            self.Afdeling.setText(text)
                   
        def q5Changed(self, text):
            self.Rechtsvorm.setText(text)
            
        def q2Changed(self, text):
            self.BTWnummer.setText(text)      
            
        def q4Changed(self, text):
            self.KvKnummer.setText(text)
      
        def q1Changed(self, text):
            self.Straat.setText(text)
                  
        def q7Changed(self, text):
            self.Huisnummer.setText(text)
    
        def q8Changed(self, text):
            self.Toevoeging.setText(text)          
    
        def q6Changed(self, text):
            self.Postcode.setText(text)
            
        def q15Changed(self, text):
            self.Woonplaats.setText(text)
              
        def q13Changed(self, text):
            self.Telefoonnr.setText(text)
            
        def q14Changed(self, text):
            self.Bedrijfverkoopnummer.setText(text)
                
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
        
        def returnStraat(self):
            return self.Straat.text()
   
        def returnHuisnummer(self):
            return self.Huisnummer.text()
    
        def returnToevoeging(self):
            return self.Toevoeging.text()
    
        def returnPostcode(self):
            return self.Postcode.text()
        
        def returnWoonplaats(self):
            return self.Woonplaats.text()
           
        def returnTelefoonnummer(self):
            return self.Telefoonnr.text()   
    
        def returnBedrijfverkoopnummer(self):
            return self.Bedrijfverkoopnummer.text() 
         
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnBedrijfsnaam(), dialog.returnRechtsvorm(),\
                    dialog.returnBTWnummer(), dialog.returnKvKnummer(),\
                    dialog.returnStraat(),dialog.returnHuisnummer(),\
                    dialog.returnToevoeging(), dialog.returnPostcode(),\
                    dialog.returnWoonplaats(), dialog.returnTelefoonnummer(),\
                    dialog.returnBedrijfverkoopnummer(), dialog.returnAfdeling()]
                
    window = Widget()
    data = window.getData()
    if data[0]:
        mbedrnaam = (data[0])
    else:
        mbedrnaam = rpkop[1]
    if data[1]:
        mrechtsvorm = (data[1]).upper()
    else:
        mrechtsvorm = rpkop[2]
    if data[2]:
        mbtwnr = data[2].upper()
    else:
        mbtwnr = rpkop[3]
    if data[3]:
        mkvknr = data[3]
    else:
        mkvknr = rpkop[4]
    if data[7]:
        mpostcode = data[7].upper()
    else:
        mpostcode = rpkop[8]
    if data[5]:
        mhuisnr = data[5]
    else:
        mhuisnr = rpkop[6]
    mhuisnr = int(mhuisnr)
    if data[6]:
        mtoev = '-'+data[6]
    else:
        mtoev = ''
    if data[9]:
        mtelnr = data[9]
    else:
        mtelnr = ''
    if not (len(mtelnr) == 10 or mtelnr == ''):
        foutTelnr()
        hoofdMenu(m_email) 
    if data[11]:
        mafdeling = data[11]
    else:
        mafdeling = rpkop[9]
                                            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    u = update(kopers).where(kopers.c.koperID == mkopernr).\
     values(bedrijfsnaam = mbedrnaam, rechtsvorm = mrechtsvorm, btwnummer =\
           mbtwnr, kvknummer = mkvknr, telnr = mtelnr, postcode = mpostcode,\
           huisnummer = mhuisnr, toevoeging = mtoev, afdeling = mafdeling)  
    conn.execute(u) 
    conn.close()
    updateOK()  
    zoekKoper(m_email)