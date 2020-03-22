from login import hoofdMenu
from datetime import datetime
from sys import platform
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QTextEdit
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                         create_engine, Float, select, update,insert, func, and_, Boolean)

def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Er zijn nog geen transacties!')
    msg.setWindowTitle('Transacties')
    msg.exec_() 
       
def foutArtikel():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Dit artikel wordt niet in ons assortiment gevoerd!')
    msg.setWindowTitle('Melding voorraad')
    msg.exec_() 
    
def onvVoorraad(magvrd):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Er is onvoldoende voorraad voor deze bestelhoeveelheid\nNog '+str(int(magvrd))+' voorradig!')
    msg.setWindowTitle('Melding voorraad')
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
            
            infolbl = QLabel('''
        \t\t\t\t\t\t\t\t\t\t
       \t\t Enterprise Resource Planning (ERP) systeem Pandora
        
        Instruktie barcode scannen.
        
        Als testscanner is een hand laserscanner gebruikt van het type Nedis BCRLR100BK
        De produkten kunnen gescand worden tot een afstand van 55cm.
        Standaard wordt gescand met een hoeveelheid van 1.
        Indien meerdere produkten van het zelfde artikelnummer benodigd zijn, kan d.m.v. de 
        spinbox het juiste aantal worden gekozen voor het scannen. 
        Dit kan met de pijltjes van de spinbox of met het muiswieltje.
        Na het scannen wordt het aantal weer automatisch teruggezet op 1.
        Als een scanfout optreedt bij het scannen, dan klinkt een akoestisch alarm.
        Als het scannen wordt gestart voor een klant wordt de sluitknop geblokkeerd tot de
        knop volgende klant wordt gedrukt. De printknop en de klantknop worden geblokkeerd
        tot de eerste transactie is geboekt.
        Als een fout bij het scannen optreedt door een leesfout van de barcode klinkt een alarm.
        Indien er te weinig voorraad is om de bestelling uit te voeren wordt een popupvenster
        getoond met de huidige voorraad.
        Eveneens een popupvenster wordt getoond als  produkt niet leverbaar is, omdat dit niet
        in het assortiment is opgenomen.
        
        Als de popupvensters niet met muisklikken of return, maar met scannen worden verwijderd,
        dient het scannen van de laatste handeling opnieuw te worden uitgevoerd, omdat het 
        produkt niet is ingevoerd, maar alleen het popupvenster met scannen is verdwenen.
        
        Nadat het scannen gereed is kan de printbon worden uitgeprint.
                
        Voor het programma wordt afgesloten, dient eerst de klantknop te worden ingedrukt,
        voor de sluitknop wordt vrijgegeven. Hiermee worden de noodzakelijke boekingen
        uitgevoerd en de order voor de volgende klant voorbereid.
       
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
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Webverkooporders printen')
    msg.exec_()

def printBon():
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Printen orderbon")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Wilt de orderbon printen?");
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
        selb = select([balieverkoop]).where(balieverkoop.c.bonnummer == mbonnr).order_by(balieverkoop.c.barcode)
        rpb = con.execute(selb)
        kop=\
        ('Balieverkoop - Ordernummer: '+ str(mbonnr)+' Datum: '+str(datetime.now())[0:10]+'\n'+
        '==============================================================================================\n'+
        'Artikelnr  Omschrijving                             Aantal       Prijs   Subtotaal     BTW 21%\n'+
        '==============================================================================================\n')
        if platform == 'win32':
            fbarc = '.\\forms\\Barcodelijsten\\'+str(mbonnr)+'.txt'
        else:
            fbarc = './forms//Barcodelijsten/'+str(mbonnr)+'.txt'
        open(fbarc, 'w').write(kop)
        mcumtot = 0
        mcumbtw = 0
        for row in rpb:
            martnr = row[2]
            momschr = row[4]
            maantal = row[5]
            mprijs = row[6]
            mtotaal = row[7]
            mtotbtw = row[8]
            open(fbarc,'a').write(str(martnr) +'  '+'{:<40s}'.format(momschr)+' '+'{:>6d}'\
                 .format(int(maantal))+'{:>12.2f}'.format(float(mprijs))+'{:>12.2f}'\
                 .format(float(mtotaal))+'{:>12.2f}'\
                 .format(float(mtotbtw))+'\n')
            mcumtot = mcumtot+mtotaal
            mcumbtw = mcumbtw+mtotbtw
        tail=\
        ('==============================================================================================\n'+
        'Totaal bedrag af te rekenen inclusief BTW  en bedrag BTW 21%          '+'{:>12.2f}'.format(mcumtot)+'{:>12.2f}'.format(mcumbtw)+' \n'+
        '==============================================================================================\n')
        open(fbarc,'a').write(tail)    
        if platform == 'win32':
            from os import startfile
            startfile(fbarc, "print")
        else:
            from os import system
            system("lpr "+fbarc)
        printing()
        
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def nextClient(nextBtn, closeBtn, printBtn):
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
    selb = select([balieverkoop]).where(balieverkoop.c.bonnummer == mbonnr)\
       .order_by(balieverkoop.c.barcode)
    rpb = con.execute(selb)
    mtotbtw = 0  
    for row in rpb:
        mtotbtw = mtotbtw + row[8]
        mmutnr = con.execute(select([func.max(artikelmutaties.c.mutatieID, type_=Integer)])).scalar()
        mmutnr += 1
        insmut = insert(artikelmutaties).values(mutatieID = mmutnr, artikelID = row[2],\
                hoeveelheid = row[5], boekdatum = mboekd, baliebonID = mbonnr,\
                tot_mag_prijs = row[7], btw_hoog = row[8])
        con.execute(insmut)
    if mtotbtw != int(0):
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
             soort = 'BTW afdracht 21%', bedrag = mtotbtw, instantie = 'Belastingdienst',\
             ovbestelID = int(mbonnr), rekeningnummer= 'NL10 ABNA 9999999977')
        con.execute(insdr)
        closeBtn.setEnabled(True)
        printBtn.setDisabled(True)
        nextBtn.setDisabled(True)
    else:
        geenGegevens()
    updpar = update(params).where(params.c.paramID == 103).values(tarief = mbonnr+1, lock = True)
    con.execute(updpar)
        
def set_barcodenr(q1Edit, text, qspin, view, tekst, nextBtn, closeBtn, printBtn):
    barcodenr = q1Edit.text()
    maantal = qspin.value()
    koptekst = tekst
    if len(barcodenr) == 13 :
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
        mbonnr = rppar[1]
        mklant = rppar[2]
        if mklant == False:
            mbonnr += 1
            mklant = True
            updpar = update(params).where(params.c.paramID == 103).values(tarief = mbonnr, lock = True)
            con.execute(updpar)
        selpar1 = select([params]).where(params.c.paramID == 1)
        rppar1 = con.execute(selpar1).first()
        mbtw = rppar1[1]
        selart = select([artikelen]).where(artikelen.c.barcode == barcodenr)
        selbal = select([balieverkoop]).where(and_(balieverkoop.c.barcode == barcodenr,\
                balieverkoop.c.bonnummer == mbonnr))
        rpart = con.execute(selart).first()
        rpbal = con.execute(selbal).first()
        if rpart and rpart[4] < maantal:
             onvVoorraad(rpart[4])
        elif rpart:
            martnr = rpart[0]
            momschr = rpart[2]
            mprijs = rpart[3]
            if rpbal:
                updbal = update(balieverkoop).where(and_(balieverkoop.c.barcode == barcodenr,\
                  balieverkoop.c.bonnummer == mbonnr)).values(aantal = balieverkoop.c.aantal+maantal,\
                  subtotaal = balieverkoop.c.aantal+maantal*mprijs,\
                  subbtw = balieverkoop.c.aantal+maantal*mprijs*mbtw)
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
                
            newtekst = koptekst+(str(martnr) +'  '+'{:<40s}'.format(momschr)+'\n'+'{:>6d}'\
             .format(int(maantal))+'{:>12.2f}'.format(mprijs)+'{:>12.2f}'\
             .format(float(mprijs)*float(maantal))+'{:>12.2f}'\
             .format(float(mprijs)*float(maantal)*mbtw)+'\n')
            view.setText(newtekst)
        else:
             foutArtikel()
      
        closeBtn.setDisabled(True)
        printBtn.setEnabled(True)
        nextBtn.setEnabled(True)
    else:
        #alarm if barcode scan failed
        if platform == 'win32':
            import winsound
            winsound.Beep(1000,200)
            winsound.Beep(2000,400)
            winsound.Beep(800,300)
        else:
            #sudo apt install sox
            from os import system
            system('play -nq -t alsa synth {} sine {}'.format(0.2, 1000))
            system('play -nq -t alsa synth {} sine {}'.format(0.4, 2000))
            system('play -nq -t alsa synth {} sine {}'.format(0.3, 800))
        
    q1Edit.setSelection(0,13)
    qspin.setValue(1)
      
def barcodeScan(m_email):
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Balieverkoop")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
            
            text = ''
            q1Edit = QLineEdit(text)
            q1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            q1Edit.setFont(QFont("Arial", 10))
            q1Edit.setFixedWidth(130)
            q1Edit.setFocus(True)
            q1Edit.returnPressed.connect(lambda: set_barcodenr(q1Edit, text, qspin, view, tekst, nextBtn, closeBtn, printBtn))
                       
            qspin = QSpinBox()
            qspin.setRange(1, 99)
            qspin.setFocusPolicy(Qt.NoFocus)
            qspin.lineEdit().setReadOnly(True)
            qspin.setFrame(True)
            qspin.setFont(QFont('Arial', 10))
            qspin.setStyleSheet("color: black;  background-color: #F8F7EE")
            qspin.setValue(1)
            qspin.setFixedSize(40, 30)
            
            def valuechange():
                qspin.setValue(qspin.value())
            qspin.valueChanged.connect(valuechange)

            grid = QGridLayout()
            grid.setSpacing(10)
          
            view = QTextEdit()
            view.setDisabled(True)
            view.setStyleSheet('color: black; background-color: #F8F7EE')
            tekst = 'Artikelnr       Omschrijving\nAantal    Prijs  Subtotaal       BTW\n\n'
            view.setText(tekst)
            view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            view.setFont(QFont("Arial", 9))
            view.setFocusPolicy(Qt.NoFocus)
            view.setFixedSize(350, 100)
                        
            grid.addWidget(view, 0 ,0, 1, 4, Qt.AlignCenter)
      
            lbl1 = QLabel('Barcodescan')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 4, 1)
            grid.addWidget(q1Edit , 4, 2, 1, 1, Qt.AlignRight)
            
            lbl2 = QLabel('Aantal    ')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 5, 2, 1, 1, Qt.AlignCenter)
            grid.addWidget(qspin, 5, 2, 1, 1, Qt.AlignRight)
                                   
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 2, 0, 1, 2)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 2, 2, 1 ,1, Qt.AlignRight)
            lbl3 = QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 8, 0, 1, 3, Qt.AlignCenter)
  
            printBtn = QPushButton('Printen')
            printBtn.clicked.connect(lambda: printBon())
      
            grid.addWidget(printBtn, 7, 2, 1, 1, Qt.AlignRight)
            printBtn.setFont(QFont("Arial",10))
            printBtn.setFocusPolicy(Qt.NoFocus)
            printBtn.setFixedWidth(100)
            printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                   
            closeBtn = QPushButton('Sluiten')
            closeBtn.clicked.connect(lambda: windowSluit(self, m_email))

            grid.addWidget(closeBtn, 7, 1, 1, 1, Qt.AlignRight)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFocusPolicy(Qt.NoFocus)
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
    
            grid.addWidget(infoBtn, 7, 0, 1, 1, Qt.AlignRight)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
            nextBtn = QPushButton('Volgende Klant')
            nextBtn.clicked.connect(lambda: nextClient(nextBtn, closeBtn, printBtn))
    
            grid.addWidget(nextBtn, 5, 0, 1, 2)   
            nextBtn.setFont(QFont("Arial",10))
            nextBtn.setFocusPolicy(Qt.NoFocus)
            nextBtn.setFixedWidth(210)            
            nextBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                     
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)

    window = widget()
    window.exec_()
    hoofdMenu(m_email)