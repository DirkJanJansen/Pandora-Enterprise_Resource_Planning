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
    msg.setText('Error report '+str(e))
    msg.setWindowTitle('Error report')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information ERP System Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Booking hours equipment')
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
                                        Information about equipment hours to mutate.  
        The module starts with the following variable data: 
        Service number: Pull down menu to choose the desired equipment number. 
        Work number: empty field to be filled in with the work number, for which work is being done. 
        Number of hours: Hours equipment used on the day of work.
        The label for the actual total hours indicates the equipment name,
        for which the equipment used hours are booked. 
        Date of work: date of the current day in the format yyyy-mm-dd 
        Button 'Mutate' Standard button with text 'Mutate' 
        When modifying or choosing the 'Services number', or fill in the fields 'Work number' and 'Date of work',
        the system will remember the last keyed data and the position of the pull down menu when the fields arise,
        so that a quick entry is possible. 
       
        When entering the data, if entered correctly, the button 'Mutate' turn green.
        In the event of an incorrect or unsuccessful entry, the button 'Mutate' turn red,
        in this case a correction should be created, because the entry was not booked!
        In the status field below the input fields, error messages are displayed.
                 
        In case an fatal error occurred (combined update and insert actions),
        a rollback is established, so consistency of the database is assured.
        
                                     
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
        Column('order_inkoop_materieelID',None, ForeignKey('orders_inkoop_materieel.order_inkoop_materieelID')),
        Column('uren_geboekt', Float),
        Column('boekbedrag', Float),
        Column('boekdatum', String),
        Column('meerwerkstatus', Boolean),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
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
        self.lblt.setText('This is not an existing worknumber!')
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
        self.lblt.setText('Order for this equipment is not found\nFirst order for this equipment!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return (1, mwerknr, mboekd, m_email)

    mlist = ['Trench machine','Pressing machine','Atlas crane','Crane big','Mainliner','Ballast scraper',\
             'Wagon','Loco motor','Locomotive','Assemble Trolley','Stormobile','Robel train']

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
        self.lblt.setText('An error has occured with insert mutations!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return 1, mwerknr, mboekd, m_email

    try:
        if rpwerk[2] == 'H':
            self.urenEdit.setText('0')
            self.lblt.setStyleSheet("font: bold ; color: red")
            self.lblt.setText('Work is ready and logged out!')
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
            self.lblt.setText('No calculated hours for this equipment!')
            self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            return mservicenr, mwerknr, mboekd, m_email
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpwerk[rpserv[0] + 18]))
        self.urenwerkEdit.setText('{:<12.2f}'.format(rpwerk[rpserv[0] + 6]))
        lblptext = 'Totals: Realised / Budgeted\nHours '+mlist[mserviceidx]
        lbltext = 'Mutate hours (work - wages) not cumulative'
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
        self.lblt.setText('Due to an error, a rollback was performed\nthe transactions for this input are not processed!')
        print(str(e))
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return mservicenr, mwerknr, mboekd, m_email

def urenMut(mservicenr, mwerknr, mboekd, m_email):
    class Widget(QDialog):
        def __init__(self):
            super(Widget,self).__init__()
            
            self.setWindowTitle("Entering hours of external works - wages")
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
            self.k0Edit.addItem('Trench machine')
            self.k0Edit.addItem('Pressing machine')
            self.k0Edit.addItem('Atlas crane')
            self.k0Edit.addItem('Crane big')
            self.k0Edit.addItem('Main liner')
            self.k0Edit.addItem('Ballast scraper')
            self.k0Edit.addItem('Wagon')
            self.k0Edit.addItem('Loco motor')
            self.k0Edit.addItem('Locomotive')
            self.k0Edit.addItem('Assemble Trolley')
            self.k0Edit.addItem('Stor mobile')
            self.k0Edit.addItem('Robel train')
  
            self.cBox = QCheckBox('More/less work')
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
            # index = self.k0Edit.currentIndex()
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

            self.lblt = QLabel('Mutate hours (work - wages) not cumulative')
            self.lblt.setStyleSheet("color: black")
            self.lblt.setFont(QFont("Arial", 10))
            grid.addWidget(self.lblt , 12, 0, 1, 4, Qt.AlignCenter)

            lbl2 = QLabel('Work number')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkwerknEdit, 7, 2, 1, 1, Qt.AlignRight)
                
            lbl3 = QLabel('Type of hours')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 8, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.k0Edit, 8, 2, 1, 1, Qt.AlignRight)
                        
            grid.addWidget(self.cBox, 8, 3)
            
            self.lblprof = QLabel('Totals: Realised / Budgeted\nHours')
            self.lblprof.setFont(QFont("Arial", 10))
            self.lblprof.setFixedWidth(200)
            self.lblprof.setAlignment(Qt.AlignRight)
            grid.addWidget(self.lblprof, 9, 1, 1, 1, Qt.AlignRight | Qt.AlignTop)
            grid.addWidget(self.urenwerkEdit, 9, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenbegrEdit, 9, 3, 1, 1)
            
            lbl4 = QLabel('Mutate hours')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenEdit, 10, 2, 1, 1, Qt.AlignRight)

            lbl5 = QLabel('Book date')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 11, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.boekdatumEdit, 11, 2, 1, 1, Qt.AlignRight)
            
            self.applyBtn = QPushButton('Mutate')
            self.applyBtn.clicked.connect(lambda: urenBoeking(self, m_email))
               
            self.applyBtn.setFont(QFont("Arial",10))
            self.applyBtn.setFixedWidth(100)
            self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(self.applyBtn,13, 3 , 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
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