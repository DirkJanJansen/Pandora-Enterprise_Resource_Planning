from login import hoofdMenu
from postcode import checkpostcode
import datetime
from PyQt5.QtCore import Qt, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QVBoxLayout,\
     QMessageBox, QLineEdit, QGridLayout, QDialog, QWidget,QTableView
     
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update, insert, func, and_

def art_refresh(koppelnr, m_email, self):
    self.close()
    artikelAfroep(koppelnr, m_email)
     
def raap_refresh(koppelnr, self):
    self.close()
    raapLijst(koppelnr)
 
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
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def foutWerknr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Work number not found\nWork number does not exist!')
    msg.setWindowTitle('Data!')
    msg.exec_()
        
def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Zipcode/house number combination does not exist!')
    msg.setWindowTitle('Request articles')
    msg.exec_()

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Request articles')
    msg.exec_()
    			            
def negVoorraad():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Too little stock for the transaction!')
    msg.setWindowTitle('Request articles')
    msg.exec_()
        
def foutHoev():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No changes\nimplemented!')
    msg.setWindowTitle('Request articles')
    msg.exec_()

def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Work number is unsubscribed,\nbookings no longer possible!')
    msg.setWindowTitle('Request articles')
    msg.exec_()
    
def geenRaaplijst(koppelnr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro; font: 10pt Arial")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No picking lines from work '+str(koppelnr)+' present!')
    msg.setWindowTitle('Request picklist')
    msg.exec_()
      
def zoekWerk(m_email, soort):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            if soort  == 0:
                self.setWindowTitle("Modify internal works.")
            else:
                self.setWindowTitle("Modify external works.")  
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Werknummer = QLabel()
            werknEdit = QLineEdit()
            werknEdit.setFixedWidth(100)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
            if soort == 0:
                reg_ex = QRegExp('^[7]{1}[0-9]{8}$')
            else:
                reg_ex = QRegExp('^[8]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, werknEdit)
            werknEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                                
    
            grid.addWidget(QLabel('Worknumber'), 1, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(werknEdit, 1, 1)
       
            zoekBtn = QPushButton('Search')
            zoekBtn.clicked.connect(self.accept)
                  
            grid.addWidget(zoekBtn, 2, 1)
            zoekBtn.setFont(QFont("Arial",10))
            zoekBtn.setFixedWidth(100)
            zoekBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(lambda: windowSluit(self, m_email))
                  
            grid.addWidget(sluitBtn, 2, 0, 1, 1, Qt.AlignRight)
            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
                     
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
        def werknChanged(self, text):
            self.Werknummer.setText(text)
    
        def returnwerkn(self):
            return self.Werknummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnwerkn()]
    
    window = Widget()
    data = window.getData()
    if data[0]:
        koppelnr = data[0]
    else:
        zoekWerk(m_email, soort)
        
    metadata = MetaData()

    if koppelnr[0] == '8':
        werken = Table('werken', metadata,
            Column('werknummerID', Integer(), primary_key=True),
            Column('voortgangstatus', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        s = select([werken]).where(werken.c.werknummerID == int(koppelnr))
        rp = conn.execute(s).first()
    elif koppelnr[0] == '7':
        orders_intern = Table('orders_intern', metadata,
            Column('werkorderID', Integer(), primary_key=True),
            Column('voortgangstatus', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        s =select([orders_intern]).where(orders_intern.c.werkorderID == int(koppelnr))
        rp = conn.execute(s).first()
    if not rp:
        foutWerknr()
        zoekWerk(m_email, soort)
    elif rp[1] == 'H':
        werkGereed()
        zoekWerk(m_email, soort)
    else:
        koppelnr = int(koppelnr)
        artikelAfroep(koppelnr, m_email)

def raapLijst(koppelnr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1000, 900)
            self.setWindowTitle('Request picklist')
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
            table_view.setColumnHidden(11, True)
            table_view.setColumnHidden(12, True)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(opvraagAfroep)
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
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('alternatief', String),
        Column('straat', String),
        Column('woonplaats', String))
       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
 
    header = ['ListID','Articlenumber','Workorder','Call-off','Delivery date','Delivered',\
          'More/less work','Zip code', 'Housenumber','Suffix', 'Alternative address',\
          'Street', 'Residence']
    
    selafr = select([raaplijst]).where(and_(raaplijst.c.werkorder == koppelnr,\
       raaplijst.c.afroep != 0)).order_by(raaplijst.c.werkorder, raaplijst.c.leverdatum)
    if con.execute(selafr).fetchone():
        rpafr = con.execute(selafr)
    else:
        geenRaaplijst(koppelnr)
        return
          
    data_list=[]
    for row in rpafr:
        data_list += [(row)]
       
    def opvraagAfroep(idx):
        mlijstnr = idx.data()
        if idx.column() == 0:
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
                Column('huisnummer', String),
                Column('toevoeging', String),
                Column('alternatief', String))
            if str(koppelnr)[0] == '7':
                materiaallijsten = Table('materiaallijsten', metadata,
                    Column('artikelID', Integer),
                    Column('icalculatie', Integer),
                    Column('afroep', Float),
                    Column('resterend', Float))
                icalculaties = Table('icalculaties', metadata,
                    Column('icalculatie', Integer),
                    Column('koppelnummer', Integer))
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selmc = select([raaplijst, materiaallijsten,icalculaties]).where(and_(raaplijst\
                    .c.lijstID == mlijstnr, raaplijst.c.werkorder == icalculaties.c.koppelnummer,\
                    icalculaties.c.icalculatie == materiaallijsten.c.icalculatie,\
                    raaplijst.c.artikelID == materiaallijsten.c.artikelID))
                rpmc = con.execute(selmc).first()
            elif str(koppelnr)[0] == '8':
                materiaallijsten = Table('materiaallijsten', metadata,
                    Column('artikelID', Integer),
                    Column('calculatie', Integer),
                    Column('afroep', Float),
                    Column('resterend', Float))
                calculaties = Table('calculaties', metadata,
                    Column('calculatie', Integer),
                    Column('koppelnummer', Integer))
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selmc = select([raaplijst, materiaallijsten,calculaties]).where(and_(raaplijst\
                    .c.lijstID == mlijstnr, raaplijst.c.werkorder == calculaties.c.koppelnummer,\
                    calculaties.c.calculatie == materiaallijsten.c.calculatie,\
                    raaplijst.c.artikelID == materiaallijsten.c.artikelID))
                rpmc = con.execute(selmc).first()
                  
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
    
            selrl = select([raaplijst]).where(and_(raaplijst.c.lijstID==mlijstnr,\
                          raaplijst.c.werkorder == koppelnr))
            rprl = con.execute(selrl).first()
            
            mresterend = rpmc[14]
            mmmstatus = rprl[6]
            mlever = rprl[4]
            mafroep = rprl[3]
            mgeleverd = rprl[5]
            mpostcode = rprl[7]
            mhuisnr = rprl[8]
            mtoev = rprl[9]
            maltern = rprl[10]
            if mhuisnr != '':
                mstrpl = checkpostcode(mpostcode,int(mhuisnr))
                mstraat = mstrpl[0]
                mplaats = mstrpl[1]
                  
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Requesting material call-off")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setFont(QFont('Arial', 10))
                                 
                    self.Werknummer = QLabel()
                    zkwerknEdit = QLineEdit(str(koppelnr))
                    zkwerknEdit.setAlignment(Qt.AlignRight)
                    zkwerknEdit.setFixedWidth(100)
                    zkwerknEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    zkwerknEdit.setDisabled(True)
                                
                    self.Artikelnummer = QLabel()
                    artEdit = QLineEdit(str(rpmc[1]))
                    artEdit.setAlignment(Qt.AlignRight)
                    artEdit.setFixedWidth(100)
                    artEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    artEdit.setDisabled(True)
            
                    self.Leverdatum = QLabel()
                    leverEdit = QLineEdit(str(mlever))
                    leverEdit.setFixedWidth(100)
                    leverEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    leverEdit.setDisabled(True)
             
                    self.Afroep = QLabel()
                    afroepEdit = QLineEdit('{:12.2f}'.format(mafroep))
                    afroepEdit.setFixedWidth(80)
                    afroepEdit.setAlignment(Qt.AlignRight)
                    afroepEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    afroepEdit.setDisabled(True)
                    
                    self.Geleverd = QLabel()
                    geleverdEdit = QLineEdit('{:12.2f}'.format(mgeleverd))
                    geleverdEdit.setFixedWidth(80)
                    geleverdEdit.setAlignment(Qt.AlignRight)
                    geleverdEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    geleverdEdit.setDisabled(True)
         
                    self.Resterend = QLabel()
                    restEdit = QLineEdit('{:12.2f}'.format(mresterend))
                    restEdit.setFixedWidth(80)
                    restEdit.setAlignment(Qt.AlignRight)
                    restEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    restEdit.setDisabled(True)
                   
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
                                 
                    lbl1 = QLabel('Worknumber')  
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(zkwerknEdit, 1, 1)
                                                  
                    lbl2 = QLabel('Articlenumber')  
                    lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(artEdit, 2, 1)
                     
                    lbl3 = QLabel('Delivery date')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(leverEdit, 3 , 1)
                    
                    lbl4 = QLabel('Call-off')  
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 4, 0)
                    grid.addWidget(afroepEdit, 4 , 1)
                    if mmmstatus:
                        grid.addWidget(QLabel('More/less work'), 4, 2)
                    
                    lbl5 = QLabel('Delivered')  
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 5, 0)
                    grid.addWidget(geleverdEdit, 5 , 1)
                    if mmmstatus:
                        grid.addWidget(QLabel('More/less work'), 5, 2)   
                   
                    lbl6 = QLabel('Remaining')  
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 6, 0)
                    grid.addWidget(restEdit, 6 , 1)
                    
                    if mpostcode and mhuisnr:
                        grid.addWidget(QLabel('Delivery address:       '+mstraat+' '+str(mhuisnr)+' '+mtoev), 7, 0, 1 ,3)
                        grid.addWidget(QLabel('Residence:        '+mpostcode+' '+mplaats), 8, 0, 1, 3)
                    if maltern:
                        grid.addWidget(QLabel('Alternative address: '+maltern), 9, 0, 1 ,3)
                               
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
                       
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.accept) 
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(cancelBtn,10, 2)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 3, Qt.AlignCenter)     
                                     
            window = Widget()
            window.exec_()
            return(koppelnr)
            
    win = MyWindow(data_list, header)
    win.exec_()
                           
