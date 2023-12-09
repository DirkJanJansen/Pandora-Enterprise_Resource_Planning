from login import hoofdMenu
import os, datetime
from PyQt5.QtCore import Qt, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton,\
     QMessageBox, QLineEdit, QGridLayout, QDialog, QWidget,QTableView, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, CheckConstraint, ForeignKey)
from sqlalchemy.sql import select, update, insert, func, and_
from sqlalchemy.exc import IntegrityError

def refresh(keuze, zoekterm, m_email, route, self):
    self.close()
    raapLijst(keuze, zoekterm, m_email, route)   

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
 
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect\ninput search term!')
    msg.setWindowTitle('Picking/printing materials')               
    msg.exec_() 
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Picking/printing materials')               
    msg.exec_() 
 
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
    
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Just a moment printing is starting!')
    msg.setWindowTitle('Printing')
    msg.exec_()
    
def printGeg(filename):
    from sys import platform
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing picklist")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Do you want to print the picklist?")
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        if platform == 'win32':
            os.startfile(filename, "print")
        else:
            os.system("lpr "+filename)
        printing()
    
def foutWerknr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Work number not found\nWork number does not exist!')
    msg.setWindowTitle('Data!')
    msg.exec_()
        
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Picklist')
    msg.exec_()
    
def negVoorraad():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Too little stock for the transaction!')
        msg.setWindowTitle('Insufficient stock')
        msg.exec_()
        
def foutHoev():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
        msg.setIcon(QMessageBox.Warning)
        msg.setText('No changes\nimplemented!')
        msg.setWindowTitle('Input error')
        msg.exec_()

def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Work number is unsubscribed,\nbookings no longer possible!')
    msg.setWindowTitle('Data!')
    msg.exec_()
          
def eindProgram():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Program closed.\nGoodbye!')
    msg.setWindowTitle('Orders')               
    msg.exec_() 
				            
