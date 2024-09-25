import os, sys, subprocess
from datetime import datetime
from argon2 import PasswordHasher
from validZt import zt
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QMovie, QColor, QRegExpValidator
from PyQt5.QtWidgets import (QDialog, QGridLayout, QMessageBox, QLabel, QLineEdit, QPushButton, QComboBox)
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, select)

def password_check(hashed_password, password):
    ph = PasswordHasher()
    try:
        if ph.verify(hashed_password, password) and (len(password) > 7):  # True
           return(True)
    except Exception:
        return(False)

def totZiens():
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    '''
    # release lock
    home = os.path.expanduser("~")
    os.remove(str(home)+'/.pandora_lock')
    '''
    msg.setText('Tot ziens!       ')
    msg.setWindowTitle('Loginscherm')
    msg.exec_()
    sys.exit()
     
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatie ERP Systeem Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Informatie ERP Pandora')
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

        Informatie Enterprise Resource Planning (ERP) systeem Pandora 
        
        De software valt onder GNU GPLv3 (Licentie is bijgesloten).
         
        Het systeem is ontworpen in Python 3 met PyQt5 als grafische interface.
        Als relationeel database systeem is toegepast PostgreSQL met interface SQLAlchemy Core.
        De inlog is gerealiseerd met gecrypte SHA256 controle met geauthoriseerde
        en per account instelbare permissies. Dit op menuniveau en op overige bewerkingen
        b.v. bestellen, opvragen, invoeren, wijzigen, printen enz. De permissies kunnen door
        bevoegde personen worden toegekend of aangepast. Het aanmaken van een account kan door elke
        persoon geschieden. Het account wordt standaard met de permissies opvragen en wijzigen
        van account, plaatsen webbestellingen, opvragen en printen van bestelgegegevens aangemaakt.
        Alle overige authorisaties dienen door een daartoe bevoegd persoon te worden uitgevoerd.
        Koppeling van het account is mogelijk naar werknemer, leverancier of koper. Met bevoegdheden
        per afdeling of werkdiscipline kunnen dan de overige bevoegdheden worden toegekend.
        Zie voor bevoegdheden de info bij onderhoudsmenu-authorisaties.
        Vanuit het hoofdmenu zijn de volgende submenu's toegankelijk:
        Accounts, Leveranciers, Werknemers, Inkoop, Verkoop, Magazijn, Werken Intern, Werken Extern,\t
        Calculatie Intern, Calculatie Extern, Loonadminstratie, Boekhouding, Voorraadmanagement,
        Management Informatie, Onderhoud, Herprinten formulieren. 
        Het authoriseren van deze submenu's en bewerkingen kunnen worden toegekend met
        het onderhoudsmenu, bevoegdheden muteren.                                   
  
     ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()
    
def closeIt(self):
    self.close()
    inlog()  
      
def geenKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen keuze\nof meer dan één keuze gemaakt!')
    msg.setWindowTitle('KEUZEMENU')
    msg.exec_()
    
def capslkOn():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Capslock is ingeschakeld!')
    msg.setWindowTitle('AANMELDING!')
    msg.exec_()

def foutemailAdres():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('E-mail adres onjuist')
    msg.setWindowTitle('AANMELDING')
    msg.exec_()

def foutWachtw():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Wachtwoord onjuist')
    msg.setWindowTitle('AANMELDING')
    msg.exec_()
    
def foutKlantnummer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Klantnummer onjuist!')
    msg.setWindowTitle('AANMELDING')
    msg.exec_()
    
def foutInlog():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Inlog onjuist!')
    msg.setWindowTitle('AANMELDING')
    msg.exec_()

def maakAccount(self):
    from invoerAccount import nieuwAccount
    nieuwAccount(self)
     
