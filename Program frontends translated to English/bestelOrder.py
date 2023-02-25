from login import hoofdMenu
import sys, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator, QColor, QImage
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout, QPushButton, QLineEdit,\
     QWidget, QMessageBox, QTableView, QVBoxLayout, QComboBox, QStyledItemDelegate,\
     QSpinBox, QCheckBox
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        Float, Boolean, ForeignKey, select, insert, update, delete, and_, func)
from sqlalchemy.exc import IntegrityError

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def bestGelukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Payment has been made\nOrder will be processed!')
    msg.setWindowTitle('Orders')               
    msg.exec_()
    
def betMislukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Payment was not successful\npayment redo!')
    msg.setWindowTitle('Payments')               
    msg.exec_()
    
def betGelukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Payment has been successful!')
    msg.setWindowTitle('Payments')               
    msg.exec_()
  
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request articles')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request articles')               
    msg.exec_() 
    
def geenRegels():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No pending order yet\nfirst order please!')
    msg.setWindowTitle('Ordering')               
    msg.exec_()
    
def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Incorrect Zipcode and/or house number inserted\nor incorrect combination of postcode and house number!')
    msg.setWindowTitle('Zipcode')               
    msg.exec_()
    return(False)
   
def negVoorraad(maant):
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    #msg.setStyleSheet("font: italic 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('There is a shortage of '+str(int(maant))+' on the stock\nThe order cannot be executed, sorry!')
    msg.setWindowTitle('Stock insufficient')
    msg.exec_()
    
def foutAlert(e):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('\n\nAn error occurred.\nPass error message to system administration.\nPress OK to exit program!\n\nError message: '+str(e))
    msg.setWindowTitle('Sytem error')
    msg.exec_()
    