def printRaaplijst(keuze, zoekterm, m_email, route):
    import validZt
    metadata = MetaData()
    raaplijst = Table('raaplijst', metadata,
        Column('lijstID', Integer,primary_key=True),
        Column('artikelID', Integer),
        Column('werkorder', Integer),
        Column('afroep', Float),
        Column('leverdatum', String),
        Column('geleverd', Float),
        Column('meerwerk', Boolean),
        Column('postcode', String),
        Column('huisnummer', Integer),
        Column('toevoeging', String),
        Column('alternatief', String),
        Column('boekdatum', String),
        Column('straat', String),
        Column('woonplaats', String))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('locatie_magazijn', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if route < 2:
        if keuze == 1:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.geleverd < raaplijst.c.afroep,\
                 raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.werkorder, raaplijst.c.leverdatum)
            kop1 = 'Picklist all call-up '
            tekst1 = ''
        elif keuze == 2:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work orders '
        elif keuze == 3:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work numbers '
        elif keuze == 4 and validZt.zt(zoekterm, 15):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder == int(zoekterm),\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist order number '
        elif keuze == 5 and validZt.zt(zoekterm, 2):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.artikelID == int(zoekterm),\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist article number '
        elif keuze == 6 and validZt.zt(zoekterm, 10):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.leverdatum.like(zoekterm+'%'),
                raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
                artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum, raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist delivery date '
        elif keuze == 7 and validZt.zt(zoekterm, 9):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.postcode.ilike(zoekterm+'%'),\
                 raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
                 artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum, raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist zipcode '
        elif keuze == 8:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.geleverd >= raaplijst.c.afroep,\
               raaplijst.c.afroep > 0, raaplijst.c.artikelID == artikelen.c.artikelID))\
               .order_by(raaplijst.c.werkorder, raaplijst.c.leverdatum)
            kop1 = 'Completed ' 
            tekst1 = ''
        else:
            ongInvoer()
            kiesSelektie(route, m_email)
    elif route == 2:
        if keuze == 2:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work orders '
        elif keuze == 4 and validZt.zt(zoekterm, 15):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
              raaplijst.c.werkorder == int(zoekterm), raaplijst.c.geleverd < raaplijst.c.afroep,\
              raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work order '
        elif keuze == 5 and validZt.zt(zoekterm, 2):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
              raaplijst.c.artikelID == int(zoekterm), raaplijst.c.geleverd < raaplijst.c.afroep,\
              raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist artlicle number '
        elif keuze == 6 and validZt.zt(zoekterm, 10):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
                raaplijst.c.leverdatum.like(zoekterm+'%'), raaplijst.c.geleverd < raaplijst.c.afroep,\
                raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum,\
                raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist delivery date '
        elif keuze == 7 and validZt.zt(zoekterm, 9):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
                 raaplijst.c.postcode.ilike(zoekterm+'%'),raaplijst.c.geleverd < raaplijst.c.afroep,\
                 raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum,\
                 raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist zipcode '
        elif keuze == 8:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder < 800000000,\
               raaplijst.c.geleverd >= raaplijst.c.afroep, raaplijst.c.afroep > 0,\
               raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.werkorder,\
                raaplijst.c.leverdatum)
            kop1 = 'Completed ' 
            tekst1 = ''
        else:
            ongInvoer()
            kiesSelektie(route, m_email)
    elif route == 3:
        if keuze == 3:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
              raaplijst.c.geleverd < raaplijst.c.afroep, raaplijst.c.artikelID ==\
              artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work numbers '
        elif keuze == 4 and validZt.zt(zoekterm, 15):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
              raaplijst.c.werkorder == int(zoekterm), raaplijst.c.geleverd < raaplijst.c.afroep,\
              raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist work number '
        elif keuze == 5 and validZt.zt(zoekterm, 2):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
              raaplijst.c.artikelID == int(zoekterm), raaplijst.c.geleverd < raaplijst.c.afroep,\
              raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum)
            kop1 = ''
            tekst1 = 'Picklist article number '
        elif keuze == 6 and validZt.zt(zoekterm, 10):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
                raaplijst.c.leverdatum.like(zoekterm+'%'), raaplijst.c.geleverd < raaplijst.c.afroep,\
                raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum,\
                raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist delivery date '
        elif keuze ==7 and validZt.zt(zoekterm, 9):
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
                 raaplijst.c.postcode.ilike(zoekterm+'%'), raaplijst.c.geleverd < raaplijst.c.afroep,\
                 raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.leverdatum,\
                 raaplijst.c.werkorder)
            kop1 = ''
            tekst1 = 'Picklist zipcode '
        elif keuze == 8:
            selrl = select([raaplijst, artikelen]).where(and_(raaplijst.c.werkorder > 800000000,\
                raaplijst.c.geleverd >= raaplijst.c.afroep, raaplijst.c.afroep > 0,\
                raaplijst.c.artikelID == artikelen.c.artikelID)).order_by(raaplijst.c.werkorder,\
                raaplijst.c.leverdatum)
            kop1 = 'Completed ' 
            tekst1 = ''
        else:
            ongInvoer()
            kiesSelektie(route, m_email)
    
    if con.execute(selrl).fetchone():
       rprl = con.execute(selrl)
    else:
       geenRecord()
       kiesSelektie(route, m_email)
    
    mblad = 1
    rgl = 0

    for row in rprl:
        from sys import platform
        if rgl == 0 or rgl%57 == 0:
            kop4=\
    (tekst1+str(kop1)+' Date: '+str(datetime.datetime.now())[0:10]+'  Page :  '+str(mblad)+' '+
     'Delivery address '+row[12]+' '+str(row[8])+row[9]+', '+row[7]+' '+row[13]+'.\n'+
    '=============================================================================================\n'+
    'Articlenr  Description                        Call-upDelivered   _date   Workorder  Location \n'+
    '=============================================================================================\n')
            kop5=\
    (tekst1+str(kop1)+' Datum: '+str(datetime.datetime.now())[0:10]+'  Blad :  '+str(mblad)+'\n'+
    '=============================================================================================\n'+
    'Artikelnr  Description                        Call-upDelivered   _date   Workorder  Location \n'+
    '=============================================================================================\n')
  
            if keuze == 2:
                kop1 = row[2]
                kop = kop5
            elif keuze == 3:
                kop1 = row[2]
                kop = kop5
            elif keuze == 4:
                kop1 = row[2]
                kop = kop4
            elif keuze == 5:
                kop1 = row[1]
                kop = kop5
            elif keuze == 6:
                kop1 = row[4]
                kop = kop5
            elif keuze == 7:
                kop1 = row[7]
                kop = kop4
            else:
                kop = kop5
            if platform == 'win32':
                filename = '.\\forms\\Raaplijsten\\picklist-'+str(kop1)+'-'+str(datetime.datetime.now())[0:10]+'.txt'
            else:
                filename = './forms/Raaplijsten/picklist-'+str(kop1)+'-'+str(datetime.datetime.now())[0:10]+'.txt'

            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<11d}'.format(row[1])+'{:<37.35s}'.format(row[15])\
            +'{:>6.2f}'.format(row[3])+'{:>6.2f}'.format(row[5])+'  '+\
            '{:10s}'.format(row[4])+' '+'{:<10d}'.format(row[2])+' '+'{:<10s}'.format(row[16])+'\n')
        rgl += 1
    printGeg(filename)
    kiesSelektie(route, m_email)
 
