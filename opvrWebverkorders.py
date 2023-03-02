from login import hoofdMenu
from postcode import checkpostcode
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout,\
                             QPushButton, QLineEdit, QWidget, QMessageBox,\
                             QTableView, QComboBox, QCheckBox
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                         create_engine, Float, ForeignKey)
from sqlalchemy.sql import select, update, and_

def refresh(m_email, keuze, zoekterm, afd, self):
    self.close()
    bestelOrder(m_email, keuze, zoekterm, afd)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Webverkooporders opvragen')               
    msg.exec_() 
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Webverkooporders opvragen')               
    msg.exec_() 
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def geenOrder():
    msg = QMessageBox()
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Webverkooporder niet gevonden!')
    msg.setWindowTitle('Webverkooporders opvragen')               
    msg.exec_()
     
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Webverkooporders opvragen')
    msg.exec_()
    
def printFactuur(rpord,mstraat,mplaats,movbestnr):
    from sys import platform
    metadata = MetaData()
    orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
        Column('ovaID', Integer, primary_key=True),
        Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('ovaantal', Integer),
        Column('ovleverdatum', String),
        Column('verkoopprijs', Float),
        Column('regel', Integer),
        Column('retour', Float),
        Column('betaaldatum', String),
        Column('leveringsdatum', String))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String),
        Column('locatie_magazijn', String))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selova = select([orders_verkoop_artikelen,artikelen]).where(and_(\
      orders_verkoop_artikelen.c.ovbestelID == movbestnr, orders_verkoop_artikelen\
      .c.artikelID == artikelen.c.artikelID)).order_by(orders_verkoop_artikelen.c.ovaID)
    rpova = con.execute(selova)
        
    mblad = 1
    rgl = 0
    if platform == 'win32':
        filename = '.\\forms\\Weborders_Facturen\\Weborder-factuur-'+str(rpord[0])+'.txt'
    else:
        filename = './forms/Weborders_Facturen/Weborder-factuur-'+str(rpord[0])+'.txt'
    adreskop=\
    ('\n\n\n\n\n\n\nFACTUUR\n\n'+rpord[10]+' '+rpord[11]+' '+rpord[12]+' '+rpord[13]+',\n'+\
     mstraat+' '+rpord[15]+rpord[16]+',\n'+\
     rpord[14]+' '+mplaats+'.\n\n\n\n\n')
    kop=\
    ('Ordernummer: '+ str(rpord[0])+'          Datum: '+str(datetime.datetime.now())[0:10]+'  Blad : '+str(mblad)+'\n'+
    '==============================================================================================\n'+
    'Artikelnr  Omschrijving                        Eenheid Aantal     Prijs   Subtotaal       BTW \n'+
    '==============================================================================================\n')
    mtotaal = 0
    
    for row in rpova:
        if rgl == 0 and mblad == 1:
            open(filename, 'w').write(adreskop)
            open(filename, 'a').write(kop)
            rgl = 16
        elif rgl%57 == 0:
            open(filename, 'a').write(kop)
            mblad += 1
        msub = row[3]*row[5]
        open(filename,'a').write('{:<11d}'.format(row[2])+'{:<37.35s}'.format(row[11])+\
         '{:>6s}'.format(row[14])+' '+'{:>6.2f}'.format(row[3])+'{:>10.2f}'.format(row[5])+\
         ' '+'{:>10.2f}'.format(msub)+' '+'{:>10.2f}'.format(msub*21/121)+'\n')
        mtotaal = mtotaal+msub
        rgl += 1
   
    tail =(\
           
    '----------------------------------------------------------------------------------------------\n'+
    'Totaal factuurbedrag inclusief 21% BTW                                  '+'{:10.2f}'.format(mtotaal)+' \n'+
    '==============================================================================================\n')    
    open(filename,'a').write(tail)
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
    