def info():
    class Widget(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Information ordering procedure")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont("Arial", 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
            
            lblinfo = QLabel('Explanation of orders')
            grid.addWidget(lblinfo, 0, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgb(45, 83, 115); font: 25pt Comic Sans MS")
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            lblinfo = QLabel(
        '''
        On the item screen, choose the row with the desired item.
        Then click the first field with the mouse. 
        This action opens an order screen.
        On this order screen you can see the details of the chosen product,
        such as price and description and also a reduced image.
        3 buttons are also visible. Photo, Order and Cart. 
        Photo shows an enlarged image of the product.
        Before ordering, enter the order quantity and with the "Order" button 
        the product is added to the shopping cart. The contents of the shopping cart
        can always be requested with the shopping cart button. 
        You can also change the numbers here, with 0 it becomes product in question removed.
        Click on first field of the subject product, change quantity and click the "Customize" button.
        If the selection is agreed, you can optionally specify a alternate shipping address.
        Enter name, postal code and house number. The street and city name is filled in by the system.
        If shipping address is not entered, the goods will be sent to the billing address.
                
        Then press the "Calculate data" button.
        After this, all amounts and other data are displayed.
        After placing the check mark for accepting the general Conditions,
        the payment button becomes active and you can proceed to checkout.
        The order of Data Calculation and General Terms and Conditions Agreement is important.\t
        As long as payment has not actually taken place, adjustments can still be made are executed.
        To do this, close and reopen the order screen. The following payment methods are possible:
        iDeal via all banks in the Netherlands. Credit card via Visa, American Express or Maestro/Mastercard.
        You can also opt for PayPal or for Afterpay. For Afterpay, however, an additional fee of Euro 2.50
        is charged for insurance and costs. 
        After successful payment, the order will be processed.
       
        ''')
                
            grid.addWidget(lblinfo, 1, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF") 
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn,  3, 0, 1, 4, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setMinimumWidth(650)
            self.setGeometry(550, 50, 900, 150)
            
    window = Widget()
    window.exec_()
    
def refresh(m_email, self, btnStatus, e1, e2, e3, e4, e5, e6, klmail):
    metadata = MetaData() 
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float),
        Column('subtotaal', Float),
        Column('btw', Float),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    btwsel = select([params]).where(params.c.paramID == 1)
    rpbtw = con.execute(btwsel).first()
    btwperc = rpbtw[1]
    selweb = select([webbestellingen]).where(webbestellingen.c.email == m_email).order_by(webbestellingen.c.artikelID)
    rpweb = con.execute(selweb)
    subtot = 0
    btwsub = 0
    for row in rpweb:
        subtot = subtot+row[3]*row[4]
        btwsub = (subtot*btwperc)/(1+btwperc)
        updw = update(webbestellingen).where(and_(webbestellingen.c.email == m_email,\
             webbestellingen.c.artikelID == row[1])).values(subtotaal = subtot, btw = btwsub,\
             voornaam=e1, tussenvoegsel=e2, achternaam=e3, postcode=e4, huisnummer=e5,\
             toevoeging=e6)
        con.execute(updw)
    btnStatus = True
    self.close()
    showBasket(m_email,  self, btnStatus, klmail, subtot, btwsub)
    
def writeVal(valint , rpweb, self):
    metadata = MetaData()
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('reserveringsaldo', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if valint == 0:
        tekst = "Number is 0, the order line has been removed"
        delart = delete(webbestellingen).where(webbestellingen.c.webID == rpweb[6])
        con.execute(delart)
    else:
        updbest = update(webbestellingen).where(webbestellingen.c.webID == rpweb[6]).\
            values(aantal = valint)
        con.execute(updbest)
    updart = update(artikelen).where(artikelen.c.artikelID == rpweb[7]).\
            values(reserveringsaldo = artikelen.c.reserveringsaldo + valint - rpweb[9])
    con.execute(updart)
    tekst = 'Order quantity has been adjusted to '+str(valint)+'.'
    self.close()
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText(tekst)
    msg.setWindowTitle('Order quantity')
    msg.exec_()
    
def invoerOK(mbedrag, mrek, martnr, mhoev, movbestnr, m_email, klmail):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    mdag =  str(datetime.datetime.now())[0:10]
    if mbedrag < 0:
        msg.setText('Credit record created for customer!\n'+klmail+' € '+'{:12.2f}'.format(mbedrag,2))
        metadata = MetaData()              
        webretouren = Table('webretouren', metadata,
            Column('retourID', Integer(), primary_key=True),
            Column('e_mail', String),
            Column('bedrag', Float),
            Column('rekening', String),
            Column('artikelID', Integer),
            Column('aantal', Float),
            Column('ordernummer', Integer),
            Column('boeking', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        try:
            retournr=(con.execute(select([func.max(webretouren.c.retourID,\
                            type_=Integer)])).scalar())
            retournr += 1
        except:
            retournr = 1
        insret = insert(webretouren).values(retourID = retournr, e_mail = klmail,\
              bedrag = mbedrag, rekening = mrek, artikelID = martnr, aantal = mhoev,\
              ordernummer = movbestnr, boeking = mdag)
        con.execute(insret)
    msg.setWindowTitle('Create return booking')
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
    
def showFoto(fotopad):
      class Widget(QDialog):
          def __init__(self, parent=None):
              super(Widget, self).__init__(parent)
              self.setWindowTitle("Image Web article")
              self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
              self.setFont(QFont('Arial', 10))
              pixmap = QPixmap(fotopad)
              lbl21 = QLabel()
              lbl21.setPixmap(pixmap)
              grid = QGridLayout()
              grid.setSpacing(20)
              grid.addWidget(lbl21 , 0, 1)
              self.setLayout(grid)
              self.setGeometry(300, 200, 150, 150)
      win = Widget()
      win.exec_()
        
def invoerBasket(martnr, martomschr, mhoev, verkprijs):
    if mhoev == 1:
        ww = ' is '
    else:
        ww = ' are '
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('There'+ww+str(int(mhoev))+' pcs. '+martomschr+'\narticlenumber: '+str(martnr)+'\nplaced in the shopping cart!')
    msg.setWindowTitle('Shopping cart contents')
    msg.exec_() 
           
def verwerkArtikel(martnr,retstat, m_email, mhoev, self, klmail):
    if retstat:
        if not mhoev.text():
            return
        mhoev = float(str(mhoev.text()))
        mhoev = -mhoev
    else:
        if not mhoev:
            return
        mhoev = float(str(mhoev))
    mjaar = int(str(datetime.datetime.now())[0:4])
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('mutatiedatum', String),
        Column('jaarverbruik_1', Float),
        Column('jaarverbruik_2', Float),
        Column('reserveringsaldo', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False))
    klanten = Table('klanten', metadata,
        Column('klantID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('rekening', String))
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True),
        Column('klantID', None, ForeignKey('klanten.klantID')),
        Column('ovbesteldatum', String),
        Column('datum_betaald', String),
        Column('bedrag', Float))
    orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
        Column('ovaID', Integer, primary_key=True),
        Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('ovaantal', Integer),
        Column('ovleverdatum', String),
        Column('verkoopprijs', Float),
        Column('regel', Integer),
        Column('retour', Float))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('lock', Boolean),
        Column('ondergrens', Float),
        Column('bovengrens', Float))
    afdrachten = Table('afdrachten', metadata,
        Column('afdrachtID', Integer(), primary_key=True),
        Column('soort', String),
        Column('bedrag', Float),
        Column('boekdatum', String),
        Column('betaaldatum', String),
        Column('instantie', String),
        Column('werknemerID', Integer),
        Column('werknummerID', Integer),
        Column('werkorderID', Integer),
        Column('rekeningnummer', String),
        Column('periode', String),
        Column('ovbestelID', Integer))
    artikelmutaties = Table('artikelmutaties', metadata,
       Column('mutatieID', Integer, primary_key=True),
       Column('artikelID', None, ForeignKey('artikelen.artikelID')),
       Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
       Column('hoeveelheid', Float),
       Column('boekdatum', String),
       Column('tot_mag_prijs', Float),
       Column('btw_hoog', Float),
       Column('regel', Integer))
                                       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
                                
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    transaction = con.begin()
    try:
        if retstat:
            selpers = select([artikelen, accounts, klanten]).\
                where(and_(artikelen.c.artikelID == martnr, accounts.c.email\
                == klmail, klanten.c.accountID == accounts.c.accountID))
            rppers = con.execute(selpers).first()
        else:
            selpers = select([artikelen, accounts, klanten]).\
                where(and_(artikelen.c.artikelID == martnr, accounts.c.email\
                == m_email, klanten.c.accountID == accounts.c.accountID))
            rppers = con.execute(selpers).first()
        selmov = select([orders_verkoop]).where(and_(orders_verkoop.\
            c.ovbesteldatum == str(datetime.datetime.now())[0:10],\
            orders_verkoop.c.klantID == rppers[10]))
        rpmov = con.execute(selmov).first()
        
        if rpmov:
            movbestnr = rpmov[0]
            selao = select([orders_verkoop_artikelen]).where(and_(\
                  orders_verkoop_artikelen.c.artikelID == martnr,\
                  orders_verkoop_artikelen.c.ovbestelID == movbestnr))
            rpao = con.execute(selao).first()
        
        mboekd = str(datetime.datetime.now())[0:10]
        movlev = str(datetime.datetime.now()+datetime.timedelta(days=7))[0:10]
        
        if rpmov and not rpao:
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
             (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
             orders_verkoop.c.klantID == rppers[10],\
             orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            if retstat == 0:
                mregel = rpreg[6]+1
                try:
                    movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                     .c.ovaID, type_=Integer)])).scalar())
                    movanr += 1
                except:
                    movanr = 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], ovaantal =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            elif retstat == 1:
                mregel = rpreg[6]+1
                try:
                    movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                      .c.ovaID, type_=Integer)])).scalar())
                    movanr += 1
                except:
                    movanr = 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], retour = mhoev,\
                 verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            if mjaar%2 == 0:    
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                    reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                    reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        elif rpmov and rpao:
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
              (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
              orders_verkoop.c.klantID == rppers[10],\
              orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            mregel = rpreg[6]
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
             (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
             orders_verkoop.c.klantID == rppers[10],\
             orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            if retstat == 0:
                mregel = rpreg[6]
                movanr= rpao[0]
                updova = update(orders_verkoop_artikelen).where(and_\
                 (orders_verkoop_artikelen.c.artikelID == martnr,\
                   orders_verkoop_artikelen.c.ovaID == movanr)).\
                   values(ovaantal=orders_verkoop_artikelen.c.ovaantal+mhoev)
                con.execute(updova)
            elif retstat == 1:
                mregel = rpreg[6]
                movanr= rpao[0]
                updova = update(orders_verkoop_artikelen).where(and_\
                 (orders_verkoop_artikelen.c.artikelID == martnr,\
                   orders_verkoop_artikelen.c.ovaID == movanr)).\
                   values(retour=orders_verkoop_artikelen.c.retour+mhoev)
                con.execute(updova)
            if mjaar%2 == 0:    
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                 reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                     reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        else:
            try:
                movbestnr=(con.execute(select([func.max(orders_verkoop.c.ovbestelID,\
                    type_=Integer)])).scalar())
            except:
                movbestnr = 1
            movbestnr = int(maak11proef(movbestnr))
            insov = insert(orders_verkoop).values(ovbestelID=movbestnr,\
              klantID=rppers[10], ovbesteldatum=str(datetime.datetime.now())[0:10],\
              datum_betaald = str(datetime.datetime.now())[0:10])
            con.execute(insov)
            if retstat == 0:
                mregel = 1
                try:
                    movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                     .c.ovaID, type_=Integer)])).scalar())
                    movanr += 1
                except:
                    movanr = 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], ovaantal =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            elif retstat == 1:
                mregel = 1
                try:
                    movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                      .c.ovaID, type_=Integer)])).scalar())
                    movanr += 1
                except:
                    movanr = 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], retour =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            if mjaar%2 == 0:           
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                   reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                  mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:                     
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                   reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                  mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        uov = update(orders_verkoop).where(and_(orders_verkoop.c.\
         ovbestelID == movbestnr, orders_verkoop_artikelen.c.ovbestelID == movbestnr,\
         orders_verkoop_artikelen.c.regel == mregel)).values(\
         bedrag = orders_verkoop.c.bedrag+\
         orders_verkoop_artikelen.c.verkoopprijs*mhoev+orders_verkoop_artikelen.c.verkoopprijs\
         *orders_verkoop_artikelen.c.retour)
        con.execute(uov)
        try:
            mafdrachtnr =(con.execute(select([func.max(afdrachten.c.afdrachtID,\
             type_=Integer)])).scalar())
            mafdrachtnr += 1
        except:
            mafdrachrnr = 1
        iafdr = insert(afdrachten).values(afdrachtID=mafdrachtnr,\
         soort = 'VAT payment 21%', instantie = 'Tax authorities',\
         rekeningnummer = 'NL10 ABNA 9999999977', boekdatum = mboekd,\
         bedrag = mhoev*rppers[2]*(1+rppar[3][1])*(rppar[0][1]),\
         periode = mboekd[0:7], ovbestelID = movbestnr)
        con.execute(iafdr)
        try:
            mutatienr=(con.execute(select([func.max(artikelmutaties.c.mutatieID,\
              type_=Integer)])).scalar())
            mutatienr += 1
        except:
            mutatienr = 1
        insmut = insert(artikelmutaties).values(mutatieID=mutatienr,\
         artikelID=martnr,ovbestelID=movbestnr, hoeveelheid = -mhoev,\
         boekdatum=mboekd, tot_mag_prijs=rppers[2]*-mhoev,\
         btw_hoog = -mhoev*(rppers[2])*(1+rppar[3][1])*(rppar[0][1]),\
         regel = mregel)  
        con.execute(insmut) 
        mbedrag = mhoev*rppers[2]*(1+rppar[3][1])*(1+rppar[0][1]) 
        mrek = rppers[12]                           
        transaction.commit()
        if retstat and mhoev != 0:
            invoerOK(mbedrag, mrek, martnr, mhoev, movbestnr, m_email, klmail)
            self.close()
    except IntegrityError as e:
        transaction.rollback()
        foutAlert(e)
        sys.exit()
        
