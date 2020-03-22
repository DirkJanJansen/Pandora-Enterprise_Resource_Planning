from login import hoofdMenu
import  datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                         QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, ForeignKey, MetaData,\
                        create_engine, func, String)
from sqlalchemy.sql import select, and_
 
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Koppelen Account')               
    msg.exec_() 
    
def geenGeboortedatum():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen geboortedatum ingevuld\nvul eerst een geboortedatum in\nvóór het koppelen van een werknemer!')
    msg.setWindowTitle('Koppelen Account')               
    msg.exec_() 
    
def foutAdmin():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Administrator bevoegdheden\nkunnen niet worden aangepast!')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()
        
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def koppelOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Koppelen gelukt!')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()
   
def koppelBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Koppeling bestaat al!')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()  
       
def foutAccountnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Account niet gevonden.')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()
    
def foutLeveranciernr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Leverancier niet gevonden.')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()
    
def foutClient():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Client niet gevonden.')
    msg.setWindowTitle('Koppelen account')
    msg.exec_()
                 
def _11check(minnr):
    number = str(minnr)
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

def zoekAccount(m_email, flag):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Account Koppelen.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Accountnummer = QLabel()
            accEdit = QLineEdit()
            accEdit.setFixedWidth(100)
            accEdit.setFont(QFont("Arial",10))
            accEdit.textChanged.connect(self.accChanged)
            reg_ex = QRegExp('^[1]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, accEdit)
            accEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                
            self.setFont(QFont('Arial', 10))
 
            grid.addWidget(QLabel('Accountnummer'), 1, 0)
            grid.addWidget(accEdit, 1, 1)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
        
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Koppel')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
        def accChanged(self, text):
            self.Accountnummer.setText(text)
    
        def returnAccountnummer(self):
            return self.Accountnummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnAccountnummer()]
   
    window = Widget()
    data = window.getData()
    if data[0]:
        maccountnr = int(data[0])
    else:
        maccountnr = 1
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('geboortedatum', String))           
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    sel = select([accounts]).where(accounts.c.accountID == maccountnr)
    rp = conn.execute(sel).first()
    if maccountnr == 100000010:
        foutAdmin()
        zoekAccount(m_email, flag)
    elif len(str(maccountnr)) == 9 and _11check(maccountnr) and rp:
        maccountnr = int(maccountnr)
        mgebdat = rp[1]
        if flag == 0 and mgebdat:
            koppelWerknemer(m_email, maccountnr, mgebdat, flag)
        elif flag == 1:
            koppelKoper(m_email, maccountnr, flag)
        elif flag == 2:
            koppelLeverancier(m_email, maccountnr, flag)
        else:
            geenGeboortedatum()
            zoekAccount(m_email, flag)
    else:
        foutAccountnr()
        zoekAccount(m_email, flag)
        
