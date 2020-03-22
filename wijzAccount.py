from login import hoofdMenu
from validZt import zt
from postcode import checkpostcode
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
     QDialog, QMessageBox, QComboBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp

def hash_password(password):
    import uuid
    import hashlib  
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    import hashlib
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    
def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Niet (alle) vereiste gegevens ingevuld!')
    msg.setWindowTitle('Gegevens!')
    msg.exec_()
     
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
      
def foutEmail():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Ongeldig email adres\nof wachtwoord ingevoerd!')
    msg.setWindowTitle('e-mailadres!')
    msg.exec_()
    
def foutWachtw():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(('Wachtwoord gegevens\nniet juist ingevuld\nof minder dan 8 teksns'))
    msg.setWindowTitle('AANMELDING')               
    msg.exec_()

def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(('Poscode / huisnummer combinatie onjuist!'))
    msg.setWindowTitle('AANMELDING')               
    msg.exec_()
        
def geenToegang():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen toegang\nNeem contact op met beheerder!')
    msg.setWindowTitle('PERMISSIE')               
    msg.exec_()

def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Je gegevens zijn aangepast!')
    msg.setWindowTitle('Gegevens!')
    msg.exec_()

def foutTelnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('geen 10 cijfers!')
    msg.setWindowTitle('Telefoonnummer!')
    msg.exec_()

def dontMatch():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Wachtwoord ongewijzigd')
    msg.setWindowTitle('Wachtwoord!')
    msg.exec_()
    
def logoutGeg():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Je wordt nu uitgelogd\n log in met je nieuwe emailadres!')
    msg.setWindowTitle('EMAIL')
    msg.exec_()
    return(1)
   
