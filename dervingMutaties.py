from login import hoofdMenu
import  datetime
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QMessageBox,\
                             QLineEdit, QGridLayout, QDialog
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, CheckConstraint, ForeignKey)
from sqlalchemy.sql import select, update, insert, func
from sqlalchemy.exc import IntegrityError
 
def _11check(mcontr):
    number = str(mcontr)
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
    
def foutInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Incorrect article number specified.!')
    msg.setWindowTitle('Mutating loss articles')               
    msg.exec_() 
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect\ninput search term!')
    msg.setWindowTitle('Provide / printing materials')               
    msg.exec_() 
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Provide / printing materials')               
    msg.exec_() 
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Mutating loss articles')
    msg.exec_()
				            
def negVoorraad():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Too little stock for the transaction!')
        msg.setWindowTitle('Mutating loss articles')
        msg.exec_()
        
def foutHoev():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Not the right amount!')
        msg.setWindowTitle('Mutating loss articles')
        msg.exec_()
                
def dervingMut(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Mutate material provision")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                       
            self.Dervingnummer = QLabel()
            derving = QComboBox()
            derving.setFixedWidth(200)
            derving.setFont(QFont("Times", 10))
            derving.setStyleSheet("color: black;  background-color: #F8F7EE")
            derving.addItem(' Choose type off loss')
            derving.addItem('1. Obsolete.')
            derving.addItem('2. Warehouse differences.')
            derving.addItem('3. Damaged')
            derving.addItem('4. Shelf life')
            derving.activated[str].connect(self.dervingChanged)
                              
            self.Artikelnummer = QLabel()
            artEdit = QLineEdit()
            artEdit.setFixedWidth(150)
            artEdit.setFont(QFont("Arial",10))
            artEdit.textChanged.connect(self.artChanged) 
            reg_ex = QRegExp("^[2]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, artEdit)
            artEdit.setValidator(input_validator)
            
            self.Hoeveelheid = QLabel()
            hoevEdit = QLineEdit()
            hoevEdit.setFixedWidth(150)
            hoevEdit.setFont(QFont("Arial",10))
            hoevEdit.textChanged.connect(self.hoevChanged) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, hoevEdit)
            hoevEdit.setValidator(input_validator)
           
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight) 
                         
            lbl1 = QLabel('Loss number')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(derving, 1, 1)
                                          
            lbl2 = QLabel('Article number')  
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 2, 0)
            grid.addWidget(artEdit, 2, 1)
             
            lbl3 = QLabel('Amount')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 3, 0)
            grid.addWidget(hoevEdit, 3 , 1)
                                             
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
            applyBtn = QPushButton('Mutate')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 5, 1, 1 , 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
            
            grid.addWidget(cancelBtn,5, 1, Qt.AlignCenter)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3, Qt.AlignCenter)     
                                                                      
        def dervingChanged(self, text):
            self.Dervingnummer.setText(text)
            
        def artChanged(self,text):
            self.Artikelnummer.setText(text)
            
        def hoevChanged(self,text):
            self.Hoeveelheid.setText(text)
                                                   
        def returnderving(self):
            return self.Dervingnummer.text()
        
        def returnart(self):
            return self.Artikelnummer.text()
        
        def returnhoev(self):
            return self.Hoeveelheid.text()
                              
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnderving(), dialog.returnart(), dialog.returnhoev()]
    
    window = Widget()
    data = window.getData()
    mhoev = 0
    if not data[0] or data[0][0] == ' ':
        ongInvoer()
        dervingMut(m_email)
    elif data[0][0] == '1':
        mderving = '999999990'
        momschr = 'Obsolete'
    elif data[0][0] == '2':
        mderving = '999999989'
        momschr = 'Warehouse differences'
    elif data[0][0] ==  '3':
        mderving = '999999977'
        momschr = 'Damaged'
    elif data[0][0] == '4':
        mderving = '999999965'
        momschr = 'Shelf life'
                   
    if data[1] and len(data[1]) == 9 and _11check(data[1]):
        martikelnr = int(data[1])
    else:
        foutInvoer()
        dervingMut(m_email)
    if data[2]:
        mhoev = float(data[2])
    else:
        foutHoev()
        dervingMut(m_email)
   
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float, CheckConstraint('art_voorraad >= 0')),
        Column('art_min_voorraad', Float),
        Column('bestelstatus', Boolean))
    derving = Table('derving', metadata,
        Column('dervingID', Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('categorienummer', None, ForeignKey('werken.werknoID')),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('boekdatum', String),
        Column('waarde', Float))
          
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    sel = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
    transaction = con.begin()
    result = con.execute(sel).first()
    if not result:
        geenRecord()
        dervingMut(m_email)
    martprijs = result[2]
    martvrd = result[3]
    martminvrd = result[4]
    mboekd = str(datetime.datetime.now())[0:10]
    if martvrd - mhoev <= martminvrd:
        martbestst = False
    else:
        martbestst = True
    if mhoev <= 0:
        foutHoev()
        dervingMut(m_email)
    try:
        stmt = update(artikelen).where(artikelen.c.artikelID == martikelnr).values(\
         art_voorraad = artikelen.c.art_voorraad - mhoev, bestelstatus = martbestst)
        con.execute(stmt)
        con = engine.connect()
        try:
            dervingnr=(con.execute(select([func.max(derving.c.dervingID,\
                type_=Integer)])).scalar())
            dervingnr += 1
        except:
            dervingnr = 1
            
        ins = insert(derving).values(dervingID = dervingnr, artikelID =\
            martikelnr, categorienummer = mderving, hoeveelheid = -mhoev, boekdatum = mboekd,\
            waarde = mhoev*martprijs, omschrijving = momschr)
        con.execute(ins)
        transaction.commit()
        invoerOK()
        dervingMut(m_email)
    except IntegrityError:
        transaction.rollback()
        negVoorraad()
        dervingMut(m_email)
    con.close 
 