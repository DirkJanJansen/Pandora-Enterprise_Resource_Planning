from login import hoofdMenu
import datetime
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QLabel, QPushButton,QGridLayout,\
     QMessageBox, QDialog, QLineEdit 
from sqlalchemy import (Table, Column, Integer, Boolean, MetaData, create_engine, select, func)

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
   
def _11check(martikelnr):
    number = str(martikelnr)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def bepaalWerknr():
    metadata = MetaData()
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    mwerknr=(conn.execute(select([func.max(orders_intern.c.werkorderID, type_=Integer)\
                                   .label('mwerknr')])).scalar())
    mwerknr=int(maak11proef(mwerknr))
    conn.close
    return(mwerknr)

def jaarweek():
    dt = datetime.datetime.now()
    week = ('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def foutInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Verplichte Invoer!')
    msg.setWindowTitle('Invoer werkorders')
    msg.exec_()
  
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt!')
    msg.setWindowTitle('Invoeren werkorders')
    msg.exec_()
    
def foutArtikel():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutief Artikelnummer ingevoerd!')
    msg.setWindowTitle('Invoer Artikelnummer')               
    msg.exec_() 
    
def geenArtnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen bestaand artikel gevonden\nNieuw artikelnummer wordt aangemaakt!')
    msg.setWindowTitle('Invoer Artikelnummer')               
    msg.exec_() 

def invWerkorder(m_email):
    from sqlalchemy import (Table, Column, String, Integer, Float, MetaData,\
                            create_engine, update, insert)
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Invoer werkorders")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                                                 
            self.Omschrijving = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            reg_ex = QRegExp("^.{0,49}$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
                                     
            self.StartWerk = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(110)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
            
            self.Artikelnummer = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setFixedWidth(110)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed) 
            reg_ex = QRegExp("^[2]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Hoeveelheid = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setFixedWidth(110)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
                      
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl1 = QLabel('Werkorder')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            
            lbl2 = QLabel(str(bepaalWerknr()))
            grid.addWidget(lbl2, 1, 1)
                   
            lbl3 = QLabel('Omschrijving')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 2, 0)
            grid.addWidget(q1Edit, 2, 1, 1, 3)
              
            lbl4 = QLabel('Start werk')  
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 3, 0)
            grid.addWidget(q2Edit, 3, 1)
        
            lbl5 = QLabel('Artikelnummer\n       Halffabrikaat   ')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 4, 0)
            grid.addWidget(q3Edit, 4, 1) 
            
            lbl6 = QLabel('Hoeveelheid')  
            lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl6, 5, 0)
            grid.addWidget(q4Edit, 5, 1) 
           
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                                 
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 3, Qt.AlignCenter)          
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
            applyBtn = QPushButton('Invoer')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 6, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 6, 1, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                 
        def q1Changed(self,text):
            self.Omschrijving.setText(text)
    
        def q2Changed(self,text):
            self.StartWerk.setText(text)
    
        def q3Changed(self,text):
            self.Artikelnummer.setText(text)
            
        def q4Changed(self,text):
            self.Hoeveelheid.setText(text)
     
        def returnq1(self):
            return self.Omschrijving.text()
        
        def returnq2(self):
            return self.StartWerk.text()
        
        def returnq3(self):
            return self.Artikelnummer.text()
            
        def returnq4(self):
            return self.Hoeveelheid.text()
     
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(), dialog.returnq4()]  
                          
    window = Widget()
    data = window.getData()
    if data[0]:
        ms0 = str(data[0])
    else:
        foutInvoer()
        invWerkorder(m_email)
    if data[1] and len(data[1]) == 10:
        mf1 = str(data[1])
    else:
        foutInvoer()
        invWerkorder(m_email)
    if data[3]:
        mf3 = float(data[3])
    else: 
        foutInvoer()
        invWerkorder(m_email)
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('categorie', Integer),
        Column('artikelgroep', String),
        Column('art_eenheid', String),
        Column('bestelsaldo', Float),
        Column('bestelstatus', Boolean))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selart = select([artikelen]).where(artikelen.c.artikelID==int(data[2]))
    if con.execute(selart):
        mf2 = int(data[2])
        updart = update(artikelen).where(artikelen.c.artikelID == int(mf2)).\
                values(bestelsaldo = artikelen.c.bestelsaldo+mf3, bestelstatus = True)
        con.execute(updart)
    else:
        foutInvoer()
        invWerkorder(m_email) 
        
    mboekd = str(datetime.datetime.now())[0:10] 
        
    from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, create_engine, ForeignKey)
    from sqlalchemy.exc import IntegrityError
    
    metadata = MetaData()
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer(), primary_key=True),
        Column('werkomschrijving', String(50)),
        Column('voortgangstatus', String(1)),
        Column('besteldatum', String),
        Column('statusweek',  String(6)),
        Column('startdatum', String),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('hoeveelheid', Float),
        Column('gereed', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    metadata.create_all(engine)
    conn = engine.connect()
    try:
        inswrk = insert(orders_intern).values(
        werkorderID=bepaalWerknr(),  
        werkomschrijving=ms0,
        besteldatum = mboekd,
        voortgangstatus='A',
        statusweek=jaarweek(),
        startdatum=mf1,
        artikelID = mf2,
        hoeveelheid = mf3)
        result = conn.execute(inswrk)
    except IntegrityError:
        foutArtikel()
        invWerkorder(m_email)
    result.close
    conn.close
    Invoer()
    invWerkorder(m_email)