def vulBasket(martnr, m_email, mhoev, verkprijs, self):
    mhoev = str(mhoev.text())
    if mhoev > '0':
        mhoev = float(mhoev)
        metadata = MetaData()              
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer, primary_key=True),
            Column('artikelomschrijving', String),
            Column('reserveringsaldo', Float),
            Column('artikelprijs', Float),
            Column('art_voorraad', Float))
        webbestellingen = Table('webbestellingen', metadata,
            Column('webID', Integer, primary_key=True),
            Column('artikelID', ForeignKey('artikelen.artikelID')),
            Column('email', String),
            Column('aantal', Float),
            Column('stukprijs', Float))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        sel = select([artikelen]).where(artikelen.c.artikelID == martnr)
        rpart = con.execute(sel).first()
          
        if rpart[4] - rpart[2] >= mhoev:
            selw = select([webbestellingen]).where(and_(webbestellingen.c.artikelID == martnr,\
                        webbestellingen.c.email == m_email))
            rpw = con.execute(selw).first()
            if rpw:
                updweb = update(webbestellingen).where(and_(webbestellingen.c.artikelID == martnr,\
                               webbestellingen.c.email == m_email)).\
                  values(aantal = webbestellingen.c.aantal + mhoev)
                con.execute(updweb)                
            else:
                try:
                    webnr=con.execute(select([func.max(webbestellingen.c.webID,\
                                        type_=Integer)])).scalar()
                    webnr += 1
                except:
                    webnr = 1
                insw = insert(webbestellingen).values(webID = webnr, artikelID = martnr, email = m_email,\
                               aantal = mhoev, stukprijs = verkprijs)
                con.execute(insw)
            selart = select([artikelen, webbestellingen]).where(and_(artikelen.c.artikelID == martnr, webbestellingen.c.email == m_email))
            rpart = con.execute(selart).first()
            updart = update(artikelen).where(artikelen.c.artikelID == martnr).values(reserveringsaldo = artikelen.c.reserveringsaldo + mhoev)
            con.execute(updart)
            martomschr = rpart[1]
            invoerBasket(martnr, martomschr, mhoev, verkprijs)
            self.close()
        else:
            negVoorraad(rpart[4]-rpart[2])
         
