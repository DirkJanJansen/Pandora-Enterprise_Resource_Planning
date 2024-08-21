from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
            QDialog, QMessageBox #,QDateEdit
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean, ForeignKey, \
                        MetaData, create_engine, select, insert, update, and_, func)
    
def foutInvoer():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Verplichte Invoer!')
    msg.setWindowTitle('Invoer werkorders')
    msg.exec_()
    
def foutLeverancier():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Leverancier niet gevonden!')
    msg.setWindowTitle('INKOOPORDER')
    msg.exec_()

def geenArtnr():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen bestaand artikel gevonden\nNieuw artikelnummer wordt aangemaakt!')
    msg.setWindowTitle('Invoer Artikelnummer')               
    msg.exec_() 

def invoerOk(mregel):
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Bestelregel '+str(mregel)+' ingevoerd')
    msg.setWindowTitle('Bestelling regelinkooporder')
    msg.exec_()
    
def reedsBesteld():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Dit produkt is in de bestelprocedure\nBestellen is weer mogelijk na uitlevering!')
    msg.setWindowTitle('Bestelling regelinkooporder')
    msg.exec_()
    
def foutArtikel():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Onjuist artikelnummer, of niet alle vereiste gegevens ingevoerd!')
    msg.setWindowTitle('Bestelling regel inkooporder')
    msg.exec_()
        
def onvBesteld(aantal):
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Er zijn '+str(aantal)+' artikelen minder opgegeven'+
     '\nom in reserveringen minus voorraad te voorzien!'+\
     '\nZie "Voorraadmanagement-Reserveringen"'+\
     '\nVoer de bestelregel opnieuw in met vergrote hoeveelheid!')
    msg.setWindowTitle('Bestelling regel inkooporder')
    msg.exec_()
  
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def sluitRegels(m_email, mlevnr, mregel, self):
    self.close()
    zoekLeverancier(m_email, mlevnr, mregel)

def foutLeveranciernr():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            msg = QMessageBox()
            msg.setStyleSheet("color: black;  background-color: gainsboro")
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Leverancier niet gevonden!')
            msg.setWindowTitle('Bestelling inkooporder')
            msg.exec_()
            
    window = Widget()
    window.show() 
                
def _11check(mlevnr):
    number = str(mlevnr)
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

def zoekLeverancier(m_email, mlevnr, mregel):
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String))
            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Leverancier zoeken materialen.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                            
            self.Leveranciernummer = QLabel()
            levEdit = QLineEdit(str(mlevnr))
            levEdit.setFixedWidth(100)
            levEdit.setFont(QFont("Arial",10))
            levEdit.textChanged.connect(self.levChanged)
            reg_ex = QRegExp('^[3]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            levEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1 ,2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
     
            grid.addWidget(QLabel('Leverancier'), 2, 1)
            grid.addWidget(levEdit, 2, 2)
       
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                    
            grid.addWidget(applyBtn, 3, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 3, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)
    
        def levChanged(self, text):
            self.Leveranciernummer.setText(text)
    
        def returnLeveranciernummer(self):
            return self.Leveranciernummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnLeveranciernummer()]
       
    window = Widget()
    data = window.getData()
    if data[0] and len(data[0]) == 9 and _11check(data[0]):
        mlevnr = int(data[0])
    sel = select([leveranciers]).where(leveranciers.c.leverancierID == mlevnr)
    rplev = conn.execute(sel).first()
    mregel = 1
    if rplev:
        inkoopRegels(m_email, rplev, mregel)
    else:
        foutLeverancier()
        zoekLeverancier(m_email, mlevnr, mregel)
           
def bepaalInkoopOrdernr(mregel):
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer, primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    try:
        morderinkoopnr=(conn.execute(select([func.max(orders_inkoop.c.orderinkoopID,\
            type_=Integer)])).scalar())
        if mregel == 1:
            morderinkoopnr=int(maak11proef(morderinkoopnr))
        conn.close
    except:
        if mregel == 1:
            morderinkoopnr = 400000003
    return(morderinkoopnr)
   
def Inkooporder(m_email, rplev, mregel):
    mlevnr = int(rplev[0])
    mbedrnaam = rplev[1]
    mrechtsvorm = rplev[2]
    mpostcode = rplev[3]
    mhuisnr = int(rplev[4])
    if rplev[5]:
        mtoev = rplev[5]
    else:
        mtoev=''
    import postcode
    mstrplts = postcode.checkpostcode(mpostcode, mhuisnr)
    mstraat = mstrplts[0]
    mplaats = mstrplts[1]
    minkordnr = bepaalInkoopOrdernr(mregel)
    return(minkordnr, mlevnr, mbedrnaam, mrechtsvorm, mstraat, mhuisnr,\
               mtoev, mpostcode, mplaats)
    