def kiesSelektie(route, m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            if route == 0:
                self.setWindowTitle("Picklist material")
            else:
                self.setWindowTitle("Picklist printing")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            if route < 2:
                self.Keuze = QLabel()
                k0Edit = QComboBox()
                k0Edit.setFixedWidth(240)
                k0Edit.setFont(QFont("Arial",10))
                k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
                k0Edit.addItem('  Search sort key')
                k0Edit.addItem('1. All call-up')
                k0Edit.addItem('2. Internal work order')
                k0Edit.addItem('3. External work order')
                k0Edit.addItem('4. By order number')
                k0Edit.addItem('5. By article number')
                k0Edit.addItem('6. By delivery date')
                k0Edit.addItem('7. By zipcode due\n     to transportation')
                k0Edit.addItem('8. Delivered call-off')
                k0Edit.activated[str].connect(self.k0Changed)
            elif route == 2:
                self.Keuze = QLabel()
                k0Edit = QComboBox()
                k0Edit.setFixedWidth(240)
                k0Edit.setFont(QFont("Arial",10))
                k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
                k0Edit.addItem('  Search sort key')
                k0Edit.addItem('2. Internal work order')
                k0Edit.addItem('4. By order number')
                k0Edit.addItem('5. By article number')
                k0Edit.addItem('6. By delivery date')
                k0Edit.addItem('7. By zipcode due\n     to transportation')
                k0Edit.addItem('8. Delivered call-off')
                k0Edit.activated[str].connect(self.k0Changed)
            elif route == 3:
                self.Keuze = QLabel()
                k0Edit = QComboBox()
                k0Edit.setFixedWidth(240)
                k0Edit.setFont(QFont("Arial",10))
                k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
                k0Edit.addItem('   Search sort key')
                k0Edit.addItem('3. External work numbers')
                k0Edit.addItem('4. By order number')
                k0Edit.addItem('5. By article number')
                k0Edit.addItem('6. By delivery date')
                k0Edit.addItem('7. By zipcode due\n     to transportation')
                k0Edit.addItem('8. Delivered call-off')
                k0Edit.activated[str].connect(self.k0Changed)  
                
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(240)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            if route == 0:
                grid.addWidget(QLabel('Drop-down menu for issuing materials'), 1, 0, 1, 3, Qt.AlignCenter)
            else:
                grid.addWidget(QLabel('Drop-down menu for printing picklists'), 1, 0, 1, 3, Qt.AlignCenter)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                                  
            grid.addWidget(k0Edit, 2, 1)
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved  dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
                      
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                                       
            grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 4, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk0(self):
            return self.Keuze.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzkterm()] 
    
    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1].upper()
    else:
        zoekterm = ''
    if route == 0:
        raapLijst(keuze,zoekterm, m_email, route)
    else:
        printRaaplijst(keuze, zoekterm, m_email, route)