def showBasket(m_email, self, btnStatus, klmail, subtot, btwsub):
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('artikelomschrijving', String),
        Column('thumb_artikel', String),
        Column('foto_artikel', String),
        Column('artikelprijs', Float),
        Column('art_eenheid', String(20)))
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float),
        Column('subtotaal', Float),
        Column('btw', Float),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
    accounts = Table('accounts', metadata,
         Column('accountID', Integer(), primary_key=True),
         Column('email', String),
         Column('voornaam', String), 
         Column('tussenvoegsel', String),
         Column('achternaam', String),
         Column('postcode', String),
         Column('huisnummer', String),
         Column('toevoeging', String))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selbest = select([artikelen, webbestellingen]).where(and_(webbestellingen.c.email == m_email,\
                    webbestellingen.c.artikelID == artikelen.c.artikelID)).order_by(webbestellingen.c.artikelID)
    rps = con.execute(selbest).fetchone()
    selw = select([webbestellingen, accounts]).where(and_(webbestellingen.c.email == m_email,\
                 webbestellingen.c.email == accounts.c.email))
    rpw = con.execute(selw).first()
    postsel = select([params]).where(params.c.paramID == 102)
    rppost = con.execute(postsel).first()
    if rps:
        rpsel = con.execute(selbest)
        class MyWindow(QDialog):
            def __init__(self, data_list, header):
                QDialog.__init__(self)
                self.setWindowTitle('Shopping cart contents')
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
                table_view.setColumnWidth(2, 100)
                table_view.verticalHeader().setDefaultSectionSize(75)
                table_view.setItemDelegateForColumn(2, showImage(self))
                table_view.setColumnHidden(3,True)
                table_view.setColumnHidden(4,True)
                table_view.setColumnHidden(6,True)             
                table_view.setColumnHidden(7,True)
                table_view.setColumnHidden(8,True)
                table_view.setColumnHidden(13,True)
                table_view.setColumnHidden(14,True)
                table_view.setColumnHidden(15,True)
                table_view.setColumnHidden(16,True)
                table_view.setColumnHidden(17,True)
                table_view.setColumnHidden(18,True)
                table_view.clicked.connect(showSpinBox)
                
                grid.addWidget(table_view, 0, 0, 1, 6)
                               
                grid.addWidget(QLabel('Delivery address:           (change if desired)'), 1, 0, 1 ,2)
                
                if rpw[7] == '':
                    e1 = QLineEdit(rpw[15])
                else:
                    e1 = QLineEdit(rpw[10])
                e1.setFixedWidth(220)
                e1.setFont(QFont("Arial",10))
                def textchange():
                    e1.setText(e1.text())
                e1.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,30}$")
                input_validator = QRegExpValidator(reg_ex, e1)
                e1.setValidator(input_validator)
                grid.addWidget(QLabel('First name'), 2, 0)
                grid.addWidget(e1, 2, 1)
                 
                if rpw[7] == '':
                    e2 = QLineEdit(rpw[16])
                else:
                    e2 = QLineEdit(rpw[11])
                e2.setFixedWidth(80)
                e2.setFont(QFont("Arial",10))
                def textchange():
                    e2.setText(e2.text())
                e2.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,10}$")
                input_validator = QRegExpValidator(reg_ex, e2)
                e2.setValidator(input_validator)
                grid.addWidget(QLabel('Infix'), 2, 2)
                grid.addWidget(e2, 2, 3)
                
                if rpw[7] == '':
                    e3 = QLineEdit(rpw[17])
                else:
                    e3 = QLineEdit(rpw[12])               
                e3.setFixedWidth(250)
                e3.setFont(QFont("Arial",10))
                def textchange():
                    e3.setText(e3.text())
                e3.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,50}$")
                input_validator = QRegExpValidator(reg_ex, e3)
                e3.setValidator(input_validator)
                grid.addWidget(QLabel('Surname'), 2, 4)
                grid.addWidget(e3, 2, 5)
                
                if rpw[7] == '':
                    e4 = QLineEdit(rpw[18])
                else:
                    e4 = QLineEdit(rpw[7])
                e4.setFixedWidth(80)
                e4.setFont(QFont("Arial",10))
                def textchange():
                    e4.setText(e4.text().upper())
                e4.textChanged.connect(textchange)
                reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
                input_validator = QRegExpValidator(reg_ex, e4)
                e4.setValidator(input_validator)
                grid.addWidget(QLabel('Zipcode'), 3, 2)
                grid.addWidget(e4, 3, 3) 
        
                if rpw[7] == '':
                    e5 = QLineEdit(rpw[19])
                else:
                    e5 = QLineEdit(rpw[8])
                e5.setFixedWidth(80)
                e5.setFont(QFont("Arial",10))
                def textchange():
                    e5.setText(e5.text())
                e5.textChanged.connect(textchange)
                reg_ex = QRegExp("^[0-9]{1,5}$")
                input_validator = QRegExpValidator(reg_ex, e5)
                e5.setValidator(input_validator)
                grid.addWidget(e5, 3, 1)  #huisnummer
                grid.addWidget(QLabel('Suffix'), 3, 1, 1, 1, Qt.AlignCenter)
                
                if rpw[7] == '':
                    e6 = QLineEdit(rpw[20])
                else:
                    e6 = QLineEdit(rpw[9])
                e6.setFixedWidth(80)
                e6.setFont(QFont("Arial",10))
                def textchange():
                    e6.setText(e6.text())
                e6.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{0,8}")
                input_validator = QRegExpValidator(reg_ex, e6)
                e6.setValidator(input_validator)
                grid.addWidget(e6, 3, 1, 1, 1, Qt.AlignRight)   #addition housenumber
                              
                from postcode import checkpostcode
                postcStatus = True
                if rpw[7] == '':
                    mstrtpls = checkpostcode(rpw[18], int(rpw[19]))
                    if mstrtpls[0] == '':
                        postcStatus=foutPostcode()
                else:
                    mstrtpls = checkpostcode(rpw[7], int(rpw[8]))
                    if mstrtpls[0] == '':
                        postcStatus=foutPostcode()   
                            
                mfactsp = checkpostcode(rpw[18], int(rpw[19]))
                grid.addWidget(QLabel('Billing address: '+rpw[15]+' '+rpw[16]+' '+rpw[17]+',  '+mfactsp[0]+' '+rpw[19]+', '+rpw[18]+' '+mfactsp[1]+'.'), 4, 0, 1 ,4)
 
                freshBtn = QPushButton('Caculate\ndata')
                freshBtn.clicked.connect(lambda: refresh(m_email, self,\
                   btnStatus, e1.text(), e2.text(), e3.text(), e4.text(), e5.text(), e6.text(), klmail))

                freshBtn.setFont(QFont("Arial",10))
                freshBtn.setFixedWidth(120) 
                freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
                grid.addWidget(freshBtn, 6, 5, 2, 1, Qt.AlignRight | Qt.AlignBottom)
                
                betaalBtn = QPushButton()
                betaalBtn.setIcon(QIcon('./images/logos/Betaal/afrekenen.png'))
                betaalBtn.setIconSize(QSize(90, 60))
                
                betaalBtn.setFixedWidth(100) 
                betaalBtn.setStyleSheet("color: black;  background-color: gainsboro")
                betaalBtn.clicked.connect(lambda: betaalBasket(m_email, klmail, factbedrag))
              
                grid.addWidget(betaalBtn, 6, 5, 2, 1, Qt.AlignLeft | Qt.AlignTop)
  
                sluitBtn = QPushButton('Close')
                sluitBtn.clicked.connect(self.close)

                sluitBtn.setFont(QFont("Arial",10))
                sluitBtn.setFixedWidth(100) 
                sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(sluitBtn, 7, 4, 1, 1, Qt.AlignRight)
                
                helpBtn = QPushButton('Information')
                helpBtn.clicked.connect(lambda: help())

                helpBtn.setFont(QFont("Arial",10))
                helpBtn.setFixedWidth(100) 
                helpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(helpBtn, 7, 3, 1, 1, Qt.AlignRight)
                
                helpBtn = QPushButton('Information')
                helpBtn.clicked.connect(lambda: info())

                helpBtn.setFont(QFont("Arial",10))
                helpBtn.setFixedWidth(100) 
                helpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(helpBtn, 7, 3, 1, 1, Qt.AlignRight)
                
                betaalBtn.setEnabled(False)
                cBox = QCheckBox('Agree terms and conditions!')
                def cboxChange():
                    cBox = self.sender()
                    if (cBox.isChecked() and postcStatus and  btnStatus):
                        betaalBtn.setEnabled(True)
                        cBox.setChecked(True)
                                                               
                cBox.toggled.connect(cboxChange)
   
                grid.addWidget(cBox, 4, 4, 1, 2)
                             
                grid.addWidget(QLabel(mstrtpls[0]), 3, 0)
                grid.addWidget(QLabel(mstrtpls[1]), 3, 4)
                
                postnl = rppost[1]
                factbedrag = subtot+postnl
                              
                grid.addWidget(QLabel('Sum subtotals:  '), 5, 0)
                grid.addWidget(QLabel('{:12.2f}'.format(subtot)), 5, 1, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('VAT amount 21%: '), 5 ,2, 1, 2)
                grid.addWidget(QLabel('{:12.2f}'.format(btwsub)), 5, 3, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('Delivery costs PostNL: '), 6, 0)
                grid.addWidget(QLabel('{:12.2f}'.format(postnl)), 6, 1, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('Total invoice amount: '), 7, 0)
                grid.addWidget(QLabel('{:12.2f}'.format(factbedrag)), 7, 1, 1, 1, Qt.AlignRight)
     
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 6, Qt.AlignCenter)
                
                self.setLayout(grid)
                self.setGeometry(250, 50, 600, 900)
                                              
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

        class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap))
 
        header = ['Articlenumber','Description', 'Thumb','Photo','Articleprice', 'Unity',\
                  'WebID','Articlenumber', 'email','Amount','Unit price', 'Subtotal', 'VAT',\
                  '','','','','','']
                          
        data_list=[]
        for row in rpsel:
            data_list += [(row)]
                          
        def showSpinBox(idx):
            artnr = idx.data()
            if idx.column() == 0 and not btnStatus:
               engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
               con = engine.connect()
               selweb = select([artikelen, webbestellingen]).where(and_(webbestellingen.c.artikelID == artnr,\
               webbestellingen.c.artikelID == artikelen.c.artikelID, webbestellingen.c.email == m_email))
               rpweb = con.execute(selweb).first()
               class MainWindow(QDialog):
                   def __init__(self):
                        QDialog.__init__(self)
                                                         
                        self.setWindowTitle("Modify number")
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        self.setFont(QFont('Arial', 10))
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                        
                        lbl = QLabel()
                        pixmap = QPixmap('./images/logos/verbinding.jpg')
                        lbl.setPixmap(pixmap)
                        grid.addWidget(lbl , 0, 0, 1, 2)
            
                        logo = QLabel()
                        pixmap = QPixmap('./images/logos/logo.jpg')
                        logo.setPixmap(pixmap)
                        grid.addWidget(logo , 0, 0, 1, 2, Qt.AlignRight)
                        
                        self.qspin = QSpinBox()
                        self.qspin.setRange(0, 100)
                        self.qspin.setFrame(True)
                        self.qspin.setFont(QFont('Arial', 10))
                        self.qspin.setValue(int(rpweb[9]))
                        self.qspin.setFixedSize(40, 30)
                        self.qspin.setStyleSheet("color: black; font: bold;  background-color: gainsboro")
                        
                        def valuechange():
                           self.qspin.setValue(self.qspin.value())
                                                                         
                        self.qspin.valueChanged.connect(valuechange)
                                                                 
                        grid.addWidget(QLabel('Modify order amount of article\n'+str(rpweb[0])+' '+rpweb[1]), 2, 0, 1, 2)
                        
                        grid.addWidget(QLabel('Order amount'), 3, 0, 1, 2, Qt.AlignCenter)
                        grid.addWidget(self.qspin, 3, 1)
                        
                        lblpic = QLabel()
                        pixmap = QPixmap(rpweb[2])
                        lblpic.setPixmap(pixmap)
                        grid.addWidget(lblpic , 3, 0, 2, 1)
                        
                        closeBtn = QPushButton('Sluiten')
                        closeBtn.clicked.connect(self.close)
                       
                        grid.addWidget(closeBtn, 4, 0, 1, 1, Qt.AlignRight)
                        closeBtn.setFont(QFont("Arial",10))
                        closeBtn.setFixedWidth(100) 
                        closeBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                                                                                   
                        aanpBtn = QPushButton('Modify')
                        aanpBtn.clicked.connect(lambda: writeVal(self.qspin.value(), rpweb, self))
                       
                        grid.addWidget(aanpBtn, 4, 1, 1, 1, Qt.AlignRight)
                        aanpBtn.setFont(QFont("Arial",10))
                        aanpBtn.setFixedWidth(100) 
                        aanpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                                                                          
                        grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 2, Qt.AlignCenter)
                        
                        self.setLayout(grid)
                        self.setGeometry(900, 200, 100, 100)
                        self.setLayout(grid)
                                                
               mainWin = MainWindow()
               mainWin.exec_()
                  
        win = MyWindow(data_list, header)
        win.exec_()
    else:
        geenRegels()
         