def inlog():
    #verification and logon
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora bedrijfs informatie systeem login scherm")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
     
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.Email = QLabel()
            emailEdit = QLineEdit()
            emailEdit.setStyleSheet("background: #F8F7EE")
            emailEdit.setFixedWidth(200)
            emailEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("([A-Za-z0-9._-]{1,}@(\\w+)(\\.(\\w+))(\\.(\\w+))?(\\.(\\w+))?)$")
            input_validator = QRegExpValidator(reg_ex, emailEdit)
            emailEdit.setValidator(input_validator)
            emailEdit.textChanged.connect(self.emailChanged)

            self.Account = QLabel()
            accountEdit = QLineEdit()
            accountEdit.setStyleSheet("background: #F8F7EE")
            accountEdit.setFixedWidth(200)
            accountEdit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^([1]{1}[0-9]{8})$")
            input_validator = QRegExpValidator(reg_ex, accountEdit)
            accountEdit.setValidator(input_validator)
            accountEdit.textChanged.connect(self.accountChanged)

            self.Wachtwoord = QLabel()
            wachtwEdit = QLineEdit()
            wachtwEdit.setStyleSheet("background: #F8F7EE")
            wachtwEdit.setEchoMode(QLineEdit.Password)
            wachtwEdit.setFixedWidth(200)
            wachtwEdit.setFont(QFont("Arial",10))
            wachtwEdit.textChanged.connect(self.wachtwChanged)
 
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)
            
            lblinfo = QLabel(' Pandora login')
            grid.addWidget(lblinfo, 0, 1, 1, 2, Qt.AlignLeft)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
             
            pandora = QLabel()
            movie = QMovie('./images/logos/pyqt5.gif')
            pandora.setMovie(movie)
            movie.start()
            grid.addWidget(pandora, 1 ,0, 1, 3, Qt.AlignCenter)

            grid.addWidget(QLabel('Login met je Emailadres of met je Accountnummer'), 2, 0, 1, 3, Qt.AlignCenter)
            grid.addWidget(QLabel('Emailadres'), 3, 1)
            grid.addWidget(emailEdit, 3, 2)

            grid.addWidget(QLabel('Accountnummer'), 4, 1)
            grid.addWidget(accountEdit, 4, 2)

            grid.addWidget(QLabel('Wachtwoord'), 5, 1)
            grid.addWidget(wachtwEdit, 5, 2)
                                   
            self.setLayout(grid)
            self.setGeometry(600, 250, 150, 150)
            
            applyBtn = QPushButton('Login')
            applyBtn.clicked.connect(self.accept)
            
            grid.addWidget(applyBtn, 6, 1, 1 , 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(90)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                       
            cancelBtn = QPushButton('Afsluiten')
            cancelBtn.clicked.connect(lambda: totZiens())
                                      
            grid.addWidget(cancelBtn, 6, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            nwBtn = QPushButton('Nieuw Account')
            nwBtn.clicked.connect(lambda: maakAccount(self))
            
            grid.addWidget(nwBtn,  6, 0, 1, 2, Qt.AlignRight)
            nwBtn.setFont(QFont("Arial",10))
            nwBtn.setFixedWidth(140)
            nwBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
            
            grid.addWidget(infoBtn,  6, 0, 1, 2)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")           
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 3, Qt.AlignCenter)

        def emailChanged(self, text):
            self.Email.setText(text)

        def accountChanged(self, text):
            self.Account.setText(text)

        def wachtwChanged(self, text):
            self.Wachtwoord.setText(text)

        def returnEmail(self):
            return self.Email.text()

        def returnAccount(self):
            return self.Account.text()

        def returnWachtwoord(self):
            return self.Wachtwoord.text()

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnEmail(), dialog.returnAccount(), dialog.returnWachtwoord()]

    window = Widget()
    data = window.getData()
    for item in data:
         if item.startswith(' '):
            geenKeuze()
            inlog()
    if sys.platform == 'win32':
        from win32api import GetKeyState
        from win32con import VK_CAPITAL
        capslk = GetKeyState(VK_CAPITAL)
        if capslk == 1:
            capslkOn()
            inlog()
    else:
        if int(subprocess.getoutput("xset q | grep LED")[65])%2 == 1:
            capslkOn()
            inlog()
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False),
        Column('password', String, nullable=False))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    if data[0] and zt(data[0], 12):
        m_email = data[0]
        sel = select([accounts]).where(accounts.c.email == m_email)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            foutemailAdres()
            inlog()
    elif data[1]:
        maccountnr = data[1]
        sel = select([accounts]).where(accounts.c.accountID == maccountnr)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            foutKlantnummer()
            inlog()
    else:
        foutInlog()()
        inlog()

    if data[2]:
        mwachtw = data[2]
    else:
        foutWachtw()
        inlog()

    if not password_check(mpassword, mwachtw):
        foutWachtw()
        inlog()
    hoofdMenu(m_email)