def koppelLeverancier(m_email, maccountnr, flag):
    class Widget(QDialog):
       def __init__(self, parent=None):
           super(Widget, self).__init__(parent)
           self.setWindowTitle("Koppel account aan leverancier.")
           self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
           self.setFont(QFont('Arial', 10))
    
           self.Leveranciernummer = QLabel()
           levEdit = QLineEdit()
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
           grid.addWidget(lbl , 0, 0)
           
           logo = QLabel()
           pixmap = QPixmap('./images/logos/logo.jpg')
           logo.setPixmap(pixmap)
           grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
           self.setFont(QFont('Arial', 10))
     
           grid.addWidget(QLabel('Leveranciernummer'), 1, 0)
           grid.addWidget(levEdit, 1, 1)
    
           grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
    
           cancelBtn = QPushButton('Sluiten')
           cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
           applyBtn = QPushButton('Koppel')
           applyBtn.clicked.connect(self.accept)
                  
           grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
           applyBtn.setFont(QFont("Arial",10))
           applyBtn.setFixedWidth(100)
           applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
           grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
           cancelBtn.setFont(QFont("Arial",10))
           cancelBtn.setFixedWidth(100)
           cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
           self.setLayout(grid)
           self.setGeometry(500, 300, 150, 150)
   
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
    if data[0]:
        mlevnr = int(data[0])
    else:
        mlevnr = 1
        
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer, primary_key=True))
    lev_accounts = Table('lev_accounts', metadata,
        Column('levaccID', Integer(), primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
        Column('accountID', None, ForeignKey('accounts.accountID')))
          
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    s = select([leveranciers]).where(leveranciers.c.leverancierID == mlevnr)
    if conn.execute(s).fetchone():
        rp = conn.execute(s)
    else:
        geenRecord()
        zoekAccount(m_email, flag)
    
    if len(str(mlevnr)) == 9 and _11check(mlevnr):
        mlevnr = int(mlevnr)
    else:
        mlevnr = 1
        foutLeveranciernr()
        zoekAccount(m_email, flag)   
          
    s = select([lev_accounts]).where(and_(lev_accounts.c.accountID == maccountnr,
             lev_accounts.c.leverancierID == mlevnr, lev_accounts.c.accountID ==\
             maccountnr))
     
    rp = conn.execute(s)
    if rp:
        regels = 0
        for record in rp:
            regels += 1
        if regels == 0:
            mlevaccnr = (conn.execute(select([func.max(lev_accounts.c.levaccID, type_=Integer)\
                                       .label('mlevaccnr')])).scalar())
            mlevaccnr += 1
            ins = lev_accounts.insert().values(levaccID = mlevaccnr, accountID = maccountnr,\
                        leverancierID = mlevnr)
            conn.execute(ins)
            conn.close()
            koppelOK()
            zoekAccount(m_email, flag)
        else:
            koppelBestaat()
            zoekAccount(m_email, flag)
     
def koppelKoper(m_email, maccountnr, flag):
    class Widget(QDialog):
       def __init__(self, parent=None):
           super(Widget, self).__init__(parent)
           self.setWindowTitle("Koppel account / koper.")
           self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
           self.setFont(QFont('Arial', 10))
    
           self.Clientnummer = QLabel()
           kbedrEdit = QLineEdit()
           kbedrEdit.setFixedWidth(100)
           kbedrEdit.setFont(QFont("Arial",10))
           kbedrEdit.textChanged.connect(self.kbedrChanged)
           reg_ex = QRegExp('^[6]{1}[0-9]{8}$')
           input_validator = QRegExpValidator(reg_ex, kbedrEdit)
           kbedrEdit.setValidator(input_validator)
                           
           grid = QGridLayout()
           grid.setSpacing(20)
    
           lbl = QLabel()
           pixmap = QPixmap('./images/logos/verbinding.jpg')
           lbl.setPixmap(pixmap)
           grid.addWidget(lbl , 0, 0)
           
           logo = QLabel()
           pixmap = QPixmap('./images/logos/logo.jpg')
           logo.setPixmap(pixmap)
           grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                
           self.setFont(QFont('Arial', 10))
    
           grid.addWidget(QLabel('Clientnummer'), 1, 0)
           grid.addWidget(kbedrEdit, 1, 1)
           grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
    
           cancelBtn = QPushButton('Sluiten')
           cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
           applyBtn = QPushButton('Koppel')
           applyBtn.clicked.connect(self.accept)
                  
           grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
           applyBtn.setFont(QFont("Arial",10))
           applyBtn.setFixedWidth(100)
           applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
           grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
           cancelBtn.setFont(QFont("Arial",10))
           cancelBtn.setFixedWidth(100)
           cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
           self.setLayout(grid)
           self.setGeometry(500, 300, 150, 150)
   
       def kbedrChanged(self, text):
           self.Clientnummer.setText(text)
    
       def returnClientnummer(self):
           return self.Clientnummer.text()
    
       @staticmethod
       def getData(parent=None):
           dialog = Widget(parent)
           dialog.exec_()
           return [dialog.returnClientnummer()]
       
    window = Widget()
    data = window.getData()
    if data[0]:
        mclientnr = int(data[0])
    else:
        mclientnr = 1
        
    metadata = MetaData()
    kopers = Table('kopers', metadata,
        Column('koperID', Integer, primary_key=True))
    koper_accounts = Table('koper_accounts', metadata,
        Column('koperaccID', Integer(), primary_key=True),
        Column('koperID', None, ForeignKey('kopers.koperID')),
        Column('accountID', None, ForeignKey('accounts.accountID')))
          
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([kopers]).where(kopers.c.koperID == mclientnr)
    if conn.execute(s).fetchone():
        rp = conn.execute(s)
    else:
        geenRecord()
        zoekAccount(m_email, flag)

    s = select([koper_accounts]).where(and_(koper_accounts.c.accountID == maccountnr,
             koper_accounts.c.koperID == int(mclientnr)))
    rp = conn.execute(s)
    if rp:
        regels = 0
        for record in rp:
            regels += 1
        if regels == 0:
            mclientaccnr = (conn.execute(select([func.max(koper_accounts.c.koperaccID, type_=Integer)\
                                               .label('mclientnr')])).scalar())
            mclientaccnr += 1
            ins = koper_accounts.insert().values(koperaccID = mclientaccnr, accountID = maccountnr,\
                                koperID = mclientnr)
            conn.execute(ins)
            koppelOK()
            zoekAccount(m_email, flag)
        else:
            koppelBestaat()
            zoekAccount(m_email, flag)
 
def koppelWerknemer(m_email, maccountnr, mgebdat, flag):
    metadata = MetaData()
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('indienst', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    mwerknemernr =(conn.execute(select([func.max(werknemers.c.werknemerID,\
            type_=Integer).label('mwerknemernr')])).scalar())
    mwerknemernr += 1
    sel = select([werknemers]).where(werknemers.c.accountID == maccountnr)
    if conn.execute(sel).fetchone():
        koppelBestaat()
        zoekAccount(m_email, flag)
    else:
        rp = conn.execute(sel)
        koppelOK()
    mindienst = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
    if rp:
        regels = 0
        for record in rp:
            regels += 1
        if regels == 0 :
            ins = werknemers.insert().values(werknemerID=mwerknemernr,accountID =\
            maccountnr, indienst = mindienst)
            conn.execute(ins)
            zoekAccount(m_email, flag)
        else:
            koppelBestaat()
            zoekAccount(m_email, flag) 