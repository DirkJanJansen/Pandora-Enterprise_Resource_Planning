from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel,\
            QPushButton, QComboBox, QCheckBox, QMessageBox
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        ForeignKey, Float, select, update, insert, func, and_, Boolean)

def _11check(mcontr):
    try:
        number = str(mcontr)
        total = 0
        fullnumber = number
        for i in range(8):
            total += int(fullnumber[i])*(9-i)
            checkdigit = total %11 %10
        if checkdigit == int(fullnumber[8]):
            return True
    except:
        return False

def Alert(e):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Fout melding '+str(e))
    msg.setWindowTitle('Fout melding')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatiie ERP Systeem Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Boeking uren Materieel')
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
            
            infolbl = QLabel(
      '''
        \t\t\t\t\t\t\t\t\t\t 
                                        Informatie over mutaties materieel uurverbruik.  
         De module start met de volgende variabele gegevens: 
        Materieel nummer: Menu om het gewenste materieel te kiezen. 
        Werk nummer: legg veld om het werknummer in te vullen, waarvoor het werk wordt uitgevoerd. 
        Aantal uren: Materieel uren die de dag van het werk zijn uitgevoerd.
        Het label voor de gemaakte totaal uren verwijzen naar de materieel naam,
        waarvoor de gemaakte materieeluren worden geboekt. 
        Datum werkzaamheden:  datum van de huidige dag in het formaat jjjj-mm-dd
        Button 'Muteren' Standaard button met tekst 'Muteren' 
        Bij het aanpassen of invullen van de velden 'Service nummer', 'Werk nummer' en 'Uitvoeringsdatum',
        zal het systeem bij opkomen van de velden de laatst ingetoetste gegevens onthouden, 
        zodat een snelle invoer mogelijk is.
         
        Bij het intoetsen van de gegevens zal  bij een juiste invoer de knop
        'Muteren' groen kleuren. Bij een foutieve of niet gelukte invoer zal de 
        knop 'Muteren' rood kleuren, in dit geval dient een korrektie te worden 
        gemaakt, omdat de invoer niet is geboekt!
        In het statusveld onder de invulvelden, wordt de status en informatie
        van de foutmeldingen getoond.
        
        In het gevaL dat een fatale fout optreedt (gecombineerde wijzigingen en invoeg akties) ,
        wordt een rollback uitgevoerd, zodat de consistentie van de database wordt gewaarborgd.           
                
                                     
    ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()

def urenBoeking(self, m_email):
    mserviceidx = self.k0Edit.currentIndex()
    mservicenr = mserviceidx+1
    mwerknr = self.zkwerknEdit.text()
    m_uren = float(self.urenEdit.text())
    mboekd = self.boekdatumEdit.text()
    mstatus = self.cBox.checkState()
    if self.urenEdit.text() == '0':
        self.lblt.setStyleSheet("font: bold ; color: red")
        self.lblt.setText('No hours entered!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return (mservicenr, '', mboekd, m_email)
    if mstatus == 0:
        mstatus = False
    else:
        mstatus = True

    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('voortgangstatus', String),
        Column('statusweek', String(6)),
        Column('aanneemsom', Float),
        Column('kosten_totaal', Float),
        Column('begr_materieel', Float),
        Column('kosten_materieel', Float),
        Column('werk_sleuvengraver_uren', Float),
        Column('werk_persapparaat_uren', Float),
        Column('werk_atlaskraan_uren', Float),
        Column('werk_kraan_groot_uren', Float),
        Column('werk_mainliner_uren', Float),
        Column('werk_hormachine_uren', Float),
        Column('werk_wagon_uren', Float),
        Column('werk_locomotor_uren', Float),
        Column('werk_locomotief_uren', Float),
        Column('werk_montagewagen_uren', Float),
        Column('werk_stormobiel_uren', Float),
        Column('werk_robeltrein_uren', Float),
        Column('begr_sleuvengraver_uren', Float),
        Column('begr_persapparaat_uren', Float),
        Column('begr_atlaskraan_uren', Float),
        Column('begr_kraan_groot_uren', Float),
        Column('begr_mainliner_uren', Float),
        Column('begr_hormachine_uren', Float),
        Column('begr_wagon_uren', Float),
        Column('begr_locomotor_uren', Float),
        Column('begr_locomotief_uren', Float),
        Column('begr_montagewagen_uren', Float),
        Column('begr_stormobiel_uren', Float),
        Column('begr_robeltrein_uren', Float),
        Column('meerminderwerk', Float))
    materieelmutaties = Table('materieelmutaties', metadata,
        Column('mutatieID', Integer(), primary_key=True),
        Column('servicesID', None, ForeignKey('params_services.servicesID')),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('order_inkoop_materieelID',None, ForeignKey('order_inkoop_materieel.order_inkoop_materieelID')),
        Column('uren_opdracht', Float),
        Column('uren_geboekt', Float),
        Column('boekbedrag', Float),
        Column('boekdatum', String),
        Column('meerwerkstatus', Boolean),
        Column('leverancierID',None, ForeignKey('leveranciers.leverancierID')),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')))
    orders_inkoop_materieel = Table('orders_inkoop_materieel', metadata,
        Column('order_inkoop_materieelID', Integer, primary_key=True),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('servicesID', None,ForeignKey('params_services.servicesID')),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')))
    params_services = Table('params_services', metadata,
        Column('servicesID', Integer(), primary_key=True),
        Column('hourly_tariff', Float),
        Column('overhead_factor', Float),
        Column('item', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selserv = select([params_services]).where(params_services.c.servicesID == mservicenr)
    rpserv = con.execute(selserv).first()

    if _11check(mwerknr):
        selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
        rpwerk = con.execute(selwerk).first()
    else:
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold ; color: red")
        self.lblt.setText('Dit is geen bestaand werknummer!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return (mservicenr, '', mboekd, m_email)

    try:
        selink = select([orders_inkoop_materieel]).where(and_(orders_inkoop_materieel.c.werknummerID==werken.c.werknummerID, \
            orders_inkoop_materieel.c.werknummerID ==mwerknr, orders_inkoop_materieel.c.servicesID==params_services.c.servicesID,
            orders_inkoop_materieel.c.servicesID==mservicenr))
        rpink = con.execute(selink).first()
        mlevnr = rpink[3]
        mordnr = rpink[0]
        m_inkorder = rpink[4]
    except:
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold ; color: red")
        self.lblt.setText('Geen order voor dit materieel gevonden\nMaak eerst een bestelling!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return (1, mwerknr, mboekd, m_email)

    mlist = ['Sleuvengraver','Persmachine','Atlaskraan','Kraan groot','Mainliner','Hormachine',\
             'Wagon','Locomotor','Locomotief','Montagewagen','Stormobiel','Robeltrein']

    transaction = con.begin()
    try:
        mutnr = (con.execute(select([func.max(materieelmutaties.c.mutatieID, type_=Integer)])).scalar())
        mutnr += 1
    except:
        mutnr = 1

    try:
        insmut = insert(materieelmutaties).values(mutatieID=mutnr,servicesID=mservicenr,werknummerID=mwerknr,uren_geboekt=m_uren,\
            boekbedrag=m_uren*rpserv[1]*rpserv[2], meerwerkstatus = mstatus, leverancierID = mlevnr,order_inkoop_materieelID=mordnr,
            orderinkoopID = m_inkorder)
        con.execute(insmut)
    except:
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold ; color: red")
        self.lblt.setText('Een fout trad op met muteren van gegevens!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return 1, mwerknr, mboekd, m_email
       
    try:
        if rpwerk[2] == 'H':
            self.urenEdit.setText('0')
            self.lblt.setStyleSheet("font: bold ; color: red")
            self.lblt.setText('Dit werk is gereed en afgesloten!')
            self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            return mservicenr, mwerknr, mboekd, m_email
        if mstatus:
            mmwerk=m_uren*rpserv[1]*rpserv[2]
        else:
            mmwerk=0
        if mservicenr == 1:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_sleuvengraver_uren =\
                     werken.c.werk_sleuvengraver_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 2:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_persapparaat_uren =\
                     werken.c.werk_persapparaat_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 3:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_atlaskraan_uren =\
                     werken.c.werk_atlaskraan_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 4:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_kraan_groot_uren =\
                     werken.c.werk_kraan_groot_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 5:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_mainliner_uren =\
                     werken.c.werk_mainliner_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 6:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_hormachine_uren =\
                     werken.c.werk_hormachine_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 7:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_wagon_uren =\
                     werken.c.werk_wagon_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 8:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_locomotor_uren =\
                     werken.c.werk_locomotor_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 9:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_locomotief_uren =\
                     werken.c.werk_locomotief_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 10:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_montagewagen_uren=\
                     werken.c.werk_montagewagen_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 11:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_stormobiel_uren=\
                     werken.c.werk_stormobiel_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        elif mservicenr == 12:
            updwerk = update(werken).where(werken.c.werknummerID==mwerknr).values(werk_robeltrein_uren =\
                     werken.c.werk_robeltrein_uren + m_uren, kosten_materieel = werken.c.kosten_materieel+\
                     m_uren*rpserv[1]*rpserv[2], kosten_totaal = werken.c.kosten_totaal+m_uren*rpserv[1]*rpserv[2],\
                     meerminderwerk = werken.c.meerminderwerk+mmwerk)
            con.execute(updwerk)
        transaction.commit()

        selwerk = select([werken]).where(werken.c.werknummerID ==mwerknr)
        rpwerk = con.execute(selwerk).first()
        if int(rpwerk[rpserv[0] + 18]) == 0:
            self.urenEdit.setText('0')
            self.lblt.setStyleSheet("font: bold;color: red")
            self.lblt.setText('Geen begrote uren voor dit materieel!')
            self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            return mservicenr, mwerknr, mboekd, m_email
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpwerk[rpserv[0] + 18]))
        self.urenwerkEdit.setText('{:<12.2f}'.format(rpwerk[rpserv[0] + 6]))
        lblptext = 'Totalen: Gerealiseerde / Begrote\nUren '+mlist[mserviceidx]
        lbltext = 'Mutaties uren (Mutaie uren (werk - bedragen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
        self.applyBtn.setStyleSheet("color: black; background-color: #00CC66")
        return mservicenr, mwerknr, mboekd, m_email
    except Exception as e:
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold;color: red")
        transaction.rollback()
        self.lblt.setText('Door een fout, is een rollback uitgevoerd\nde transaktie is niet uitgevoerd!')
        print(str(e))
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return mservicenr, mwerknr, mboekd, m_email

def urenMut(mservicenr, mwerknr, mboekd, m_email):
    class Widget(QDialog):
        def __init__(self):
            super(Widget,self).__init__()
            
            self.setWindowTitle("Inbreng uren voor externe werken - bedragen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))

            self.zkwerknEdit = QLineEdit(str(mwerknr))
            self.zkwerknEdit.setFixedWidth(150)
            self.zkwerknEdit.setFont(QFont("Arial",10))
            self.zkwerknEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[8]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, self.zkwerknEdit)
            self.zkwerknEdit.setValidator(input_validator)

            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(150)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.setMaxVisibleItems(12)
            self.k0Edit.setCurrentIndex(mservicenr)
            self.k0Edit.addItem('Sleuvengraver')
            self.k0Edit.addItem('Persmachine')
            self.k0Edit.addItem('Atlaskraan')
            self.k0Edit.addItem('Kraan groot')
            self.k0Edit.addItem('Mainliner')
            self.k0Edit.addItem('Hormachine')
            self.k0Edit.addItem('Wagon')
            self.k0Edit.addItem('Locomotor')
            self.k0Edit.addItem('Locomotief')
            self.k0Edit.addItem('Montagewagen')
            self.k0Edit.addItem('Stormobiel')
            self.k0Edit.addItem('Robeltrein')
  
            self.cBox = QCheckBox('Meer/minder werk')
            self.cBox.setFont(QFont("Arial",10))
            self.cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                                                                     
            self.urenEdit = QLineEdit('0')
            self.urenEdit.setFixedWidth(150)
            self.urenEdit.setFont(QFont("Arial",10))
            self.urenEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.urenEdit)
            self.urenEdit.setValidator(input_validator)
            
            self.urenwerkEdit = QLineEdit('0')
            self.urenwerkEdit.setFixedWidth(150)
            self.urenwerkEdit.setDisabled(True)
            self.urenwerkEdit.setFont(QFont("Arial",10))
            self.urenwerkEdit.setStyleSheet("color: black")
    
            self.urenbegrEdit = QLineEdit('0')
            self.urenbegrEdit.setFixedWidth(150)
            self.urenbegrEdit.setDisabled(True)
            self.urenbegrEdit.setFont(QFont("Arial",10))
            self.urenbegrEdit.setStyleSheet("color: black")        
                                                         
            self.boekdatumEdit = QLineEdit(mboekd)
            self.boekdatumEdit.setFixedWidth(150)
            self.boekdatumEdit.setFont(QFont("Arial",10))
            self.boekdatumEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[2]{1}[0-1]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, self.boekdatumEdit)
            self.boekdatumEdit.setValidator(input_validator)

            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)

            def werknChanged():
                self.zkwerknEdit.setText(self.zkwerknEdit.text())
            self.zkwerknEdit.textChanged.connect(werknChanged)
             
            '''
            # QCombobox connect both index and text with this function
            def k0Changed():
                self.k0Edit.setCurrentText(self.k0Edit.currentText())
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.activated.connect(k0Changed)
            # catch changed text with:
            # text = self.k0Edit.currentText()
            # catch changed index with:
            # index = (self.k0Edit.currentIndex()
            '''

            def cboxChanged():
                self.cBox.setCheckState(self.cBox.checkState())
            self.cBox.stateChanged.connect(cboxChanged)
            
            def urenChanged():
                self.urenEdit.setText(self.urenEdit.text())
            self.urenEdit.textChanged.connect(urenChanged)
            
            def boekdatumChanged():
                self.boekdatumEdit.setText(self.boekdatumEdit.text())
            self.boekdatumEdit.textChanged.connect(boekdatumChanged)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0 , 1)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)       

            self.lblt = QLabel('Muteren uren (werk - bedragen) niet cumulatief')
            self.lblt.setStyleSheet("color: black")
            self.lblt.setFont(QFont("Arial", 10))
            grid.addWidget(self.lblt , 12, 0, 1, 4, Qt.AlignCenter)

            lbl2 = QLabel('Werknummer')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkwerknEdit, 7, 2, 1, 1, Qt.AlignRight)
                
            lbl3 = QLabel('Type uren')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 8, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.k0Edit, 8, 2, 1, 1, Qt.AlignRight)
                        
            grid.addWidget(self.cBox, 8, 3)
            
            self.lblprof = QLabel('Totalen: Werkelijk / Begroot\nUren')
            self.lblprof.setFont(QFont("Arial", 10))
            self.lblprof.setFixedWidth(200)
            self.lblprof.setAlignment(Qt.AlignRight)
            grid.addWidget(self.lblprof, 9, 1, 1, 1, Qt.AlignRight | Qt.AlignTop)
            grid.addWidget(self.urenwerkEdit, 9, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenbegrEdit, 9, 3, 1, 1)
            
            lbl4 = QLabel('Muteren  uren')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenEdit, 10, 2, 1, 1, Qt.AlignRight)

            lbl5 = QLabel('Boekdatum')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 11, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.boekdatumEdit, 11, 2, 1, 1, Qt.AlignRight)
            
            self.applyBtn = QPushButton('Mutatie')
            self.applyBtn.clicked.connect(lambda: urenBoeking(self, m_email))
               
            self.applyBtn.setFont(QFont("Arial",10))
            self.applyBtn.setFixedWidth(100)
            self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(self.applyBtn,13, 3 , 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Sluit')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 13, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
                   
            infoBtn = QPushButton('Info')
            infoBtn.clicked.connect(lambda: info()) 
    
            grid.addWidget(infoBtn, 13, 1, 1, 1, Qt.AlignRight)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
            rightslbl = QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl')
            rightslbl.setFont(QFont("Arial", 10))
            grid.addWidget(rightslbl, 14, 1, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
                
    window = Widget()
    window.exec_()  