def printPakbon(rpord,mstraat,mplaats,movbestnr): 
    from sys import platform
    metadata = MetaData()
    orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
        Column('ovaID', Integer, primary_key=True),
        Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('ovaantal', Integer),
        Column('ovleverdatum', String),
        Column('verkoopprijs', Float),
        Column('regel', Integer),
        Column('retour', Float),
        Column('betaaldatum', String),
        Column('leveringsdatum', String))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String),
        Column('locatie_magazijn', String))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selova = select([orders_verkoop_artikelen,artikelen]).where(and_(\
      orders_verkoop_artikelen.c.ovbestelID == movbestnr, orders_verkoop_artikelen\
      .c.artikelID == artikelen.c.artikelID)).order_by(orders_verkoop_artikelen.c.ovaID)
    rpova = con.execute(selova)

    mblad = 1
    rgl = 0
    if platform == 'win32':
        filename = '.\\forms\\Weborders_Pakbonnen\\Weborder-pakbon-'+str(rpord[0])+'.txt'
    else:
        filename = './forms/Weborders_Pakbonnen/Weborder-pakbon-'+str(rpord[0])+'.txt'
    adreskop=\
    ('\n\n\n\n\n\n\nPAKBON\n\n'+rpord[10]+' '+rpord[11]+' '+rpord[12]+' '+rpord[13]+',\n'+\
     mstraat+' '+rpord[15]+rpord[16]+',\n'+\
     rpord[14]+' '+mplaats+'.\n\n\n\n\n')
    open(filename,'w').write(adreskop)
    kop=\
    ('Ordernummer: '+ str(rpord[0])+'          Datum: '+str(datetime.datetime.now())[0:10]+'  Blad : '+str(mblad)+'\n'+
    '==============================================================================================\n'+
    'Artikelnr  Omschrijving                        Eenheid Aantal  Locatie    Geleverd            \n'+
    '==============================================================================================\n')
    
    for row in rpova:
        if rgl == 0 and mblad == 1:
            open(filename, 'w').write(adreskop)
            open(filename, 'a').write(kop)
            rgl = 16
        elif rgl%57 == 0:
            open(filename, 'a').write(kop)
            mblad += 1
        open(filename,'a').write('{:<11d}'.format(row[2])+'{:<37.35s}'.format(row[11])+\
           '{:>6s}'.format(row[14])+' '+'{:>6.2f}'.format(row[3])+' '\
           +'{:>8s}'.format(row[15])+'{:>12s}'.format(row[9])+'  ________ \n')
        rgl += 1
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
    
