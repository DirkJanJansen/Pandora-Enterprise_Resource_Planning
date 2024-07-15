import login
import datetime, re
from argon2 import PasswordHasher
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
     QDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                          create_engine, func, ForeignKey)
from sqlalchemy.sql import select

def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Incorrect Zipcode inserted!')
    msg.setWindowTitle('ZIPCODE!')
    msg.exec_()
  
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("About creating a new account")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
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

        About creating a new account                                                 
                                                                                              
                                                                                               
        Required fields to insert:

        First name and last name. \t\t                                                              
                                                                                               
        Zip code 4 numbers and 2 letters without space.\t\t
        House number. (Dutch format)           
                                                                                               
        Valid email address.                                                                     
                                                                                               
        Password minimum 8 signs.                                                       
        Password control same as password.

        Date of birth format yyyy-mm-dd                                       
        
        Optional: 
        Phone number 10 digits, 1st digit a 0.  (Dutch format)                                         
    
  
     ''')
            grid.addWidget(infolbl, 0, 0)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn,  2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 1, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(350, 250, 150, 100)
            
    window = Widget()
    window.exec_()

def password_check(password):
    ph = PasswordHasher()
    try:
        if ph.verify(ph.hash(password), password) and (len(password) > 7):  # True
            return(True)
    except Exception:
        return(False)

def valid(item, valnr):
    if valnr == 1:
        # Zipcode
        ab = re.compile("^([0-9]{4}[A-Za-z]{2})+$")
        if ab.match(item):
            return(True)
        else:
            return(False)
    elif valnr == 2:
        #housenumber
        if item.isnumeric() and len(item) < 7:
            return(True)
        else:
            return(False)
    elif valnr == 3:
        #e-mail
        ab = re.compile("[^@]+@[^@]+\.[^@]+$")
        if ab.match(item):
            return(True)
        else:
            return(False)
    elif valnr == 6:
        #telephonnumber
        if (len(item) == 10 and item.isnumeric and item[0] == '0') or item == '':
            return(True)
        else:
            return(False) 
 
def windowSluit(self):
    self.close()
    login.inlog()

def password_hash(password):
    ph = PasswordHasher()
    return(ph.hash(password))  # store hashpass in bisystem table  accounts,  field password

def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Not (all) required information filled in correctly!')
    msg.setWindowTitle('Information!')
    msg.exec_()

def fout_email():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('incorrect email address!')
    msg.setWindowTitle('e-mail address!')
    msg.exec_()

def foutTelnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('no 10 digits!')
    msg.setWindowTitle('Telephone number!')
    msg.exec_()

def accountBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Pre-existing account!')
    msg.setWindowTitle('Account')
    msg.exec_()

def noMatch():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Password do not match!')
    msg.setWindowTitle('Passwords')
    msg.exec_()

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11 % 10
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalAccountnr():
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    try:
        maccountnr=(conn.execute(select([func.max(accounts.c.accountID,\
            type_=Integer)])).scalar())
        maccountnr=int(maak11proef(maccountnr))
    except:
        maccountnr = 100000010
    return(maccountnr)
   
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Account information')
    msg.exec_()
    
def nieuwAccount(self):
    self.close()
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Insert account")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                
            self.Aanhef = QLabel()
            q2Edit = QComboBox()
            q2Edit.setFixedWidth(80)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.setStyleSheet("color: black;  background-color: gainsboro")
            q2Edit.addItem(' ')
            q2Edit.addItem('Mr. ')
            q2Edit.addItem('Ms. ')
            q2Edit.addItem('Mss. ')
            q2Edit.activated[str].connect(self.q2Changed)
            
            self.Voornaam = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setFixedWidth(200)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^.{1,30}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Tussenvoegsel = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setFixedWidth(80)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^.{1,10}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q4Edit.setValidator(input_validator)
            
            self.Achternaam = QLabel()
            q5Edit = QLineEdit()
            q5Edit.setFixedWidth(540)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
    
            self.Postcode = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setFixedWidth(80)
            font = QFont("Arial",10)
            font.setCapitalization(QFont.AllUppercase)
            q6Edit.setFont(font)
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
            
            self.Huisnummer = QLabel()
            q7Edit = QLineEdit()
            q7Edit.setFixedWidth(60)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[0-9]{1,5}$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
    
            self.Toevoeging = QLabel()
            q8Edit = QLineEdit()
            q8Edit.setFixedWidth(80)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            reg_ex = QRegExp("^[A-Za-z0-9-]{0,8}")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
               
            self.email = QLabel()
            q9Edit = QLineEdit()
            q9Edit.setFixedWidth(300)
            q9Edit.setFont(QFont("Arial",10))
            q9Edit.textChanged.connect(self.q9Changed)
            reg_ex = QRegExp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            input_validator = QRegExpValidator(reg_ex, q9Edit)
            q9Edit.setValidator(input_validator)
       
            self.Wachtwoord = QLabel()
            q10Edit = QLineEdit()
            q10Edit.setFixedWidth(300)
            q10Edit.setFont(QFont("Arial",10))
            q10Edit.setEchoMode(QLineEdit.Password)
            q10Edit.textChanged.connect(self.q10Changed)
            
            self.ContrWachtwoord = QLabel()
            q11Edit = QLineEdit()
            q11Edit.setFixedWidth(300)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.setEchoMode(QLineEdit.Password)
            q11Edit.textChanged.connect(self.q11Changed)
    
            self.Telefoonnr = QLabel()
            q12Edit = QLineEdit()
            q12Edit.setFixedWidth(100)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed)
            reg_ex = QRegExp("^[0]{1}[0-9]{9}$")
            input_validator = QRegExpValidator(reg_ex, q12Edit)
            q12Edit.setValidator(input_validator)
            
            self.Accountnummer = QLabel()
            q13Edit = QLineEdit(str(bepaalAccountnr()))
            q13Edit.setFixedWidth(100)
            q13Edit.setDisabled(True)
            q13Edit.setStyleSheet("QLineEdit { background-color: ; color: black }")
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.textChanged.connect(self.q13Changed)
            
            self.Geboortedatum = QLabel()
            q14Edit = QLineEdit()
            q14Edit.setFixedWidth(100)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.textChanged.connect(self.q14Changed)
            reg_ex = QRegExp('^[1-2]{1}[09]{1}[0-9]{2}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q14Edit)
            q14Edit.setValidator(input_validator)  
            
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
            grid.addWidget(QLabel('Inserting new account'), 1, 1)
                        
            grid.addWidget(QLabel('                                  *'), 2, 0) 
            grid.addWidget(QLabel('Required fields'), 2, 1)   
                         
            grid.addWidget(QLabel('Prefix'), 3, 0)
            grid.addWidget(q2Edit, 3, 1)
             
            grid.addWidget(QLabel('FirstName                   *'), 4, 0)
            grid.addWidget(q3Edit, 4, 1)  
     
            grid.addWidget(QLabel('Infix'), 5, 0)
            grid.addWidget(q4Edit, 5 , 1) 
             
            grid.addWidget(QLabel('Surname                     *'), 6, 0)
            grid.addWidget(q5Edit, 6, 1, 1 , 2) 
            
            grid.addWidget(QLabel('DateOfBirth                 *'), 7, 0)
            grid.addWidget(QLabel('                             formaat: yyyy-mm-dd'), 7, 1, 1, 2 )
            grid.addWidget(q14Edit, 7, 1)
                 
            grid.addWidget(QLabel('Zipcode                      *'), 8, 0)
            grid.addWidget(q6Edit, 8, 1)
     
            grid.addWidget(QLabel('House number            *'), 9, 0)
            grid.addWidget(q7Edit, 9, 1)
            
            grid.addWidget(QLabel('Suffix'), 9, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 9, 2)
    
            grid.addWidget(QLabel('e-mail                         *'), 10, 0)
            grid.addWidget(q9Edit, 10, 1, 1 ,2)
        
            grid.addWidget(QLabel('Password                   *'), 11, 0)
            grid.addWidget(q10Edit, 11, 1, 1 ,2) 
            
            grid.addWidget(QLabel('Password Check         *'), 12, 0)
            grid.addWidget(q11Edit, 12, 1, 1, 2) 
    
            grid.addWidget(QLabel('TelephoneNumber'), 13, 0)
            grid.addWidget(q12Edit, 13, 1) 
           
            grid.addWidget(QLabel('Account number'), 14, 0)
            grid.addWidget(q13Edit, 14, 1) 
                                
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 0, 1, 3, Qt.AlignCenter)
            
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 14, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self))
        
            grid.addWidget(cancelBtn, 13, 2 , 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            helpBtn = QPushButton('Info')
            helpBtn.clicked.connect(lambda: info())
          
            grid.addWidget(helpBtn, 12, 2 , 1, 1, Qt.AlignRight)
            helpBtn.setFont(QFont("Arial",10))
            helpBtn.setFixedWidth(100)
            helpBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(400, 150, 350, 300)
                  
        def q2Changed(self, text):
            self.Aanhef.setText(text)
          
        def q3Changed(self, text):
            self.Voornaam.setText(text)
            
        def q4Changed(self, text):
            self.Tussenvoegsel.setText(text)
            
        def q5Changed(self, text):
            self.Achternaam.setText(text)
    
        def q6Changed(self, text):
            self.Postcode.setText(text)
                  
        def q7Changed(self, text):
            self.Huisnummer.setText(text)
    
        def q8Changed(self, text):
            self.Toevoeging.setText(text)
    
        def q9Changed(self, text):
            self.email.setText(text)
       
        def q10Changed(self, text):
            self.Wachtwoord.setText(text)
            
        def q11Changed(self, text):
            self.ContrWachtwoord.setText(text)
        
        def q12Changed(self, text):
            self.Telefoonnr.setText(text)
            
        def q13Changed(self, text):
            self.Accountnummer.setText(text)
            
        def q14Changed(self, text):
            self.Geboortedatum.setText(text)
            
        def returnAanhef(self):
            return self.Aanhef.text()
        
        def returnVoornaam(self):
            return self.Voornaam.text()
        
        def returnTussenvoegsel(self):
            return self.Tussenvoegsel.text()
    
        def returnAchternaam(self):
            return self.Achternaam.text()
    
        def returnPostcode(self):
            return self.Postcode.text()
        
        def returnHuisnummer(self):
            return self.Huisnummer.text()
    
        def returnToevoeging(self):
            return self.Toevoeging.text()
        
        def returnemail(self):
            return self.email.text()   
        
        def returnWachtwoord(self):
            return self.Wachtwoord.text()
    
        def returnContrWachtwoord(self):
            return self.ContrWachtwoord.text()   
    
        def returnTelefoonnummer(self):
            return self.Telefoonnr.text()   
    
        def returnAccountnummer(self):
            return self.Accountnummer.text() 
      
        def returnGeboortedatum(self):
            return self.Geboortedatum.text() 
         
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnAanhef(), dialog.returnVoornaam(),\
                    dialog.returnTussenvoegsel(), dialog.returnAchternaam(),\
                    dialog.returnPostcode(), dialog.returnHuisnummer(),\
                    dialog.returnToevoeging(), dialog.returnemail(),\
                    dialog.returnWachtwoord(), dialog.returnContrWachtwoord(),\
                    dialog.returnTelefoonnummer(),dialog.returnAccountnummer(),\
                    dialog.returnGeboortedatum()]
                    
    window = Widget()
    data = window.getData()

    if data[8] != data[9]:
        noMatch()
        nieuwAccount(self)

    if data[1] and data[3] and valid(data[4], 1) and valid(data[5],2)\
         and valid(data[7],3) and data[12] and password_check(data[8]) and valid(data[10],6):
        if data[0]:
            maanhef = data[0]
        else:
            maanhef = ' '
        mvoornaam = (data[1]).title()
        mtussenv = (data[2]).lower()
        if mtussenv:
            mtussenv =  mtussenv+' '
        machternaam = (data[3]).title()
        mpostcode = (data[4]).upper()
        mhuisnr = int(data[5])
        mtoev = (data[6])
        if mtoev:
            mtoev = '-'+mtoev
        m_email = (data[7])
        mpassword = password_hash(data[8])
        mtelnr = (data[10])
        if data[12]:
            mgebdatum = data[12]
        import postcode
        mstrpl = postcode.checkpostcode(mpostcode,mhuisnr)
        if mstrpl[0]:
            metadata = MetaData()
            accounts = Table('accounts', metadata,
                Column('accountID', Integer(), primary_key=True),
                Column('aanhef', String(8)),
                Column('voornaam', String(30), nullable=False), 
                Column('achternaam', String(50), nullable=False),
                Column('tussenvoegsel', String(10)),
                Column('telnr', String(10)),
                Column('email', String, nullable=False),
                Column('huisnummer', String(5), nullable=False),
                Column('postcode', String(6), nullable=False),       
                Column('toevoeging', String),
                Column('password', String, nullable=False),
                Column('account_count', Integer(), nullable=False),
                Column('account_created', String),
                Column('geboortedatum', String))
                
            klanten = Table('klanten', metadata,
                Column('klantID', Integer(), primary_key=True),
                Column('accountID', None, ForeignKey('accounts.c.accountID')),
                Column('klant_status', Integer()))
                         
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            metadata.create_all(engine)
            conn = engine.connect()
            maccountnr=bepaalAccountnr()
            try:
                mklantnr=(conn.execute(select([func.max(klanten.c.klantID,\
                    type_=Integer)])).scalar())
                mklantnr += 1
            except:
                mklantnr = 1
                
            metadata.create_all(engine)
            insacc = accounts.insert().values(
            accountID=maccountnr,
            aanhef=maanhef,
            voornaam=mvoornaam,
            tussenvoegsel=mtussenv,
            achternaam=machternaam,
            postcode=mpostcode.upper(),
            huisnummer=mhuisnr,
            toevoeging=mtoev,
            email=m_email,
            password=mpassword,
            account_count=1,
            account_created = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10],
            telnr=mtelnr,
            geboortedatum = mgebdatum)
              
            insklant = klanten.insert().values(
            klantID = mklantnr,
            accountID = maccountnr,
            klant_status = 9)
                     
            conn = engine.connect()
            s = select([accounts]).where(accounts.c.email == m_email)
            result = conn.execute(s).first()
            if result:
                accountBestaat()
                login.inlog()
            else:
                result = conn.execute(insacc)
                insacc.bind = engine
                result = conn.execute(insklant)
                insklant.bind = engine
                conn.close()
                Invoer()
                login.inlog()
        else:
            foutPostcode()
            nieuwAccount(self)
    else:
        geenGegevens()
        self.close()
        nieuwAccount(self)