def betaalBasket(m_email, klmail, factbedrag):
    metadata = MetaData()              
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selbest = select([webbestellingen]).where(webbestellingen.c.email == m_email)
    rps = con.execute(selbest).fetchone()
    if rps:
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
                self.setWindowTitle("Shopping cart and payment")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                self.setFont(QFont('Arial', 10))
                grid = QGridLayout()
                grid.setSpacing(20)
                self.setLayout(grid)
                self.setGeometry(400, 100, 250, 150)
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl , 0, 0, 1, 2)
                
                lblinfo = QLabel('Payment\n€ '+'{:12.2f}'.format(factbedrag))
                grid.addWidget(lblinfo, 0, 2, 1, 2, Qt.AlignCenter)
                lblinfo.setStyleSheet("color: rgb(45, 83, 115); font: 18pt Comic Sans MS")
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 0, 4, 1, 1, Qt.AlignRight)
                
                ideal = QLabel()
                pixmap = QPixmap('./images/logos/Betaal/iDEAL.png')
                ideal.setPixmap(pixmap.scaled(120, 120))
                grid.addWidget(ideal, 1, 0, 1, 5, Qt.AlignCenter)
  
                ABNamroBtn = QPushButton()
                ABNamroBtn.clicked.connect(lambda: handler(m_email, self))
                ABNamroBtn.setCheckable(True)
                grid.addWidget(ABNamroBtn, 2, 0)
                ABNamroBtn.setIcon(QIcon('./images/logos/Betaal/ABNAmro.png'))
                ABNamroBtn.setIconSize(QSize(90, 60))
                ABNamroBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                ASNBankBtn = QPushButton()
                ASNBankBtn.clicked.connect(lambda: handler(m_email, self))
                ASNBankBtn.setCheckable(True)
                grid.addWidget(ASNBankBtn, 2, 1)
                ASNBankBtn.setIcon(QIcon('./images/logos/Betaal/ASNBank.png'))
                ASNBankBtn.setIconSize(QSize(90, 60))
                ASNBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                INGBtn = QPushButton()
                INGBtn.clicked.connect(lambda: handler(m_email, self))
                INGBtn.setCheckable(True)
                grid.addWidget(INGBtn, 2, 2)
                INGBtn.setIcon(QIcon('./images/logos/Betaal/ING.png'))
                INGBtn.setIconSize(QSize(90, 60))
                INGBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                KnabBtn = QPushButton()
                KnabBtn.clicked.connect(lambda: handler(m_email, self))
                KnabBtn.setCheckable(True)
                grid.addWidget(KnabBtn, 2, 3)
                KnabBtn.setIcon(QIcon('./images/logos/Betaal/Knab.png'))
                KnabBtn.setIconSize(QSize(90, 60))
                KnabBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                RabobankBtn = QPushButton()
                RabobankBtn.clicked.connect(lambda: handler(m_email, self))
                RabobankBtn.setCheckable(True)
                grid.addWidget(RabobankBtn, 2, 4)
                RabobankBtn.setIcon(QIcon('./images/logos/Betaal/Rabobank.png'))
                RabobankBtn.setIconSize(QSize(90, 60))
                RabobankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                RegioBankBtn = QPushButton()
                RegioBankBtn.clicked.connect(lambda: handler(m_email, self))
                RegioBankBtn.setCheckable(True)
                grid.addWidget(RegioBankBtn, 3, 0)
                RegioBankBtn.setIcon(QIcon('./images/logos/Betaal/RegioBank.png'))
                RegioBankBtn.setIconSize(QSize(90, 60))
                RegioBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                SNSBankBtn = QPushButton()
                SNSBankBtn.clicked.connect(lambda: handler(m_email, self))
                SNSBankBtn.setCheckable(True)
                grid.addWidget(SNSBankBtn, 3, 1)
                SNSBankBtn.setIcon(QIcon('./images/logos/Betaal/SNSBank.png'))
                SNSBankBtn.setIconSize(QSize(90, 60))
                SNSBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                TriodosBankBtn = QPushButton()
                TriodosBankBtn.clicked.connect(lambda: handler(m_email, self))
                TriodosBankBtn.setCheckable(True)
                grid.addWidget(TriodosBankBtn, 3, 2)
                TriodosBankBtn.setIcon(QIcon('./images/logos/Betaal/TriodosBank.png'))
                TriodosBankBtn.setIconSize(QSize(90, 60))
                TriodosBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                VanLanschotBtn = QPushButton()
                VanLanschotBtn.clicked.connect(lambda: handler(m_email, self))
                VanLanschotBtn.setCheckable(True)
                grid.addWidget(VanLanschotBtn, 3, 3)
                VanLanschotBtn.setIcon(QIcon('./images/logos/Betaal/VanLanschot.png'))
                VanLanschotBtn.setIconSize(QSize(90, 60))
                VanLanschotBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                credit = QLabel()
                pixmap = QPixmap('./images/logos/Betaal/creditcard.jpg')
                credit.setPixmap(pixmap.scaled(120, 70))
                grid.addWidget(credit, 4, 0, 1, 5, Qt.AlignCenter)
                 
                VisaBtn = QPushButton()
                VisaBtn.clicked.connect(lambda: handler(m_email, self))
                VisaBtn.setCheckable(True)
                grid.addWidget(VisaBtn, 5, 1)
                VisaBtn.setIcon(QIcon('./images/logos/Betaal/Visa.png'))
                VisaBtn.setIconSize(QSize(90, 60))
                VisaBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                
                MasterCardBtn = QPushButton()
                MasterCardBtn.clicked.connect(lambda: handler(m_email, self))
                MasterCardBtn.setCheckable(True)
                grid.addWidget(MasterCardBtn, 5, 2)
                MasterCardBtn.setIcon(QIcon('./images/logos/Betaal/MasterCard.png'))
                MasterCardBtn.setIconSize(QSize(90, 60))
                MasterCardBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                AmericanExpressBtn = QPushButton()
                AmericanExpressBtn.clicked.connect(lambda: handler(m_email, self))
                AmericanExpressBtn.setCheckable(True)
                grid.addWidget(AmericanExpressBtn, 5, 3)
                AmericanExpressBtn.setIcon(QIcon('./images/logos/Betaal/AmericanExpress.png'))
                AmericanExpressBtn.setIconSize(QSize(90, 60))
                AmericanExpressBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                PayPalBtn = QPushButton()
                PayPalBtn.clicked.connect(lambda: handler(m_email, self))
                PayPalBtn.setCheckable(True)
                grid.addWidget(PayPalBtn, 6, 0)
                PayPalBtn.setIcon(QIcon('./images/logos/Betaal/PayPal.png'))
                PayPalBtn.setIconSize(QSize(90, 60))
                PayPalBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                        
                afterPayBtn = QPushButton()
                afterPayBtn.clicked.connect(lambda: handler(m_email, self))
                afterPayBtn.setCheckable(True)
                grid.addWidget(afterPayBtn, 6, 4)
                afterPayBtn.setIcon(QIcon('./images/logos/Betaal/afterpay.png'))
                afterPayBtn.setIconSize(QSize(90, 60))
                afterPayBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
                sluitenBtn = QPushButton('Close')
                sluitenBtn.clicked.connect(self.accept)
                
                grid.addWidget(sluitenBtn, 7, 4)
                sluitenBtn.setFont(QFont("Arial",10))
                sluitenBtn.setFixedWidth(100) 
                sluitenBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 6, Qt.AlignCenter)
                                
                def handler(m_email, self):
                    if PayPalBtn.isChecked() or ABNamroBtn.isChecked() or afterPayBtn.isChecked()\
                        or ASNBankBtn.isChecked() or INGBtn.isChecked() or KnabBtn.isChecked()\
                        or RabobankBtn.isChecked() or RegioBankBtn.isChecked() or\
                        SNSBankBtn.isChecked() or TriodosBankBtn.isChecked() or\
                        VanLanschotBtn.isChecked() or AmericanExpressBtn.isChecked() or\
                        MasterCardBtn.isChecked() or VisaBtn.isChecked():
                    
                        #if production, pass on amount and name Pandora BV Vianen 
                        #and customer e-mail upon receiving back agreement, run below  
                        #else notification to make payment again!

                        rpsel = con.execute(selbest)
                        for row in rpsel:
                            verwerkArtikel(row[1], 0, m_email, row[3], self, klmail)
                            delsel = delete(webbestellingen).where(webbestellingen.c.email == m_email)
                            con.execute(delsel)
                        bestGelukt()
                        self.close()
                    else:
                        betMislukt()
                        self.close()
                               
        win = Widget()
        win.exec_()
    else:
        geenRegels()
 