def inkoopRegels(m_email, rplev, mregel):
    minkgeg = Inkooporder(m_email, rplev, mregel)
    minkordnr = minkgeg[0]
    mlevnr = minkgeg[1]
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle('Bestelregels inkooporder materialen invoeren')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                       
            self.Inkoopordernummer = QLabel()
            inkorderEdit = QLineEdit(str(minkordnr))
            inkorderEdit.setStyleSheet("color: black ")
            inkorderEdit.setDisabled(True)
            inkorderEdit.setAlignment(Qt.AlignRight)
            inkorderEdit.setFixedWidth(130)
            inkorderEdit.setFont(QFont("Arial",10))
            inkorderEdit.textChanged.connect(self.inkorderChanged) 
            
            self.BestelregelArtikel = QLabel()
            artEdit = QLineEdit()
            artEdit.setFixedWidth(130)
            artEdit.setFont(QFont("Arial",10))
            artEdit.textChanged.connect(self.artChanged) 
            reg_ex = QRegExp("^[2]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, artEdit)
            artEdit.setValidator(input_validator)
            
            self.BestelHoeveelheid = QLabel()
            hoevEdit = QLineEdit()
            hoevEdit.setFixedWidth(130)
            hoevEdit.setFont(QFont("Arial",10))
            hoevEdit.textChanged.connect(self.hoevChanged) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, hoevEdit)
            hoevEdit.setValidator(input_validator)
            
            self.Inkoopeenheidsprijs = QLabel()
            prijsEdit = QLineEdit()
            prijsEdit.setFixedWidth(130)
            prijsEdit.setFont(QFont("Arial",10))
            prijsEdit.textChanged.connect(self.prijsChanged) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, prijsEdit)
            prijsEdit.setValidator(input_validator)    
        
            self.Levering_start = QLabel()
            #levertEdit = QDateEdit(datetime.date)
            startEdit = QLineEdit('')
            startEdit.setCursorPosition(0)
            startEdit.setFixedWidth(130)
            startEdit.setFont(QFont("Arial",10))
            startEdit.textChanged.connect(self.startChanged) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, startEdit)
            startEdit.setValidator(input_validator) 
            
            self.Levering_end = QLabel()
            #levertEdit = QDateEdit(datetime.date)
            endEdit = QLineEdit('')
            endEdit.setCursorPosition(0)
            endEdit.setFixedWidth(130)
            endEdit.setFont(QFont("Arial",10))
            endEdit.textChanged.connect(self.endChanged) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, endEdit)
            endEdit.setValidator(input_validator)  
                        
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0, 0)
            grid.addWidget(QLabel("Artikelen bestellen"), 0, 1)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
            
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Bestelling voor\nLeverancier: '+str(minkgeg[1])+\
              ',\n'+minkgeg[2]+' '+minkgeg[3]+',\n'+minkgeg[4]+' '+str(minkgeg[5])+\
              minkgeg[6]+',\n'+minkgeg[7]+' '+minkgeg[8]+'.\nOrderregel '+str(mregel)), 1, 1, 5, 2)
            
            grid.addWidget(QLabel("* Invoer vereist"), 6 , 2)
                                             
            lbl1 = QLabel('Ordernummer')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 6, 0)
            grid.addWidget(inkorderEdit, 6, 1)
                                          
            lbl2 = QLabel('Artikelnummer')  
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 7, 0)
            grid.addWidget(artEdit, 7, 1)
            grid.addWidget(QLabel("*"), 7,2)
            
            lbl3 = QLabel('Bestelhoeveelheid')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 8, 0)
            grid.addWidget(hoevEdit,8, 1)
            grid.addWidget(QLabel("*"), 8,2)
                       
            lbl4 = QLabel('Inkoopeenheidsprijs')  
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 9, 0)
            grid.addWidget(prijsEdit,9, 1)
            grid.addWidget(QLabel("*"), 9,2)
            
            lbl5 = QLabel('Levering start jjjj-mm-dd')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 10, 0)
            grid.addWidget(startEdit, 10, 1)
            grid.addWidget(QLabel("*"),10, 2)
            
            lbl6 = QLabel('Levering eind jjjj-mm-dd')  
            lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl6, 11, 0)
            grid.addWidget(endEdit, 11, 1)
                        
            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)
    
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 12, 2, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(lambda: sluitRegels(m_email, mlevnr, 0, self))
    
            grid.addWidget(sluitBtn, 12, 1, 1, 1, Qt.AlignRight)
            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 3, Qt.AlignCenter)
                                                                                            
        def inkorderChanged(self, text):
            self.Inkoopordernummer.setText(text)
            
        def artChanged(self,text):
            self.BestelregelArtikel.setText(text)
            
        def hoevChanged(self,text):
            self.BestelHoeveelheid.setText(text)
            
        def prijsChanged(self,text):
            self.Inkoopeenheidsprijs.setText(text)
        
        def startChanged(self,text):
            self.Levering_start.setText(text)
            
        def endChanged(self, text):
            self.Levering_end.setText(text)
          
        def returninkorder(self):
            return self.Inkoopordernummer.text()
        
        def returnart(self):
            return self.BestelregelArtikel.text()
        
        def returnhoev(self):
            return self.BestelHoeveelheid.text()
        
        def returnprijs(self):
            return self.Inkoopeenheidsprijs.text()
        
        def returnstart(self):
            return self.Levering_start.text()
        
        def returnend(self):
            return self.Levering_end.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnart(), dialog.returnhoev(),\
                    dialog.returnprijs(), dialog.returnstart(), dialog.returnend()]  

    window = Widget()
    data = window.getData() 
    if mregel == 1 and data[0]:
        datum = str(datetime.datetime.now())
        mbestdatum = (datum[0:4]+'-'+datum[8:10]+'-'+datum[5:7])
        metadata = MetaData()
        orders_inkoop = Table('orders_inkoop', metadata,
            Column('orderinkoopID', Integer(), primary_key=True),
            Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')),
            Column('besteldatum', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        mbestdatum = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
        ins = insert(orders_inkoop).values(orderinkoopID = minkordnr, leverancierID =\
                    mlevnr, besteldatum = mbestdatum)
        conn.execute(ins)
    elif mregel == 0:
        mregel = 1
    if data[0]: 
        martikelnr = int(data[0])
    else:
        martikelnr = 0
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('bestelstatus', Boolean))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
    rpart=conn.execute(s).first()
    if rpart and rpart[1] == False:
        reedsBesteld()
        inkoopRegels(m_email, rplev, mregel)
    if rpart and data[1] and data[2] and data[3]:
        martikelnr = int(data[0])
        mhoev = float(data[1])
        mprijs = float(data[2])
        mleverstart = data[3]
        if data[4]:
            mlevereind = data[4]
        else:
            mlevereind = data[3]
    else:
        foutArtikel()
        inkoopRegels(m_email, rplev, mregel)
    
    metadata = MetaData()
    orders_inkoop_artikelen = Table('orders_inkoop_artikelen', metadata,
        Column('ordartlevID', Integer(), primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.order_inkoopID')),
        Column('bestelaantal', Float),
        Column('inkoopprijs', Float),
        Column('levering_start', String),
        Column('levering_eind', String),
        Column('regel', Integer))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('bestelsaldo', Float),
        Column('bestelstatus', Boolean),
        Column('art_voorraad', Float),
        Column('reserveringsaldo', Float))
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('orderinkoopID', Integer),
        Column('hoeveelheid', Float),
        Column('reserverings_datum', String),
        Column('levertijd_begin', String),
        Column('levertijd_end', String))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    try:
        mordlevnr=(conn.execute(select([func.max(orders_inkoop_artikelen.c.ordartlevID,\
            type_=Integer)])).scalar())
        mordlevnr += 1
    except:
        mordlevnr = 1
    mlevnr = minkgeg[1]
          
    insrgl = insert(orders_inkoop_artikelen).values(ordartlevID = mordlevnr,\
                 orderinkoopID = minkordnr, artikelID = martikelnr,\
                 bestelaantal = mhoev, inkoopprijs = mprijs, levering_start = mleverstart,\
                 levering_eind = mlevereind, regel = mregel)
    conn.execute(insrgl)
    selart1 = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
    rpart1 = conn.execute(selart1).first()
    mressaldo = rpart1[4]
    martvrd = rpart1[3]
    mbestsaldo = rpart1[1]
     
    selmat = select([materiaallijsten]).where(and_(materiaallijsten.c.artikelID == martikelnr,\
            materiaallijsten.c.orderinkoopID == 0))
    rpmat = conn.execute(selmat)
    mbehoefte = martvrd + mbestsaldo +mhoev - mressaldo
    if mbehoefte >= 0:
        if rpart1:
            updart = update(artikelen).where(and_(orders_inkoop_artikelen.c.artikelID == \
                  artikelen.c.artikelID, artikelen.c.artikelID == martikelnr))\
                  .values(bestelsaldo = artikelen.c.bestelsaldo + mhoev, bestelstatus = False)
            conn.execute(updart)
            mregel += 1
        else:
            foutInvoer()
            inkoopRegels(m_email, rplev, mregel)
    for row in rpmat:
        if mbehoefte >= 0:
            updmat = update(materiaallijsten).where(materiaallijsten.c.artikelID\
              == martikelnr).values(orderinkoopID = minkordnr, levertijd_begin\
              = mleverstart, levertijd_end = mlevereind) 
            conn.execute(updmat)
        else:
            if mregel == 1:
                mregel = 0
            onvBesteld(-mbehoefte)
            inkoopRegels(m_email, rplev, mregel)
            
    invoerOk(mregel-1)
    conn.close
    inkoopRegels(m_email, rplev, mregel)