def updateAccount(m_email):
    from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                            create_engine, update)
    from sqlalchemy.sql import select
        
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
        Column('password', String, nullable=False),
        Column('telnr', String(10)), 
        Column('account_count', Integer(), nullable=False),
        Column('geboortedatum', String))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([accounts]).\
            where(accounts.c.email == m_email)
    rpaccount = conn.execute(sel).first()
    if rpaccount:
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
        mtelnr = rpaccount[10]
        mcount = rpaccount[11]
        mcount = int(mcount)+1
        mgebdat = rpaccount[12]
        mstrtplts = checkpostcode(mpostcode,mhuisnr)
        mstraat = mstrtplts[0]
        mplaats = mstrtplts[1]
             
    class Widget(QDialog):
         def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Bedrijfs Informatie Systeem")
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
            q2Edit.setCurrentIndex(q2Edit.findText(rpaccount[1]))
            q2Edit.activated[str].connect(self.q2Changed)
           
            self.Voornaam = QLabel()
            q3Edit = QLineEdit(mvoornaam)
            q3Edit.setFixedWidth(200)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^[^0-9]{1,30}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Tussenvoegsel = QLabel()
            q4Edit = QLineEdit('')
            q4Edit.setFixedWidth(80)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            q4Edit.setText(mtussenv)
            reg_ex = QRegExp("^[^0-9]{1,10}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q4Edit.setValidator(input_validator)
            
            self.Achternaam = QLabel()
            q5Edit = QLineEdit(machternaam)
            q5Edit.setFixedWidth(400)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp("^[^0-9]{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
      
            self.Straat = QLabel()
            q6Edit = QLineEdit(mstraat)
            q6Edit.setFixedWidth(500)
            q6Edit.setDisabled(True)
            q6Edit.setStyleSheet("QLineEdit { background-color: ; color: black }")
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed)
                       
            self.Huisnummer = QLabel()
            q7Edit = QLineEdit(str(mhuisnr))
            q7Edit.setFixedWidth(60)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[0-9]{1,5}$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
    
            self.Toevoeging = QLabel()
            q8Edit = QLineEdit('')
            q8Edit.setFixedWidth(80)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            q8Edit.setText(mtoev)
            reg_ex = QRegExp("^[A-Za-z0-9-#]{0,10}")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
       
            self.Postcode = QLabel()
            q9Edit = QLineEdit(mpostcode)
            q9Edit.setFixedWidth(70)
            font = QFont("Arial",10)
            font.setCapitalization(QFont.AllUppercase)
            q9Edit.setFont(font)
            q9Edit.textChanged.connect(self.q9Changed)
            reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
            input_validator = QRegExpValidator(reg_ex, q9Edit)
            q9Edit.setValidator(input_validator)
            
            self.Woonplaats = QLabel()
            q10Edit = QLineEdit(mplaats)
            q10Edit.setFixedWidth(500)
            q10Edit.setDisabled(True)
            q10Edit.setFont(QFont("Arial",10))
            q10Edit.setStyleSheet("QLineEdit { background-color: ; color: black }")
            q10Edit.textChanged.connect(self.q10Changed)
               
            self.email = QLabel()
            q11Edit = QLineEdit(m_email)
            q11Edit.setFixedWidth(300)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.textChanged.connect(self.q11Changed)
            reg_ex = QRegExp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            input_validator = QRegExpValidator(reg_ex, q11Edit)
            q11Edit.setValidator(input_validator)
            
            self.BestaandWachtwoord = QLabel()
            q12Edit = QLineEdit()
            q12Edit.setFixedWidth(300)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.setEchoMode(QLineEdit.Password)
            q12Edit.textChanged.connect(self.q12Changed)
            
            self.NieuwWachtwoord = QLabel()
            q13Edit = QLineEdit()
            q13Edit.setFixedWidth(300)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setEchoMode(QLineEdit.Password)
            q13Edit.textChanged.connect(self.q13Changed)
  
            self.NieuwWachtwoordControle = QLabel()
            q14Edit = QLineEdit()
            q14Edit.setFixedWidth(300)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.setEchoMode(QLineEdit.Password)
            q14Edit.textChanged.connect(self.q14Changed)
    
            self.Telefoonnr = QLabel()
            q15Edit = QLineEdit('')
            q15Edit.setFixedWidth(100)
            q15Edit.setFont(QFont("Arial",10))
            q15Edit.textChanged.connect(self.q15Changed)
            q15Edit.setText(mtelnr)
            reg_ex = QRegExp("^[#0]{1}[0-9]{9}$")
            input_validator = QRegExpValidator(reg_ex, q15Edit)
            q15Edit.setValidator(input_validator)
            
            self.Accountnummer = QLabel()
            q16Edit = QLineEdit(str(maccountnr))
            q16Edit.setFixedWidth(100)
            q16Edit.setDisabled(True)
            q16Edit.setStyleSheet("QLineEdit { background-color: ; color: black }")
            q16Edit.setFont(QFont("Arial",10))
            q16Edit.textChanged.connect(self.q16Changed)
            
            self.Geboortedatum = QLabel()
            q17Edit = QLineEdit(mgebdat)
            q17Edit.setFixedWidth(100)
            q17Edit.setFont(QFont("Arial",10))
            q17Edit.textChanged.connect(self.q17Changed)
            reg_ex = QRegExp('^[1-2]{1}[09]{1}[0-9]{2}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q17Edit)
            q17Edit.setValidator(input_validator)  
        
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
            grid.addWidget(QLabel('Opvragen of aanpassen persoongegevens'), 1, 1)
                        
            grid.addWidget(QLabel('                                           *'), 2, 0) 
            grid.addWidget(QLabel('Verplichte velden'), 2, 1)   
                         
            grid.addWidget(QLabel('Aanhef'), 3, 0)
            grid.addWidget(q2Edit, 3, 1)
            
            grid.addWidget(QLabel('Voornaam                            *'), 4, 0)
            grid.addWidget(q3Edit, 4, 1)  
     
            grid.addWidget(QLabel('Tussenvoegsel'), 5, 0)
            grid.addWidget(q4Edit, 5 , 1) 
             
            grid.addWidget(QLabel('Achternaam                         *'), 6, 0)
            grid.addWidget(q5Edit, 6, 1, 1, 2)
            
            grid.addWidget(QLabel('Geboortedatum                     *'), 7, 0)
            grid.addWidget(QLabel('                       formaat: jjjj-mm-dd'), 7, 1, 1, 2 )
            grid.addWidget(q17Edit, 7, 1)
                 
            grid.addWidget(QLabel('Straat'), 8, 0)
            grid.addWidget(q6Edit, 8, 1, 1, 2) 
       
            grid.addWidget(QLabel('Huisnummer                        *'), 9, 0)
            grid.addWidget(q7Edit, 9, 1)
            
            grid.addWidget(QLabel('Toevoeging'), 9, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(q8Edit, 9, 2)
             
            grid.addWidget(QLabel('Postcode                            *'), 10, 0)
            grid.addWidget(q9Edit, 10, 1)
            
            grid.addWidget(QLabel('Woonplaats'), 11, 0)
            grid.addWidget(q10Edit, 11, 1, 1, 2)    
     
            grid.addWidget(QLabel('e-mail                                 *'), 12, 0)
            grid.addWidget(q11Edit, 12, 1, 1 ,2)
                   
            grid.addWidget(QLabel('Bestaand wachtwoord          *'), 13, 0)
            grid.addWidget(q12Edit, 13, 1, 1 ,2) 
            
            grid.addWidget(QLabel('Nieuw wachtwoord               *'), 14, 0)
            grid.addWidget(q13Edit, 14, 1, 1 ,2) 
    
            grid.addWidget(QLabel('Nieuw wachtwoord controle  *'), 15, 0)
            grid.addWidget(q14Edit, 15, 1, 1 ,2) 
    
            grid.addWidget(QLabel('Telefoonnummer'), 16, 0)
            grid.addWidget(q15Edit, 16, 1) 
            
            grid.addWidget(QLabel('Accountnummer'),17, 0)
            grid.addWidget(q16Edit, 17, 1, 1, 2) 
                        
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 18, 0, 1, 3, Qt.AlignCenter)
                                 
            self.setLayout(grid)
            self.setGeometry(500, 50, 350, 300)
            
            applyBtn = QPushButton('Wijzigen')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 17, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
       
            grid.addWidget(cancelBtn, 16, 2, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                     
         def q2Changed(self, text):
            self.Aanhef.setText(text)
          
         def q3Changed(self, text):
            self.Voornaam.setText(text)
            
         def q4Changed(self, text):
            self.Tussenvoegsel.setText(text)
            
         def q5Changed(self, text):
            self.Achternaam.setText(text)
            
         def q6Changed(self, text):
            self.Straat.setText(text)    
            
         def q7Changed(self, text):
            self.Huisnummer.setText(text)
    
         def q8Changed(self, text):
            self.Toevoeging.setText(text)
    
         def q9Changed(self, text):
            self.Postcode.setText(text)
       
         def q10Changed(self, text):
            self.Woonplaats.setText(text)             
    
         def q11Changed(self, text):
            self.email.setText(text)
                   
         def q12Changed(self, text):
            self.BestaandWachtwoord.setText(text)
            
         def q13Changed(self, text):
            self.NieuwWachtwoord.setText(text)
            
         def q14Changed(self, text):
            self.NieuwWachtwoordControle.setText(text)
        
         def q15Changed(self, text):
            self.Telefoonnr.setText(text)
            
         def q16Changed(self, text):
            self.Accountnummer.setText(text)
            
         def q17Changed(self, text):
            self.Geboortedatum.setText(text)
      
         def returnAanhef(self):
            return self.Aanhef.text()
        
         def returnVoornaam(self):
            return self.Voornaam.text()
        
         def returnTussenvoegsel(self):
            return self.Tussenvoegsel.text()
    
         def returnAchternaam(self):
            return self.Achternaam.text()
      
         def returnStraat(self):
            return self.Straat.text()
       
         def returnHuisnummer(self):
            return self.Huisnummer.text()
        
         def returnToevoeging(self):
            return self.Toevoeging.text()
     
         def returnPostcode(self):
            return self.Postcode.text()
    
         def returnWoonplaats(self):
            return self.Woonplaats.text()
        
         def returnemail(self):
            return self.email.text()   
                
         def returnBestaandWachtwoord(self):
            return self.BestaandWachtwoord.text()
    
         def returnNieuwWachtwoord(self):
            return self.NieuwWachtwoord.text()   
 
         def returnNieuwWachtwoordControle(self):
            return self.NieuwWachtwoordControle.text()   
    
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
                    dialog.returnStraat(), dialog.returnHuisnummer(),\
                    dialog.returnToevoeging(), dialog.returnPostcode(),\
                    dialog.returnWoonplaats(), dialog.returnemail(),\
                    dialog.returnBestaandWachtwoord(), dialog.returnNieuwWachtwoord(),\
                    dialog.returnNieuwWachtwoordControle(), dialog.returnTelefoonnummer(),\
                    dialog.returnAccountnummer(),dialog.returnGeboortedatum()]
     
    window = Widget()
    data = window.getData()
    if data[0]:
        maanhef = data[0]
    else:
        maanhef = rpaccount[1]
    if data[1]:
        mvoornaam = (data[1]).title()
    else:
        mvoornaam = rpaccount[2].title()
    if data[2]:
        mtussenv = data[2]
    else:
        mtussenv = ''
    if data[3]:
        machternaam = (data[3]).title()
    else:
        machternaam = rpaccount[4].title()
    if data[5]:
        mhuisnr = data[5]
    else:
        mhuisnr = rpaccount[6]
    if data[7]:
        mpostcode = data[7].upper()
    else:
        mpostcode = rpaccount[5]
    if  checkpostcode(mpostcode, int(mhuisnr))[0] == '':
        foutPostcode()
        hoofdMenu(m_email)
    if data[6]:
        mtoev = '-'+data[6]
    else:
        mtoev = ''
    if data[9]:
        if zt(data[9], 12):
            m_email = (data[9])
        else:
            foutEmail()
            hoofdMenu(m_email)
    else:
        m_email = rpaccount[8]
    mpassword = rpaccount[9]
    old_password = ''
    nw_password = ''
    contr_nwpass = ''
    if data[10] and data[11] and data[12]:
        old_password = data[10]
        nw_password = data[11]
        contr_nwpass = data[12]
        if check_password(mpassword, old_password) and len(nw_password) > 7 \
                                          and (nw_password == contr_nwpass):
            nw_passwd = hash_password(nw_password)
        else:
            foutWachtw()
            hoofdMenu(m_email)    
    else:
        nw_passwd = mpassword
        dontMatch()
    if data[13]:
        mtelnr = data[13]
    else:
        mtelnr = ''
    if not (len(mtelnr) == 10 or mtelnr == ''):
        foutTelnr()
        hoofdMenu(m_email)        
    if data[15]:
        mgebdat = data[15]
    else:
        mgebdat = rpaccount[12]
                   
    u = update(accounts).where(accounts.c.accountID == maccountnr).\
    values(aanhef = maanhef, voornaam = mvoornaam, tussenvoegsel =\
    mtussenv, achternaam = machternaam, huisnummer = int(mhuisnr),\
    toevoeging = mtoev, postcode = mpostcode, email = m_email, password =\
    nw_passwd, telnr = mtelnr, account_count = mcount, geboortedatum = mgebdat)  
    conn.execute(u)
    conn.close()
    updateOK()
    hoofdMenu(m_email)