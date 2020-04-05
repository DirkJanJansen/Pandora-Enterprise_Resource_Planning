import os, sys
from datetime import datetime
from validZt import zt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon, QMovie
from PyQt5.QtWidgets import (QDialog, QGridLayout, QMessageBox,\
                             QLabel, QLineEdit, QPushButton, QComboBox)
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                    create_engine, select)

def check_password(hashed_password, user_password):
    import hashlib
    (password, salt) = hashed_password.split(':')
    return (password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())

def totZiens():
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    # release lock
    home = os.path.expanduser("~")
    os.remove(str(home)+'/.pandora_lock')
    msg.setText('Tot ziens!       ')
    msg.setWindowTitle('Loginscherm')
    msg.exec_()
     
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
    
def geenMenu():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Dit is de titelregel, kies een menuregel!')
    msg.setWindowTitle('Geen Menukeuze')
    msg.exec_()

def geenToegang():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('U bent niet geauthoriseerd voor deze keuze')
    msg.setWindowTitle('AUTHORISATIE')
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
            
            self.email = QLabel()
            emailEdit = QLineEdit()
            emailEdit.setStyleSheet("background: #F8F7EE")
            emailEdit.setFixedWidth(200)
            emailEdit.setFont(QFont("Arial",10))
            emailEdit.textChanged.connect(self.emailChanged)

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
                 
            grid.addWidget(QLabel('emailadres of\nKlantnummer'), 3, 1)
            grid.addWidget(emailEdit, 3, 2)
    
            grid.addWidget(QLabel('Wachtwoord'), 4, 1)
            grid.addWidget(wachtwEdit, 4, 2)
                                   
            self.setLayout(grid)
            self.setGeometry(600, 250, 150, 150)
            
            applyBtn = QPushButton('Login')
            applyBtn.clicked.connect(self.accept)
            
            grid.addWidget(applyBtn, 5, 1, 1 , 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(90)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                       
            cancelBtn = QPushButton('Afsluiten')
            cancelBtn.clicked.connect(lambda: sys.exit(totZiens()))
                                      
            grid.addWidget(cancelBtn,  5, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            nwBtn = QPushButton('Nieuw Account')
            nwBtn.clicked.connect(lambda: maakAccount(self))
            
            grid.addWidget(nwBtn,  5, 0, 1, 2, Qt.AlignRight)
            nwBtn.setFont(QFont("Arial",10))
            nwBtn.setFixedWidth(140)
            nwBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
            
            grid.addWidget(infoBtn,  5, 0, 1, 2)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")           
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3, Qt.AlignCenter)
                       
        def emailChanged(self, text):
            self.email.setText(text)
        
        def wachtwChanged(self, text):
            self.Wachtwoord.setText(text)
        
        def returnemail(self):
            return self.email.text()
        
        def returnWachtwoord(self):
            return self.Wachtwoord.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnemail(), dialog.returnWachtwoord()]

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
        import subprocess
        if (subprocess.getoutput("xset q | grep LED")[65]) == '1':
            capslkOn()
            inlog()
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False),
        Column('password', String, nullable=False))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if data[0] and zt(data[0],12):
        m_email = data[0]
        sel = select([accounts]).where(accounts.c.email == m_email)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            maccountnr = rpaccount[0]
            maccountnr = int(maccountnr)
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            foutemailAdres()
            inlog()
    elif data[0] and zt(data[0],1):
        mklantnr = data[0]
        sel = select([accounts]).where(accounts.c.accountID == mklantnr)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            maccountnr = rpaccount[0]
            maccountnr = int(maccountnr)
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            foutKlantnummer()
            inlog()
    else:
        foutInlog()
        inlog()
       
    if data[1]:
        mwachtw = data[1]
    else:
        foutWachtw()
        inlog()

    if not check_password(mpassword,mwachtw):
        foutWachtw()
        inlog()
    hoofdMenu(m_email)
       