def zoekWeborder(m_email, afd):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen Webverkooporder")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Alle Orders')
            k0Edit.addItem('2. Gefilterd op postcode')
            k0Edit.addItem('3. Gefilterd op achternaam')
            k0Edit.addItem('4. Gefilterd op ordernummer')
            k0Edit.addItem('5. Gefilterd op besteldatum')
            k0Edit.activated[str].connect(self.k0Changed)
               
            self.Zoekterm = QLabel()
            zktrmEdit = QLineEdit()
            zktrmEdit.setFixedWidth(220)
            zktrmEdit.setFont(QFont("Arial",10))
            zktrmEdit.textChanged.connect(self.zktrmChanged)
            reg_ex = QRegExp('.*$')
            input_validator = QRegExpValidator(reg_ex, zktrmEdit)
            zktrmEdit.setValidator(input_validator)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0, 1 ,2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 2, Qt.AlignRight)
                                  
            lbl1 = QLabel('Zoekterm')  
            grid.addWidget(lbl1, 3, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(zktrmEdit, 3, 1, 1, 2)
            grid.addWidget(k0Edit, 2, 1, 1 , 2, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
        
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 4, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            closeBtn = QPushButton('Sluiten')
            closeBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(closeBtn, 4, 1, 1, 1, Qt.AlignRight)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktrmChanged(self, text):
            self.Zoekterm.setText(text)
            
        def returnk0(self):
            return self.Keuze.text()
        
        def returnzktrmEdit(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzktrmEdit()] 
        
    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    bestelOrder(m_email, keuze, zoekterm, afd)
     
def regelsOrder(rpova, afd):
    for rij in rpova:
        class RegelWindow(QDialog):
            def __init__(self):
                QDialog.__init__(self)
                
                grid = QGridLayout()
                grid.setSpacing(20)
                            
                self.setWindowTitle("Bestelling Artikelregel")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                
                self.setFont(QFont('Arial', 10))   
                                                  
                self.lbl = QLabel()
                self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                self.lbl.setPixmap(self.pixmap)
                grid.addWidget(self.lbl , 0, 0)
                
                grid.addWidget(QLabel('Bestelling Artikelregel: ' +str(rij[6])),0, 1, 1, 2)
        
                self.logo = QLabel()
                self.pixmap = QPixmap('./images/logos/logo.jpg')
                self.logo.setPixmap(self.pixmap)
                grid.addWidget(self.logo , 0, 5, 1, 1, Qt.AlignRight) 
                
                lbl1 = QLabel('OrderregelID')
                q1Edit = QLineEdit(str(rij[0]))
                q1Edit.setAlignment(Qt.AlignRight)
                q1Edit.setFixedWidth(90)
                q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q1Edit.setDisabled(True)
                
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1,1)
                
                lbl2 = QLabel('Ordernummer')
                q2Edit = QLineEdit(str(rij[1]))
                q2Edit.setFixedWidth(100)
                q2Edit.setAlignment(Qt.AlignRight)
                q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q2Edit.setDisabled(True)
                
                grid.addWidget(lbl2, 1, 2)
                grid.addWidget(q2Edit, 1,3)
                
                lbl3 = QLabel('Artikelnummer')
                q3Edit = QLineEdit(str(rij[10]))
                q3Edit.setFixedWidth(100)
                q2Edit.setAlignment(Qt.AlignRight)
                q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q3Edit.setDisabled(True)
                
                grid.addWidget(lbl3, 2, 0)
                grid.addWidget(q3Edit, 2,1)
                
                lbl9 = QLabel('Omschrijving')
                q9Edit = QLineEdit(str(rij[11]))
                q9Edit.setFixedWidth(350)
                q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q9Edit.setDisabled(True)
                
                grid.addWidget(lbl9, 2, 2)
                grid.addWidget(q9Edit, 2, 3, 1 ,3)
                                     
                lbl4 = QLabel('Aantal')
                q4Edit = QLineEdit('{:12.2f}'.format(rij[3]))
                q4Edit.setFixedWidth(100)
                q4Edit.setAlignment(Qt.AlignRight)
                q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q4Edit.setDisabled(True)
                
                grid.addWidget(lbl4, 3, 0)
                grid.addWidget(q4Edit, 3, 1)
                
                lbl5 = QLabel('Verkoopprijs')
                q5Edit = QLineEdit('{:12.2f}'.format(rij[5]))
                q5Edit.setFixedWidth(100)
                q5Edit.setAlignment(Qt.AlignRight)
                q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q5Edit.setDisabled(True)
             
                grid.addWidget(lbl5, 3, 2)
                grid.addWidget(q5Edit, 3, 3)
                
                lbl6 = QLabel('Leverdatum')
                q6Edit = QLineEdit(str(rij[4]))
                q6Edit.setFixedWidth(100)
                q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q6Edit.setDisabled(True)
                
                grid.addWidget(lbl6, 4, 0)
                grid.addWidget(q6Edit, 4, 1)
                
                lbl7 = QLabel('RetourLevering')
                q7Edit = QLineEdit('{:12.2f}'.format(rij[7]))
                q7Edit.setFixedWidth(100)
                q7Edit.setAlignment(Qt.AlignRight)
                q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q7Edit.setDisabled(True)
                                            
                grid.addWidget(lbl7, 4, 2)
                grid.addWidget(q7Edit, 4, 3)
                          
                lbl8 = QLabel('Betaaldatum')
                q8Edit = QLineEdit(str(rij[8]))
                q8Edit.setFixedWidth(100)
                q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q8Edit.setDisabled(True)
                                            
                grid.addWidget(lbl8, 5, 0)
                grid.addWidget(q8Edit, 5, 1)
                
                cBox = QCheckBox('Betaling ontvangen')
                cBox.stateChanged.connect(self.cBoxChanged)
                if not afd or afd == 2 or rij[8]:
                    cBox.setDisabled(True)
                grid.addWidget(cBox, 5, 2)
                
                lbl9 = QLabel('Datum geleverd')
                q9Edit = QLineEdit(str(rij[9]))
                q9Edit.setFixedWidth(100)
                q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q9Edit.setDisabled(True)
                                            
                grid.addWidget(lbl9, 5, 3)
                grid.addWidget(q9Edit, 5, 4)
                
                cBox1 = QCheckBox('Geleverd')
                cBox1.stateChanged.connect(self.cBox1Changed)
                if afd or rij[9] :
                    cBox1.setDisabled(True)
                grid.addWidget(cBox1,5, 5)
                
                regelBtn = QPushButton('Regel')
                regelBtn.clicked.connect(self.accept)
        
                grid.addWidget(regelBtn, 6, 5)
                regelBtn.setFont(QFont("Arial",10))
                regelBtn.setFixedWidth(100)
                regelBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 1, 1, 3, Qt.AlignCenter)
                                                                                                       
                self.setLayout(grid)
                self.setGeometry(250, 300, 150, 150)
           
            state = False   
            def cBoxChanged(self, state):
                if state == Qt.Checked:
                    self.state = True
                    
            def returncBox(self):
                return self.state
            
            state1 = False   
            def cBox1Changed(self, state1):
                if state1 == Qt.Checked:
                    self.state1 = True
                    
            def returncBox1(self):
                return self.state1
        
            @staticmethod
            def getData(parent=None):
                dialog = RegelWindow()
                dialog.exec_()
                return [dialog.returncBox(), dialog.returncBox1()]
                   
        regelWin = RegelWindow()
        data = regelWin.getData()
        
        metadata = MetaData()
        orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
            Column('ovaID', Integer, primary_key=True),
            Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
            Column('regel', Integer),
            Column('betaaldatum', String),
            Column('leveringsdatum', String))
          
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selb = select([orders_verkoop_artikelen]).where(and_(orders_verkoop_artikelen.\
            c.ovbestelID == rij[1], orders_verkoop_artikelen.c.regel == rij[6]))
        rpb = con.execute(selb).first()
        if data[0] and not rpb[3]:
            up = update(orders_verkoop_artikelen).where(and_(orders_verkoop_artikelen\
             .c.regel == rij[6], orders_verkoop_artikelen.c.ovbestelID == rij[1]))\
             .values(betaaldatum = str(datetime.datetime.now())[0:10]) 
            con.execute(up)
        if data[1] and not rpb[4]:
                upl = update(orders_verkoop_artikelen).where(and_(orders_verkoop_artikelen\
                 .c.regel == rij[6], orders_verkoop_artikelen.c.ovbestelID == rij[1]))\
                 .values(leveringsdatum = str(datetime.datetime.now())[0:10]) 
                con.execute(upl)
        metadata = MetaData()
        orders_verkoop = Table('orders_verkoop', metadata,
            Column('ovbestelID', Integer, primary_key=True),
            Column('datum_betaald', String),
            Column('datum_geleverd', String))
        orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
            Column('ovaID', Integer, primary_key=True),
            Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
            Column('regel', Integer),
            Column('betaaldatum', String),
            Column('leveringsdatum', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selb = select([orders_verkoop, orders_verkoop_artikelen]).where(and_\
            (orders_verkoop_artikelen.c.ovbestelID==rij[1], orders_verkoop_artikelen.\
             c.ovbestelID == orders_verkoop.c.ovbestelID)).order_by\
            (orders_verkoop_artikelen.c.regel.desc())
        rpbal = con.execute(selb)
        rpbmax = con.execute(selb).first()
        mrgl = rpbmax[5]
        mregel = 0
        if not rpbmax[1]:
            for item in rpbal:
                mbet=item[6]
                if mbet:
                    mregel += 1
                    if mrgl == mregel:
                        updbet = update(orders_verkoop).where(orders_verkoop.c.ovbestelID ==\
                         rij[1]).values(datum_betaald = str(datetime.datetime.now())[0:10])
                        con.execute(updbet)
                        rpbal = con.execute(selb)
        mregel1 = 0
        if not rpbmax[2]:
            for item1 in rpbal:
                mlev=item1[7]
                if mlev:
                    mregel1 += 1
                    if mrgl == mregel1:
                        updlev =  update(orders_verkoop).where(orders_verkoop.c.ovbestelID ==\
                         rij[1]).values(datum_geleverd = str(datetime.datetime.now())[0:10])
                        con.execute(updlev)
                                                   
def bestelOrder(m_email, keuze, zoekterm, afd): 
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Webverkooporders')
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
            table_view.setColumnHidden(1,True)
            table_view.setColumnHidden(6,True)
            table_view.setColumnHidden(9,True)
            table_view.clicked.connect(showSelorder)
            grid.addWidget(table_view, 0, 0, 1, 13)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 12, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(m_email, keuze, zoekterm, afd, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 11, 1, 1, Qt.AlignRight)
            
            sluitBtn = QPushButton('Sluiten')
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
  
    header = ['Ordernr','-','Besteldatum', 'Betaald','Geleverd','Totaalbedrag','-', 'Accountnr',\
              'Rekeningnr','-','Aanhef', 'Voornaam','Tussen', 'Achternaam',\
              'Postcode', 'Huisnummer', 'Toev','e-mailadres','Telefoon']
    
    metadata = MetaData()
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True),
        Column('klantID', None, ForeignKey('klanten.klantID')),
        Column('ovbesteldatum', String),
        Column('datum_betaald', String),
        Column('datum_geleverd', String),
        Column('bedrag', Float))
    klanten = Table('klanten', metadata,
        Column('klantID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('rekening', String))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('aanhef', String),
        Column('voornaam', String), 
        Column('tussenvoegsel', String),
        Column('achternaam', String),
        Column('postcode', String),       
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('email', String),
        Column('telnr', String)) 

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    import validZt  
    if keuze == 1:
        selwo = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
            .c.klantID == klanten.c.klantID, klanten.c.accountID == accounts\
            .c.accountID)).order_by(orders_verkoop.c.ovbestelID)
    elif keuze == 2 and validZt.zt(zoekterm, 9):
        selwo = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
            .c.klantID == klanten.c.klantID, klanten.c.accountID == accounts\
            .c.accountID, accounts.c.postcode.ilike(zoekterm+'%')))\
            .order_by(orders_verkoop.c.ovbestelID)
    elif keuze == 3:
        selwo = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
            .c.klantID == klanten.c.klantID, klanten.c.accountID == accounts\
            .c.accountID, accounts.c.achternaam.ilike('%'+zoekterm+'%')))\
            .order_by(orders_verkoop.c.ovbestelID)
    elif keuze == 4 and validZt.zt(zoekterm, 5):
        selwo = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
            .c.klantID == klanten.c.klantID, klanten.c.accountID == accounts\
            .c.accountID, orders_verkoop.c.ovbestelID == int(zoekterm)))\
            .order_by(orders_verkoop.c.ovbestelID)
    elif keuze == 5 and validZt.zt(zoekterm, 10):
        selwo = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
            .c.klantID == klanten.c.klantID, klanten.c.accountID == accounts\
            .c.accountID, orders_verkoop.c.ovbesteldatum.like(zoekterm+'%')))\
            .order_by(orders_verkoop.c.ovbestelID)
    else:
        ongInvoer()
        zoekWeborder(m_email, afd)
    
    if con.execute(selwo).fetchone():
        rpwo = con.execute(selwo)
    else:
        geenRecord()
        zoekWeborder(m_email, afd)
  
    data_list=[]
    for row in rpwo:
        data_list += [(row)]
        
    def showSelorder(idx):
        movbestnr = idx.data()
        if idx.column() == 0:
            metadata = MetaData()
            orders_verkoop = Table('orders_verkoop', metadata,
                Column('ovbestelID', Integer, primary_key=True),
                Column('klantID', None, ForeignKey('klanten.klantID')),
                Column('ovbesteldatum', String),
                Column('bedrag', Float),
                Column('datum_betaald', String),
                Column('datum_geleverd',String))
            klanten = Table('klanten', metadata,
                Column('klantID', Integer(), primary_key=True),
                Column('accountID', None, ForeignKey('accounts.accountID')),
                Column('rekening', String))
            accounts = Table('accounts', metadata,
                Column('accountID', Integer(), primary_key=True),
                Column('aanhef', String),
                Column('voornaam', String), 
                Column('tussenvoegsel', String),
                Column('achternaam', String),
                Column('postcode', String),       
                Column('huisnummer', String),
                Column('toevoeging', String),
                Column('email', String),
                Column('telnr', String)) 
            orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
                Column('ovaID', Integer, primary_key=True),
                Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
                Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                Column('ovaantal', Integer),
                Column('ovleverdatum', String),
                Column('verkoopprijs', Float),
                Column('regel', Integer),
                Column('retour', Float),
                Column('betaaldatum', String),
                Column('leveringsdatum', String))
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float),
                Column('art_voorraad', Float),
                Column('art_eenheid', String),
                Column('locatie_magazijn', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            
            selord = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop\
                .c.ovbestelID == movbestnr, orders_verkoop.c.klantID == klanten.c.klantID,\
                 klanten.c.accountID == accounts.c.accountID))
            rpord = con.execute(selord).first()
                 
            selova = select([orders_verkoop_artikelen,artikelen]).where(and_(\
              orders_verkoop_artikelen.c.ovbestelID == movbestnr, orders_verkoop_artikelen\
             .c.artikelID == artikelen.c.artikelID)).order_by(orders_verkoop_artikelen.c.ovaID)
            rpova = con.execute(selova)
            
            mpostcode = rpord[14]
            mhuisnr = int(rpord[15])
            madres = checkpostcode(mpostcode,mhuisnr)
            mstraat = madres[0]
            mplaats = madres[1]
                 
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                
                    self.setWindowTitle("Bestelling Webartikelen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Bestelling Webartikelen'),0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 4, 1, 1, Qt.AlignRight) 
                    
                    lbl1 = QLabel('Ordernummer')
                    q1Edit = QLineEdit(str(rpord[0]))
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setFixedWidth(90)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                    
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1,1)
                    
                    lbl2 = QLabel('Bestel- / Leveringsdatum')
                    q2Edit = QLineEdit(str(rpord[2]))
                    q2Edit.setFixedWidth(100)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                    q17Edit = QLineEdit(str(rpord[5]))
                    q17Edit.setFixedWidth(90)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    grid.addWidget(lbl2, 1, 2)
                    grid.addWidget(q2Edit, 1, 3)
                    grid.addWidget(q17Edit, 1, 4, 1, 1,Qt.AlignRight)
                    
                    lbl3 = QLabel('Totaalbedrag')
                    q3Edit = QLineEdit('{:12.2f}'.format(rpord[3]))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q3Edit, 2,1)
                                         
                    lbl4 = QLabel('Betaaldatum')
                    q4Edit = QLineEdit(rpord[4])
                    q4Edit.setFixedWidth(100)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    grid.addWidget(lbl4, 2, 2)
                    grid.addWidget(q4Edit, 2, 3, 1, 2)
                    
                    lbl5 = QLabel('Accountnummer')
                    q5Edit = QLineEdit(str(rpord[7]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                 
                    grid.addWidget(lbl5, 3, 0)
                    grid.addWidget(q5Edit,3,1)
                    
                    lbl6 = QLabel('Rekeningnummer')
                    q6Edit = QLineEdit(str(rpord[8]))
                    q6Edit.setFixedWidth(200)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    grid.addWidget(lbl6, 3, 2)
                    grid.addWidget(q6Edit, 3, 3, 1 ,2)
                    
                    lbl7 = QLabel('Aanhef')
                    q7Edit = QLineEdit(str(rpord[10]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    grid.addWidget(lbl7, 4, 0)
                    grid.addWidget(q7Edit, 4, 1)
                    
                    lbl8 = QLabel('Voornaam')
                    q8Edit = QLineEdit(str(rpord[11]))
                    q8Edit.setFixedWidth(230)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    grid.addWidget(lbl8, 4, 2)
                    grid.addWidget(q8Edit, 4, 3, 1 ,2)
                    
                    lbl9 = QLabel('Tussen')
                    q9Edit = QLineEdit(str(rpord[12]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                    
                    grid.addWidget(lbl9, 5, 0)
                    grid.addWidget(q9Edit, 5, 1)
                    
                    lbl10 = QLabel('Achternaam')
                    q10Edit = QLineEdit(str(rpord[13]))
                    q10Edit.setFixedWidth(230)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                    
                    grid.addWidget(lbl10, 5, 2)
                    grid.addWidget(q10Edit, 5, 3, 1, 2)
                                  
                    lbl11= QLabel('Straatnaam')
                    q11Edit = QLineEdit(mstraat)
                    q11Edit.setFixedWidth(260)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                    
                    grid.addWidget(lbl11, 6, 0)
                    grid.addWidget(q11Edit, 6, 1, 1, 3)
                    
                    lbl12= QLabel('Huisnummer')
                    q12Edit = QLineEdit(str(rpord[15])+rpord[16])
                    q12Edit.setFixedWidth(100)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                    
                    grid.addWidget(lbl12, 6, 3)
                    grid.addWidget(q12Edit, 6, 4)
                                                   
                    lbl13= QLabel('Postcode')
                    q13Edit = QLineEdit(rpord[14])
                    q13Edit.setFixedWidth(70)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
                    
                    grid.addWidget(lbl13, 7, 0)
                    grid.addWidget(q13Edit, 7, 1)
                    
                    lbl14= QLabel('Woonplaats')
                    q14Edit = QLineEdit(str(mplaats))
                    q14Edit.setFixedWidth(230)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                    
                    grid.addWidget(lbl14, 7, 2)
                    grid.addWidget(q14Edit, 7, 3, 1 , 2)
                    
                    lbl15= QLabel('E-Mailadres')
                    q15Edit = QLineEdit(rpord[17])
                    q15Edit.setFixedWidth(260)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
                    
                    grid.addWidget(lbl15, 8, 0)
                    grid.addWidget(q15Edit, 8, 1, 1, 3)
                    
                    lbl16= QLabel('Telefoon')
                    q16Edit = QLineEdit(str(rpord[18]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                    
                    grid.addWidget(lbl16, 8, 3)
                    grid.addWidget(q16Edit, 8, 3 , 1, 2, Qt.AlignRight)
                    
                    regelBtn = QPushButton('Bestelregels')
                    regelBtn.clicked.connect(lambda: regelsOrder(rpova, afd))
                            
                    grid.addWidget(regelBtn, 10, 4)
                    regelBtn.setFont(QFont("Arial",10))
                    regelBtn.setFixedWidth(110)
                    regelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, 10, 3, 1, 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(110)
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                   
                    pakbonBtn = QPushButton('Print Pakbon')
                    pakbonBtn.clicked.connect(lambda: printPakbon(rpord,mstraat,mplaats,movbestnr))
                           
                    grid.addWidget(pakbonBtn, 9, 4)
                    pakbonBtn.setFont(QFont("Arial",10))
                    pakbonBtn.setFixedWidth(110)
                               
                    factuurBtn = QPushButton('Print Factuur')
                    factuurBtn.clicked.connect(lambda: printFactuur(rpord,mstraat,mplaats,movbestnr))
    
                    grid.addWidget(factuurBtn, 9, 3, 1, 1, Qt.AlignRight)
                    factuurBtn.setFont(QFont("Arial",10))
                    factuurBtn.setFixedWidth(110)
                      
                    if afd == 1:
                        pakbonBtn.setDisabled(True)
                        factuurBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    elif afd == 0:
                        factuurBtn.setDisabled(True)
                        pakbonBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    elif afd == 2:
                        factuurBtn.setDisabled(True)
                        pakbonBtn.setDisabled(True)
                            
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 1, 1, 3, Qt.AlignCenter)
                                                                                                           
                    self.setLayout(grid)
                    self.setGeometry(300, 150, 150, 150)
                         
            mainWin = MainWindow()
            mainWin.exec_()
      
    win = MyWindow(data_list, header)
    win.exec_()
    zoekWeborder(m_email, afd)