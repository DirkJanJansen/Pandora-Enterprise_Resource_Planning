from login import hoofdMenu
from postcode import checkpostcode
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QDialog, QComboBox,\
      QLineEdit, QGridLayout, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, ForeignKey, MetaData,\
                        create_engine)
from sqlalchemy.sql import select, and_

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Requesting Accounts')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Requesting Accounts')               
    msg.exec_() 

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def accKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Requesting Accounts")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.addItem(' Search sort key')
            k0Edit.addItem('1. All accounts')
            k0Edit.addItem('2. Zip code')
            k0Edit.addItem('3. email address.')
            k0Edit.addItem('4. Surname.')
            k0Edit.addItem('5. Accounts suppliers.')
            k0Edit.addItem('6. Accounts employees.')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(220)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 1)
            lbl1 = QLabel('Search key')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 , 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 3, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 1, 1 , 1)
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
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonAccounts(keuze,zoekterm, m_email)
    
def toonAccounts(keuze, zoekterm, m_email):
    import validZt
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('aanhef', String(8)),
        Column('voornaam', String(30), nullable=False), 
        Column('tussenvoegsel', String(10)),
        Column('achternaam', String(50), nullable=False),
        Column('postcode', String(6), nullable=False),       
        Column('huisnummer', String(5), nullable=False),
        Column('toevoeging', String),
        Column('email', String, nullable=False),
        Column('telnr', String(10)), 
        Column('account_count', Integer(), nullable=False),
        Column('geboortedatum', String))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String))
    lev_accounts = Table('lev_accounts', metadata,
        Column('levaccID', Integer, primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),     
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer, primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', Integer))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if keuze == 1:
        sel = select([accounts]).order_by(accounts.c.accountID)
    elif keuze == 2 and validZt.zt(zoekterm, 9):
        sel = select([accounts]).where(accounts.c.postcode.ilike(zoekterm))
    elif keuze == 3 and validZt.zt(zoekterm, 12):
        sel = select([accounts]).where(accounts.c.email.ilike('%'+zoekterm+'%'))
    elif keuze == 4:
        sel = select([accounts]).where(accounts.c.achternaam.ilike('%'+zoekterm+'%'))
    elif keuze == 5:
        sel = select([accounts, leveranciers.c.leverancierID, leveranciers.c.bedrijfsnaam,\
         leveranciers.c.rechtsvorm]).where(and_(lev_accounts.c.accountID ==\
         accounts.c.accountID, leveranciers.c.leverancierID == lev_accounts.c.leverancierID))
    elif keuze == 6:
        sel = select([accounts, werknemers.c.werknemerID, werknemers.c.loonID]).where(werknemers.c.accountID ==\
            accounts.c.accountID)
    else:
        ongInvoer()
        accKeuze(m_email)
     
    if conn.execute(sel).fetchone():
        rpaccount = conn.execute(sel)
    else:
        geenRecord()
        accKeuze(m_email)
     
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1700, 900)
            self.setWindowTitle('Request account information')
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
  
    header = ['Account number','Prefix', 'Firstname','Infix', 'Surname', 'Zipcode',\
              'House number','Suffix', 'E-mail', 'Telephone number', 'Account count', 'Date of birth']
    
    if keuze == 5:
        header1 = ['Supplier number', 'Company name', 'Legal form']
        header.extend(header1)
    elif keuze == 6:
        header2 = ['Employee number', 'Payscale']
        header.extend(header2)
   
    data_list=[]
    for row in rpaccount:
        data_list += [(row)] 

    win = MyWindow(data_list, header)
    win.exec_()
    accKeuze(m_email)