def hoofdMenu(m_email):
    #structure Menu's
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora bedrijfs informatie systeem")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
            self.Keuze0 = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(290)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                    Accounts')
            k0Edit.addItem('1. Wijzigen account') 
            k0Edit.addItem('2. Opvragen accounts')
            k0Edit.addItem('3. Bestellen webartikelen')
            k0Edit.addItem('4. Opvragen besteloverzicht')
            k0Edit.addItem('5. Printen orderfacturen')
            k0Edit.activated[str].connect(self.k0Changed)
             
            self.Keuze1 = QLabel()
            k1Edit = QComboBox()
            k1Edit.setFixedWidth(290)
            k1Edit.setFont(QFont("Arial",10))
            k1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k1Edit.addItem('                  Leveranciers')
            k1Edit.addItem('1. Invoeren leveranciergegevens')
            k1Edit.addItem('2. Wijzigen leveranciergegevens')
            k1Edit.addItem('3. Opvragen leveranciergegevens')
            k1Edit.addItem('4. Zelf gegevens opvragen.')
            k1Edit.activated[str].connect(self.k1Changed)
            
            self.Keuze2 = QLabel()
            k2Edit = QComboBox()
            k2Edit.setFixedWidth(290)
            k2Edit.setFont(QFont("Arial",10))
            k2Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k2Edit.addItem('                   Werknemers')
            k2Edit.addItem('1. Koppelen account-werknemer')
            k2Edit.addItem('2. Wijzigen werknemergegevens')
            k2Edit.addItem('3. Opvragen werknemersgegevens')
            k2Edit.addItem('4. Opvragen werknemer-periode')
            k2Edit.activated[str].connect(self.k2Changed)
            
            self.Keuze3 = QLabel()
            k3Edit = QComboBox()
            k3Edit.setFixedWidth(290)
            k3Edit.setFont(QFont("Arial",10))
            k3Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k3Edit.addItem('                      Inkoop')
            k3Edit.addItem('1. Invoeren orders materialen')
            k3Edit.addItem('2. Wijzigen orders materialen')
            k3Edit.addItem('3. Invoeren orders diensten')
            k3Edit.addItem('4. Wijzigen orders diensten')
            k3Edit.addItem('5. Opvragen orders materialen')
            k3Edit.addItem('6. Opvragen orders diensten')
            k3Edit.activated[str].connect(self.k3Changed)
            
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(290)
            k4Edit.setFont(QFont("Arial",10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem('                     Verkoop')
            k4Edit.addItem('1. Verkoop-bedrijf aanmaken')
            k4Edit.addItem('2. Verkoop-bedrijf wijzigen')
            k4Edit.addItem('3. Verkoop-bedrijven opvragen')
            k4Edit.addItem('4. Zelf gegevens opvragen')
            k4Edit.addItem('5. Webverkooporders opvragen')
            k4Edit.activated[str].connect(self.k4Changed)
 
            self.Keuze5 = QLabel()
            k5Edit = QComboBox()
            k5Edit.setFixedWidth(290)
            k5Edit.setFont(QFont("Arial",10))
            k5Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k5Edit.addItem('                    Magazijn')
            k5Edit.addItem('1. Invoeren artikelen')
            k5Edit.addItem('2. Wijzigen artikelen')
            k5Edit.addItem('3. Opvragen artikelen')
            k5Edit.addItem('4. Uitgifte materialen (raaplijst)')
            k5Edit.addItem('5. Printen raaplijsten')
            k5Edit.addItem('6. Incourant / Magazijnverschillen\n    Afkeur of bombage boeken')
            k5Edit.addItem('7. Uitgifte webartikelen /\n    printen pakbon')
            k5Edit.addItem('8. Web-artikelen retour boeken')
            k5Edit.addItem('9. Balieverkoop - barcodescan')
            k5Edit.activated[str].connect(self.k5Changed)
              
            self.Keuze6 = QLabel()
            k6Edit = QComboBox()
            k6Edit.setFixedWidth(290)
            k6Edit.setFont(QFont("Arial",10))
            k6Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k6Edit.addItem('                  Werken intern')
            k6Edit.addItem('1. Invoer werkopdrachten')
            k6Edit.addItem('2. Wijzig werkopdrachten')
            k6Edit.addItem('3. Opvragen werkopdrachten\n    Printen Werkbrief')
            k6Edit.addItem('4. Afroepen materialen')
            k6Edit.addItem('5. Printen raaplijsten')
            k6Edit.addItem('6. Uurverbruik muteren')
            k6Edit.activated[str].connect(self.k6Changed)
            
            self.Keuze7 = QLabel()
            k7Edit = QComboBox()
            k7Edit.setFixedWidth(290)
            k7Edit.setFont(QFont("Arial",10))
            k7Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k7Edit.addItem('                Werken extern')
            k7Edit.addItem('1. Invoeren werken')
            k7Edit.addItem('2. Wijzigen werken')
            k7Edit.addItem('3. Opvragen werken')
            k7Edit.addItem('4. Afroepen materialen')
            k7Edit.addItem('5. Printen raaplijsten')
            k7Edit.addItem('6. Muteren kosten diensten')
            k7Edit.addItem('7. Uurverbruik muteren')
            k7Edit.activated[str].connect(self.k7Changed)
            
            self.Keuze8 = QLabel()
            k8Edit = QComboBox()
            k8Edit.setFixedWidth(290)
            k8Edit.setFont(QFont("Arial",10))
            k8Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k8Edit.addItem('        Calculatie interne werken')
            k8Edit.addItem('1. Nieuwe clusters aanmaken')
            k8Edit.addItem('2. Clustergegevens invoeren')
            k8Edit.addItem('3. Clustergegevens opvragen')
            k8Edit.addItem('4. Invoeren artikelregels per cluster')
            k8Edit.addItem('5. Opvragen artikelregels per cluster')
            k8Edit.addItem('6. Calculatie maken / wijzigen')
            k8Edit.addItem('7. Calculatie / Artikellijst - \n    berekenen / opvragen / printen')
            k8Edit.addItem('8. Calculatie koppelen -> produktie')
            k8Edit.activated[str].connect(self.k8Changed)
        
            self.Keuze9 = QLabel()
            k9Edit = QComboBox()
            k9Edit.setFixedWidth(290)
            k9Edit.setFont(QFont("Arial",10))
            k9Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k9Edit.addItem('        Calculatie externe werken')
            k9Edit.addItem('1. Nieuwe clusters aanmaken')
            k9Edit.addItem('2. Clustergegevens invoeren')
            k9Edit.addItem('3. Clustergegevens opvragen')
            k9Edit.addItem('4. Invoeren artikelregels per cluster')
            k9Edit.addItem('5. Opvragen artikelregels per cluster')
            k9Edit.addItem('6. Calculatie maken / wijzigen')
            k9Edit.addItem('7. Calculatie / Artikellijst - \n    berekenen / opvragen / printen')
            k9Edit.addItem('8. Calculatie koppelen -> produktie')
            k9Edit.activated[str].connect(self.k9Changed)
  
            self.Keuze10 = QLabel()
            k10Edit = QComboBox()
            k10Edit.setFixedWidth(290)
            k10Edit.setFont(QFont("Arial",10))
            k10Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k10Edit.addItem('               Loonadministratie')
            k10Edit.addItem('1. Uren mutaties opvragen')
            k10Edit.addItem('2. Controle uren tbv maanlonen')
            k10Edit.addItem('3. Maandelijkse loonbetalingen')
            k10Edit.addItem('4. Opvragen loonbetalingen')
            k10Edit.addItem('5. Invoeren Loonschalen')
            k10Edit.addItem('6. Loonschalen wijzigen / opvragen')
            k10Edit.addItem('7. Procentueel lonen verhogen')
            k10Edit.activated[str].connect(self.k10Changed)
            
            self.Keuze11 = QLabel()
            k11Edit = QComboBox()
            k11Edit.setFixedWidth(290)
            k11Edit.setFont(QFont("Arial",10))
            k11Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k11Edit.addItem('                 Boekhouding')
            k11Edit.addItem('1. Artikel mutaties opvragen.')
            k11Edit.addItem('2. Diensten mutaties opvragen')
            k11Edit.addItem('3. Inzien en betalen afdrachten')
            k11Edit.addItem('4. Weborders betalingen /\n    printen factuur')
            k11Edit.addItem('5. Retouren betalingen boeken')
            k11Edit.addItem('6. Printen lijst te factureren\n    bedragen van externe werken')
            k11Edit.addItem('7. Uren mutaties opvragen')
            k11Edit.activated[str].connect(self.k11Changed)
            
            self.Keuze12 = QLabel()
            k12Edit = QComboBox()
            k12Edit.setFixedWidth(290)
            k12Edit.setFont(QFont("Arial",10))
            k12Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k12Edit.addItem('             Voorraadmanagement')
            k12Edit.addItem('1. Voorraadbeheersing\n    bestellen artikelen')
            k12Edit.addItem('2. Grafiek voorraden \n    magazijn financiëel') 
            k12Edit.addItem('3. Overzicht voorraden financiëel')
            k12Edit.addItem('4. Opvragen reserveringen')
            k12Edit.activated[str].connect(self.k12Changed)
            
            self.Keuze13 = QLabel()
            k13Edit = QComboBox()
            k13Edit.setFixedWidth(290)
            k13Edit.setFont(QFont("Arial",10))
            k13Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k13Edit.addItem('           Management informatie')
            k13Edit.addItem('1. Berekenen financiëele gegevens\n    eind iedere week uitvoeren')
            k13Edit.addItem('2. Printen grafieken financiëele\n    overzichten externe werken')
            k13Edit.addItem('3. Printen grafieken aantal werken\n    extern voortgangstatus')
            k13Edit.addItem('4. Opvragen resultaten werken')
            k13Edit.activated[str].connect(self.k13Changed) 
         
            self.Keuze14 = QLabel()
            k14Edit = QComboBox()
            k14Edit.setFixedWidth(290)
            k14Edit.setFont(QFont("Arial",10))
            k14Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k14Edit.addItem('                   Onderhoud')
            k14Edit.addItem('1. Bevoegdheden muteren')
            k14Edit.addItem('2. Koppel account-leverancier')
            k14Edit.addItem('3. Koppel account-verkoopbedrijf')
            k14Edit.addItem('4. Invoeren parameters')
            k14Edit.addItem('5. Wijzigen parameters')
            k14Edit.addItem('6. Opvragen parameters')
            k14Edit.addItem('7. Verkoop-werktarieven bijwerken')
            k14Edit.activated[str].connect(self.k14Changed)

            self.Keuze15 = QLabel()
            k15Edit = QComboBox()
            k15Edit.setFixedWidth(290)
            k15Edit.setFont(QFont("Arial",10))
            k15Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k15Edit.addItem('      Herprinten van formulieren')
            k15Edit.addItem('1. Calculatie interne werken') 
            k15Edit.addItem('2. Calculatie externe werken')  
            k15Edit.addItem('3. Interne orderbrieven tbv inkoop')
            k15Edit.addItem('4. Afroepen werken intern')
            k15Edit.addItem('5. Afroepen werken extern')
            k15Edit.addItem('6. Raaplijsten magazijn')
            k15Edit.addItem('7. Web orders pakbon')
            k15Edit.addItem('8. Controle uren tbv lonen')
            k15Edit.addItem('9. Loonspecificaties personeel')
            k15Edit.addItem('A. Factureren externe werken')
            k15Edit.addItem('B. Web orders betalingen') 
            k15Edit.addItem('C. Inkooporders diensten/materieel')  
            k15Edit.addItem('D. Balieverkoop orderfacturen') 
            k15Edit.activated[str].connect(self.k15Changed)
            
            #disable menu's if no permission is granted in table accounts
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
            mplist=[k0Edit,k1Edit,k2Edit,k3Edit,k4Edit,k5Edit,k6Edit,k7Edit,\
                    k8Edit,k9Edit,k10Edit,k11Edit,k12Edit,k13Edit,k14Edit,k15Edit]
            for k in range(0,16):
                if mp[k][0] == '0':
                    mplist[k].setDisabled(True)
                    mplist[k].setStyleSheet("color: darkgrey; background-color: gainsboro")
 
            grid = QGridLayout()
            grid.setSpacing(20)
             
            grid.addWidget(k0Edit, 2, 0)
            grid.addWidget(k8Edit, 2, 1)
            
            grid.addWidget(k1Edit, 3, 0)
            grid.addWidget(k9Edit, 3, 1)
            
            grid.addWidget(k2Edit, 4, 0)
            grid.addWidget(k10Edit, 4, 1)
            
            grid.addWidget(k3Edit, 5, 0)
            grid.addWidget(k11Edit, 5, 1)
          
            grid.addWidget(k4Edit, 6, 0)
            grid.addWidget(k12Edit, 6, 1)
        
            grid.addWidget(k5Edit, 7, 0)
            grid.addWidget(k13Edit, 7, 1)
            
            grid.addWidget(k6Edit, 8, 0)
            grid.addWidget(k14Edit, 8, 1)
            
            grid.addWidget(k7Edit, 9 ,0)
            grid.addWidget(k15Edit, 9, 1)
                            
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
            
            applyBtn = QPushButton('Kiezen')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 13, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Times",10))
            applyBtn.setFixedWidth(130)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Uitloggen')
            cancelBtn.clicked.connect(lambda: closeIt(self))
    
            grid.addWidget(cancelBtn, 13, 1)
            cancelBtn.setFont(QFont("Times",10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
        def k0Changed(self, text):
            self.Keuze0.setText(text)
    
        def k1Changed(self, text):
            self.Keuze1.setText(text)
            
        def k2Changed(self,text):
            self.Keuze2.setText(text)
            
        def k3Changed(self,text):
             self.Keuze3.setText(text)
            
        def k4Changed(self,text):
             self.Keuze4.setText(text)
            
        def k5Changed(self,text):
             self.Keuze5.setText(text)
            
        def k6Changed(self,text):
            self.Keuze6.setText(text)
            
        def k7Changed(self,text):
            self.Keuze7.setText(text)
               
        def k8Changed(self,text):
            self.Keuze8.setText(text)
            
        def k9Changed(self,text):
            self.Keuze9.setText(text)
            
        def k10Changed(self,text):
            self.Keuze10.setText(text)
            
        def k11Changed(self,text):
            self.Keuze11.setText(text)
            
        def k12Changed(self,text):
            self.Keuze12.setText(text)
            
        def k13Changed(self,text):
            self.Keuze13.setText(text)
            
        def k14Changed(self,text):
            self.Keuze14.setText(text)
            
        def k15Changed(self,text):
            self.Keuze15.setText(text)
    
        def returnk0(self):
            return self.Keuze0.text()
    
        def returnk1(self):
            return self.Keuze1.text()
    
        def returnk2(self):
            return self.Keuze2.text()
        
        def returnk3(self):
            return self.Keuze3.text()
      
        def returnk4(self):
            return self.Keuze4.text()
    
        def returnk5(self):
            return self.Keuze5.text()
    
        def returnk6(self):
            return self.Keuze6.text()
        
        def returnk7(self):
            return self.Keuze7.text()
        
        def returnk8(self):
            return self.Keuze8.text()
        
        def returnk9(self):
            return self.Keuze9.text()   
        
        def returnk10(self):
            return self.Keuze10.text()
        
        def returnk11(self):
            return self.Keuze11.text()
        
        def returnk12(self):
            return self.Keuze12.text()
        
        def returnk13(self):
            return self.Keuze13.text()
        
        def returnk14(self):
            return self.Keuze14.text()
        
        def returnk15(self):
            return self.Keuze15.text()
       
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnk1(),dialog.returnk2(),\
                dialog.returnk3(), dialog.returnk4(), dialog.returnk5(),\
                dialog.returnk6(), dialog.returnk7(),  dialog.returnk8(),\
                dialog.returnk9(), dialog.returnk10(), dialog.returnk11(),\
                dialog.returnk12(), dialog.returnk13(), dialog.returnk14(),\
                dialog.returnk15()]
      
    window = Widget()
    data = window.getData()
   
    #grant/deny access to submenuitems if permission not granted in table accounts
    
    mk0, mk1, mk2, mk3, mk4, mk5, mk6, mk7, mk8, mk9, mk10, mk11, mk12, mk13, mk14, mk15 = (0,)*16
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
    dlist = []
    for item in data:
        if item.startswith(' '):
            item = ''
        dlist += [item]
    del data
    if dlist[0]:
        mk0 = dlist[0][0]
    elif dlist[1]:
        mk1 = dlist[1][0]
    elif dlist[2]:
        mk2 = dlist[2][0]
    elif dlist[3]:
        mk3 = dlist[3][0]
    elif dlist[4]:
        mk4 = dlist[4][0]
    elif dlist[5]:
        mk5 = dlist[5][0]
    elif dlist[6]:
        mk6 = dlist[6][0]
    elif dlist[7]:
        mk7 = dlist[7][0]
    elif dlist[8]:
        mk8 = dlist[8][0]
    elif dlist[9]:
        mk9 = dlist[9][0]
    elif dlist[10]:
        mk10 = dlist[10][0]
    elif dlist[11]:
        mk11 = dlist[11][0]
    elif dlist[12]:
        mk12 = dlist[12][0]
    elif dlist[13]:
        mk13 = dlist[13][0]
    elif dlist[14]:
        mk14 = dlist[14][0]
    elif dlist[15]:
        mk15 = dlist[15][0] 
    else:
        geenMenu()
        hoofdMenu(m_email)

    if mk0 == '1' and mp[0][4] == '1':
        import wijzAccount
        wijzAccount.updateAccount(m_email)
    elif mk0 == '2' and mp[0][6] == '1':
         import opvrAccounts
         opvrAccounts.accKeuze(m_email)
    elif mk0 == '3' and mp[0][2] == '1': 
         klmail = '' 
         import bestelOrder
         bestelOrder.artKeuze(m_email, 0, klmail)
    elif mk0 == '4' and mp[0][6] == '1':
        import opvrKlantenorders
        opvrKlantenorders.bestellingen(m_email)
    elif mk0 == '5' and mp[0][5] == '1':
        import printFacturen
        printFacturen.kiesOrder(m_email)
    elif mk1 == '1' and mp[1][3] == '1':
        import invoerLeverancier
        invoerLeverancier.bepaalLeverancier(m_email)
    elif mk1 == '2' and mp[1][4] == '1':
        import wijzLeverancier
        wijzLeverancier.zoekLeverancier(m_email)
    elif mk1 == '3' and mp[1][6] == '1':
        import opvrLeveranciers
        opvrLeveranciers.leveranciersKeuze(m_email)
    elif mk1 == '4' and mp[1][1]:
        import opvrEigenleverancier
        opvrEigenleverancier.eigenLeverancier(m_email)
    elif mk2 == '1' and mp[2][1] == '1':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 0)
    elif mk2 == '2' and mp[2][4] == '1':
        import wijzWerknemer
        while True:
            wijzWerknemer.zoekWerknemer(m_email)
    elif mk2 == '3' and mp[2][6] == '1':
        import opvrWerknemers
        opvrWerknemers.accKeuze(m_email)
    elif mk2 == '4' and mp[2][6] == '1':
        import opvrWerknperiode
        opvrWerknperiode.zoekWerknemer(m_email)
    elif mk3 == '1' and mp[3][3] == '1':
        mlevnr = 3
        mregel = 1
        import invoerInkooporder
        invoerInkooporder.zoekLeverancier(m_email, mlevnr,mregel)
    elif mk3 == '2' and mp[3][4] == '1':
        import wijzInkooporder
        mregel = 0
        minkordernr = 4
        wijzInkooporder.zoekInkooporder(m_email, minkordernr, mregel)
    elif mk3 == '3' and mp[3][3] == '1':
        mlevnr = 3
        mwerknr = 8
        mregel = 1
        import invoerDienstenorder
        invoerDienstenorder.zoekLeverancier(m_email, mlevnr, mwerknr, mregel)
    elif mk3 == '4' and mp[3][4] == '1':
        import wijzDienstenorder
        mregel = 0
        minkordernr = 4
        wijzDienstenorder.zoekInkooporder(m_email, minkordernr, mregel)
    elif mk3 == '5' and mp[3][6] == '1':
        import opvrInkooporders
        opvrInkooporders.inkooporderKeuze(m_email)
    elif mk3 == '6' and mp[3][6] == '1':
        import opvrDienstenorders
        opvrDienstenorders.inkooporderKeuze(m_email)
    elif mk3 == '7' and mp[3][6] == '1':
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email) 
    elif mk4 == '1' and mp[4][3] == '1' :
        import invoerVerkoopbedrijf
        while True:
            invoerVerkoopbedrijf.invBedrijf(m_email)
    elif mk4 == '2' and mp[4][4] == '1' :
        import wijzVerkoopbedrijf
        while True:
            wijzVerkoopbedrijf.zoekKoper(m_email)
    elif mk4 == '3' and mp[4][6] == '1' :
        import opvrVerkoopbedrijven
        opvrVerkoopbedrijven.koperKeuze(m_email)
    elif mk4 == '4' and mp[4][1] == '1' :
        import opvrEigenbedrijf
        opvrEigenbedrijf.eigenBedrijf(m_email)
    elif mk4 == '5' and mp[4][6] == '1' :
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 2) 
    elif mk5 == '1' and mp[5][3] == '1':
        import invoerArtikelen
        while True:
            invoerArtikelen.invArtikel(m_email)
    elif mk5 == '2' and mp[5][4] == '1':
        import wijzArtikel
        wijzArtikel.zoekArtikel(m_email)
    elif mk5 == '3' and mp[5][6] == '1':
        import opvrArtikelen
        opvrArtikelen.artKeuze(m_email)
    elif mk5 == '4' and mp[5][4] == '1':
        import magUitgifte
        magUitgifte.kiesSelektie(0, m_email)
    elif mk5 == '5' and mp[5][5] == '1':
        import magUitgifte
        magUitgifte.kiesSelektie(1, m_email)
    elif mk5 == '6' and mp[5][1] == '1':
        import dervingMutaties
        while True:
            dervingMutaties.dervingMut(m_email)
    elif mk5 == '7' and mp[5][6] == '1':
        import opvrWebverkorders
        while True:
            opvrWebverkorders.zoekWeborder(m_email, 0) 
    elif mk5 == '8' and mp[5][3] == '1':
        import retourPortalWeb
        klmail = ''
        while True:
            retourPortalWeb.zoekEmailadres(m_email, klmail) 
    elif mk5 == '9' and mp[5][6] == '1':
        if mp[5][1] == '1':
            mret = True
        else:
            mret = False
        import barcodeScan
        barcodeScan.barcodeScan(m_email, mret)
    elif mk6 == '1' and mp[6][3] == '1' :
        import invoerInternorder
        invoerInternorder.invWerkorder(m_email)
    elif mk6 == '2' and mp[6][4] == '1' :
        import wijzInternorder
        wijzInternorder.zoeken(m_email)        
    elif mk6 == '3' and mp[6][6] == '1' :
        import opvrInternorders
        opvrInternorders.zoeken(m_email)
    elif mk6 == '4' and mp[6][3] == '1' : 
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 0)
    elif mk6 == '5' and mp[6][5] == '1' :
        import magUitgifte
        magUitgifte.kiesSelektie(2, m_email)
    elif mk6 == '6' and mp[6][3] == '1' :
        import urenImutaties
        maccountnr = '1'
        mwerknr = '7'
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenImutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
	        # for convenience start with last used work , employee and mboekd 
            maccountnr = accwerk[0]
            mwerknr = accwerk[1]
            mboekd = accwerk[2]
    elif mk7 == '1' and mp[7][3] == '1':
        import invoerWerken
        invoerWerken.invWerk(m_email)
    elif mk7 == '2' and mp[7][4] == '1':
        import wijzWerken
        wijzWerken.zoekWerk(m_email)
    elif mk7 == '3' and mp[7][6] == '1':
        import opvrWerken
        opvrWerken.werkenKeuze(m_email)        
    elif mk7 == '4' and mp[7][2] == '1': 
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 1)
    elif mk7 == '5' and mp[7][6] == '1':
        import magUitgifte
        magUitgifte.kiesSelektie(3, m_email)
    elif mk7 == '6' and mp[7][3] == '1':
        import dienstenMutaties
        dienstenMutaties.mutatieKeuze(m_email)
    elif mk7 == '7' and mp[7][3] == '1':
        import urenMutaties
        maccountnr = '1'
        mwerknr = '8'
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenMutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
            # for convenience start with last used work , employee and mboekd 
            maccountnr = accwerk[0]
            mwerknr = accwerk[1]
            mboekd = accwerk[2]
    elif mk8 == '1' and mp[8][3] == '1':
        import maakIcluster
        while True:
            maakIcluster.kiesCluster(m_email)
    elif mk8 == '2' and mp[8][4] == '1':
        import wijzIclusters
        while True:
            wijzIclusters.zoeken(m_email)
    elif mk8 == '3' and mp[8][6] == '1':
        import opvrIclusters
        opvrIclusters.zoeken(m_email)
    elif mk8 == '4' and mp[8][3] == '1':
        import invoerIcluster_artikelen
        while True:
            invoerIcluster_artikelen.zoeken(m_email)
    elif mk8 == '5' and mp[8][6] == '1':
        import opvrIcluster_artikelen
        opvrIcluster_artikelen.zoeken(m_email)
    elif mk8 == '6' and mp[8][3] == '1':
        import invoerIclustercalculatie
        invoerIclustercalculatie.zoeken(m_email)
    elif mk8 == '7' and mp[8][6] == '1':
        import opvrIclustercalculatie
        while True:
            opvrIclustercalculatie.zoekCalculatie(m_email)
    elif mk8 == '8' and mp[8][1] == '1':
        import koppelIbegroting
        while True:
            koppelIbegroting.zoekBegroting(m_email)
    elif mk9 == '1' and mp[9][4] == '1':
        import maakCluster
        while True:
            maakCluster.kiesCluster(m_email)
    elif mk9 == '2' and mp[9][4] == '1':
        import wijzClusters
        while True:
            wijzClusters.zoeken(m_email)
    elif mk9 == '3' and mp[9][6] == '1':
        import opvrClusters
        opvrClusters.zoeken(m_email)                
    elif mk9 == '4' and mp[9][3] == '1':
        import invoerCluster_artikelen
        while True:
            invoerCluster_artikelen.zoeken(m_email)
    elif mk9 == '5' and mp[9][6] == '1':
        import opvrCluster_artikelen
        opvrCluster_artikelen.zoeken(m_email)
    elif mk9 == '6' and mp[9][3] == '1':
        import invoerClustercalculatie
        while True:
            invoerClustercalculatie.zoeken(m_email)
    elif mk9 == '7' and mp[9][6] == '1':
        import opvrClustercalculatie
        while True:
            opvrClustercalculatie.zoekCalculatie(m_email)
    elif mk9 == '8' and mp[9][1] == '1':
        import koppelBegroting
        while True:
            koppelBegroting.zoekBegroting(m_email)
    elif mk10 == '1' and mp[10][6] == '1' :
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif mk10 == '2' and mp[10][2] == '1' :
        import proefrun
        proefrun.maandPeriode(m_email)
    elif mk10 == '3' and mp[10][1] == '1' :
        import uitbetalenLonen
        uitbetalenLonen.maandBetalingen(m_email)
    elif mk10 == '4' and mp[10][6] == '1' :
        import opvrLoonbetalingen
        opvrLoonbetalingen.zoeken(m_email)
    elif mk10 == '5' and mp[10][3] == '1' :
        import invoerLoontabel
        while True:
            invoerLoontabel.invoerSchaal(m_email)        
    elif mk10 == '6' and mp[10][4] == '1' :
        import wijzLoontabel
        wijzLoontabel.zoeken(m_email)
    elif mk10 == '7' and mp[10][1] == '1' :
        import percentageLonen
        while True:
            percentageLonen.percLoonschaal(m_email)
    elif mk11 == '1' and mp[11][6] == '1' :
        import opvrArtikelmutaties
        opvrArtikelmutaties.mutatieKeuze(m_email)
    elif mk11 == '2' and mp[11][6] == '1' :
        import opvrDienstenmutaties
        opvrDienstenmutaties.mutatieKeuze(m_email)
    elif mk11 == '3' and mp[11][2] == '1' :
        import afdrBetalen
        afdrBetalen.zoeken(m_email)
    elif mk11 == '4' and mp[11][6] == '1' :
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 1)
    elif mk11 == '5' and mp[11][2] == '1' :
        import webRetouren
        webRetouren.retKeuze(m_email)
    elif mk11 == '6' and mp[11][5] == '1' :
        import printFacturatie
        printFacturatie.maakLijst(m_email) 
    elif mk11 == '7' and mp[11][6] == '1' :
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif mk12 == '1' and mp[12][0] == '1':
        import voorraadbeheersing
        voorraadbeheersing.vrdKeuze(m_email)
    elif mk12 == '2' and mp[12][1] == '1':  
        import magvrdGrafiek
        magvrdGrafiek.toonGrafiek(m_email)
    elif mk12 == '3' and mp[12][1] == '1':  
        import magvrdGrafiek
        magvrdGrafiek.magVoorraad(m_email)  
    elif mk12 == '4'and mp[12][1] == '1':
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email)
    elif mk13== '1' and mp[13][1] == '1' :
        import rapportage
        rapportage.JN(m_email)
    elif mk13 == '2' and mp[13][6] == '1':
        import toonGrafieken
        toonGrafieken.zoekwk(m_email)
    elif mk13 == '3' and mp[13][6] == '1' :
        import voortgangGrafiek
        while True:
            voortgangGrafiek.zoekwk(m_email)
    elif mk13 == '4' and mp[13][6] == '1' : 
        import toonResultaten
        toonResultaten.toonResult(m_email)
    elif mk14 == '1' and mp[14][1] == '1':
        import maakAuthorisatie
        while True:
             maakAuthorisatie.zoekAccount(m_email)
    elif mk14 == '2' and mp[14][3] == '1':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 2)
    elif mk14 == '3' and mp[14][3] == '1':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 1)
    elif mk14 == '4' and mp[14][3] == '1':
        import invoerParams
        while True:
            invoerParams.invParams(m_email)
    elif mk14 == '5' and mp[14][4] == '1':
        import wijzigParams
        wijzigParams.toonParams(m_email) 
    elif mk14 == '6' and mp[14][6] == '1':
        import opvrParams
        opvrParams.toonParams(m_email)
    elif mk14 == '7' and mp[14][4] == '1':
        import wijzWerktarief
        wijzWerktarief.winKeuze(m_email)
    elif mk15 == '1' and mp[8][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Clustercalculaties\\'
        else:
            path = './forms/Intern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '2' and mp[9][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties\\'
        else:
            path = './forms/Extern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif mk15 == '3' and (mp[5][5] == '1' or mp[3][5] == '1'):
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Orderbrieven\\'
        else:
            path = './forms/Intern_Orderbrieven/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '4' and mp[6][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '5' and mp[7][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '6' and mp[5][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '7' and mp[5][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Pakbonnen\\'
        else:
            path = './forms/Weborders_Pakbonnen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '8' and mp[10][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Uren\\'
        else:
            path = './forms/Uren/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '9' and mp[10][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Lonen\\'
        else:
            path = './forms/Lonen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif (mk15 == 'A') and mp[11][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Facturen_Werken\\'
        else:
            path = './forms/Facturen_Werken/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif (mk15 == 'B') and mp[11][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Facturen\\'
        else:
            path = './forms/Weborders_Facturen/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif (mk15 == 'C') and (mp[3][5] == '1' or mp[7][5] == '1' or mp[9][5] == '1'):
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties_Diensten\\'
        else:
            path = './forms/Extern_Clustercalculaties_Diensten/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif (mk15 == 'D') and mp[5][5] == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Barcodelijsten\\'
        else:
            path = './forms/Barcodelijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    else:
        geenToegang() 
        hoofdMenu(m_email)
        
inlog()