def artKeuze(m_email, retstat, klmail):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request / Order Webarticles")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(240)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Search sort key')
            k0Edit.addItem('1. Sorted on articlenumber')
            k0Edit.addItem('2. Sorted on stock')
            k0Edit.addItem('3. Filtered description')
            k0Edit.addItem('4. Filtered articlegroup.')
            k0Edit.addItem('5. Filtered storagelocation.')
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
            grid.addWidget(lbl , 1, 0, 1 ,2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 2, Qt.AlignRight)
                                  
            grid.addWidget(k0Edit, 2, 1)
            lbl1 = QLabel('Search term')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3)
        
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
      
            grid.addWidget(applyBtn, 5, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(closeBtn, 5, 1, 1, 1)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
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
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonArtikellijst(m_email, retstat, keuze, zoekterm, klmail)
                   
def toonArtikellijst(m_email, retstat, keuze, zoekterm, klmail):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Articlelist')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setColumnWidth(2, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.setItemDelegateForColumn(2, showImage(self))
            table_view.clicked.connect(showSelart)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
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
        
    class showImage(QStyledItemDelegate):  
       def __init__(self, parent):
           QStyledItemDelegate.__init__(self, parent)
       def paint(self, painter, option, index):        
            painter.fillRect(option.rect,QColor(255,255,255))
            image = QImage(index.data())
            pixmap = QPixmap(image)
            pixmap.scaled(256,256) 
            return(painter.drawPixmap(option.rect, pixmap))
       
    header = ['Articlenumber','Description', 'Thumb','Articleprice', 'Stock',\
              'Unit','Minimum Stock','Order size', 'Location',\
              'Articlegroup', 'Category', 'Size']
    
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('thumb_artikel', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float),
        Column('locatie_magazijn', String(10)),
        Column('artikelgroep', String),
        Column('categorie', String(10)),
        Column('afmeting', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
        sel = select([artikelen]).order_by(artikelen.c.artikelID)
    elif keuze == 2:
        sel = select([artikelen]).order_by(artikelen.c.art_voorraad)
    elif keuze == 3:
        sel = select([artikelen]).where(artikelen.c.artikelomschrijving.ilike\
           ('%'+zoekterm+'%')).order_by(artikelen.c.artikelID) 
    elif keuze == 4:
        sel = select([artikelen]).where(artikelen.c.artikelgroep.ilike\
            ('%'+zoekterm+'%')).order_by(artikelen.c.artikelgroep)
    elif keuze == 5:
        sel = select([artikelen]).where(artikelen.c.locatie_magazijn.\
        ilike('%'+zoekterm+'%')).order_by(artikelen.c.locatie_magazijn)
    else:
        ongInvoer()
        artKeuze(m_email, retstat, klmail)

    if con.execute(sel).fetchone():
        rpartikelen = con.execute(sel)
    else:
        geenRecord()
        artKeuze(m_email,retstat,klmail)
     
    data_list=[]
    for row in rpartikelen:
        data_list += [(row)]
        
    def showSelart(idx):
        martnr = idx.data()
        if idx.column() == 0:
            header = ['Articlenumber','Description','Articleprice', 'Stock',\
              'Unit','Minimum Stock','Ordersize', 'Location',\
              'Articlegroup', 'Category', 'Size', 'Image']
        
            metadata = MetaData()              
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float),
                Column('art_voorraad', Float),
                Column('art_eenheid', String(20)),
                Column('art_min_voorraad', Float),
                Column('art_bestelgrootte', Float),
                Column('locatie_magazijn', String(10)),
                Column('artikelgroep', String),
                Column('categorie', String(10)),
                Column('afmeting', String),
                Column('thumb_artikel', String),
                Column('foto_artikel', String))
            params = Table('params', metadata,
                Column('paramID', Integer, primary_key=True),
                Column('tarief', Float))
             
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
      
            sel = select([artikelen]).where(artikelen.c.artikelID == martnr)
            rpartikelen = con.execute(sel).first()
                
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
            verkprijs = rpartikelen[2]*(1+rppar[3][1])*(1+rppar[0][1])
                                 
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                
                    self.setWindowTitle("Orders Webarticles")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Orders Webarticles'),0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)                
                    index = 1
                    for item in header:
                        self.lbl = QLabel(header[index-1])
                        self.Gegevens = QLabel()
                        if index == 2:
                            q1Edit = QLineEdit(str(rpartikelen[index-1]))
                            q1Edit.setFixedWidth(400)
                        elif index == 3:
                            q1Edit = QLineEdit('{:12.2f}'.format(rpartikelen[index-1]*(1+rppar[3][1])*(1+rppar[0][1])))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setAlignment(Qt.AlignRight)
                        elif index == 12:
                            pixmap = QPixmap(rpartikelen[11])
                            lbl21 = QLabel(self)
                            lbl21.setPixmap(pixmap)
                            grid.addWidget(lbl21 , index, 1, 3, 1)
                        else:
                            q1Edit = QLineEdit(str(rpartikelen[index-1]))
                            q1Edit.setFixedWidth(100)
                                                     
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q1Edit.setDisabled(True)
                        grid.addWidget(self.lbl, index, 0)
                        if index != 12 and index != 13:
                            grid.addWidget(q1Edit, index, 1, 1, 2)
          
                        index += 1
                    
                    self.Bestelaantal = QLabel(self)
                    if retstat == 0:
                        self.Bestelaantal.setText('                     Ordersize ')
                    else:
                        self.Bestelaantal.setText('                          Return\n                          Quantity')
                    self.best = QLineEdit(self)
                    self.best.setFixedWidth(50)
                    
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.best)
                    self.best.setValidator(input_validator)
                    
                    grid.addWidget(self.Bestelaantal, index-1, 1)
                    grid.addWidget(self.best, index-1, 1, 1, 1, Qt.AlignRight)
                    
                    subtot = 0
                    btwsub = 0
                    basket = QPushButton()
                    grid.addWidget(basket, index-5, 2, 2, 1, Qt.AlignLeft)
                    btnStatus = False
                    basket.setIcon(QIcon('./images/logos/basket.jpg'))
                    basket.setIconSize(QSize(90, 90))
                    basket.setStyleSheet("color: black;  background-color: gainsboro")
                    basket.clicked.connect(lambda: showBasket(m_email, self, btnStatus, klmail, subtot,btwsub))
                                      
                    fotoBtn = QPushButton('Big Photo')
                    fotoBtn.clicked.connect(lambda: showFoto(rpartikelen[12]))
            
                    grid.addWidget(fotoBtn, index-3, 2, 1, 1, Qt.AlignTop)
                    fotoBtn.setFont(QFont("Arial",10))
                    fotoBtn.setFixedWidth(100) 
                    fotoBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
                    terugBtn = QPushButton('Close')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, index-2, 2)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100) 
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    mhoev = self.best
                    if retstat == 1:
                        basket.setDisabled(True)
                        bestelBtn = QPushButton('Return')
                        bestelBtn.clicked.connect(lambda: verwerkArtikel(str(martnr),retstat, m_email, mhoev, self, klmail))
                    else:
                        basket.setDisabled(False)
                        bestelBtn = QPushButton('Ordering')
                        bestelBtn.clicked.connect(lambda: vulBasket(str(martnr), m_email, mhoev, verkprijs, self))
                     
                    grid.addWidget(bestelBtn, index-1, 2)
                    bestelBtn.setFont(QFont("Arial",10))
                    bestelBtn.setFixedWidth(100) 
                    bestelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                 
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+4, 0, 1, 3, Qt.AlignCenter)
                                                                               
                    self.setLayout(grid)
                    self.setGeometry(300, 150, 150, 150)
                                                               
            mainWin = MainWindow()
            mainWin.exec_()
                      
    win = MyWindow(data_list, header)
    win.exec_()
    artKeuze(m_email, retstat, klmail)