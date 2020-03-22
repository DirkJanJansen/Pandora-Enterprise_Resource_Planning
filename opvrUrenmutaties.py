from login import hoofdMenu
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, \
                        ForeignKey, create_engine, Boolean)
from sqlalchemy.sql import select, desc, and_
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout,\
      QMessageBox, QDialog, QComboBox, QLineEdit, QGridLayout , QTableView 

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email) 
     
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Urenmutaties opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Urenmutaties opvragen')               
    msg.exec_() 

def foutInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Foutieve Invoer')
    msg.setWindowTitle('Urenmutaties opvragen')               
    msg.exec_() 
  
def loonKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Overzicht loongegevens portal-boekhouding")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Times', 10))
    
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(220)
            k4Edit.setFont(QFont("Times", 10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem('         Maak uw keuze')
            k4Edit.addItem('1. Alle loongegevens')
            k4Edit.addItem('2. Soort uren categorie')
            k4Edit.addItem('3. Loongroep tot-met.')
            k4Edit.addItem('4. Periode jjjj(-mm(-dd)).')
            k4Edit.addItem('5. Werknummer.')
            k4Edit.addItem('6. Indirect/Direct I of D.')
            k4Edit.addItem('7. Op (deel) achternaam.')
            k4Edit.activated[str].connect(self.k4Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(200)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k4Edit, 1, 1)
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(110)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
        def k4Changed(self, text):
            self.Keuze4.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk4(self):
            return self.Keuze4.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk4(), dialog.returnzkterm()]       

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
    toonMutaties(keuze, zoekterm, m_email)

def toonMutaties(keuze, zoekterm, m_email):
    import validZt
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')))
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('werknummerID', Integer),
        Column('boekdatum', String(6)),
        Column('aantaluren', Float),
        Column('soort', String),
        Column('meerwerkstatus', Boolean),
        Column('bruto_loonbedrag', Float))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur', Float),
        Column('reisuur', Float),
        Column('direct', Boolean))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
               accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
               wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
               wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.accountID, desc(wrkwnrln.c.boekdatum))
    elif keuze == 2 and validZt.zt(zoekterm, 24):
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
               accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
               wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
               wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]   
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
          werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
          lonen.c.loonID == werknemers.c.loonID, wrkwnrln.c.soort.ilike('%'+zoekterm+'%')))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.achternaam, desc(wrkwnrln.c.boekdatum))
    elif keuze == 3 and validZt.zt(zoekterm, 23):
        zoekterm = zoekterm.split('-')
        zk1 = int(zoekterm[0])
        zk2 = int(zoekterm[1])
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
               accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
               wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
               wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID,\
                 lonen.c.loonID.between(zk1, zk2)))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.accountID, desc(wrkwnrln.c.boekdatum))
    elif keuze == 4 and validZt.zt(zoekterm, 10):
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
               accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
               wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
               wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID,\
                 wrkwnrln.c.boekdatum.like(zoekterm+'%')))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.accountID, desc(wrkwnrln.c.boekdatum))
    elif keuze == 5  and validZt.zt(zoekterm, 21):
        zoekterm = int(zoekterm)
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
               accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
               wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
               wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID,\
                 wrkwnrln.c.werknummerID == zoekterm))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.achternaam, desc(wrkwnrln.c.boekdatum))
    elif keuze == 6  and validZt.zt(zoekterm, 22):
        zoekterm=zoekterm.upper()
        if zoekterm[0] == 'I' or zoekterm == 'i':
            zoekterm = False
        else:
            zoekterm = True
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
                 accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
                 wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
                 wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID,\
                 lonen.c.direct == zoekterm))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.achternaam, desc(wrkwnrln.c.boekdatum))
    elif keuze == 7:
        columns = [accounts.c.accountID, accounts.c.voornaam, accounts.c.tussenvoegsel,\
                 accounts.c.achternaam, lonen.c.loonID, lonen.c.tabelloon, lonen.c.reisuur,\
                 wrkwnrln.c.aantaluren, wrkwnrln.c.soort,wrkwnrln.c.bruto_loonbedrag, \
                 wrkwnrln.c.werknummerID, wrkwnrln.c.boekdatum, wrkwnrln.c.meerwerkstatus]
        loonuren = select(columns).where(and_(accounts.c.accountID == werknemers.c.accountID,\
                 werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
                 lonen.c.loonID == werknemers.c.loonID,\
                 accounts.c.achternaam.ilike('%'+zoekterm+'%')))
        loonuren = loonuren.select_from(wrkwnrln.join(werknemers).join(lonen).join(accounts))\
               .order_by(accounts.c.achternaam, desc(wrkwnrln.c.boekdatum))           
    else:
        ongInvoer()
        loonKeuze(m_email)
     
    if con.execute(loonuren).fetchone():
        rpwrklonen = con.execute(loonuren)
    else:
        geenRecord()
        loonKeuze(m_email)
    
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(10, 50, 1400, 900)
            self.setWindowTitle('Loonbetalingen opvragen')
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
            #table_view.clicked.connect(selectRow)
            #table_view.clicked.connect(showSelection)
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
              
    header = ['Acountnummer', 'Voornaam', 'Tussenvoegsel', 'Achternaam', 'Loonschaal',\
      'Tabelloon', 'Reisuurloon','Aantal uren','Soort uren', 'Bruto-loonbedrag',\
      'Werknummer', 'Boekdatum','Meerwerkstatus']
    
    data_list=[]
    for row in rpwrklonen:
        data_list += [(row)]
        
    win = Widget(data_list, header)
    win.exec_()
    loonKeuze(m_email)