def artikelAfroep(koppelnr, m_email): 
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Call-off materials')
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
            table_view.setColumnHidden(2,True)
            table_view.setColumnHidden(3,True)
            table_view.setColumnHidden(5,True)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(artAfroep)
            grid.addWidget(table_view, 0, 0, 1, 8)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 7, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Refresh')
            freshBtn.clicked.connect(lambda: art_refresh(koppelnr, m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 6, 1, 1, Qt.AlignRight)
        
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 5)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 2)
            
            self.setLayout(grid)
            self.setGeometry(50, 50, 900, 900)
            self.setLayout(grid)
    
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
    if  str(koppelnr)[0] == '7':
        soort = 0
        materiaallijsten = Table('materiaallijsten', metadata,       
            Column('matlijstID', Integer, primary_key=True),
            Column('icalculatie', Integer),
            Column('hoeveelheid', Float),
            Column('artikelID', None, ForeignKey('artikelen.artikelID')),
            Column('resterend', Float),
            Column('afroep', Float))
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer, primary_key=True),
            Column('artikelomschrijving', String))
        icalculaties = Table('icalculaties', metadata,
            Column('icalcID', Integer, primary_key=True),
            Column('icalculatie', Integer),
            Column('koppelnummer', Integer))
        orders_intern = Table('orders_intern', metadata,
            Column('werkorderID', Integer, primary_key=True))
        
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selcl = select([icalculaties]).where(icalculaties.c.koppelnummer == koppelnr)
        rpcl = con.execute(selcl).first()
        selam = select([artikelen, materiaallijsten, orders_intern]).where(and_(artikelen.c.\
            artikelID==materiaallijsten.c.artikelID, materiaallijsten.c.icalculatie == rpcl[1],\
            orders_intern.c.werkorderID == koppelnr))
        rpam = con.execute(selam)
    elif str(koppelnr)[0] == '8':
        soort = 1
        materiaallijsten = Table('materiaallijsten', metadata,       
            Column('matlijstID', Integer, primary_key=True),
            Column('calculatie', Integer),
            Column('hoeveelheid', Float),
            Column('artikelID', None, ForeignKey('artikelen.artikelID')),
            Column('resterend', Float),
            Column('afroep', Float))
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer, primary_key=True),
            Column('artikelomschrijving', String))
        calculaties = Table('calculaties', metadata,
            Column('calcID', Integer, primary_key=True),
            Column('calculatie', Integer),
            Column('koppelnummer', Integer))
        werken = Table('werken', metadata,
            Column('werknummerID', Integer, primary_key=True))
          
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
    
        selcl = select([calculaties]).where(calculaties.c.koppelnummer == koppelnr)
        rpcl = con.execute(selcl).first()
        selam = select([artikelen, materiaallijsten, werken]).where(and_(artikelen.c.\
            artikelID==materiaallijsten.c.artikelID, materiaallijsten.c.calculatie == rpcl[1],\
            werken.c.werknummerID == koppelnr)).order_by(materiaallijsten.c.artikelID)
   
        rpam = con.execute(selam)

    header = ['Articlenumber','Articledescription','-','-','Amount','-',\
          'Remaining','Call-off', 'Worknumber']

    data_list=[]
    for row in rpam:
        data_list += [(row)]
        
    def artAfroep(idx):
        martnr = idx.data()
        if idx.column() == 0:
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Request materials")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            
                    self.setFont(QFont('Arial', 10))
                               
                    self.Werkorder = QLabel()
                    zkwerknEdit = QLineEdit(str(koppelnr))
                    zkwerknEdit.setAlignment(Qt.AlignRight)
                    zkwerknEdit.setFixedWidth(100)
                    zkwerknEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    zkwerknEdit.setDisabled(True) 
    
                    self.Artikelnummer = QLabel()
                    artEdit = QLineEdit(str(martnr))
                    artEdit.setAlignment(Qt.AlignRight)
                    artEdit.setFixedWidth(100)
                    artEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    artEdit.setDisabled(True)
                       
                    self.Hoeveelheid = QLabel()
                    hoevEdit = QLineEdit()
                    hoevEdit.setFixedWidth(80)
                    hoevEdit.setFont(QFont("Arial",10))
                    hoevEdit.textChanged.connect(self.hoevChanged) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, hoevEdit)
                    hoevEdit.setValidator(input_validator)
                    
                    self.Postcode = QLabel()
                    pcEdit = QLineEdit()
                    pcEdit.setFixedWidth(80)
                    font = QFont("Arial",10)
                    font.setCapitalization(QFont.AllUppercase)
                    pcEdit.setFont(font)
                    pcEdit.textChanged.connect(self.pcChanged) 
                    reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
                    input_validator = QRegExpValidator(reg_ex, pcEdit)
                    pcEdit.setValidator(input_validator)
                    
                    self.Huisnummer = QLabel()
                    hnoEdit = QLineEdit()
                    hnoEdit.setFixedWidth(60)
                    hnoEdit.setFont(QFont("Arial",10))
                    hnoEdit.textChanged.connect(self.hnoChanged) 
                    reg_ex = QRegExp("^[0-9]{1,5}$")
                    input_validator = QRegExpValidator(reg_ex, hnoEdit)
                    hnoEdit.setValidator(input_validator)
                    
                    self.Toevoeging = QLabel()
                    toevEdit = QLineEdit()
                    toevEdit.setFixedWidth(50)
                    toevEdit.setFont(QFont("Arial",10))
                    toevEdit.textChanged.connect(self.toevChanged) 
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, toevEdit)
                    toevEdit.setValidator(input_validator)
                    
                    self.Alternatief = QLabel()
                    altEdit = QLineEdit()
                    altEdit.setFixedWidth(280)
                    altEdit.setFont(QFont("Arial",10))
                    altEdit.textChanged.connect(self.altChanged) 
                    reg_ex = QRegExp("^.{0,30}$")
                    input_validator = QRegExpValidator(reg_ex, altEdit)
                    altEdit.setValidator(input_validator)
                     
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                  
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0, 0)
                    
                    lbl4 = QLabel('Assemble call-off materials')
                    lbl4.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl4, 0, 1)
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight) 
               
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 3, Qt.AlignCenter)
                                     
                    lbl1 = QLabel('Worknumber')  
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(zkwerknEdit, 1, 1)
                                                  
                    lbl2 = QLabel('Articlenumber')  
                    lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(artEdit, 2, 1)
                     
                    lbl3 = QLabel('Call-off')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(hoevEdit, 3 ,1)
                   
                    cBox = QCheckBox('More/less work')
                    cBox.stateChanged.connect(self.cBoxChanged)
                    grid.addWidget(cBox, 3, 2)
                  
                    lbl8 = QLabel('Delivery address')
                    lbl8.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl8, 4, 1)
                    
                    lbl4 = QLabel('Zip code')  
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 5, 0)
                    grid.addWidget(pcEdit, 5 , 1)
                    
                    lbl5 = QLabel('Housenumber')  
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 6, 0)
                    grid.addWidget(hnoEdit, 6 , 1)
                    
                    lbl6 = QLabel('Suffix')  
                    grid.addWidget(lbl6, 6, 0, 1, 2, Qt.AlignRight)
                    grid.addWidget(toevEdit, 6, 2)
                    
                    lbl7 = QLabel('Alternative address')  
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 7, 0)
                    grid.addWidget(altEdit, 7 , 1, 1, 3)
                                            
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
                   
                    applyBtn = QPushButton('Mutate')
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 8, 2, 1 , 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                     
                    sluitBtn = QPushButton('Close')
                    sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                    sluitBtn.clicked.connect(self.close)
            
                    grid.addWidget(sluitBtn, 8, 0, 1, 2, Qt.AlignRight)
                    sluitBtn.setFont(QFont("Arial",10))
                    sluitBtn.setFixedWidth(100)
                    
                    opvrBtn = QPushButton('Picklist')
                    opvrBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                    opvrBtn.clicked.connect(lambda: raapLijst(koppelnr))
            
                    grid.addWidget(opvrBtn, 8, 1, 1, 3)
                    opvrBtn.setFont(QFont("Arial",10))
                    opvrBtn.setFixedWidth(100)
                                     
                def hoevChanged(self,text):
                    self.Hoeveelheid.setText(text)
                                         
                state = False  
                def cBoxChanged(self, state):
                     if state == Qt.Checked:
                         self.state = True
                         
                def pcChanged(self,text):
                    self.Postcode.setText(text)
                    
                def hnoChanged(self,text):
                    self.Huisnummer.setText(text)
                    
                def altChanged(self,text):
                    self.Alternatief.setText(text)
                    
                def toevChanged(self,text):
                    self.Toevoeging.setText(text)
          
                def returnhoev(self):
                    return self.Hoeveelheid.text()
                                            
                def returncBox(self):
                    return self.state
                
                def returnpc(self):
                    return self.Postcode.text()
    
                def returnhno(self):
                    return self.Huisnummer.text()
    
                def returntoev(self):
                    return self.Toevoeging.text()
                
                def returnalt(self):
                    return self.Alternatief.text()
               
                @staticmethod
                def getData(parent=None):
                    dialog = Widget(parent)
                    dialog.exec_()
                    return [dialog.returnhoev(), dialog.returncBox(), dialog.returnpc(),\
                            dialog.returnhno(), dialog.returntoev(), dialog.returnalt()]
            
            window = Widget()
            data = window.getData()
            mhoev = 0
            martikelnr = int(martnr) 
            metadata = MetaData()
            if str(koppelnr)[0] == '7':
                orders_intern = Table('orders_intern', metadata,
                    Column('werkorderID', Integer, primary_key=True),
                    Column('voortgangstatus', String))
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selwerk = select([orders_intern]).where(orders_intern.c.werkorderID == koppelnr)
                rpwerk = con.execute(selwerk).first()
               
                materiaallijsten = Table('materiaallijsten', metadata,       
                    Column('matlijstID', Integer, primary_key=True),
                    Column('icalculatie', Integer),
                    Column('hoeveelheid', Float),
                    Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                    Column('resterend', Float),
                    Column('afroep', Float))
                artikelen = Table('artikelen', metadata,
                    Column('artikelID', Integer, primary_key=True),
                    Column('artikelomschrijving', String))
                icalculaties = Table('icalculaties', metadata,
                    Column('icalcID', Integer, primary_key=True),
                    Column('icalculatie', Integer),
                    Column('koppelnummer', Integer))
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
                    Column('straat', String),
                    Column('woonplaats', String))
                
                if rpwerk[1] == 'H':
                    werkGereed()
                    return()
                    
                mlevdat = str(datetime.datetime.now()+datetime.timedelta(days=7))[0:10]
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                sel = select([icalculaties]).where(icalculaties.c.koppelnummer == koppelnr)
                rpsel = con.execute(sel).first() 
            elif str(koppelnr)[0] == '8':
                werken = Table('werken', metadata,
                    Column('werknummerID', Integer, primary_key=True),
                    Column('voortgangstatus', String))
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selwerk = select([werken]).where(werken.c.werknummerID == koppelnr)
                rpwerk = con.execute(selwerk).first()
               
                materiaallijsten = Table('materiaallijsten', metadata,       
                    Column('matlijstID', Integer, primary_key=True),
                    Column('calculatie', Integer),
                    Column('hoeveelheid', Float),
                    Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                    Column('resterend', Float),
                    Column('afroep', Float))
                artikelen = Table('artikelen', metadata,
                    Column('artikelID', Integer, primary_key=True),
                    Column('artikelomschrijving', String))
                calculaties = Table('calculaties', metadata,
                    Column('calcID', Integer, primary_key=True),
                    Column('calculatie', Integer),
                    Column('koppelnummer', Integer))
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
                    Column('straat', String),
                    Column('woonplaats', String))
                
                if rpwerk[1] == 'H':
                    werkGereed()
                    return()
                    
                mlevdat = str(datetime.datetime.now()+datetime.timedelta(days=7))[0:10]
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                sel = select([calculaties]).where(calculaties.c.koppelnummer == koppelnr)
                rpsel = con.execute(sel).first()
            if data[0]:
                mhoev = float(data[0])
            else:
                return()
            if data[1]:
                mmmstatus = True
            else:
                mmmstatus = False
            if data[3]:
                mhuisnr = int(data[3])
            else:
                mhuisnr = 0
            if data[2] and data[3]:
                mpostcode = data[2].upper()
                mstrpl = checkpostcode(mpostcode, mhuisnr)
                if mstrpl[0]:
                    mstraat = mstrpl[0]
                    mplaats = mstrpl[1]
                else:
                    mpostcode = ''
                    mhuisnr = ''
                    mstraat = ''
                    mplaats = ''
                    foutPostcode()
                    return()
            else:
                mpostcode = ''
                mhuisnr = ''
                mstraat = ''
                mplaats = ''
            if data[4]:
                mtoev = data[4]
            else:
                mtoev = ''
            if data[5]:
                maltern = data[5]
            else:
                maltern = ''
                       
            if mhoev != 0:
                if str(koppelnr)[0] == '7':
                    selmatl = select([materiaallijsten]).where(and_(materiaallijsten.c.icalculatie ==\
                        rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                        materiaallijsten.c.artikelID == martikelnr))
                    rpmatl = con.execute(selmatl).first()
                    mresterend = rpmatl[4]
                    if mresterend < mhoev:
                        class Button(QDialog):
                            def __init__(self, parent=None):
                                super(Button, self).__init__(parent)
                                                            
                                msgBox = QMessageBox()
                                msgBox.setWindowTitle("Call-off articles")
                                msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                msgBox.setStyleSheet("color: black;  background-color: gainsboro; font-size: 16px;height: 20px; width: 50px")
                                msgBox.setText('The call-off '+str(mhoev)+' is bigger than yet to be delivered '+str(round(mresterend,3)))
                                msgBox.addButton(QPushButton('Continue'), QMessageBox.YesRole)
                                msgBox.addButton(QPushButton('Stop'), QMessageBox.RejectRole)
                                retour = msgBox.exec_()
                                if retour:
                                    artAfroep(idx)
                                else:
                                    updmatl = update(materiaallijsten).where(and_(materiaallijsten.c.icalculatie ==\
                                        rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                                        materiaallijsten.c.artikelID == martikelnr)).values(afroep = mhoev,\
                                        resterend=materiaallijsten.c.resterend - round(mhoev,4))
                                    con.execute(updmatl)
                                    
                                    try:
                                        mlijstnr=(con.execute(select([func.max(raaplijst.c.lijstID,\
                                         type_=Integer)])).scalar())
                                        mlijstnr += 1
                                    except:
                                        mlijstnr = 1
                                            
                                    insrl = insert(raaplijst).values(lijstID = mlijstnr, artikelID = martikelnr,\
                                        werkorder = koppelnr, afroep = mhoev, leverdatum = mlevdat,\
                                        meerwerk = mmmstatus, postcode = mpostcode, huisnummer = mhuisnr,\
                                        toevoeging = mtoev, alternatief = maltern, straat = mstraat, woonplaats = mplaats)
                                    con.execute(insrl)
                                    invoerOK()
                        btn = Button()
                        btn.show()
                    else:
                        updmatl = update(materiaallijsten).where(and_(materiaallijsten.c.icalculatie ==\
                            rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                            materiaallijsten.c.artikelID == martikelnr)).values(afroep = mhoev,\
                            resterend=materiaallijsten.c.resterend -  round(mhoev,4))
                        con.execute(updmatl)
                        try:
                            mlijstnr=(con.execute(select([func.max(raaplijst.c.lijstID,\
                                   type_=Integer)])).scalar())
                            mlijstnr += 1
                        except:
                            mlijstnr = 1
                            
                        insrl = insert(raaplijst).values(lijstID = mlijstnr, artikelID = martikelnr,\
                            werkorder = koppelnr, afroep = mhoev, leverdatum = mlevdat,\
                            meerwerk = mmmstatus, postcode = mpostcode, huisnummer = mhuisnr,\
                            toevoeging = mtoev, alternatief = maltern, straat = mstraat, woonplaats = mplaats)
                        con.execute(insrl)
                        invoerOK()
                                            
                elif str(koppelnr)[0] == '8':
                    selmatl = select([materiaallijsten]).where(and_(materiaallijsten.c.calculatie ==\
                        rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                        materiaallijsten.c.artikelID == martikelnr))
                    rpmatl = con.execute(selmatl).first()
                    mresterend = rpmatl[4]
                    if mresterend < mhoev:
                        class Button(QDialog):
                            def __init__(self, parent=None):
                                super(Button, self).__init__(parent)
                                
                                msgBox = QMessageBox()
                                msgBox.setWindowTitle("Call-off articles")
                                msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                msgBox.setStyleSheet("color: black;  background-color: gainsboro; font-size: 10pt")
                                msgBox.setText('The call-off '+str(mhoev)+' is bigger than yet to be delivered '+str(round(mresterend,3)))
                                msgBox.addButton(QPushButton('Continue'), QMessageBox.YesRole)
                                msgBox.addButton(QPushButton('Stop'), QMessageBox.RejectRole)
                                retour = msgBox.exec_()
                                if retour:
                                    artAfroep(idx)
                                else:
                                    updmatl = update(materiaallijsten).where(and_(materiaallijsten.c.calculatie ==\
                                        rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                                        materiaallijsten.c.artikelID == martikelnr)).values(afroep = mhoev,\
                                        resterend=materiaallijsten.c.resterend - round(mhoev,4))
                                    con.execute(updmatl)
                                    
                                    try:
                                        mlijstnr=(con.execute(select([func.max(raaplijst.c.lijstID,\
                                           type_=Integer)])).scalar())
                                        mlijstnr += 1
                                    except:
                                        mlijstnr = 1
                                    insrl = insert(raaplijst).values(lijstID = mlijstnr, artikelID = martikelnr,\
                                        werkorder = koppelnr, afroep = mhoev, leverdatum = mlevdat,\
                                        meerwerk = mmmstatus, postcode = mpostcode, huisnummer = mhuisnr,\
                                        toevoeging = mtoev, alternatief = maltern, straat = mstraat, woonplaats = mplaats)
                                    con.execute(insrl)
                                    invoerOK()
                        btn = Button()
                        btn.show()
                    else:
                        updmatl = update(materiaallijsten).where(and_(materiaallijsten.c.calculatie ==\
                            rpsel[1], materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                            materiaallijsten.c.artikelID == martikelnr)).values(afroep = mhoev,\
                            resterend=materiaallijsten.c.resterend - round(mhoev,4))
                        con.execute(updmatl)
                        
                        try:
                            mlijstnr=(con.execute(select([func.max(raaplijst.c.lijstID,\
                                type_=Integer)])).scalar())
                            mlijstnr += 1
                        except:
                            mlijstnr = 1
                        insrl = insert(raaplijst).values(lijstID = mlijstnr, artikelID = martikelnr,\
                            werkorder = koppelnr, afroep = mhoev, leverdatum = mlevdat,\
                            meerwerk = mmmstatus, postcode = mpostcode, huisnummer = mhuisnr,\
                            toevoeging = mtoev, alternatief = maltern, straat = mstraat, woonplaats = mplaats)
                        con.execute(insrl)
                        invoerOK()
    
    win = MyWindow(data_list, header)
    win.exec_()
    zoekWerk(m_email, soort)