def hoofdMenu(m_email):
    # declare database table accounts for authorizations
    metadata = MetaData()
    accounts = Table('accounts', metadata,
                     Column('accountID', Integer(), primary_key=True),
                     Column('email', String, nullable=False),
                     Column('p1', String),
                     Column('p2', String),
                     Column('p3', String),
                     Column('p4', String),
                     Column('p5', String),
                     Column('p6', String),
                     Column('p7', String),
                     Column('p8', String),
                     Column('p9', String),
                     Column('p10', String),
                     Column('p11', String),
                     Column('p12', String),
                     Column('p13', String),
                     Column('p14', String),
                     Column('p15', String),
                     Column('p16', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([accounts]).where(accounts.c.email == m_email)
    rpaccount = conn.execute(sel).first()
    mp = rpaccount[2:18]

    #structure Menu's
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora bedrijfs informatie systeem")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
           
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(310)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k0Edit.addItem('Accounts')
            self.k0Edit.setEditable(True)
            self.k0Edit.lineEdit().setFont(QFont("Arial",10))
            self.k0Edit.lineEdit().setReadOnly(True)
            self.k0Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k0Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k0Edit.addItem('1. Wijzigen account') 
            self.k0Edit.addItem('2. Opvragen accounts')
            self.k0Edit.addItem('3. Bestellen webartikelen')
            self.k0Edit.addItem('4. Opvragen besteloverzicht')
            self.k0Edit.addItem('5. Printen orderfacturen')
 
            self.k1Edit = QComboBox()
            self.k1Edit.setFixedWidth(310)
            self.k1Edit.setFont(QFont("Arial",10))
            self.k1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k1Edit.addItem('Leveranciers')
            self.k1Edit.setEditable(True)
            self.k1Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k1Edit.lineEdit().setReadOnly(True)
            self.k1Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k1Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k1Edit.addItem('1. Invoeren leveranciergegevens')
            self.k1Edit.addItem('2. Wijzigen leveranciergegevens')
            self.k1Edit.addItem('3. Opvragen leveranciergegevens')
            self.k1Edit.addItem('4. Zelf gegevens opvragen.')
 
            self.k2Edit = QComboBox()
            self.k2Edit.setFixedWidth(310)
            self.k2Edit.setFont(QFont("Arial",10))
            self.k2Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k2Edit.addItem('Werknemers')
            self.k2Edit.setEditable(True)
            self.k2Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k2Edit.lineEdit().setReadOnly(True)
            self.k2Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k2Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k2Edit.addItem('1. Koppelen account-werknemer')
            self.k2Edit.addItem('2. Wijzigen werknemergegevens')
            self.k2Edit.addItem('3. Opvragen werknemersgegevens')
            self.k2Edit.addItem('4. Opvragen werknemer-periode')
 
            self.k3Edit = QComboBox()
            self.k3Edit.setFixedWidth(310)
            self.k3Edit.setFont(QFont("Arial",10))
            self.k3Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k3Edit.addItem('Inkoop')
            self.k3Edit.setEditable(True)
            self.k3Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k3Edit.lineEdit().setReadOnly(True)
            self.k3Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k3Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k3Edit.addItem('1. Invoeren orders materialen')
            self.k3Edit.addItem('2. Wijzigen orders materialen')
            self.k3Edit.addItem('3. Invoeren orders van stelposten')
            self.k3Edit.addItem('4. Bestellen / opvragen materieel orders')
            self.k3Edit.addItem('5. Wijzigen van orders stelposten')
            self.k3Edit.addItem('6. Opvragen orders materialen')
            self.k3Edit.addItem('7. Opvragen orders stelposten')
            self.k3Edit.addItem('8. Opvragen reserveringen materialen')
  
            self.k4Edit = QComboBox()
            self.k4Edit.setFixedWidth(310)
            self.k4Edit.setFont(QFont("Arial",10))
            self.k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k4Edit.addItem('Verkoop')
            self.k4Edit.setEditable(True)
            self.k4Edit.lineEdit().setFont(QFont("Arial",10))
            self.k4Edit.lineEdit().setReadOnly(True)
            self.k4Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k4Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k4Edit.addItem('1. Verkoop-bedrijf aanmaken')
            self.k4Edit.addItem('2. Verkoop-bedrijf wijzigen')
            self.k4Edit.addItem('3. Verkoop-bedrijven opvragen')
            self.k4Edit.addItem('4. Zelf gegevens opvragen')
            self.k4Edit.addItem('5. Webverkooporders opvragen')

            self.k5Edit = QComboBox()
            self.k5Edit.setFixedWidth(310)
            self.k5Edit.setFont(QFont("Arial",10))
            self.k5Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k5Edit.addItem('Magazijn')
            self.k5Edit.setEditable(True)
            self.k5Edit.lineEdit().setFont(QFont("Arial",10))
            self.k5Edit.lineEdit().setReadOnly(True)
            self.k5Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k5Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k5Edit.addItem('1. Invoeren artikelen')
            self.k5Edit.addItem('2. Wijzigen artikelen')
            self.k5Edit.addItem('3. Opvragen artikelen')
            self.k5Edit.addItem('4. Uitgifte materialen (raaplijst)')
            self.k5Edit.addItem('5. Printen raaplijsten')
            self.k5Edit.addItem('6. Boeken verschillen/overbodig')
            self.k5Edit.addItem('7. Uitgifte webartikelen /printen')
            self.k5Edit.addItem('8. Web-artikelen retour boeken')
            self.k5Edit.addItem('9. Balieverkoop - barcodescan')

            self.k6Edit = QComboBox()
            self.k6Edit.setFixedWidth(310)
            self.k6Edit.setFont(QFont("Arial",10))
            self.k6Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k6Edit.addItem('Werken intern')
            self.k6Edit.setEditable(True)
            self.k6Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k6Edit.lineEdit().setReadOnly(True)
            self.k6Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k6Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k6Edit.addItem('1. Invoer werkopdrachten')
            self.k6Edit.addItem('2. Wijzig werkopdrachten')
            self.k6Edit.addItem('3. Opvragen werkopdrachten/printen')
            self.k6Edit.addItem('4. Afroepen materialen')
            self.k6Edit.addItem('5. Printen raaplijsten')
            self.k6Edit.addItem('6. Uurverbruik muteren')
 
            self.k7Edit = QComboBox()
            self.k7Edit.setFixedWidth(310)
            self.k7Edit.setFont(QFont("Arial",10))
            self.k7Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k7Edit.addItem('Werken extern')
            self.k7Edit.setEditable(True)
            self.k7Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k7Edit.lineEdit().setReadOnly(True)
            self.k7Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k7Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k7Edit.addItem('1. Invoeren werken')
            self.k7Edit.addItem('2. Wijzigen werken')
            self.k7Edit.addItem('3. Opvragen werken')
            self.k7Edit.addItem('4. Afroepen materialen')
            self.k7Edit.addItem('5. Printen raaplijsten')
            self.k7Edit.addItem('6. Muteren kosten diensten')
            self.k7Edit.addItem('7. Uurverbruik muteren')
            self.k7Edit.addItem('8. Materieel uurverbruik muteren')
            self.k7Edit.addItem('9. Parameters Diensten')

            self.k8Edit = QComboBox()
            self.k8Edit.setFixedWidth(310)
            self.k8Edit.setFont(QFont("Arial",10))
            self.k8Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k8Edit.addItem('Calculatie interne werken')
            self.k8Edit.setEditable(True)
            self.k8Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k8Edit.lineEdit().setReadOnly(True)
            self.k8Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k8Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k8Edit.addItem('1. Nieuwe clusters aanmaken')
            self.k8Edit.addItem('2. Clustergegevens invoeren')
            self.k8Edit.addItem('3. Clustergegevens opvragen')
            self.k8Edit.addItem('4. Invoeren artikelregels per cluster')
            self.k8Edit.addItem('5. Opvragen artikelregels per cluster')
            self.k8Edit.addItem('6. Calculatie maken/wijzigen')
            self.k8Edit.addItem('7. Calculatie/Artikellijst printen')
            self.k8Edit.addItem('8. Calculatie koppelen -> produktie')
            self.k8Edit.addItem('9. Wijzigen Cluster Menus Interne werken')

            self.k9Edit = QComboBox()
            self.k9Edit.setFixedWidth(310)
            self.k9Edit.setFont(QFont("Arial",10))
            self.k9Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k9Edit.addItem('Calculatie externe werken')
            self.k9Edit.setEditable(True)
            self.k9Edit.lineEdit().setFont(QFont("Arial",10))
            self.k9Edit.lineEdit().setReadOnly(True)
            self.k9Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k9Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k9Edit.addItem('1. Nieuwe clusters aanmaken')
            self.k9Edit.addItem('2. Clustergegevens invoeren')
            self.k9Edit.addItem('3. Clustergegevens opvragen')
            self.k9Edit.addItem('4. Invoeren artikelregels per cluster')
            self.k9Edit.addItem('5. Opvragen artikelregels per cluster')
            self.k9Edit.addItem('6. Calculatie maken / wijzigen')
            self.k9Edit.addItem('7. Calculatie/Artikellijst printen')
            self.k9Edit.addItem('8. Calculatie koppelen -> produktie')
            self.k9Edit.addItem('9. Wijzigen Cluster Menus Externe werken')

            self.k10Edit = QComboBox()
            self.k10Edit.setFixedWidth(310)
            self.k10Edit.setFont(QFont("Arial",10))
            self.k10Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k10Edit.addItem('Loonadministratie')
            self.k10Edit.setEditable(True)
            self.k10Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k10Edit.lineEdit().setReadOnly(True)
            self.k10Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k10Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k10Edit.addItem('  1. Uren mutaties opvragen')
            self.k10Edit.addItem('  2. Controle uren tbv maanlonen')
            self.k10Edit.addItem('  3. Maandelijkse loonbetalingen')
            self.k10Edit.addItem('  4. Opvragen loonbetalingen')
            self.k10Edit.addItem('  5. Invoeren Loonschalen')
            self.k10Edit.addItem('  6. Loonschalen wijzigen/opvragen')
            self.k10Edit.addItem('  7. Procentueel lonen verhogen')
            self.k10Edit.addItem('  8. Parameters werkuren')
            self.k10Edit.addItem('  9. Parameters Inhoudingen')
            self.k10Edit.addItem('10. Parameters Perioden Lonen')

            self.k11Edit = QComboBox()
            self.k11Edit.setFixedWidth(310)
            self.k11Edit.setFont(QFont("Arial",10))
            self.k11Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k11Edit.addItem('Boekhouding')
            self.k11Edit.setEditable(True)
            self.k11Edit.lineEdit().setFont(QFont("Arial",10))
            self.k11Edit.lineEdit().setReadOnly(True)
            self.k11Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k11Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k11Edit.addItem('1. Artikel mutaties opvragen.')
            self.k11Edit.addItem('2. Diensten mutaties opvragen')
            self.k11Edit.addItem('3. Inzien en betalen afdrachten')
            self.k11Edit.addItem('4. Weborders betaling/printen factuur')
            self.k11Edit.addItem('5. Retouren betalingen boeken')
            self.k11Edit.addItem('6. Printen lijst te factureren')
            self.k11Edit.addItem('7. Uren mutaties opvragen')
            self.k11Edit.addItem('8. Parameters Financiëel')

            self.k12Edit = QComboBox()
            self.k12Edit.setFixedWidth(310)
            self.k12Edit.setFont(QFont("Arial",10))
            self.k12Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k12Edit.addItem('Voorraadmanagement')
            self.k12Edit.setEditable(True)
            self.k12Edit.lineEdit().setFont(QFont("Arial",10))
            self.k12Edit.lineEdit().setReadOnly(True)
            self.k12Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k12Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k12Edit.addItem('1. Voorraadbeheersing/artikelen')
            self.k12Edit.addItem('2. Grafiek voorraden/financiëel')
            self.k12Edit.addItem('3. Overzicht voorraden financiëel')
            self.k12Edit.addItem('4. Opvragen reserveringen')

            self.k13Edit = QComboBox()
            self.k13Edit.setFixedWidth(310)
            self.k13Edit.setFont(QFont("Arial",10))
            self.k13Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k13Edit.addItem('Management informatie')
            self.k13Edit.setEditable(True)
            self.k13Edit.lineEdit().setFont(QFont("Arial",10))
            self.k13Edit.lineEdit().setReadOnly(True)
            self.k13Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k13Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k13Edit.addItem('1. Bereken financiën eens/week')
            self.k13Edit.addItem('2. Printen grafieken financiën werken')
            self.k13Edit.addItem('3. Printen grafieken voortgangstatus')
            self.k13Edit.addItem('4. Opvragen resultaten werken')
            self.k13Edit.addItem('5. Parameters Grafieken')
  
            self.k14Edit = QComboBox()
            self.k14Edit.setFixedWidth(310)
            self.k14Edit.setFont(QFont("Arial",10))
            self.k14Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k14Edit.addItem('Onderhoud')
            self.k14Edit.setEditable(True)
            self.k14Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k14Edit.lineEdit().setReadOnly(True)
            self.k14Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k14Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k14Edit.addItem('1. Bevoegdheden muteren')
            self.k14Edit.addItem('2. Koppel account-leverancier')
            self.k14Edit.addItem('3. Koppel account-verkoopbedrijf')
            self.k14Edit.addItem('4. Parameters systeem')
            self.k14Edit.addItem('5. Verkoop-werktarieven bijwerken')

            self.k15Edit = QComboBox()
            self.k15Edit.setFixedWidth(310)
            self.k15Edit.setFont(QFont("Arial",10))
            self.k15Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k15Edit.addItem('Herprinten van formulieren')
            self.k15Edit.setMaxVisibleItems(15)
            self.k15Edit.setEditable(True)
            self.k15Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k15Edit.lineEdit().setReadOnly(True)
            self.k15Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k15Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k15Edit.addItem(' 1. Calculatie interne werken')
            self.k15Edit.addItem(' 2. Calculatie externe werken')
            self.k15Edit.addItem(' 3. Interne orderbrieven tbv inkoop')
            self.k15Edit.addItem(' 4. Afroepen werken intern')
            self.k15Edit.addItem(' 5. Afroepen werken extern')
            self.k15Edit.addItem(' 6. Raaplijsten magazijn')
            self.k15Edit.addItem(' 7. Web orders pakbon')
            self.k15Edit.addItem(' 8. Controle uren tbv lonen')
            self.k15Edit.addItem(' 9. Loonspecificaties personeel')
            self.k15Edit.addItem('10. Factureren externe werken')
            self.k15Edit.addItem('11. Web orders betalingen')
            self.k15Edit.addItem('12. Inkooporders diensten/materieel')
            self.k15Edit.addItem('13. Balieverkoop orderfacturen')
            self.k15Edit.addItem('14. Materieel inkoop orders')

            # disable menu's if no permission is granted in table accounts
            # list of Mainmenu
            mplist = [self.k0Edit, self.k1Edit, self.k2Edit, self.k3Edit, self.k4Edit, self.k5Edit, self.k6Edit, self.k7Edit, \
                      self.k8Edit, self.k9Edit, self.k10Edit, self.k11Edit, self.k12Edit, self.k13Edit, self.k14Edit, self.k15Edit]

            # list of pointers by mainmenu and menulines per groups pointers towards database table accountpermissions
            lineperm = (
            [0, 4, 6, 2, 2, 5], [0, 3, 4, 6, 1], [0, 1, 4, 6, 6], [0, 3, 4, 3, 7, 6, 6, 6], [0, 3, 4, 6, 1, 6], \
            [0, 3, 4, 6, 4, 5, 1, 6, 3, 6], [0, 3, 4, 6, 3, 5, 3], [0, 3, 4, 6, 2, 6, 3, 3, 3, 7], \
            [0, 3, 4, 6, 3, 6, 3, 6, 1, 7], [0, 4, 4, 6, 3, 6, 3, 6, 1, 7], [0, 6, 2, 1, 6, 3, 4, 1, 7, 7, 7], \
            [0, 6, 6, 2, 6, 2, 5, 6, 7], [0, 2, 1, 1, 1], [0, 1, 6, 6, 6, 7], [0, 7, 3, 3, 7, 4], [0])
            #loop on mainmenu and permissions in table accounts
            for menu in range(0,16):
                menuperms = lineperm[menu]
                perms = mp[menu]
                # if value in database is 0 for index 0 then disable mainmenulines
                if mp[menu][0] == '0':
                    mplist[menu].setDisabled(True)
                    mplist[menu].setStyleSheet("color: darkgrey; background-color: gainsboro")
                # subloop on menulines per menu
                # translate submenuline with linepointer from lineperm list, check if 0 in accounts table
                # if so disable menuline from selecting
                for lines in range(0,len(menuperms)):
                    linepointer = menuperms[lines]
                    mperm = perms[linepointer]
                    if mperm == '0' and linepointer > 0:
                         mplist[menu].model().item(lines).setEnabled(False)
                         mplist[menu].model().item(lines).setForeground(QColor('darkgrey'))
                         mplist[menu].model().item(lines).setBackground(QColor('gainsboro'))
            # combine account table functions with reprint functions, disable if 0
            if mp[8][5] == '0':
                mplist[15].model().item(1).setEnabled(False)
                mplist[15].model().item(1).setForeground(QColor('darkgrey'))
                mplist[15].model().item(1).setBackground(QColor('gainsboro'))
            if mp[9][5] == '0':
                mplist[15].model().item(2).setEnabled(False)
                mplist[15].model().item(2).setForeground(QColor('darkgrey'))
                mplist[15].model().item(2).setBackground(QColor('gainsboro'))
            if mp[3][5] == '0':
                mplist[15].model().item(3).setEnabled(False)
                mplist[15].model().item(3).setForeground(QColor('darkgrey'))
                mplist[15].model().item(3).setBackground(QColor('gainsboro'))
                mplist[15].model().item(12).setEnabled(False)
                mplist[15].model().item(12).setForeground(QColor('darkgrey'))
                mplist[15].model().item(12).setBackground(QColor('gainsboro'))
            if mp[6][5] == '0':
                mplist[15].model().item(4).setEnabled(False)
                mplist[15].model().item(4).setForeground(QColor('darkgrey'))
                mplist[15].model().item(4).setBackground(QColor('gainsboro'))
            if mp[7][5] == '0':
                mplist[15].model().item(5).setEnabled(False)
                mplist[15].model().item(5).setForeground(QColor('darkgrey'))
                mplist[15].model().item(5).setBackground(QColor('gainsboro'))
            if mp[5][5] == '0':
                mplist[15].model().item(6).setEnabled(False)
                mplist[15].model().item(6).setForeground(QColor('darkgrey'))
                mplist[15].model().item(6).setBackground(QColor('gainsboro'))
                mplist[15].model().item(7).setEnabled(False)
                mplist[15].model().item(7).setForeground(QColor('darkgrey'))
                mplist[15].model().item(7).setBackground(QColor('gainsboro'))
                mplist[15].model().item(13).setEnabled(False)
                mplist[15].model().item(13).setForeground(QColor('darkgrey'))
                mplist[15].model().item(13).setBackground(QColor('gainsboro'))
            if mp[3][5] == '0' or mp[3][7] == '0':
                mplist[15].model().item(14).setEnabled(False)
                mplist[15].model().item(14).setForeground(QColor('darkgrey'))
                mplist[15].model().item(14).setBackground(QColor('gainsboro'))
            if mp[10][5] == '0':
                mplist[15].model().item(8).setEnabled(False)
                mplist[15].model().item(8).setForeground(QColor('darkgrey'))
                mplist[15].model().item(8).setBackground(QColor('gainsboro'))
                mplist[15].model().item(9).setEnabled(False)
                mplist[15].model().item(9).setForeground(QColor('darkgrey'))
                mplist[15].model().item(9).setBackground(QColor('gainsboro'))
            if mp[11][5] == '0':
                mplist[15].model().item(10).setEnabled(False)
                mplist[15].model().item(10).setForeground(QColor('darkgrey'))
                mplist[15].model().item(10).setBackground(QColor('gainsboro'))
                mplist[15].model().item(11).setEnabled(False)
                mplist[15].model().item(11).setForeground(QColor('darkgrey'))
                mplist[15].model().item(11).setBackground(QColor('gainsboro'))

            grid = QGridLayout()
            grid.setSpacing(20)
             
            grid.addWidget(self.k0Edit, 2, 0)
            grid.addWidget(self.k8Edit, 2, 1)
            
            grid.addWidget(self.k1Edit, 3, 0)
            grid.addWidget(self.k9Edit, 3, 1)
            
            grid.addWidget(self.k2Edit, 4, 0)
            grid.addWidget(self.k10Edit, 4, 1)
            
            grid.addWidget(self.k3Edit, 5, 0)
            grid.addWidget(self.k11Edit, 5, 1)
          
            grid.addWidget(self.k4Edit, 6, 0)
            grid.addWidget(self.k12Edit, 6, 1)
        
            grid.addWidget(self.k5Edit, 7, 0)
            grid.addWidget(self.k13Edit, 7, 1)
            
            grid.addWidget(self.k6Edit, 8, 0)
            grid.addWidget(self.k14Edit, 8, 1)
            
            grid.addWidget(self.k7Edit, 9 ,0)
            grid.addWidget(self.k15Edit, 9, 1)
                            
            pandora = QLabel()
            pixmap = QPixmap('./images/logos/menu.png')
            pandora.setPixmap(pixmap)
            grid.addWidget(pandora, 0 ,0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 11, 1, 2, 1, Qt.AlignRight)
            
            pandora = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            pandora.setPixmap(pixmap)
            grid.addWidget(pandora, 11 ,0, 2, 1)
                                                       
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 14, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 100, 150, 150)

            cancelBtn = QPushButton('Uitloggen')
            cancelBtn.clicked.connect(lambda: closeIt(self))

            grid.addWidget(cancelBtn,13, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
                self.accept()
            self.k0Edit.currentIndexChanged.connect(k0Changed)

            def k1Changed():
                self.k1Edit.setCurrentIndex(self.k1Edit.currentIndex())
                self.accept()
            self.k1Edit.currentIndexChanged.connect(k1Changed)

            def k2Changed():
                self.k2Edit.setCurrentIndex(self.k2Edit.currentIndex())
                self.accept()
            self.k2Edit.currentIndexChanged.connect(k2Changed)

            def k3Changed():
                self.k3Edit.setCurrentIndex(self.k3Edit.currentIndex())
                self.accept()
            self.k3Edit.currentIndexChanged.connect(k3Changed)

            def k4Changed():
                self.k4Edit.setCurrentIndex(self.k4Edit.currentIndex())
                self.accept()
            self.k4Edit.currentIndexChanged.connect(k4Changed)

            def k5Changed():
                self.k5Edit.setCurrentIndex(self.k5Edit.currentIndex())
                self.accept()
            self.k5Edit.currentIndexChanged.connect(k5Changed)

            def k6Changed():
                self.k6Edit.setCurrentIndex(self.k6Edit.currentIndex())
                self.accept()
            self.k6Edit.currentIndexChanged.connect(k6Changed)

            def k7Changed():
                self.k7Edit.setCurrentIndex(self.k7Edit.currentIndex())
                self.accept()
            self.k7Edit.currentIndexChanged.connect(k7Changed)

            def k8Changed():
                self.k8Edit.setCurrentIndex(self.k8Edit.currentIndex())
                self.accept()
            self.k8Edit.currentIndexChanged.connect(k8Changed)

            def k9Changed():
                self.k9Edit.setCurrentIndex(self.k9Edit.currentIndex())
                self.accept()
            self.k9Edit.currentIndexChanged.connect(k9Changed)

            def k10Changed():
                self.k10Edit.setCurrentIndex(self.k10Edit.currentIndex())
                self.accept()
            self.k10Edit.currentIndexChanged.connect(k10Changed)

            def k11Changed():
                self.k11Edit.setCurrentIndex(self.k11Edit.currentIndex())
                self.accept()
            self.k11Edit.currentIndexChanged.connect(k11Changed)

            def k12Changed():
                self.k12Edit.setCurrentIndex(self.k12Edit.currentIndex())
                self.accept()
            self.k12Edit.currentIndexChanged.connect(k12Changed)

            def k13Changed():
                self.k13Edit.setCurrentIndex(self.k13Edit.currentIndex())
                self.accept()
            self.k13Edit.currentIndexChanged.connect(k13Changed)

            def k14Changed():
                self.k14Edit.setCurrentIndex(self.k14Edit.currentIndex())
                self.accept()
            self.k14Edit.currentIndexChanged.connect(k14Changed)

            def k15Changed():
                self.k15Edit.setCurrentIndex(self.k15Edit.currentIndex())
                self.accept()
            self.k15Edit.currentIndexChanged.connect(k15Changed)

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.k0Edit.currentIndex(), dialog.k1Edit.currentIndex(), dialog.k2Edit.currentIndex(), \
                    dialog.k3Edit.currentIndex(), dialog.k4Edit.currentIndex(), dialog.k5Edit.currentIndex(), \
                    dialog.k6Edit.currentIndex(), dialog.k7Edit.currentIndex(), dialog.k8Edit.currentIndex(), \
                    dialog.k9Edit.currentIndex(), dialog.k10Edit.currentIndex(), dialog.k11Edit.currentIndex(), \
                    dialog.k12Edit.currentIndex(), dialog.k13Edit.currentIndex(), dialog.k14Edit.currentIndex(), \
                    dialog.k15Edit.currentIndex()]

    window = Widget()
    dlist = window.getData()

    if dlist[0] == 1:
        import wijzAccount
        wijzAccount.updateAccount(m_email)
    elif dlist[0] == 2:
         import opvrAccounts
         opvrAccounts.accKeuze(m_email)
    elif dlist[0] == 3:
         klmail = ''
         import bestelOrder
         bestelOrder.artKeuze(m_email, 0, klmail)
    elif dlist[0] == 4:
        import opvrKlantenorders
        opvrKlantenorders.bestellingen(m_email)
    elif dlist[0] == 5:
        import printFacturen
        printFacturen.kiesOrder(m_email)
    elif dlist[1] == 1:
        import invoerLeverancier
        invoerLeverancier.bepaalLeverancier(m_email)
    elif dlist[1] == 2:
        import wijzLeverancier
        wijzLeverancier.zoekLeverancier(m_email)
    elif dlist[1] == 3:
        import opvrLeveranciers
        opvrLeveranciers.leveranciersKeuze(m_email)
    elif dlist[1] == 4:
        import opvrEigenleverancier
        opvrEigenleverancier.eigenLeverancier(m_email)
    elif dlist[2] == 1:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 0)
    elif dlist[2] == 2:
        import wijzWerknemer
        while True:
            wijzWerknemer.zoekWerknemer(m_email)
    elif dlist[2] == 3:
        import opvrWerknemers
        opvrWerknemers.accKeuze(m_email)
    elif dlist[2] == 4:
        import opvrWerknperiode
        opvrWerknperiode.zoekWerknemer(m_email)
    elif dlist[3] == 1:
        mlevnr = 3
        mregel = 1
        import invoerInkooporder
        invoerInkooporder.zoekLeverancier(m_email, mlevnr,mregel)
    elif dlist[3] == 2:
        import wijzInkooporder
        mregel = 0
        minkordernr = 4
        wijzInkooporder.zoekInkooporder(m_email, minkordernr, mregel)
    elif dlist[3] == 3:
        mlevnr = 3
        mwerknr = 8
        mregel = 1
        import invoerDienstenorder
        invoerDienstenorder.zoekLeverancier(m_email, mlevnr, mwerknr, mregel)
    elif dlist[3] == 4:
        import invoerEquipmentorder
        invoerEquipmentorder.calKeuze(m_email, int(mp[3][3]), int(mp[3][4]), int(mp[3][6]))
    elif dlist[3] == 5:
        import wijzDienstenorder
        mregel = 0
        minkordernr = 4
        wijzDienstenorder.zoekInkooporder(m_email, minkordernr, mregel)
    elif dlist[3] == 6:
        import opvrInkooporders
        opvrInkooporders.inkooporderKeuze(m_email)
    elif dlist[3] == 7:
        import opvrDienstenorders
        opvrDienstenorders.inkooporderKeuze(m_email)
    elif dlist[3] == 8:
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email)
    elif dlist[4] == 1:
        import invoerVerkoopbedrijf
        while True:
            invoerVerkoopbedrijf.invBedrijf(m_email)
    elif dlist[4] == 2:
        import wijzVerkoopbedrijf
        while True:
            wijzVerkoopbedrijf.zoekKoper(m_email)
    elif dlist[4] == 3:
        import opvrVerkoopbedrijven
        opvrVerkoopbedrijven.koperKeuze(m_email)
    elif dlist[4] == 4:
        import opvrEigenbedrijf
        opvrEigenbedrijf.eigenBedrijf(m_email)
    elif dlist[4] == 5:
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 2)
    elif dlist[5] == 1:
        import invoerArtikelen
        while True:
            invoerArtikelen.invArtikel(m_email)
    elif dlist[5] == 2:
        import wijzArtikel
        wijzArtikel.zoekArtikel(m_email)
    elif dlist[5] == 3:
        import opvrArtikelen
        opvrArtikelen.artKeuze(m_email)
    elif dlist[5] == 4:
        import magUitgifte
        magUitgifte.kiesSelektie(0, m_email)
    elif dlist[5] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(1, m_email)
    elif dlist[5] == 6:
        import dervingMutaties
        while True:
            dervingMutaties.dervingMut(m_email)
    elif dlist[5] == 7:
        import opvrWebverkorders
        while True:
            opvrWebverkorders.zoekWeborder(m_email, 0)
    elif dlist[5] == 8:
        import retourPortalWeb
        klmail = ''
        while True:
            retourPortalWeb.zoekEmailadres(m_email, klmail)
    elif dlist[5] == 9:
        if mp[5][1] == '1':
            mret = True
        else:
            mret = False
        import barcodeScan
        barcodeScan.barcodeScan(m_email, mret)
    elif dlist[6] == 1:
        import invoerInternorder
        invoerInternorder.invWerkorder(m_email)
    elif dlist[6] == 2:
        import wijzInternorder
        wijzInternorder.zoeken(m_email)
    elif dlist[6] == 3:
        import opvrInternorders
        opvrInternorders.zoeken(m_email)
    elif dlist[6] == 4 :
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 0)
    elif dlist[6] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(2, m_email)
    elif dlist[6] == 6:
        import urenImutaties
        maccountnr = '1'
        mwerknr = 7
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenImutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
            # for convenience start with last used work , employee and mboekd
            try:
                maccountnr = accwerk[0]
                mwerknr = accwerk[1]
                mboekd = accwerk[2]
            except:
                maccountnr = '1'
                mwerknr = '7'
                mboekd = str(datetime.now())[0:10]
    elif dlist[7] == 1:
        import invoerWerken
        invoerWerken.invWerk(m_email)
    elif dlist[7] == 2:
        import wijzWerken
        wijzWerken.zoekWerk(m_email)
    elif dlist[7] == 3:
        import opvrWerken
        opvrWerken.werkenKeuze(m_email)
    elif dlist[7] == 4:
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 1)
    elif dlist[7] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(3, m_email)
    elif dlist[7] == 6:
        import dienstenMutaties
        dienstenMutaties.mutatieKeuze(m_email)
    elif dlist[7] == 7:
        import urenMutaties
        maccountnr = '1'
        mwerknr = '8'
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenMutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
            # for convenience start with last used work , employee and mboekd
            try:
                maccountnr = accwerk[0]
                mwerknr = accwerk[1]
                mboekd = accwerk[2]
            except:
                maccountnr = '1'
                mwerknr = '8'
                mboekd = str(datetime.now())[0:10]
    elif dlist[7] == 8:
        import materieel_urenMutaties
        mservicenr = 1
        mwerknr = '8'
        mboekd = str(datetime.now())[0:10]
        while True:
            servicewerk = materieel_urenMutaties.urenMut(mservicenr, mwerknr, mboekd, m_email)
            # for convenience start with last used equipment, work and bookdate
            try:
                mservicenr = servicewerk[0]
                mwerknr = servicewerk[1]
                mboekd = servicewerk[2]
            except:
                mservicenr = 1
                mwerknr = '8'
                mboekd = str(datetime.now())[0:10]
    elif dlist[7] == 9:
        import params_services
        params_services.chooseSubMenu(m_email, int(mp[7][6]), int(mp[7][4]), int(mp[7][3]))
    elif dlist[8] == 1:
        import maakIcluster
        while True:
            maakIcluster.kiesCluster(m_email)
    elif dlist[8] == 2:
        import wijzIclusters
        while True:
            wijzIclusters.zoeken(m_email)
    elif dlist[8] == 3:
        import opvrIclusters
        opvrIclusters.zoeken(m_email)
    elif dlist[8] == 4:
        import invoerIcluster_artikelen
        while True:
            invoerIcluster_artikelen.zoeken(m_email)
    elif dlist[8] == 5:
        import opvrIcluster_artikelen
        opvrIcluster_artikelen.zoeken(m_email)
    elif dlist[8] == 6:
        import invoerIclustercalculatie
        invoerIclustercalculatie.zoeken(m_email)
    elif dlist[8] == 7:
        import opvrIclustercalculatie
        while True:
            opvrIclustercalculatie.zoekCalculatie(m_email)
    elif dlist[8] == 8:
        import koppelIbegroting
        while True:
            koppelIbegroting.zoekBegroting(m_email)
    elif dlist[8] == 9:
        sector = 'internal'
        import modifyStruct
        modifyStruct.menuStructure(sector, m_email) #internal works
    elif dlist[9] == 1:
        import maakCluster
        while True:
            maakCluster.kiesCluster(m_email)
    elif dlist[9] == 2:
        import wijzClusters
        while True:
            wijzClusters.zoeken(m_email)
    elif dlist[9] == 3:
        import opvrClusters
        opvrClusters.zoeken(m_email)
    elif dlist[9] == 4:
        import invoerCluster_artikelen
        while True:
            invoerCluster_artikelen.zoeken(m_email)
    elif dlist[9] == 5:
        import opvrCluster_artikelen
        opvrCluster_artikelen.zoeken(m_email)
    elif dlist[9] == 6:
        import invoerClustercalculatie
        while True:
            invoerClustercalculatie.zoeken(m_email)
    elif dlist[9] == 7:
        import opvrClustercalculatie
        while True:
            opvrClustercalculatie.zoekCalculatie(m_email)
    elif dlist[9] == 8:
        import koppelBegroting
        while True:
            koppelBegroting.zoekBegroting(m_email)
    elif dlist[9] == 9:
        sector = 'external'
        import modifyStruct
        modifyStruct.menuStructure(sector, m_email) # external
    elif dlist[10] == 1:
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif dlist[10] == 2:
        import proefrun
        proefrun.maandPeriode(m_email)
    elif dlist[10] == 3:
        import uitbetalenLonen
        uitbetalenLonen.maandBetalingen(m_email)
    elif dlist[10] == 4:
        import opvrLoonbetalingen
        opvrLoonbetalingen.zoeken(m_email)
    elif dlist[10] == 5:
        import invoerLoontabel
        while True:
            invoerLoontabel.invoerSchaal(m_email)
    elif dlist[10] == 6:
        import wijzLoontabel
        wijzLoontabel.zoeken(m_email)
    elif dlist[10] == 7:
        import percentageLonen
        while True:
            percentageLonen.percLoonschaal(m_email)
    elif dlist[10] == 8:
        import params_hours
        params_hours.chooseSubMenu(m_email, int(mp[10][6]), int(mp[10][4]), int(mp[10][3]))
    elif dlist[10] == 9:
        import params_wages
        params_wages.chooseSubMenu(m_email, int(mp[10][6]), int(mp[10][4]), int(mp[10][3]))
    elif dlist[10] == 10:
        import params_periods
        params_periods.chooseSubMenu(m_email, int(mp[10][6]), int(mp[10][4]), int(mp[10][3]))
    elif dlist[11] == 1:
        import opvrArtikelmutaties
        opvrArtikelmutaties.mutatieKeuze(m_email)
    elif dlist[11] == 2:
        import opvrDienstenmutaties
        opvrDienstenmutaties.mutatieKeuze(m_email)
    elif dlist[11] == 3:
        import afdrBetalen
        afdrBetalen.zoeken(m_email)
    elif dlist[11] == 4:
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 1)
    elif dlist[11] == 5:
        import webRetouren
        webRetouren.retKeuze(m_email)
    elif dlist[11] == 6:
        import printFacturatie
        printFacturatie.maakLijst(m_email)
    elif dlist[11] == 7:
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif dlist[11] == 8:
        import params_finance
        params_finance.chooseSubMenu(m_email, int(mp[11][6]), int(mp[11][4]), int(mp[11][3]))
    elif dlist[12] == 1:
        import voorraadbeheersing
        voorraadbeheersing.vrdKeuze(m_email)
    elif dlist[12] == 2:
        import magvrdGrafiek
        magvrdGrafiek.toonGrafiek(m_email)
    elif dlist[12] == 3:
        import magvrdGrafiek
        magvrdGrafiek.magVoorraad(m_email)
    elif dlist[12] == 4:
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email)
    elif dlist[13]== 1:
        import rapportage
        rapportage.JN(m_email)
    elif dlist[13] == 2:
        import toonGrafieken
        toonGrafieken.zoekwk(m_email)
    elif dlist[13] == 3:
        import voortgangGrafiek
        while True:
            voortgangGrafiek.zoekwk(m_email)
    elif dlist[13] == 4:
        import toonResultaten
        toonResultaten.toonResult(m_email)
    elif dlist[13] == 5:
        import params_graphs
        params_graphs.chooseSubMenu(m_email, int(mp[13][6]),int(mp[13][3]), int(mp[13][2]))
    elif dlist[14] == 1:
        import maakAuthorisatie
        while True:
             maakAuthorisatie.zoekAccount(m_email)
    elif dlist[14] == 2:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 2)
    elif dlist[14] == 3:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 1)
    elif dlist[14] == 4:
        import params_system
        params_system.chooseSubMenu(m_email, int(mp[14][6]), int(mp[14][4]), int(mp[14][3]))
    elif dlist[14] == 5:
        import wijzWerktarief
        wijzWerktarief.winKeuze(m_email)
    elif dlist[15] == 1:
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Clustercalculaties\\'
        else:
            path = './forms/Intern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 2:
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties\\'
        else:
            path = './forms/Extern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 3:
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Orderbrieven\\'
        else:
            path = './forms/Intern_Orderbrieven/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 4:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 5:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 6:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 7:
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Pakbonnen\\'
        else:
            path = './forms/Weborders_Pakbonnen/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 8:
        if sys.platform == 'win32':
            path = '.\\forms\\Uren\\'
        else:
            path = './forms/Uren/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 9:
        if sys.platform == 'win32':
            path = '.\\forms\\Lonen\\'
        else:
            path = './forms/Lonen/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 10:
        if sys.platform == 'win32':
            path = '.\\forms\\Facturen_Werken\\'
        else:
            path = './forms/Facturen_Werken/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 11:
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Facturen\\'
        else:
            path = './forms/Weborders_Facturen/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 12:
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties_Diensten\\'
        else:
            path = './forms/Extern_Clustercalculaties_Diensten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 13:
        if sys.platform == 'win32':
            path = '.\\forms\\Barcodelijsten\\'
        else:
            path = './forms/Barcodelijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 14:
        if sys.platform == 'win32':
            path = '.\\forms\\Equipment_Orders\\'
        else:
            path = './forms/Equipment_Orders/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    else:
        hoofdMenu(m_email)
inlog()