def raapLijst(keuze, zoekterm, m_email, route):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Picklist Request / Mutate')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(boekAfroep)
            grid.addWidget(table_view, 0, 0, 1, 13)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 12, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Refresh')
            freshBtn.clicked.connect(lambda: refresh(keuze, zoekterm, m_email, route, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 11, 1, 1, Qt.AlignRight)
            
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 10)
          
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 0, 1, 13, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(50, 50, 1500, 900)
            
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
       
    metadata = MetaData()
    raaplijst = Table('raaplijst', metadata,
        Column('lijstID', Integer,primary_key=True),
        Column('artikelID', Integer),
        Column('werkorder', Integer),
        Column('afroep', Float),
        Column('leverdatum', String),
        Column('geleverd', Float),
        Column('meerwerk', Boolean),
        Column('postcode', String),
        Column('huisnummer', Integer),
        Column('toevoeging', String),
        Column('alternatief', String),
        Column('boekdatum', String),
        Column('straat', String),
        Column('woonplaats', String))
       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
 
    header = ['ListID','Article number','Work order','Call-up','Delivery date','Delivered',\
          'Additional work','Zipcode', 'House number','Suffix', 'Alternative Address',\
          'Booking date','Street','Residence']
    
    import validZt 
    if keuze == 1:
        selafr = select([raaplijst]).where(raaplijst.c.geleverd < raaplijst.c.afroep)\
           .order_by(raaplijst.c.werkorder, raaplijst.c.leverdatum)
    elif keuze == 2: 
        selafr = select([raaplijst]).where(and_(raaplijst.c.werkorder < 800000000,\
             raaplijst.c.geleverd < raaplijst.c.afroep)).order_by(raaplijst.c.leverdatum)
    elif keuze == 3:
        selafr = select([raaplijst]).where(and_(raaplijst.c.werkorder > 800000000,
        raaplijst.c.geleverd < raaplijst.c.afroep)).order_by(raaplijst.c.leverdatum)
    elif keuze == 4 and validZt.zt(zoekterm, 15):
        selafr = select([raaplijst]).where(and_(raaplijst.c.werkorder == int(zoekterm),\
          raaplijst.c.geleverd < raaplijst.c.afroep)).order_by(raaplijst.c.leverdatum.desc())
    elif keuze == 5 and validZt.zt(zoekterm, 2):
        selafr = select([raaplijst]).where(and_(raaplijst.c.artikelID == int(zoekterm),\
          raaplijst.c.geleverd < raaplijst.c.afroep)).order_by(raaplijst.c.leverdatum.desc())
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        selafr = select([raaplijst]).where(and_(raaplijst.c.leverdatum.like(zoekterm+'%'),
                raaplijst.c.geleverd < raaplijst.c.afroep))\
            .order_by(raaplijst.c.leverdatum, raaplijst.c.werkorder)
    elif keuze == 7 and validZt.zt(zoekterm, 9):
        selafr = select([raaplijst]).where(and_(raaplijst.c.postcode.ilike(zoekterm+'%'),\
             raaplijst.c.geleverd < raaplijst.c.afroep))\
            .order_by(raaplijst.c.leverdatum, raaplijst.c.werkorder)
    elif keuze == 8:
        selafr = select([raaplijst]).where(and_(raaplijst.c.geleverd >= raaplijst.c.afroep,\
                       raaplijst.c.afroep > 0))\
           .order_by(raaplijst.c.werkorder, raaplijst.c.leverdatum)
    else:
        ongInvoer()
        kiesSelektie(0, m_email)
   
    if con.execute(selafr).fetchone():
       rpafr = con.execute(selafr)
    else:
       geenRecord()
       kiesSelektie(0, m_email)
       
    data_list=[]
    for row in rpafr:
        data_list += [(row)]
        
    def boekAfroep(idx):
        mlijstnr = idx.data()
        if idx.column() == 0 :
            metadata = MetaData()
            raaplijst = Table('raaplijst', metadata,
                Column('lijstID', Integer,primary_key=True),
                Column('artikelID', Integer),
                Column('werkorder', Integer),
                Column('afroep', Float),
                Column('leverdatum', String),
                Column('geleverd', Float),
                Column('meerwerk', Boolean),
                Column('postcode', String),
                Column('huisnummer', Integer),
                Column('toevoeging', String),
                Column('alternatief', String),
                Column('boekdatum', String),
                Column('straat', String),
                Column('woonplaats', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
      
            selrlr = select([raaplijst]).where(raaplijst.c.lijstID == mlijstnr)                           
            rprlr = con.execute(selrlr).first()
           
            mwerknr = rprlr[2]
            martnr = rprlr[1]
            mleverdat = rprlr[4]
            mmmstatus = rprlr[6]
            mafroep = rprlr[3]
            mgeleverd = rprlr[5]
            
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Mutate material provision")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            
                    self.setFont(QFont('Arial', 10))
                               
                    self.Werknummer = QLabel()
                    zkwerknEdit = QLineEdit(str(mwerknr))
                    zkwerknEdit.setFont(QFont("Arial",10))
                    zkwerknEdit.setDisabled(True)
                    zkwerknEdit.setStyleSheet("color:black")
                    zkwerknEdit.setAlignment(Qt.AlignRight)
                    zkwerknEdit.textChanged.connect(self.zkwerknChanged) 
                    reg_ex = QRegExp("^[8]{1}[0-9]{8}$")
                    input_validator = QRegExpValidator(reg_ex, zkwerknEdit)
                    zkwerknEdit.setValidator(input_validator)
                                
                    self.Artikelnummer = QLabel()
                    artEdit = QLineEdit(str(martnr))
                    artEdit.setFixedWidth(150)
                    artEdit.setFont(QFont("Arial",10))
                    artEdit.setDisabled(True)
                    artEdit.setStyleSheet("color:black")
                    artEdit.setAlignment(Qt.AlignRight)
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
                                 
                    lbl1 = QLabel('Work number')
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(zkwerknEdit, 1, 1)
                                                  
                    lbl2 = QLabel('Article number')
                    lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(artEdit, 2, 1)
                    
                    lbl4 = QLabel('Call-up: '+ str(mafroep)+ ' - Already delivered: '+str(mgeleverd))
                    grid.addWidget(lbl4, 3, 0, 1, 3, Qt.AlignCenter)
                    lbl3 = QLabel('Provide')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 4, 0)
                    grid.addWidget(hoevEdit, 4 , 1)
                    
                    if mmmstatus:
                        grid.addWidget(QLabel('Additional work'), 4, 2)
                        
                    grid.addWidget(QLabel('Delivery date'), 5, 0, Qt.AlignRight)
                    grid.addWidget(QLabel(mleverdat), 5, 1)                     
                    
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
              
                    applyBtn = QPushButton('Mutate')
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 6, 2, 1 , 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    sluitBtn = QPushButton('Close')
                    sluitBtn.clicked.connect(self.close)
            
                    grid.addWidget(sluitBtn, 6, 0, 1, 2, Qt.AlignRight)
                    sluitBtn.setFont(QFont("Arial",10))
                    sluitBtn.setFixedWidth(100)
                    sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 3, Qt.AlignCenter)     
                                                                              
                def zkwerknChanged(self, text):
                    self.Werknummer.setText(text)
                    
                def artChanged(self,text):
                    self.Artikelnummer.setText(text)
                    
                def hoevChanged(self,text):
                    self.Hoeveelheid.setText(text)
                                                            
                def returnzkwerkn(self):
                    return self.Werknummer.text()
                
                def returnart(self):
                    return self.Artikelnummer.text()
                
                def returnhoev(self):
                    return self.Hoeveelheid.text()
                                        
                @staticmethod
                def getData(parent=None):
                    dialog = Widget(parent)
                    dialog.exec_()
                    return [dialog.returnzkwerkn(), dialog.returnart(), dialog.returnhoev()]
               
            window = Widget()
            data = window.getData()
            mhoev = 0
            if data[0] and len(data[0]) == 9 and _11check(data[0]):
                mwerknr = int(data[0])
            elif not data[0] and len(str(mwerknr)) == 9 and _11check(mwerknr):
                mwerknr = int(mwerknr)
            else:
                foutWerknr()
                return('')
     
            if str(mwerknr)[0] == '7':
                metadata = MetaData()   
                orders_intern = Table('orders_intern', metadata,
                    Column('werkorderID', Integer(), primary_key=True),
                    Column('voortgangstatus', String))
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selwerk = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
                rpwerk = con.execute(selwerk).first()
                metadata = MetaData()
                orders_intern = Table('orders_intern', metadata,
                    Column('werkorderID',Integer(), primary_key=True),
                    Column('werk_materialen', Float),
                    Column('meerminderwerk', Float))
                artikelmutaties = Table('artikelmutaties', metadata,
                    Column('mutatieID', Integer, primary_key=True),
                    Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                    Column('werkorderID', None, ForeignKey('orders_intern.werkorderID')),
                    Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                    Column('hoeveelheid', Float),
                    Column('boekdatum', String),
                    Column('tot_mag_prijs', Float),
                    Column('btw_hoog', Float),
                    Column('mmstatus', Boolean))
            elif str(mwerknr)[0] == '8':
                metadata = MetaData()   
                werken = Table('werken', metadata,
                    Column('werknummerID', Integer, primary_key=True),
                    Column('voortgangstatus', String),
                    Column('kosten_materialen', Float),
                    Column('meerminderwerk', Float))
                artikelmutaties = Table('artikelmutaties', metadata,
                    Column('mutatieID', Integer, primary_key=True),
                    Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                    Column('werknummerID', None, ForeignKey('werken.werknoID')),
                    Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                    Column('hoeveelheid', Float),
                    Column('boekdatum', String),
                    Column('tot_mag_prijs', Float),
                    Column('btw_hoog', Float),
                    Column('mmstatus', Boolean))
    
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
                rpwerk = con.execute(selwerk).first()
                      
            if rpwerk[1] == 'H':
                werkGereed()
                return(mwerknr)
            if data[2]:
                mhoev = float(data[2])
            else:
                return(mwerknr)
              
            metadata = MetaData()
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float),
                Column('art_voorraad', Float, CheckConstraint('art_voorraad >= 0')),
                Column('art_min_voorraad', Float),
                Column('art_bestelgrootte', Float),
                Column('bestelstatus', Boolean),
                Column('mutatiedatum', String),
                Column('reserveringsaldo', Float),
                Column('jaarverbruik_1', Float),
                Column('jaarverbruik_2', Float))
                      
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([artikelen]).where(artikelen.c.artikelID == martnr)
            transaction = con.begin()
            result = con.execute(sel).first()
            martprijs = result[2]
            martvrd = result[3]
            martminvrd = result[4]
            mboekd = str(datetime.datetime.now())[0:10]
            mjaar = int(str(datetime.datetime.now())[0:4])

            if martvrd - mhoev <= martminvrd:
                martbestst = False
            else:
                martbestst = True
            if mhoev <= 0:
                foutHoev()
                return('')
            try:
                if mjaar%2 == 0:            #even jaartal
                    stmt = update(artikelen).where(artikelen.c.artikelID == martnr).values(\
                     art_voorraad = artikelen.c.art_voorraad - mhoev, bestelstatus = martbestst,\
                     mutatiedatum = mboekd, reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                     jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                    con.execute(stmt)
                    mwaarde = martprijs*1.1*mhoev
                    con = engine.connect()
                elif mjaar%2 == 1:                     #oneven jaartal
                    stmt = update(artikelen).where(artikelen.c.artikelID == martnr).values(\
                     art_voorraad = artikelen.c.art_voorraad - mhoev, bestelstatus = martbestst,\
                     mutatiedatum = mboekd, reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                     jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                    con.execute(stmt)
                    mwaarde = martprijs*1.1*mhoev
                    con = engine.connect()
                if mmmstatus:
                    mmeerminder = mwaarde
                else:
                    mmeerminder = 0

                if str(mwerknr)[0] == '8':
                    stmt = update(werken).where(werken.c.werknummerID == mwerknr).values(\
                     kosten_materialen = werken.c.kosten_materialen + mwaarde,\
                     meerminderwerk = werken.c.meerminderwerk + mmeerminder)
                    con.execute(stmt)
                    try:
                        mutatienr=(con.execute(select([func.max(artikelmutaties.c.mutatieID,\
                            type_=Integer)])).scalar())
                        mutatienr += 1
                    except:
                        mutatienr = 1
                    ins = insert(artikelmutaties).values(mutatieID = mutatienr, artikelID =\
                        martnr, werknummerID = mwerknr, hoeveelheid = -mhoev, boekdatum = mboekd,\
                        tot_mag_prijs = mhoev*martprijs, btw_hoog = .21*mhoev*martprijs,\
                        mmstatus = mmmstatus) 
                    con.execute(ins)
                elif str(mwerknr)[0] == '7':
                    stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).values(\
                     werk_materialen = orders_intern.c.werk_materialen + mwaarde,\
                     meerminderwerk = orders_intern.c.meerminderwerk + mmeerminder)
                    con.execute(stmt)
                    try:
                        mutatienr=(con.execute(select([func.max(artikelmutaties.c.mutatieID,\
                          type_=Integer)])).scalar())
                        mutatienr += 1
                    except:
                        mutatienr = 1
                    ins = insert(artikelmutaties).values(mutatieID = mutatienr, artikelID =\
                        martnr, werkorderID = mwerknr, hoeveelheid = -mhoev, boekdatum = mboekd,\
                        tot_mag_prijs = mhoev*martprijs, btw_hoog = .21*mhoev*martprijs,\
                        mmstatus = mmmstatus)
                    con.execute(ins)
                updrl = update(raaplijst).where(raaplijst.c.lijstID == mlijstnr).\
                values(geleverd = raaplijst.c.geleverd+mhoev, boekdatum = mboekd )
                con.execute(updrl)
                transaction.commit()
                invoerOK()
            except IntegrityError:
                transaction.rollback()
                negVoorraad()
            con.close 
            return(mwerknr)
    
    win = MyWindow(data_list, header)
    win.exec_() 
    kiesSelektie(route, m_email)