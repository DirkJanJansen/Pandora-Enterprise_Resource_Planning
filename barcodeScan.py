from login import hoofdMenu
from datetime import datetime
from sys import platform
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QTextEdit
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, Float,\
                        select, update,insert, delete, func, and_, Boolean)

def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Er zijn nog geen transacties!')
    msg.setWindowTitle('Transacties')
    msg.exec_() 

def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatie Barcodescannen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Informatie ERP Pandora')
            grid.addWidget(lblinfo, 0, 0, 1, 2, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            
            infolbl = QLabel('''\t\t\t\t\t\t\t\t\t\t
        Instruktie barcode scannen.
        
        Als testscanner is een hand laserscanner gebruikt van het type Nedis BCRLR100BK
        De produkten kunnen gescand worden tot een afstand van 55cm.
        Standaard wordt gescand met een hoeveelheid van 1.
        Indien meerdere produkten van het zelfde artikelnummer benodigd zijn, kan d.m.v. de 
        spinbox het juiste aantal worden gekozen voor het scannen. 
        Dit kan met de pijltjes van de spinbox of met het muiswieltje.
        Na de barcodescan wordt het aantal weer teruggezet op 1.
        Indien het scannen wordt gestart wordt de sluitknop geblokkeerd tot de knop volgende
        klant wordt gedrukt.
        De printknop en de klantknop worden geblokkeerd tot de eerste transactie is geboekt.
        In de volgende gevallen wordt onder het displayscherm in het rood een foutmelding
        getoond.
        
        1. Als een leesfout met scannen van de barcode plaatsvindt.
        2. Bij onvoldoende voorraad om de bestelling te leveren, tevens wordt de magazijn 
           voorraad getoond.
        3. Indien het produkt (nog) niet in het assortiment is opgenomen.
        Tevens klinkt in deze 3 gevallen een akoestisch alarm.
        
        Indien het artikel niet gescand kan worden, is het mogelijk om de barcode handmatig 
        in te geven, toets hierna <Enter> op het toetsenbord.
                           
        Nadat het scannen gereed is kan de printbon worden uitgeprint.
        Voor het programma wordt afgesloten, dient eerst de klantknop te worden ingedrukt,
        voor de sluitknop wordt vrijgegeven. Hiermee worden de noodzakelijke boekingen
        uitgevoerd en de order voor de volgende klant voorbereid.
        
        Voor het retourboeken van een artikel wordt de ± button gebruikt. Deze knop is
        beschikbaar als de rol (S) van Magazijn in het menu authorisaties is geactiveerd..
        ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setFont(QFont("Arial", 10))
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Webverkooporders printen')
    msg.exec_()
    
def heading(mblad, mbonnr):
    kop=\
    ('Balieverkoop - Ordernummer: '+ str(mbonnr)+' Datum: '+str(datetime.now())[0:10]+' bladzijde '+str(mblad)+' \n'+
    '==============================================================================================\n'+
    'Artikelnr  Omschrijving                             Aantal       Prijs   Subtotaal     BTW 21%\n'+
    '==============================================================================================\n')
    return(kop)

def printBon(self):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Printen orderbon")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Wilt U de orderbon printen?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        metadata = MetaData()
        balieverkoop = Table('balieverkoop', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('bonnummer', Integer),
            Column('artikelID', Integer),
            Column('barcode', String),
            Column('omschrijving', String),
            Column('aantal', Float),
            Column('prijs', Float),
            Column('subtotaal', Float),
            Column('subbtw', Float))
        params = Table('params', metadata,
            Column('paramID', Integer(), primary_key=True),
            Column('tarief', Float),
            Column('lock', Boolean))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selpar = select([params]).where(params.c.paramID == 103)
        rppar = con.execute(selpar).first()
        mbonnr = int(rppar[1])
        delbal = delete(balieverkoop).where(and_(balieverkoop.c.aantal == 0,\
                       balieverkoop.c.bonnummer == mbonnr))
        con.execute(delbal)
        selb = select([balieverkoop]).where(balieverkoop.c.bonnummer == mbonnr).order_by(balieverkoop.c.barcode)
        rpb = con.execute(selb)
        mblad = 0
        rgl = 0
        if platform == 'win32':
            fbarc = '.\\forms\\Barcodelijsten\\'+str(mbonnr)+'.txt'
        else:
            fbarc = './forms//Barcodelijsten/'+str(mbonnr)+'.txt'
        
        for row in rpb:
            rgl += 1
            if rgl == 1 :
                mblad += 1
                open(fbarc, 'w').write(heading(mblad, mbonnr))
            elif rgl%57 == 1:
                mblad += 1
                open(fbarc, 'a').write(heading(mblad, mbonnr))
                
            martnr = row[2]
            momschr = row[4]
            maantal = row[5]
            mprijs = row[6]
            msubtotaal = row[7]
            msubtotbtw = row[8]
            open(fbarc,'a').write(str(martnr) +'  '+'{:<40s}'.format(momschr)+' '+'{:>6d}'\
                     .format(int(maantal))+'{:>12.2f}'.format(float(mprijs))+'{:>12.2f}'\
                     .format(float(msubtotaal))+'{:>12.2f}'\
                     .format(float(msubtotbtw))+'\n')
             
        tail=\
        ('==============================================================================================\n'+
        'Totaal bedrag af te rekenen inclusief BTW  en bedrag BTW 21%          '+'{:>12.2f}'.format(self.mtotaal)+'{:>12.2f}'.format(self.mtotbtw)+' \n'+
        '==============================================================================================\n')
        if rgl > 0:
            open(fbarc,'a').write(tail) 
            if platform == 'win32':
                from os import startfile
                startfile(fbarc, "print")
            else:
                from os import system
                system("lpr "+fbarc)
            printing()
        else:
            geenGegevens()
        
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def nextClient(self):
    mboekd = str(datetime.now())[0:10]
    metadata = MetaData()
    balieverkoop = Table('balieverkoop', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('bonnummer', Integer),
        Column('artikelID', Integer),
        Column('barcode', String),
        Column('omschrijving', String),
        Column('aantal', Float),
        Column('prijs', Float),
        Column('subtotaal', Float),
        Column('subbtw', Float))
    artikelmutaties = Table('artikelmutaties', metadata,
        Column('mutatieID', Integer, primary_key=True),
        Column('artikelID', Integer),
        Column('hoeveelheid', Float),
        Column('boekdatum', String),
        Column('baliebonID', Integer),
        Column('tot_mag_prijs', Float),
        Column('btw_hoog', Float))
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('tarief', Float),
        Column('lock', Boolean))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).where(params.c.paramID == 103)
    rppar = con.execute(selpar).first()
    mbonnr = rppar[1]
    delbal = delete(balieverkoop).where(and_(balieverkoop.c.aantal == 0,\
               balieverkoop.c.bonnummer == mbonnr))
    con.execute(delbal)

    selb = select([balieverkoop]).where(balieverkoop.c.bonnummer == mbonnr)\
                      .order_by(balieverkoop.c.barcode)
    rpb = con.execute(selb)
    for row in rpb:
        mmutnr = con.execute(select([func.max(artikelmutaties.c.mutatieID, type_=Integer)])).scalar()
        mmutnr += 1
        insmut = insert(artikelmutaties).values(mutatieID = mmutnr, artikelID = row[2],\
                hoeveelheid = row[5], boekdatum = mboekd, baliebonID = mbonnr,\
                tot_mag_prijs = row[7], btw_hoog = row[8])
        con.execute(insmut)
    if self.mtotbtw != int(0):
        metadata = MetaData() 
        afdrachten = Table('afdrachten', metadata,
            Column('afdrachtID', Integer(), primary_key=True),
            Column('soort', String),
            Column('bedrag', Float),
            Column('boekdatum', String),
            Column('betaaldatum', String),
            Column('instantie', String),
            Column('rekeningnummer', String),
            Column('ovbestelID', Integer))
     
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        mafdrnr = (con.execute(select([func.max(afdrachten.c.afdrachtID,\
                      type_=Integer).label('mafdrnr')])).scalar())
        mafdrnr += 1
        insdr = insert(afdrachten).values(afdrachtID = mafdrnr, boekdatum = mboekd,\
             soort = 'BTW afdracht 21%', bedrag = self.mtotbtw, instantie = 'Belastingdienst',\
             ovbestelID = int(mbonnr), rekeningnummer= 'NL10 ABNA 9999999977')
        con.execute(insdr)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")
        self.printBtn.setDisabled(True)
        self.printBtn.setStyleSheet("color: grey; background-color: gainsboro")
        self.nextBtn.setDisabled(True)
        self.nextBtn.setStyleSheet("color: grey; background-color: gainsboro")
        mbonnr += 1
        updpar = update(params).where(params.c.paramID == 103).values(tarief = mbonnr, lock = False)
        con.execute(updpar)
        self.mtotaal = 0.00
        self.mtotbtw = 0.00
        self.mlist = []
        self.view.setText('')
        self.qtailtext = 'Totaal incl. BTW  '+'{:\u2000>12.2f}'.format(self.mtotaal)+'{:\u2000>12.2f}'.format(self.mtotbtw)+' BTW'
        self.qtailEdit.setText(self.qtailtext)
    else:
        updpar = update(params).where(params.c.paramID == 103).values(lock = False)
        con.execute(updpar)
        geenGegevens()
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")

def geefAlarm():
    if platform == 'win32':
        import winsound
        winsound.Beep(800,200)
        winsound.Beep(400,400)
        winsound.Beep(600,200)
    else:
        #sudo apt install sox
        from os import system
        system('play -nq -t alsa synth {} sine {}'.format(0.2, 800))
        system('play -nq -t alsa synth {} sine {}'.format(0.4, 400))
        system('play -nq -t alsa synth {} sine {}'.format(0.2, 600))
   
def plusminChange(self):
    if self.plusminBtn.isChecked():
        self.plusminBtn.setText('-')
        self.qspin.setRange(-99, -1)
    else:
        self.plusminBtn.setText('+')
        self.qspin.setRange(1, 99)
        
def checkBarcode(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+int(c[8])+int(c[10])+(int(c[1])+
                int(c[3])+int(c[5])+int(c[7])+int(c[9])+int(c[11]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[12]):
        return True
    else:
        return False
    
def set_barcodenr(self):
    barcodenr = self.q1Edit.text()
    maantal = self.qspin.value()
    self.albl.setText('')
    if len(barcodenr) == 13 and checkBarcode(barcodenr):
        metadata = MetaData()
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer(), primary_key=True),
            Column('barcode', String),
            Column('artikelomschrijving', String),
            Column('artikelprijs', Float),
            Column('art_voorraad', Float))
        balieverkoop = Table('balieverkoop', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('bonnummer', Integer),
            Column('artikelID', Integer),
            Column('barcode', String),
            Column('omschrijving', String),
            Column('aantal', Float),
            Column('prijs', Float),
            Column('subtotaal', Float),
            Column('subbtw', Float))
        params = Table('params', metadata,
            Column('paramID', Integer(), primary_key=True),
            Column('tarief', Float),
            Column('lock', Boolean))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selpar = select([params]).where(params.c.paramID == 103)
        rppar = con.execute(selpar).first()
        selpar1 = select([params]).where(params.c.paramID == 1)
        rppar1 = con.execute(selpar1).first()
        mbtw = rppar1[1]
        mbonnr = rppar[1]
        mklant = rppar[2]
        if mklant == False:
            updpar = update(params).where(params.c.paramID == 103).values(lock = True)
            con.execute(updpar)
        selart = select([artikelen]).where(artikelen.c.barcode == barcodenr)
        selbal = select([balieverkoop]).where(and_(balieverkoop.c.barcode == barcodenr,\
                balieverkoop.c.bonnummer == mbonnr))
        rpart = con.execute(selart).first()
        rpbal = con.execute(selbal).first()
        if rpart and rpart[4] < maantal:
            self.albl.setText('Foutmelding: '+str(int(rpart[4]))+' voorradig!')
            geefAlarm()
        elif rpart:
            martnr = rpart[0]
            momschr = rpart[2]
            momschr = momschr[:40] if len(momschr) > 40 else momschr
            mprijs = rpart[3]
            if rpbal:
                updbal = update(balieverkoop).where(and_(balieverkoop.c.barcode == barcodenr,\
                  balieverkoop.c.bonnummer == mbonnr)).values(aantal = balieverkoop.c.aantal+maantal,\
                  subtotaal = (balieverkoop.c.aantal+maantal)*mprijs,\
                  subbtw = (balieverkoop.c.aantal+maantal)*mprijs*mbtw)
                con.execute(updbal)
            else:
                midnr = (con.execute(select([func.max(balieverkoop.c.ID, type_=Integer)])).scalar()) 
                midnr += 1
                insbal = insert(balieverkoop).values(ID = midnr, bonnummer = mbonnr, artikelID = martnr,\
                  barcode = barcodenr, omschrijving = momschr, aantal = maantal, prijs = mprijs,\
                  subtotaal = maantal*mprijs, subbtw = maantal*mprijs*mbtw)
                con.execute(insbal)
                
            updart = update(artikelen).where(artikelen.c.artikelID == rpart[0])\
                .values(art_voorraad = artikelen.c.art_voorraad - float(maantal))
            con.execute(updart)
            
            self.mlist.append('{:\u2000<10d}'.format(martnr)+'{:\u2000<40s}'.format(momschr)+'\n'+'{:\u2000>6d}'\
             .format(int(maantal))+'{:\u2000>12.2f}'.format(mprijs)+'{:\u2000>12.2f}'\
             .format(float(mprijs)*float(maantal))+'{:\u2000>12.2f}'\
             .format(float(mprijs)*float(maantal)*mbtw))
            self.mtotaal += float(mprijs)*float(maantal)
            self.mtotbtw += float(mprijs)*float(maantal)*mbtw
            self.qtailtext = 'Totaal incl. BTW  '+'{:\u2000>12.2f}'.format(self.mtotaal)+'{:\u2000>12.2f}'.format(self.mtotbtw)+' BTW'
            self.qtailEdit.setText(self.qtailtext)
            
            self.view.append(self.mlist[-1])
        else:
            self.albl.setText('Foutmelding: Artikel niet in assortiment!')
            geefAlarm()
                  
        self.closeBtn.setDisabled(True)
        self.closeBtn.setStyleSheet("color: grey; background-color: gainsboro")
        self.printBtn.setEnabled(True)
        self.printBtn.setStyleSheet("color: black; background-color: gainsboro")
        self.nextBtn.setEnabled(True)
        self.nextBtn.setStyleSheet("font: 12pt Arial; color: black; background-color: gainsboro")
    else:
        #alarm if barcode scan failed
        self.albl.setText('Foutmelding: Scanfout barcode!')
        geefAlarm()
    
    self.q1Edit.setSelection(0,13)
    self.qspin.setValue(1)
      
def barcodeScan(m_email, mret):
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Balieverkoop")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            
            self.q1Edit = QLineEdit('')
            self.q1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.q1Edit.setFont(QFont("Arial", 12))
            self.q1Edit.setFixedSize(155, 30)
            self.q1Edit.setFocus(True)
            reg_ex = QRegExp("^[0-9]{13}$")
            input_validator = QRegExpValidator(reg_ex, self.q1Edit)
            self.q1Edit.setValidator(input_validator)
            self.q1Edit.returnPressed.connect(lambda: set_barcodenr(self))
                       
            self.qspin = QSpinBox()
            self.qspin.setRange(1, 99)
            self.qspin.setValue(1)
            self.qspin.setFocusPolicy(Qt.NoFocus)
            self.qspin.lineEdit().setReadOnly(True)
            self.qspin.setFrame(True)
            self.qspin.setFont(QFont('Arial', 12))
            self.qspin.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.qspin.setFixedSize(60, 30)
             
            def valuechange():
                self.qspin.setValue(self.qspin.value())
            self.qspin.valueChanged.connect(valuechange)
            
            grid = QGridLayout()
            grid.setSpacing(10)
          
            koplbl = QLabel('Pandora kassasysteem')
            koplbl.setStyleSheet("color:rgba(45, 83, 115, 255); font: 30pt Comic Sans MS")
            grid.addWidget(koplbl, 1, 0, 1, 3, Qt.AlignCenter)
            
            mkop = QTextEdit()
            mkoptext = 'Artikelnr Omschrijving\nAantal       Prijs   Subtotaal         BTW'
            mkop.setText(mkoptext)
            mkop.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            mkop.setReadOnly(True)
            mkop.setFont(QFont("Consolas", 12, 75))
            mkop.setStyleSheet("color: black; background-color: #F8F7EE")  
            mkop.setFocusPolicy(Qt.NoFocus)
            mkop.setFixedSize(600, 55)  
            
            self.view = QTextEdit()
            self.view.setStyleSheet('color: black; background-color: #F8F7EE')  
            self.mlist = []
            self.view.setText('')
            self.view.setFont(QFont("Consolas", 12, 75))
            self.view.setFocusPolicy(Qt.NoFocus)
            self.view.setFixedSize(600, 335)  
            
            self.mtotaal = 0.00
            self.mtotbtw = 0.00
            self.qtailEdit = QLineEdit()
            self.qtailEdit.setFont(QFont("Consolas", 12, 75))
            self.qtailEdit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.qtailEdit.setReadOnly(True)
            self.qtailEdit.setFixedWidth(600)
            self.qtailEdit.setFocusPolicy(Qt.NoFocus)
            self.qtailtext = 'Totaal incl. BTW  '+'{:\u2000>12.2f}'.format(self.mtotaal)+'{:\u2000>12.2f}'.format(self.mtotbtw)+' BTW'
            self.qtailEdit.setText(self.qtailtext)
            
            grid .addWidget(mkop, 2, 0, 1, 3, Qt.AlignCenter)           
            grid.addWidget(self.view, 3 ,0, 1, 3, Qt.AlignCenter)
            grid.addWidget(self.qtailEdit, 4, 0, 1, 3, Qt.AlignCenter)
            
            self.albl = QLabel('')
            self.albl.setStyleSheet("font: bold 18px; color: red")
            grid.addWidget(self.albl, 5, 0, 1, 3, Qt.AlignCenter)

            lbl1 = QLabel('Barcodescan')
            lbl1.setFont(QFont("Arial", 12))
            grid.addWidget(lbl1, 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q1Edit , 7, 2, 1, 1, Qt.AlignRight)
            
            lbl2 = QLabel('Aantal      ')
            lbl2.setFont(QFont("Arial", 12))
            grid.addWidget(lbl2, 8, 2, 1, 1, Qt.AlignCenter)
            grid.addWidget(self.qspin, 8, 2, 1, 1, Qt.AlignRight)
            
            if mret:
                self.plusminBtn = QPushButton('+')
                self.plusminBtn.setCheckable(True)
                self.plusminBtn.clicked.connect(lambda: plusminChange(self))
          
                grid.addWidget(self.plusminBtn, 8, 2)
                self.plusminBtn.setFocusPolicy(Qt.NoFocus)
                self.plusminBtn.setFixedSize(20, 30)
                self.plusminBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                   
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            lbl3 = QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 11, 0, 1, 3, Qt.AlignCenter)
            
            self.printBtn = QPushButton('Printen')
            self.printBtn.clicked.connect(lambda: printBon(self))
      
            grid.addWidget(self.printBtn, 10, 2, 1, 1, Qt.AlignRight)
            self.printBtn.setFont(QFont("Arial",12))
            self.printBtn.setFocusPolicy(Qt.NoFocus)
            self.printBtn.setFixedWidth(100)
            self.printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                   
            self.closeBtn = QPushButton('Sluiten')
            self.closeBtn.clicked.connect(lambda: windowSluit(self, m_email))

            grid.addWidget(self.closeBtn, 10, 1, 1, 2, Qt.AlignCenter)
            self.closeBtn.setFont(QFont("Arial",12))
            self.closeBtn.setFocusPolicy(Qt.NoFocus)
            self.closeBtn.setFixedWidth(100)
            self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")
                                   
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
    
            grid.addWidget(infoBtn, 10, 1)
            infoBtn.setFont(QFont("Arial",12))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.nextBtn = QPushButton('Volgende Klant')
            self.nextBtn.clicked.connect(lambda: nextClient(self))
    
            grid.addWidget(self.nextBtn, 8, 1, 2, 1, Qt.AlignCenter)   
            self.nextBtn.setFont(QFont("Arial",12))
            self.nextBtn.setFocusPolicy(Qt.NoFocus)
            self.nextBtn.setFixedSize(160, 60)            
            self.nextBtn.setStyleSheet("color:black; background-color: gainsboro")
            
            kassa = QLabel()
            pixmap = QPixmap('./images/logos/kassa.png')
            kassa.setPixmap(pixmap.scaled(150, 150))
            grid.addWidget(kassa, 7, 0, 4, 1, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(600, 100, 600, 300)

    window = widget()
    window.exec_()
    hoofdMenu(m_email)