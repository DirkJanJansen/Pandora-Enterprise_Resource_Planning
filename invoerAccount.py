import login
import datetime, re
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
    msg.setText('Foutieve postcode ingevoerd!')
    msg.setWindowTitle('POSTCODE!')
    msg.exec_()
  
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatie over aanmaken nieuw account")
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

        Informatie over aanmaken nieuw account                                                  
                                                                                              
                                                                                               
        Verplichte invoervelden: 

        Voornaam en achternaam.                                                              
                                                                                               
        Postcode 4 cijfers en 2 letters zonder spatie.\t\t
        Huisnummer.            
                                                                                               
        Geldig emailadres.                                                                     
                                                                                               
        Wachtwoord minimaal 8 tekens.                                                          
        Wachtwoord controle identiek aan  wachtwoord.   

        Geboortedatum formaat jjjj-mm-dd                                       
        
        Optioneel:                                                                                       
        Telefoonnummer 10 cijfers, 1e cijfer een 0.                                            
    
  
     ''')
            grid.addWidget(infolbl, 0, 0)
            
            cancelBtn = QPushButton('Sluiten')
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

def passwcontrol(password, passwcontrol):
    if  (password == passwcontrol) and (len(password) > 7):
        return(True)
    else:
        return(False)
 
def valid(item, valnr):
    if valnr == 1:
        # Postcode
        ab = re.compile("^([0-9]{4}[A-Za-z]{2})+$")
        if ab.match(item):
            return(True)
        else:
            return(False)
    elif valnr == 2:
        #huisnummer
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
        #telefoonnummer
        if (len(item) == 10 and item.isnumeric and item[0] == '0') or item == '':
            return(True)
        else:
            return(False) 
 
def windowSluit(self):
    self.close()
    login.inlog()
     
def hash_password(password):
    import uuid
    import hashlib  
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
   
def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Niet (alle) vereiste gegevens juist ingevuld!')
    msg.setWindowTitle('Gegevens!')
    msg.exec_()

def fout_email():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('ongeldig email adres!')
    msg.setWindowTitle('e-mailadres!')
    msg.exec_()

def foutTelnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('geen 10 cijfers!')
    msg.setWindowTitle('Telefoonnummer!')
    msg.exec_()

def accountBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Reeds bestaand account!')
    msg.setWindowTitle('Account')
    msg.exec_()

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalAccountnr():
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    maccountnr=(conn.execute(select([func.max(accounts.c.accountID, type_=Integer)\
                                   .label('maccountnr')])).scalar())
    maccountnr=int(maak11proef(maccountnr))
    conn.close
    return(maccountnr)
   
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt!')
    msg.setWindowTitle('Accountgegevens')
    msg.exec_()
    
def nieuwAccount(self):
    self.close()
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Invoer account")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                
            self.Aanhef = QLabel()
            q2Edit = QComboBox()
            q2Edit.setFixedWidth(80)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.setStyleSheet("color: black;  background-color: gainsboro")
            q2Edit.addItem(' ')
            q2Edit.addItem('Dhr. ')
            q2Edit.addItem('Mevr. ')
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
            grid.addWidget(QLabel('Nieuw account invoeren'), 1, 1)
                        
            grid.addWidget(QLabel('                                  *'), 2, 0) 
            grid.addWidget(QLabel('Verplichte velden'), 2, 1)   
                         
            grid.addWidget(QLabel('Aanhef'), 3, 0)
            grid.addWidget(q2Edit, 3, 1)
             
            grid.addWidget(QLabel('Voornaam                   *'), 4, 0)
            grid.addWidget(q3Edit, 4, 1)  
     
            grid.addWidget(QLabel('Tussenvoegel'), 5, 0)
            grid.addWidget(q4Edit, 5 , 1) 
             
            grid.addWidget(QLabel('Achternaam                *'), 6, 0)
            grid.addWidget(q5Edit, 6, 1, 1 , 2) 
            
            grid.addWidget(QLabel('Geboortedatum           *'), 7, 0)
            grid.addWidget(QLabel('                             formaat: jjjj-mm-dd'), 7, 1, 1, 2 )
            grid.addWidget(q14Edit, 7, 1)
                 
            grid.addWidget(QLabel('Postcode                    *'), 8, 0)
            grid.addWidget(q6Edit, 8, 1)
     
            grid.addWidget(QLabel('Huisnummer                *'), 9, 0)
            grid.addWidget(q7Edit, 9, 1)
            
            grid.addWidget(QLabel('Toevoeging'), 9, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 9, 2)
    
            grid.addWidget(QLabel('e-mail                         *'), 10, 0)
            grid.addWidget(q9Edit, 10, 1, 1 ,2)
        
            grid.addWidget(QLabel('Wachtwoord                *'), 11, 0)
            grid.addWidget(q10Edit, 11, 1, 1 ,2) 
            
            grid.addWidget(QLabel('Wachtwoord controle    *'), 12, 0)
            grid.addWidget(q11Edit, 12, 1, 1, 2) 
    
            grid.addWidget(QLabel('Telefoonnummer'), 13, 0)
            grid.addWidget(q12Edit, 13, 1) 
           
            grid.addWidget(QLabel('Accountnummer'), 14, 0)
            grid.addWidget(q13Edit, 14, 1) 
                                
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 0, 1, 3, Qt.AlignCenter)
            
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 14, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
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
    
    if data[1] and data[3] and valid(data[4], 1) and valid(data[5],2)\
         and valid(data[7],3) and data[12] and passwcontrol(data[8], data[9]) and valid(data[10],6):
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
        mpassword = hash_password(data[8])
        mtelnr = (data[10])
        maccountnr = (data[11])
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
            mklantnr=(conn.execute(select([func.max(klanten.c.klantID, type_=Integer)\
                                           .label('mklantnr')])).scalar())
            mklantnr += 1
            maccdatum = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
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
            telnr=mtelnr,
            account_created = maccdatum,
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
                result.inserted_primary_key
                result = conn.execute(insklant)
                insklant.bind = engine
                result.inserted_primary_key
                conn.close()
                Invoer()
                login.inlog()
        else:
            foutPostcode()
            self.close
            nieuwAccount(self) 
    else:
        geenGegevens()
        self.close()
        nieuwAccount(self)