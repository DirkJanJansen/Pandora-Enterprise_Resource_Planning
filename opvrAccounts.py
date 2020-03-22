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
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Accounts opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Accounts opvragen')               
    msg.exec_() 

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def accKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen accounts")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.addItem(' Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Alle accounts')
            k0Edit.addItem('2. Postcode')
            k0Edit.addItem('3. emailadres.')
            k0Edit.addItem('4. Achternaam.')
            k0Edit.addItem('5. Accounts leveranciers.')
            k0Edit.addItem('6. Accounts werknemers.')
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
            lbl1 = QLabel('Zoekterm')  
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
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 3, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
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
        sel = select([accounts, werknemers]).where(werknemers.c.accountID ==\
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
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Accountgegevens opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            if keuze == 6:
                table_view.setColumnHidden(13,True)
                table_view.setColumnHidden(14,True)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showAccount)
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
  
    header = ['Accountnummer','Aanhef', 'Voornaam','Tussenvoegsel', 'Achternaam', 'Postcode',\
              'Huisnummer','Toevoeging', 'E-mail', 'Telefoonnummer', 'Accountcount', 'Geboortedatum']  
    
    if keuze == 5:
        header1 = ['Leveranciernummer', 'Bedrijfsnaam', 'Rechtsvorm'] 
        header.extend(header1)
    elif keuze == 6:
        header2 = ['Werknemernummer','Account', 'Loonschaal']
        header.extend(header2)
   
    data_list=[]
    for row in rpaccount:
        data_list += [(row)] 
        
    def showAccount(idx):
        maccountnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            conn = engine.connect()
            sel = select([accounts, werknemers]).where(accounts.c.accountID == maccountnr)
            rpaccount = conn.execute(sel).first()
      
            maccountnr = rpaccount[0]
            maanhef = rpaccount[1]
            mvoornaam = rpaccount[2]
            mtussenv = rpaccount[3]
            machternaam = rpaccount[4]
            mpostcode = rpaccount[5]
            mhuisnr = rpaccount[6]
            mhuisnr = int(mhuisnr)
            mtoev = rpaccount[7]
            m_email = rpaccount[8]
            mtelnr = rpaccount[9]
            mcount = rpaccount[10]
            mcount = int(mcount)+1
            mgebdat = rpaccount[11]
            mhuisnr = int(mhuisnr)
            mstrtplts = checkpostcode(mpostcode,mhuisnr)
            mstraat = mstrtplts[0]
            mplaats = mstrtplts[1]
         
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Accountgegevens opvragen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                          
                    self.setFont(QFont('Arial', 10))
                        
                    self.Aanhef = QLabel()
                    q2Edit = QLineEdit(maanhef)
                    q2Edit.setFixedWidth(80)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                    
                    self.Voornaam = QLabel()
                    q3Edit = QLineEdit(mvoornaam)
                    q3Edit.setFixedWidth(200)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                     
                    self.Tussenvoegsel = QLabel()
                    q4Edit = QLineEdit(mtussenv)
                    q4Edit.setFixedWidth(80)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
    
                    self.Achternaam = QLabel()
                    q5Edit = QLineEdit(machternaam)
                    q5Edit.setFixedWidth(400)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
               
                    self.Straat = QLabel()
                    q6Edit = QLineEdit(mstraat)
                    q6Edit.setFixedWidth(500)
                    q6Edit.setDisabled(True)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                                                                   
                    self.Huisnummer = QLabel()
                    q7Edit = QLineEdit(str(mhuisnr))
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setFixedWidth(60)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
             
                    self.Toevoeging = QLabel()
                    q8Edit = QLineEdit(mtoev)
                    q8Edit.setFixedWidth(80)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                 
                    self.Postcode = QLabel()
                    q9Edit = QLineEdit(mpostcode)
                    q9Edit.setFixedWidth(70)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                     
                    self.Woonplaats = QLabel()
                    q10Edit = QLineEdit(mplaats)
                    q10Edit.setFixedWidth(500)
                    q10Edit.setDisabled(True)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                                                               
                    self.email = QLabel()
                    q11Edit = QLineEdit(m_email)
                    q11Edit.setFixedWidth(300)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                     
                    self.Telefoonnr = QLabel()
                    q15Edit = QLineEdit(mtelnr)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
                    
                    self.Accountnummer = QLabel()
                    q16Edit = QLineEdit(str(maccountnr))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setDisabled(True)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                                                               
                    self.Geboortedatum = QLabel()
                    q17Edit = QLineEdit(mgebdat)
                    q17Edit.setFixedWidth(100)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
               
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl , 1, 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 1, 2, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Opvragen persoongegevens'), 1, 1)
                                       
                    grid.addWidget(QLabel('Aanhef'), 2, 0)
                    grid.addWidget(q2Edit, 2, 1)
                    
                    grid.addWidget(QLabel('Voornaam'), 3, 0)
                    grid.addWidget(q3Edit, 3, 1)  
             
                    grid.addWidget(QLabel('Tussenvoegsel'), 4, 0)
                    grid.addWidget(q4Edit, 4 , 1) 
                     
                    grid.addWidget(QLabel('Achternaam'), 5, 0)
                    grid.addWidget(q5Edit, 5, 1, 1, 2)
                    
                    grid.addWidget(QLabel('Geboortedatum'), 6, 0)
                    grid.addWidget(q17Edit, 6, 1)
                         
                    grid.addWidget(QLabel('Straat'), 7, 0)
                    grid.addWidget(q6Edit, 7, 1, 1, 2) 
               
                    grid.addWidget(QLabel('Huisnummer'), 8, 0)
                    grid.addWidget(q7Edit, 8, 1)
                    
                    grid.addWidget(QLabel('Toevoeging'), 8, 1, 1, 1, Qt.AlignRight)
                    grid.addWidget(q8Edit, 8, 2)
                     
                    grid.addWidget(QLabel('Postcode'), 9, 0)
                    grid.addWidget(q9Edit, 9, 1)
                    
                    grid.addWidget(QLabel('Woonplaats'), 10, 0)
                    grid.addWidget(q10Edit, 10, 1, 1, 2)    
             
                    grid.addWidget(QLabel('e-mail'), 11, 0)
                    grid.addWidget(q11Edit, 11, 1, 1 ,2)
                       
                    grid.addWidget(QLabel('Telefoonnummer'), 12, 0)
                    grid.addWidget(q15Edit, 12, 1) 
                    
                    grid.addWidget(QLabel('Accountnummer'),13, 0)
                    grid.addWidget(q16Edit, 13, 1, 1, 2) 
                                                     
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 3, Qt.AlignCenter)
                                         
                    self.setLayout(grid)
                    self.setGeometry(500, 150, 350, 300)
                                                         
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
               
                    grid.addWidget(cancelBtn, 14, 2, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            win = Widget()
            win.exec_()
    
    win = MyWindow(data_list, header)
    win.exec_()
    accKeuze(m_email)