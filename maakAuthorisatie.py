from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QGridLayout, QDialog, QLineEdit,\
                        QMessageBox, QPushButton, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import MetaData, Integer, Table, Column, String, create_engine,\
                       select, update
           
def foutAccountnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Accountnummer niet aanwezig!')
    msg.setWindowTitle('ACCOUNT')
    msg.exec_()
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email) 
    
def winSluit(self, m_email):
    self.close()
    zoekAccount(m_email)

def updateOK(maccountnr,mvoorn,mtussen,machtern):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('De bevoegdheden van: \n'+mvoorn+' '+mtussen+' '+machtern+'\nAccountnr.: '+str(maccountnr)+'\nzijn aangepast!')
    msg.setWindowTitle('AUTHORISATIE')
    msg.exec_()

def _11check(maccountnr):
    number = str(maccountnr)
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

def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatie authorisatie")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            lblinfo = QLabel(
        '''
            
        Maak hoofdmenuitems toegankelijk door de checkboxen onder
        Menu aan te vinken voor het desbetreffende account.
        
        De menuvolgorde is als volgt: van linksboven naar beneden
        en vervolgens van rechtsboven naar beneden.
        
        Hoofdmenuingangen:       
            
        Accounts                     Calculatie Intern
        Leveranciers                Calculatie Extern
        Werknemers                Loonadministratie
        Inkoop                         Boekhouding
        Verkoop                       Voorraadmanagement
        Magazijn                      Management Info
        Werken intern             Onderhoud Systeem
        Werken extern            Herprinten Formulieren (alleen hoofdmenu -
                                                         overige bevoegdheden bij afdelingen)\t\t 
        
        De submenu's zijn toegankelijk te maken door de checkboxen
        naast de hoofdmenuitems te activeren.
        
        De authorisaties zijn  van links naar rechts en vervolgens
        van boven naar beneden weergegeven.
        
        Menu = Hoofdmenuitems actief/inactief maken.
        
        Authorisaties:
            
        S = Speciaal  B = Bestellen  I = Invoeren   W = Wijzigen 
        P = Printen    O = Opvragen  R = Gereserveerd
        ''')
                
            grid.addWidget(lblinfo, 1, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 4,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setMinimumWidth(650)
            self.setGeometry(550, 50, 150, 150)
            
    window = Widget()
    window.exec_()
    
def zoekAccount(m_email):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Authorisatie programma.")
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
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight) 
    
            grid.addWidget(QLabel('Accountnummer'), 1, 1)
            grid.addWidget(accEdit, 1, 2)
       
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(500, 400, 150, 150)
    
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
        maccountnr = 0
    
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
  
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([accounts]).where(accounts.c.accountID == maccountnr)
    rpacc = conn.execute(s).first()
    if len(str(maccountnr)) == 9 and _11check(maccountnr) and rpacc:
        geefAuth(rpacc, m_email)
    else:
        foutAccountnr()
        zoekAccount(m_email)
  
def geefAuth(rpacc, m_email):
    maccountnr = int(rpacc[0])
    mvoorn = rpacc[1]
    mtussen = rpacc[2]
    machtern = rpacc[3]      
    metadata = MetaData()
    accounts = Table('accounts', metadata,
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
        Column('p16', String),
        Column('accountID', Integer(), primary_key=True))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([accounts]).where(accounts.c.accountID == maccountnr)
    rpa = conn.execute(sel).first()
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Aanpassen Bevoegdheden")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(15)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1 ,2)
                       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 10, 1, 5, Qt.AlignRight)
            
            self.Accountnummer = QLabel()
            accEdit = QLineEdit(str(maccountnr))
            accEdit.setFixedWidth(100)
            accEdit.setFont(QFont("Arial",10))
            accEdit.setDisabled(True)  
    
            grid.addWidget(QLabel(mvoorn+' '+mtussen+' '+machtern), 0, 2, 1, 9, Qt.AlignTop)     
            grid.addWidget(QLabel('Accountnummer'), 0, 2, 1, 4, Qt.AlignBottom)
            grid.addWidget(accEdit, 0, 6, 1, 4, Qt.AlignBottom) 
          
            grid.addWidget(QLabel('                   Menu'), 2, 0, 1, 3)     
            grid.addWidget(QLabel('S    B     I     W    P    O    R'), 2, 1, 1, 8)
            
            grid.addWidget(QLabel('                      Menu'), 2, 8, 1, 3)     
            grid.addWidget(QLabel('S    B     I    W    P   O    R'), 2, 9, 1, 8)
  
            cBox0 = QCheckBox('Accounts')
            cBox0.setLayoutDirection(Qt.RightToLeft)
            cBox0.setChecked(bool(int(rpa[0][0])))
            cBox0.stateChanged.connect(self.cBox0Changed)
            grid.addWidget(cBox0, 3, 0)
            cBox0a = QCheckBox()
            cBox0a.setChecked(bool(int(rpa[0][1])))
            cBox0a.stateChanged.connect(self.cBox0aChanged)
            grid.addWidget(cBox0a, 3, 1)
            cBox0b = QCheckBox()
            cBox0b.setChecked(bool(int(rpa[0][2])))
            cBox0b.stateChanged.connect(self.cBox0bChanged)
            grid.addWidget(cBox0b, 3, 2)
            cBox0c = QCheckBox()
            cBox0c.setChecked(bool(int(rpa[0][3])))
            cBox0c.stateChanged.connect(self.cBox0cChanged)
            grid.addWidget(cBox0c, 3, 3)
            cBox0d = QCheckBox()
            cBox0d.setChecked(bool(int(rpa[0][4])))
            cBox0d.stateChanged.connect(self.cBox0dChanged)
            grid.addWidget(cBox0d, 3, 4)
            cBox0e = QCheckBox()
            cBox0e.setChecked(bool(int(rpa[0][5])))
            cBox0e.stateChanged.connect(self.cBox0eChanged)
            grid.addWidget(cBox0e, 3, 5)
            cBox0f = QCheckBox()
            cBox0f.setChecked(bool(int(rpa[0][6])))
            cBox0f.stateChanged.connect(self.cBox0fChanged)
            grid.addWidget(cBox0f, 3, 6)
            cBox0g = QCheckBox()
            cBox0g.setChecked(bool(int(rpa[0][7])))
            cBox0g.stateChanged.connect(self.cBox0gChanged)
            grid.addWidget(cBox0g, 3, 7)
            
            cBox1 = QCheckBox('Leveranciers')
            cBox1.setLayoutDirection(Qt.RightToLeft)
            cBox1.setChecked(bool(int(rpa[1][0])))
            cBox1.stateChanged.connect(self.cBox1Changed)
            grid.addWidget(cBox1, 4, 0)
            cBox1a = QCheckBox()
            cBox1a.setChecked(bool(int(rpa[1][1])))
            cBox1a.stateChanged.connect(self.cBox1aChanged)
            grid.addWidget(cBox1a, 4, 1)
            cBox1b = QCheckBox()
            cBox1b.setChecked(bool(int(rpa[1][2])))
            cBox1b.stateChanged.connect(self.cBox1bChanged)
            grid.addWidget(cBox1b, 4, 2)
            cBox1c = QCheckBox()
            cBox1c.setChecked(bool(int(rpa[1][3])))
            cBox1c.stateChanged.connect(self.cBox1cChanged)
            grid.addWidget(cBox1c, 4, 3)
            cBox1d = QCheckBox()
            cBox1d.setChecked(bool(int(rpa[1][4])))
            cBox1d.stateChanged.connect(self.cBox1dChanged)
            grid.addWidget(cBox1d, 4, 4)
            cBox1e = QCheckBox()
            cBox1e.setChecked(bool(int(rpa[1][5])))
            cBox1e.stateChanged.connect(self.cBox1eChanged)
            grid.addWidget(cBox1e, 4, 5)
            cBox1f = QCheckBox()
            cBox1f.setChecked(bool(int(rpa[1][6])))
            cBox1f.stateChanged.connect(self.cBox1fChanged)
            grid.addWidget(cBox1f, 4, 6)
            cBox1g = QCheckBox()
            cBox1g.setChecked(bool(int(rpa[1][7])))
            cBox1g.stateChanged.connect(self.cBox1gChanged)
            grid.addWidget(cBox1g, 4, 7)
            
            cBox2 = QCheckBox('Werknemers')
            cBox2.setLayoutDirection(Qt.RightToLeft)
            cBox2.setChecked(bool(int(rpa[2][0])))
            cBox2.stateChanged.connect(self.cBox2Changed)
            grid.addWidget(cBox2, 5, 0)
            cBox2a = QCheckBox()
            cBox2a.setChecked(bool(int(rpa[2][1])))
            cBox2a.stateChanged.connect(self.cBox2aChanged)
            grid.addWidget(cBox2a, 5, 1)
            cBox2b = QCheckBox()
            cBox2b.setChecked(bool(int(rpa[2][2])))
            cBox2b.stateChanged.connect(self.cBox2bChanged)
            grid.addWidget(cBox2b, 5, 2)
            cBox2c = QCheckBox()
            cBox2c.setChecked(bool(int(rpa[2][3])))
            cBox2c.stateChanged.connect(self.cBox2cChanged)
            grid.addWidget(cBox2c, 5, 3)
            cBox2d = QCheckBox()
            cBox2d.setChecked(bool(int(rpa[2][4])))
            cBox2d.stateChanged.connect(self.cBox2dChanged)
            grid.addWidget(cBox2d, 5, 4)
            cBox2e = QCheckBox()
            cBox2e.setChecked(bool(int(rpa[2][5])))
            cBox2e.stateChanged.connect(self.cBox2eChanged)
            grid.addWidget(cBox2e, 5, 5)
            cBox2f = QCheckBox()
            cBox2f.setChecked(bool(int(rpa[2][6])))
            cBox2f.stateChanged.connect(self.cBox2fChanged)
            grid.addWidget(cBox2f, 5, 6)
            cBox2g = QCheckBox()
            cBox2g.setChecked(bool(int(rpa[2][7])))
            cBox2g.stateChanged.connect(self.cBox2gChanged)
            grid.addWidget(cBox2g, 5, 7)
            
            cBox3 = QCheckBox('Inkoop')
            cBox3.setLayoutDirection(Qt.RightToLeft)
            cBox3.setChecked(bool(int(rpa[3][0])))
            cBox3.stateChanged.connect(self.cBox3Changed)
            grid.addWidget(cBox3, 6, 0)
            cBox3a = QCheckBox()
            cBox3a.setChecked(bool(int(rpa[3][1])))
            cBox3a.stateChanged.connect(self.cBox3aChanged)
            grid.addWidget(cBox3a, 6, 1)
            cBox3b = QCheckBox()
            cBox3b.setChecked(bool(int(rpa[3][2])))
            cBox3b.stateChanged.connect(self.cBox3bChanged)
            grid.addWidget(cBox3b, 6, 2)
            cBox3c = QCheckBox()
            cBox3c.setChecked(bool(int(rpa[3][3])))
            cBox3c.stateChanged.connect(self.cBox3cChanged)
            grid.addWidget(cBox3c, 6, 3)
            cBox3d = QCheckBox()
            cBox3d.setChecked(bool(int(rpa[3][4])))
            cBox3d.stateChanged.connect(self.cBox3dChanged)
            grid.addWidget(cBox3d, 6, 4)
            cBox3e = QCheckBox()
            cBox3e.setChecked(bool(int(rpa[3][5])))
            cBox3e.stateChanged.connect(self.cBox3eChanged)
            grid.addWidget(cBox3e, 6, 5)
            cBox3f = QCheckBox()
            cBox3f.setChecked(bool(int(rpa[3][6])))
            cBox3f.stateChanged.connect(self.cBox3fChanged)
            grid.addWidget(cBox3f, 6, 6)
            cBox3g = QCheckBox()
            cBox3g.setChecked(bool(int(rpa[3][7])))
            cBox3g.stateChanged.connect(self.cBox3gChanged)
            grid.addWidget(cBox3g, 6, 7)
            
            cBox4 = QCheckBox('Verkoop')
            cBox4.setLayoutDirection(Qt.RightToLeft)
            cBox4.setChecked(bool(int(rpa[4][0])))
            cBox4.stateChanged.connect(self.cBox4Changed)
            grid.addWidget(cBox4, 7, 0)
            cBox4a = QCheckBox()
            cBox4a.setChecked(bool(int(rpa[4][1])))
            cBox4a.stateChanged.connect(self.cBox4aChanged)
            grid.addWidget(cBox4a, 7, 1)
            cBox4b = QCheckBox()
            cBox4b.setChecked(bool(int(rpa[4][2])))
            cBox4b.stateChanged.connect(self.cBox4bChanged)
            grid.addWidget(cBox4b, 7, 2)
            cBox4c = QCheckBox()
            cBox4c.setChecked(bool(int(rpa[4][3])))
            cBox4c.stateChanged.connect(self.cBox4cChanged)
            grid.addWidget(cBox4c, 7, 3)
            cBox4d = QCheckBox()
            cBox4d.setChecked(bool(int(rpa[4][4])))
            cBox4d.stateChanged.connect(self.cBox4dChanged)
            grid.addWidget(cBox4d, 7, 4)
            cBox4e = QCheckBox()
            cBox4e.setChecked(bool(int(rpa[4][5])))
            cBox4e.stateChanged.connect(self.cBox4eChanged)
            grid.addWidget(cBox4e, 7, 5)
            cBox4f = QCheckBox()
            cBox4f.setChecked(bool(int(rpa[4][6])))
            cBox4f.stateChanged.connect(self.cBox4fChanged)
            grid.addWidget(cBox4f, 7, 6)
            cBox4g = QCheckBox()
            cBox4g.setChecked(bool(int(rpa[4][7])))
            cBox4g.stateChanged.connect(self.cBox4gChanged)
            grid.addWidget(cBox4g, 7, 7)
            
            cBox5 = QCheckBox('Magazijn')
            cBox5.setLayoutDirection(Qt.RightToLeft)
            cBox5.setChecked(bool(int(rpa[5][0])))
            cBox5.stateChanged.connect(self.cBox5Changed)
            grid.addWidget(cBox5, 8, 0)
            cBox5a = QCheckBox()
            cBox5a.setChecked(bool(int(rpa[5][1])))
            cBox5a.stateChanged.connect(self.cBox5aChanged)
            grid.addWidget(cBox5a, 8, 1)
            cBox5b = QCheckBox()
            cBox5b.setChecked(bool(int(rpa[5][2])))
            cBox5b.stateChanged.connect(self.cBox5bChanged)
            grid.addWidget(cBox5b, 8, 2)
            cBox5c = QCheckBox()
            cBox5c.setChecked(bool(int(rpa[5][3])))
            cBox5c.stateChanged.connect(self.cBox5cChanged)
            grid.addWidget(cBox5c, 8, 3)
            cBox5d = QCheckBox()
            cBox5d.setChecked(bool(int(rpa[5][4])))
            cBox5d.stateChanged.connect(self.cBox5dChanged)
            grid.addWidget(cBox5d, 8, 4)
            cBox5e = QCheckBox()
            cBox5e.setChecked(bool(int(rpa[5][5])))
            cBox5e.stateChanged.connect(self.cBox5eChanged)
            grid.addWidget(cBox5e, 8, 5)
            cBox5f = QCheckBox()
            cBox5f.setChecked(bool(int(rpa[5][6])))
            cBox5f.stateChanged.connect(self.cBox5fChanged)
            grid.addWidget(cBox5f, 8, 6)
            cBox5g = QCheckBox()
            cBox5g.setChecked(bool(int(rpa[5][7])))
            cBox5g.stateChanged.connect(self.cBox5gChanged)
            grid.addWidget(cBox5g, 8, 7)
            
            cBox6 = QCheckBox('Werken intern')
            cBox6.setLayoutDirection(Qt.RightToLeft)
            cBox6.setChecked(bool(int(rpa[6][0])))
            cBox6.stateChanged.connect(self.cBox6Changed)
            grid.addWidget(cBox6, 9, 0)
            cBox6a = QCheckBox()
            cBox6a.setChecked(bool(int(rpa[6][1])))
            cBox6a.stateChanged.connect(self.cBox6aChanged)
            grid.addWidget(cBox6a, 9, 1)
            cBox6b = QCheckBox()
            cBox6b.setChecked(bool(int(rpa[6][2])))
            cBox6b.stateChanged.connect(self.cBox6bChanged)
            grid.addWidget(cBox6b, 9, 2)
            cBox6c = QCheckBox()
            cBox6c.setChecked(bool(int(rpa[6][3])))
            cBox6c.stateChanged.connect(self.cBox6cChanged)
            grid.addWidget(cBox6c, 9, 3)
            cBox6d = QCheckBox()
            cBox6d.setChecked(bool(int(rpa[6][4])))
            cBox6d.stateChanged.connect(self.cBox6dChanged)
            grid.addWidget(cBox6d, 9, 4)
            cBox6e = QCheckBox()
            cBox6e.setChecked(bool(int(rpa[6][5])))
            cBox6e.stateChanged.connect(self.cBox6eChanged)
            grid.addWidget(cBox6e, 9, 5)
            cBox6f = QCheckBox()
            cBox6f.setChecked(bool(int(rpa[6][6])))
            cBox6f.stateChanged.connect(self.cBox6fChanged)
            grid.addWidget(cBox6f, 9, 6)
            cBox6g = QCheckBox()
            cBox6g.setChecked(bool(int(rpa[6][7])))
            cBox6g.stateChanged.connect(self.cBox6gChanged)
            grid.addWidget(cBox6g, 9, 7)
            
            cBox7 = QCheckBox('Werken extern')
            cBox7.setLayoutDirection(Qt.RightToLeft)
            cBox7.setChecked(bool(int(rpa[7][0])))
            cBox7.stateChanged.connect(self.cBox7Changed)
            grid.addWidget(cBox7, 10, 0)
            cBox7a = QCheckBox()
            cBox7a.setChecked(bool(int(rpa[7][1])))
            cBox7a.stateChanged.connect(self.cBox7aChanged)
            grid.addWidget(cBox7a, 10, 1)
            cBox7b = QCheckBox()
            cBox7b.setChecked(bool(int(rpa[7][2])))
            cBox7b.stateChanged.connect(self.cBox7bChanged)
            grid.addWidget(cBox7b, 10, 2)
            cBox7c = QCheckBox()
            cBox7c.setChecked(bool(int(rpa[7][3])))
            cBox7c.stateChanged.connect(self.cBox7cChanged)
            grid.addWidget(cBox7c, 10, 3)
            cBox7d = QCheckBox()
            cBox7d.setChecked(bool(int(rpa[7][4])))
            cBox7d.stateChanged.connect(self.cBox7dChanged)
            grid.addWidget(cBox7d, 10, 4)
            cBox7e = QCheckBox()
            cBox7e.setChecked(bool(int(rpa[7][5])))
            cBox7e.stateChanged.connect(self.cBox7eChanged)
            grid.addWidget(cBox7e, 10, 5)
            cBox7f = QCheckBox()
            cBox7f.setChecked(bool(int(rpa[7][6])))
            cBox7f.stateChanged.connect(self.cBox7fChanged)
            grid.addWidget(cBox7f, 10, 6)  
            cBox7g = QCheckBox()
            cBox7g.setChecked(bool(int(rpa[7][7])))
            cBox7g.stateChanged.connect(self.cBox7gChanged)
            grid.addWidget(cBox7g, 10,7)
          
            cBox8 = QCheckBox('Calculatie intern')
            cBox8.setLayoutDirection(Qt.RightToLeft)
            cBox8.setChecked(bool(int(rpa[8][0])))
            cBox8.stateChanged.connect(self.cBox8Changed)
            grid.addWidget(cBox8, 3, 8)
            cBox8a = QCheckBox()
            cBox8a.setChecked(bool(int(rpa[8][1])))
            cBox8a.stateChanged.connect(self.cBox8aChanged)
            grid.addWidget(cBox8a, 3, 9)
            cBox8b = QCheckBox()
            cBox8b.setChecked(bool(int(rpa[8][2])))
            cBox8b.stateChanged.connect(self.cBox8bChanged)
            grid.addWidget(cBox8b, 3, 10)
            cBox8c = QCheckBox()
            cBox8c.setChecked(bool(int(rpa[8][3])))
            cBox8c.stateChanged.connect(self.cBox8cChanged)
            grid.addWidget(cBox8c, 3, 11)
            cBox8d = QCheckBox()
            cBox8d.setChecked(bool(int(rpa[8][4])))
            cBox8d.stateChanged.connect(self.cBox8dChanged)
            grid.addWidget(cBox8d, 3, 12)
            cBox8e = QCheckBox()
            cBox8e.setChecked(bool(int(rpa[8][5])))
            cBox8e.stateChanged.connect(self.cBox8eChanged)
            grid.addWidget(cBox8e, 3, 13)
            cBox8f = QCheckBox()
            cBox8f.setChecked(bool(int(rpa[8][6])))
            cBox8f.stateChanged.connect(self.cBox8fChanged)
            grid.addWidget(cBox8f, 3, 14)
            cBox8g = QCheckBox()
            cBox8g.setChecked(bool(int(rpa[8][7])))
            cBox8g.stateChanged.connect(self.cBox8gChanged)
            grid.addWidget(cBox8g, 3, 15)
              
            cBox9 = QCheckBox('Calculatie extern')
            cBox9.setLayoutDirection(Qt.RightToLeft)
            cBox9.setChecked(bool(int(rpa[9][0])))
            cBox9.stateChanged.connect(self.cBox9Changed)
            grid.addWidget(cBox9, 4, 8)
            cBox9a = QCheckBox()
            cBox9a.setChecked(bool(int(rpa[9][1])))
            cBox9a.stateChanged.connect(self.cBox9aChanged)
            grid.addWidget(cBox9a, 4, 9)
            cBox9b = QCheckBox()
            cBox9b.setChecked(bool(int(rpa[9][2])))
            cBox9b.stateChanged.connect(self.cBox9bChanged)
            grid.addWidget(cBox9b, 4, 10)
            cBox9c = QCheckBox()
            cBox9c.setChecked(bool(int(rpa[9][3])))
            cBox9c.stateChanged.connect(self.cBox9cChanged)
            grid.addWidget(cBox9c, 4, 11)
            cBox9d = QCheckBox()
            cBox9d.setChecked(bool(int(rpa[9][4])))
            cBox9d.stateChanged.connect(self.cBox9dChanged)
            grid.addWidget(cBox9d, 4, 12)
            cBox9e = QCheckBox()
            cBox9e.setChecked(bool(int(rpa[9][5])))
            cBox9e.stateChanged.connect(self.cBox9eChanged)
            grid.addWidget(cBox9e, 4, 13)
            cBox9f = QCheckBox()
            cBox9f.setChecked(bool(int(rpa[9][6])))
            cBox9f.stateChanged.connect(self.cBox9fChanged)
            grid.addWidget(cBox9f, 4, 14)
            cBox9g = QCheckBox()
            cBox9g.setChecked(bool(int(rpa[9][7])))
            cBox9g.stateChanged.connect(self.cBox9gChanged)
            grid.addWidget(cBox9g, 4,15)
            
            cBox10 = QCheckBox('Loonadminstratie')
            cBox10.setLayoutDirection(Qt.RightToLeft)
            cBox10.setChecked(bool(int(rpa[10][0])))
            cBox10.stateChanged.connect(self.cBox10Changed)
            grid.addWidget(cBox10, 5, 8)
            cBox10a = QCheckBox()
            cBox10a.setChecked(bool(int(rpa[10][1])))
            cBox10a.stateChanged.connect(self.cBox10aChanged)
            grid.addWidget(cBox10a, 5, 9)
            cBox10b = QCheckBox()
            cBox10b.setChecked(bool(int(rpa[10][2])))
            cBox10b.stateChanged.connect(self.cBox10bChanged)
            grid.addWidget(cBox10b, 5, 10)
            cBox10c = QCheckBox()
            cBox10c.setChecked(bool(int(rpa[10][3])))
            cBox10c.stateChanged.connect(self.cBox10cChanged)
            grid.addWidget(cBox10c, 5, 11)
            cBox10d = QCheckBox()
            cBox10d.setChecked(bool(int(rpa[10][4])))
            cBox10d.stateChanged.connect(self.cBox10dChanged)
            grid.addWidget(cBox10d, 5, 12)
            cBox10e = QCheckBox()
            cBox10e.setChecked(bool(int(rpa[10][5])))
            cBox10e.stateChanged.connect(self.cBox10eChanged)
            grid.addWidget(cBox10e, 5, 13)
            cBox10f = QCheckBox()
            cBox10f.setChecked(bool(int(rpa[10][6])))
            cBox10f.stateChanged.connect(self.cBox10fChanged)
            grid.addWidget(cBox10f, 5, 14)
            cBox10g = QCheckBox()
            cBox10g.setChecked(bool(int(rpa[10][7])))
            cBox10g.stateChanged.connect(self.cBox10gChanged)
            grid.addWidget(cBox10g, 5, 15)
            
            cBox11 = QCheckBox('Boekhouding')
            cBox11.setLayoutDirection(Qt.RightToLeft)
            cBox11.setChecked(bool(int(rpa[11][0])))
            cBox11.stateChanged.connect(self.cBox11Changed)
            grid.addWidget(cBox11, 6, 8)
            cBox11a = QCheckBox()
            cBox11a.setChecked(bool(int(rpa[11][1])))
            cBox11a.stateChanged.connect(self.cBox11aChanged)
            grid.addWidget(cBox11a, 6, 9)
            cBox11b = QCheckBox()
            cBox11b.setChecked(bool(int(rpa[11][2])))
            cBox11b.stateChanged.connect(self.cBox11bChanged)
            grid.addWidget(cBox11b, 6, 10)
            cBox11c = QCheckBox()
            cBox11c.setChecked(bool(int(rpa[11][3])))
            cBox11c.stateChanged.connect(self.cBox11cChanged)
            grid.addWidget(cBox11c, 6, 11)
            cBox11d = QCheckBox()
            cBox11d.setChecked(bool(int(rpa[11][4])))
            cBox11d.stateChanged.connect(self.cBox11dChanged)
            grid.addWidget(cBox11d, 6, 12)
            cBox11e = QCheckBox()
            cBox11e.setChecked(bool(int(rpa[11][5])))
            cBox11e.stateChanged.connect(self.cBox11eChanged)
            grid.addWidget(cBox11e, 6, 13)
            cBox11f = QCheckBox()
            cBox11f.setChecked(bool(int(rpa[11][6])))
            cBox11f.stateChanged.connect(self.cBox11fChanged)
            grid.addWidget(cBox11f, 6, 14)
            cBox11g = QCheckBox()
            cBox11g.setChecked(bool(int(rpa[11][7])))
            cBox11g.stateChanged.connect(self.cBox11gChanged)
            grid.addWidget(cBox11g, 6, 15)
            
            cBox12 = QCheckBox('Management\nVoorraad')
            cBox12.setLayoutDirection(Qt.RightToLeft)
            cBox12.setChecked(bool(int(rpa[12][0])))
            cBox12.stateChanged.connect(self.cBox12Changed)
            grid.addWidget(cBox12, 7, 8)
            cBox12a = QCheckBox()
            cBox12a.setChecked(bool(int(rpa[12][1])))
            cBox12a.stateChanged.connect(self.cBox12aChanged)
            grid.addWidget(cBox12a, 7, 9)
            cBox12b = QCheckBox()
            cBox12b.setChecked(bool(int(rpa[12][2])))
            cBox12b.stateChanged.connect(self.cBox12bChanged)
            grid.addWidget(cBox12b, 7, 10)
            cBox12c = QCheckBox()
            cBox12c.setChecked(bool(int(rpa[12][3])))
            cBox12c.stateChanged.connect(self.cBox12cChanged)
            grid.addWidget(cBox12c, 7, 11)
            cBox12d = QCheckBox()
            cBox12d.setChecked(bool(int(rpa[12][4])))
            cBox12d.stateChanged.connect(self.cBox12dChanged)
            grid.addWidget(cBox12d, 7, 12)
            cBox12e = QCheckBox()
            cBox12e.setChecked(bool(int(rpa[12][5])))
            cBox12e.stateChanged.connect(self.cBox12eChanged)
            grid.addWidget(cBox12e, 7, 13)
            cBox12f = QCheckBox()
            cBox12f.setChecked(bool(int(rpa[12][6])))
            cBox12f.stateChanged.connect(self.cBox12fChanged)
            grid.addWidget(cBox12f, 7, 14)
            cBox12g = QCheckBox()
            cBox12g.setChecked(bool(int(rpa[12][7])))
            cBox12g.stateChanged.connect(self.cBox12gChanged)
            grid.addWidget(cBox12g, 7,15)
            
            cBox13 = QCheckBox('Management\nWerken extern')
            cBox13.setLayoutDirection(Qt.RightToLeft)
            cBox13.setChecked(bool(int(rpa[13][0])))
            cBox13.stateChanged.connect(self.cBox13Changed)
            grid.addWidget(cBox13, 8, 8)
            cBox13a = QCheckBox()
            cBox13a.setChecked(bool(int(rpa[13][1])))
            cBox13a.stateChanged.connect(self.cBox13aChanged)
            grid.addWidget(cBox13a, 8, 9)
            cBox13b = QCheckBox()
            cBox13b.setChecked(bool(int(rpa[13][2])))
            cBox13b.stateChanged.connect(self.cBox13bChanged)
            grid.addWidget(cBox13b, 8, 10)
            cBox13c = QCheckBox()
            cBox13c.setChecked(bool(int(rpa[13][3])))
            cBox13c.stateChanged.connect(self.cBox13cChanged)
            grid.addWidget(cBox13c, 8, 11)
            cBox13d = QCheckBox()
            cBox13d.setChecked(bool(int(rpa[13][4])))
            cBox13d.stateChanged.connect(self.cBox13dChanged)
            grid.addWidget(cBox13d, 8, 12)
            cBox13e = QCheckBox()
            cBox13e.setChecked(bool(int(rpa[13][5])))
            cBox13e.stateChanged.connect(self.cBox13eChanged)
            grid.addWidget(cBox13e, 8, 13)
            cBox13f = QCheckBox()
            cBox13f.setChecked(bool(int(rpa[13][6])))
            cBox13f.stateChanged.connect(self.cBox13fChanged)
            grid.addWidget(cBox13f, 8, 14)
            cBox13g = QCheckBox()
            cBox13g.setChecked(bool(int(rpa[13][7])))
            cBox13g.stateChanged.connect(self.cBox13gChanged)
            grid.addWidget(cBox13g, 8, 15)
            
            cBox14 = QCheckBox('Onderhoud')
            cBox14.setLayoutDirection(Qt.RightToLeft)
            cBox14.setChecked(bool(int(rpa[14][0])))
            cBox14.stateChanged.connect(self.cBox14Changed)
            grid.addWidget(cBox14, 9, 8)
            cBox14a = QCheckBox()
            cBox14a.setChecked(bool(int(rpa[14][1])))
            cBox14a.stateChanged.connect(self.cBox14aChanged)
            grid.addWidget(cBox14a, 9, 9)
            cBox14b = QCheckBox()
            cBox14b.setChecked(bool(int(rpa[14][2])))
            cBox14b.stateChanged.connect(self.cBox14bChanged)
            grid.addWidget(cBox14b, 9, 10)
            cBox14c = QCheckBox()
            cBox14c.setChecked(bool(int(rpa[14][3])))
            cBox14c.stateChanged.connect(self.cBox14cChanged)
            grid.addWidget(cBox14c, 9, 11)
            cBox14d = QCheckBox()
            cBox14d.setChecked(bool(int(rpa[14][4])))
            cBox14d.stateChanged.connect(self.cBox14dChanged)
            grid.addWidget(cBox14d, 9, 12)
            cBox14e = QCheckBox()
            cBox14e.setChecked(bool(int(rpa[14][5])))
            cBox14e.stateChanged.connect(self.cBox14eChanged)
            grid.addWidget(cBox14e, 9, 13)
            cBox14f = QCheckBox()
            cBox14f.setChecked(bool(int(rpa[14][6])))
            cBox14f.stateChanged.connect(self.cBox14fChanged)
            grid.addWidget(cBox14f, 9, 14)
            cBox14g = QCheckBox()
            cBox14g.setChecked(bool(int(rpa[14][7])))
            cBox14g.stateChanged.connect(self.cBox14gChanged)
            grid.addWidget(cBox14g, 9,15)
              
            cBox15 = QCheckBox('Herprinten')
            cBox15.setLayoutDirection(Qt.RightToLeft)
            cBox15.setChecked(bool(int(rpa[15][0])))
            cBox15.stateChanged.connect(self.cBox15Changed)
            grid.addWidget(cBox15, 10, 8)
            '''
            cBox15a = QCheckBox()
            cBox15a.setChecked(bool(int(rpa[15][1])))
            cBox15a.stateChanged.connect(self.cBox15aChanged)
            grid.addWidget(cBox15a, 10, 9)
            cBox15b = QCheckBox()
            cBox15b.setChecked(bool(int(rpa[15][2])))
            cBox15b.stateChanged.connect(self.cBox15bChanged)
            grid.addWidget(cBox15b, 10, 10)
            cBox15c = QCheckBox()
            cBox15c.setChecked(bool(int(rpa[15][3])))
            cBox15c.stateChanged.connect(self.cBox15cChanged)
            grid.addWidget(cBox15c, 10, 11)
            cBox15d = QCheckBox()
            cBox15d.setChecked(bool(int(rpa[15][4])))
            cBox15d.stateChanged.connect(self.cBox15dChanged)
            grid.addWidget(cBox15d, 10, 12)
            cBox15e = QCheckBox()
            cBox15e.setChecked(bool(int(rpa[15][5])))
            cBox15e.stateChanged.connect(self.cBox15eChanged)
            grid.addWidget(cBox15e, 10, 13)
            cBox15f = QCheckBox()
            cBox15f.setChecked(bool(int(rpa[15][5])))
            cBox15f.stateChanged.connect(self.cBox15fChanged)
            grid.addWidget(cBox15f, 10, 14)
            cBox15g = QCheckBox()
            cBox15g.setChecked(bool(int(rpa[15][6])))
            cBox15g.stateChanged.connect(self.cBox15gChanged)
            grid.addWidget(cBox15g, 10, 15)
            '''
                      
            applyBtn = QPushButton('Opslaan')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 12, 12, 1, 5, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: winSluit(self, m_email))
            
            grid.addWidget(cancelBtn, 12, 9, 1, 5)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
            
            grid.addWidget(infoBtn, 12, 8, 1, 5)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 16, Qt.AlignCenter)
                 
            self.setLayout(grid)
            self.setGeometry(500, 200, 150, 100)
                
        state0 = bool(int(rpa[0][0]))
        def cBox0Changed(self, state0):
             if state0 == Qt.Checked:
                 self.state0 = True
             else:
                 self.state0 = False
        def returncBox0(self):
             return self.state0
        state0a = bool(int(rpa[0][1]))
        def cBox0aChanged(self, state0a):
             if state0a == Qt.Checked:
                 self.state0a = True
             else:
                 self.state0a = False
        def returncBox0a(self):
            return self.state0a
        state0b = bool(int(rpa[0][2]))
        def cBox0bChanged(self, state0b):
             if state0b == Qt.Checked:
                 self.state0b = True
             else:
                 self.state0b = False
        def returncBox0b(self):
            return self.state0b
        state0c = bool(int(rpa[0][3]))
        def cBox0cChanged(self, state0c):
             if state0c == Qt.Checked:
                 self.state0c = True
             else:
                 self.state0c = False
        def returncBox0c(self):
            return self.state0c
        state0d = bool(int(rpa[0][4]))
        def cBox0dChanged(self, state0d):
             if state0d == Qt.Checked:
                 self.state0d = True
             else:
                 self.state0d = False
        def returncBox0d(self):
            return self.state0d
        state0e = bool(int(rpa[0][5]))
        def cBox0eChanged(self, state0e):
             if state0e == Qt.Checked:
                 self.state0e = True
             else:
                 self.state0e = False
        def returncBox0e(self):
            return self.state0e
        state0f = bool(int(rpa[0][6]))
        def cBox0fChanged(self, state0f):
             if state0f == Qt.Checked:
                 self.state0f = True
             else:
                 self.state0f = False
        def returncBox0f(self):
            return self.state0f
        state0g = bool(int(rpa[0][7]))
        def cBox0gChanged(self, state0g):
             if state0g == Qt.Checked:
                 self.state0g = True
             else:
                 self.state0g = False
        def returncBox0g(self):
            return self.state0g
    
        state1 = bool(int(rpa[1][0]))     
        def cBox1Changed(self, state1):
             if state1 == Qt.Checked:
                 self.state1 = True
             else:
                 self.state1 = False
        def returncBox1(self):
            return self.state1
        state1a = bool(int(rpa[1][1]))   
        def cBox1aChanged(self, state1a):
             if state1a == Qt.Checked:
                 self.state1a = True
             else:
                 self.state1a = False
        def returncBox1a(self):
            return self.state1a
        state1b = bool(int(rpa[1][2]))
        def cBox1bChanged(self, state1b):
             if state1b == Qt.Checked:
                 self.state1b = True
             else:
                 self.state1b = False
        def returncBox1b(self):
            return self.state1b
        state1c = bool(int(rpa[1][3]))
        def cBox1cChanged(self, state1c):
             if state1c == Qt.Checked:
                 self.state1c = True
             else:
                 self.state1c = False
        def returncBox1c(self):
            return self.state1c
        state1d = bool(int(rpa[1][4]))
        def cBox1dChanged(self, state1d):
             if state1d == Qt.Checked:
                 self.state1d = True
             else:
                 self.state0 = False
        def returncBox1d(self):
            return self.state1d
        state1e = bool(int(rpa[1][5]))
        def cBox1eChanged(self, state1e):
             if state1e == Qt.Checked:
                 self.state1e = True
             else:
                 self.state1e = False
        def returncBox1e(self):
            return self.state1e
        state1f = bool(int(rpa[1][6]))
        def cBox1fChanged(self, state1f):
             if state1f == Qt.Checked:
                 self.state1f = True
             else:
                 self.state1f = False
        def returncBox1f(self):
            return self.state1f
        state1g = bool(int(rpa[1][7]))
        def cBox1gChanged(self, state1g):
             if state1g == Qt.Checked:
                 self.state1g = True
             else:
                 self.state1g = False
        def returncBox1g(self):
            return self.state1g
        
        state2 = bool(int(rpa[2][0]))
        def cBox2Changed(self, state2):
             if state2 == Qt.Checked:
                 self.state2 = True
             else:
                 self.state2 = False
        def returncBox2(self):
            return self.state2
        state2a = bool(int(rpa[2][1]))             
        def cBox2aChanged(self, state2a):
             if state2a == Qt.Checked:
                 self.state2a = True
             else:
                 self.state2a = False
        def returncBox2a(self):
            return self.state2a
        state2b = bool(int(rpa[2][2]))
        def cBox2bChanged(self, state2b):
             if state2b == Qt.Checked:
                 self.state2b = True
             else:
                 self.state2b = False
        def returncBox2b(self):
            return self.state2b
        state2c = bool(int(rpa[2][3]))
        def cBox2cChanged(self, state2c):
             if state2c == Qt.Checked:
                 self.state2c = True
             else:
                 self.state2c = False
        def returncBox2c(self):
            return self.state2c
        state2d = bool(int(rpa[2][4]))
        def cBox2dChanged(self, state2d):
             if state2d == Qt.Checked:
                 self.state2d = True
             else:
                 self.state2d = False
        def returncBox2d(self):
            return self.state2d
        state2e = bool(int(rpa[2][5]))
        def cBox2eChanged(self, state2e):
             if state2e == Qt.Checked:
                 self.state2e = True
             else:
                 self.state2e = False
        def returncBox2e(self):
            return self.state2e
        state2f = bool(int(rpa[2][6]))
        def cBox2fChanged(self, state2f):
             if state2f == Qt.Checked:
                 self.state2f = True
             else:
                 self.state2f = False
        def returncBox2f(self):
            return self.state2f
        state2g = bool(int(rpa[2][7]))
        def cBox2gChanged(self, state2g):
             if state2g == Qt.Checked:
                 self.state2g = True
             else:
                 self.state2g = False
        def returncBox2g(self):
            return self.state2g
     
        state3 = bool(int(rpa[3][0]))        
        def cBox3Changed(self, state3):
             if state3 == Qt.Checked:
                 self.state3 = True
             else:
                 self.state3 = False
        def returncBox3(self):
            return self.state3
        state3a = bool(int(rpa[3][1]))    
        def cBox3aChanged(self, state3a):
             if state3a == Qt.Checked:
                 self.state3a = True
             else:
                 self.state3a = False
        def returncBox3a(self):
            return self.state3a
        state3b = bool(int(rpa[3][2]))
        def cBox3bChanged(self, state3b):
             if state3b == Qt.Checked:
                 self.state3b = True
             else:
                 self.state3b = False
        def returncBox3b(self):
            return self.state3b
        state3c = bool(int(rpa[3][3]))
        def cBox3cChanged(self, state3c):
             if state3c == Qt.Checked:
                 self.state3c = True
             else:
                 self.state3c = False
        def returncBox3c(self):
            return self.state3c
        state3d = bool(int(rpa[3][4]))
        def cBox3dChanged(self, state3d):
             if state3d == Qt.Checked:
                 self.state3d = True
             else:
                 self.state3d = False
        def returncBox3d(self):
            return self.state3d
        state3e = bool(int(rpa[3][5]))
        def cBox3eChanged(self, state3e):
             if state3e == Qt.Checked:
                 self.state3e = True
             else:
                 self.state3e = False
        def returncBox3e(self):
            return self.state3e
        state3f = bool(int(rpa[3][6]))
        def cBox3fChanged(self, state3f):
             if state3f == Qt.Checked:
                 self.state3f = True
             else:
                 self.state3f = False
        def returncBox3f(self):
            return self.state3f
        state3g = bool(int(rpa[3][7]))
        def cBox3gChanged(self, state3g):
             if state3g == Qt.Checked:
                 self.state3g = True
             else:
                 self.state3g = False
        def returncBox3g(self):
            return self.state3g
    
        state4 = bool(int(rpa[4][0]))     
        def cBox4Changed(self, state4):
             if state4 == Qt.Checked:
                 self.state4 = True
             else:
                 self.state4 = False
        def returncBox4(self):
            return self.state4
        state4a = bool(int(rpa[4][1]))    
        def cBox4aChanged(self, state4a):
             if state4a == Qt.Checked:
                 self.state4a = True
             else:
                 self.state4a = False
        def returncBox4a(self):
            return self.state4a
        state4b = bool(int(rpa[4][2]))
        def cBox4bChanged(self, state4b):
             if state4b == Qt.Checked:
                 self.state4b = True
             else:
                 self.state4b = False
        def returncBox4b(self):
            return self.state4b
        state4c = bool(int(rpa[4][3]))
        def cBox4cChanged(self, state4c):
             if state4c == Qt.Checked:
                 self.state4c = True
             else:
                 self.state4c = False
        def returncBox4c(self):
            return self.state4c
        state4d = bool(int(rpa[4][4]))
        def cBox4dChanged(self, state4d):
             if state4d == Qt.Checked:
                 self.state4d = True
             else:
                 self.state4d = False
        def returncBox4d(self):
            return self.state4d
        state4e = bool(int(rpa[4][5]))
        def cBox4eChanged(self, state4e):
             if state4e == Qt.Checked:
                 self.state4e = True
             else:
                 self.state4e = False
        def returncBox4e(self):
            return self.state4e
        state4f = bool(int(rpa[4][6]))
        def cBox4fChanged(self, state4f):
             if state4f == Qt.Checked:
                 self.state4f = True
             else:
                 self.state4f = False
        def returncBox4f(self):
            return self.state4f
        state4g = bool(int(rpa[4][7]))
        def cBox4gChanged(self, state4g):
             if state4g == Qt.Checked:
                 self.state4g = True
             else:
                 self.state4g = False
        def returncBox4g(self):
            return self.state4g
    
        state5 = bool(int(rpa[5][0]))    
        def cBox5Changed(self, state5):
             if state5 == Qt.Checked:
                 self.state5 = True
             else:
                 self.state5 = False
        def returncBox5(self):
            return self.state5
        state5a = bool(int(rpa[5][1]))    
        def cBox5aChanged(self, state5a):
             if state5a == Qt.Checked:
                 self.state5a = True
             else:
                 self.state5a = False
        def returncBox5a(self):
            return self.state5a
        state5b = bool(int(rpa[5][2]))
        def cBox5bChanged(self, state5b):
             if state5b == Qt.Checked:
                 self.state5b = True
             else:
                 self.state5b = False
        def returncBox5b(self):
            return self.state5b
        state5c = bool(int(rpa[5][3]))
        def cBox5cChanged(self, state5c):
             if state5c == Qt.Checked:
                 self.state5c = True
             else:
                 self.state5c = False
        def returncBox5c(self):
            return self.state5c
        state5d = bool(int(rpa[5][4]))
        def cBox5dChanged(self, state5d):
             if state5d == Qt.Checked:
                 self.state5d = True
             else:
                 self.state5d = False
        def returncBox5d(self):
            return self.state5d
        state5e = bool(int(rpa[5][5]))
        def cBox5eChanged(self, state5e):
             if state5e == Qt.Checked:
                 self.state5e = True
             else:
                 self.state5e = False
        def returncBox5e(self):
            return self.state5e
        state5f = bool(int(rpa[5][6]))
        def cBox5fChanged(self, state5f):
             if state5f == Qt.Checked:
                 self.state5f = True
             else:
                 self.state5f = False
        def returncBox5f(self):
            return self.state5f
        state5g = bool(int(rpa[5][7]))
        def cBox5gChanged(self, state5g):
             if state5g == Qt.Checked:
                 self.state5g = True
             else:
                 self.state5g = False
        def returncBox5g(self):
            return self.state5g
    
        state6 = bool(int(rpa[6][0]))   
        def cBox6Changed(self, state6):
             if state6 == Qt.Checked:
                 self.state6 = True
             else:
                 self.state6 = False
        def returncBox6(self):
            return self.state6
        state6a = bool(int(rpa[6][1]))    
        def cBox6aChanged(self, state6a):
             if state6a == Qt.Checked:
                 self.state6a = True
             else:
                 self.state6a = False
        def returncBox6a(self):
            return self.state6a
        state6b = bool(int(rpa[6][2]))
        def cBox6bChanged(self, state6b):
             if state6b == Qt.Checked:
                 self.state6b = True
             else:
                 self.state6b = False
        def returncBox6b(self):
            return self.state6b
        state6c = bool(int(rpa[6][3]))
        def cBox6cChanged(self, state6c):
             if state6c == Qt.Checked:
                 self.state6c = True
             else:
                 self.state6c = False
        def returncBox6c(self):
            return self.state6c
        state6d = bool(int(rpa[6][4]))
        def cBox6dChanged(self, state6d):
             if state6d == Qt.Checked:
                 self.state6d = True
             else:
                 self.state6d = False
        def returncBox6d(self):
            return self.state6d
        state6e = bool(int(rpa[6][5]))
        def cBox6eChanged(self, state6e):
             if state6e == Qt.Checked:
                 self.state6e = True
             else:
                 self.state6e = False
        def returncBox6e(self):
            return self.state6e
        state6f = bool(int(rpa[6][6]))
        def cBox6fChanged(self, state6f):
             if state6f == Qt.Checked:
                 self.state6f = True
             else:
                 self.state6f = False
        def returncBox6f(self):
            return self.state6f
        state6g = bool(int(rpa[6][7]))
        def cBox6gChanged(self, state6g):
             if state6g == Qt.Checked:
                 self.state6g = True
             else:
                 self.state6g = False
        def returncBox6g(self):
            return self.state6g
    
        state7 = bool(int(rpa[7][0]))  
        def cBox7Changed(self, state7):
             if state7 == Qt.Checked:
                 self.state7 = True
             else:
                 self.state7 = False
        def returncBox7(self):
            return self.state7
        state7a = bool(int(rpa[7][1]))    
        def cBox7aChanged(self, state7a):
             if state7a == Qt.Checked:
                 self.state7a = True
             else:
                 self.state7a = False
        def returncBox7a(self):
            return self.state7a
        state7b = bool(int(rpa[7][2]))
        def cBox7bChanged(self, state7b):
             if state7b == Qt.Checked:
                 self.state7b = True
             else:
                 self.state7b = False
        def returncBox7b(self):
            return self.state7b
        state7c = bool(int(rpa[7][3]))
        def cBox7cChanged(self, state7c):
             if state7c == Qt.Checked:
                 self.state7c = True
             else:
                 self.state7c = False
        def returncBox7c(self):
            return self.state7c
        state7d = bool(int(rpa[7][4]))
        def cBox7dChanged(self, state7d):
             if state7d == Qt.Checked:
                 self.state7d = True
             else:
                 self.state7d = False
        def returncBox7d(self):
            return self.state7d
        state7e = bool(int(rpa[7][5]))
        def cBox7eChanged(self, state7e):
             if state7e == Qt.Checked:
                 self.state7e = True
             else:
                 self.state7e = False
        def returncBox7e(self):
            return self.state7e
        state7f = bool(int(rpa[7][6]))
        def cBox7fChanged(self, state7f):
             if state7f == Qt.Checked:
                 self.state7f = True
             else:
                 self.state7f = False
        def returncBox7f(self):
            return self.state7f
        state7g = bool(int(rpa[7][7]))
        def cBox7gChanged(self, state7g):
             if state7g == Qt.Checked:
                 self.state7g = True
             else:
                 self.state7g = False
        def returncBox7g(self):
            return self.state7g
        
        state8 = bool(int(rpa[8][0]))
        def cBox8Changed(self, state8):
             if state8 == Qt.Checked:
                 self.state8 = True
             else:
                 self.state8 = False
        def returncBox8(self):
            return self.state8
        state8a = bool(int(rpa[8][1]))
        def cBox8aChanged(self, state8a):
             if state8a == Qt.Checked:
                 self.state8a = True
             else:
                 self.state8a = False
        def returncBox8a(self):
            return self.state8a
        state8b = bool(int(rpa[8][2]))
        def cBox8bChanged(self, state8b):
             if state8b == Qt.Checked:
                 self.state8b = True
             else:
                 self.state8b = False
        def returncBox8b(self):
            return self.state8b
        state8c = bool(int(rpa[8][3]))
        def cBox8cChanged(self, state8c):
             if state8c == Qt.Checked:
                 self.state8c = True
             else:
                 self.state8c = False
        def returncBox8c(self):
            return self.state8c
        state8d = bool(int(rpa[8][4]))
        def cBox8dChanged(self, state8d):
             if state8d == Qt.Checked:
                 self.state8d = True
             else:
                 self.state8d = False
        def returncBox8d(self):
            return self.state8d
        state8e = bool(int(rpa[8][5]))
        def cBox8eChanged(self, state8e):
             if state8e == Qt.Checked:
                 self.state8e = True
             else:
                 self.state8e = False
        def returncBox8e(self):
            return self.state8e
        state8f = bool(int(rpa[8][6]))
        def cBox8fChanged(self, state8f):
             if state8f == Qt.Checked:
                 self.state8f = True
             else:
                 self.state8f = False
        def returncBox8f(self):
            return self.state8f
        state8g = bool(int(rpa[8][7]))
        def cBox8gChanged(self, state8g):
             if state8g == Qt.Checked:
                 self.state8g = True
             else:
                 self.state8g = False
        def returncBox8g(self):
            return self.state8g
    
        state9 = bool(int(rpa[9][0]))
        def cBox9Changed(self, state9):
             if state9 == Qt.Checked:
                 self.state9 = True
             else:
                 self.state9 = False
        def returncBox9(self):
            return self.state9
        state9a = bool(int(rpa[9][1]))
        def cBox9aChanged(self, state9a):
             if state9a == Qt.Checked:
                 self.state9a = True
             else:
                 self.state9a = False
        def returncBox9a(self):
            return self.state9a
        state9b = bool(int(rpa[9][2]))
        def cBox9bChanged(self, state9b):
             if state9b == Qt.Checked:
                 self.state9b = True
             else:
                 self.state9b = False
        def returncBox9b(self):
            return self.state9b
        state9c = bool(int(rpa[9][3]))
        def cBox9cChanged(self, state9c):
             if state9c == Qt.Checked:
                 self.state9c = True
             else:
                 self.state9c = False
        def returncBox9c(self):
            return self.state9c
        state9d = bool(int(rpa[9][4]))
        def cBox9dChanged(self, state9d):
             if state9d == Qt.Checked:
                 self.state9d = True
             else:
                 self.state9d = False
        def returncBox9d(self):
            return self.state9d
        state9e = bool(int(rpa[9][5]))
        def cBox9eChanged(self, state9e):
             if state9e == Qt.Checked:
                 self.state9e = True
             else:
                 self.state9e = False
        def returncBox9e(self):
            return self.state9e
        state9f = bool(int(rpa[9][6]))
        def cBox9fChanged(self, state9f):
             if state9f == Qt.Checked:
                 self.state9f = True
             else:
                 self.state9f = False
        def returncBox9f(self):
            return self.state9f
        state9g = bool(int(rpa[9][7]))
        def cBox9gChanged(self, state9g):
             if state9g == Qt.Checked:
                 self.state9g = True
             else:
                 self.state9g = False
        def returncBox9g(self):
            return self.state9g
    
        state10 = bool(int(rpa[10][0]))
        def cBox10Changed(self, state10):
             if state10 == Qt.Checked:
                 self.state10 = True
             else:
                 self.state10 = False
        def returncBox10(self):
            return self.state10
        state10a = bool(int(rpa[10][1]))
        def cBox10aChanged(self, state10a):
             if state10a == Qt.Checked:
                 self.state10a = True
             else:
                 self.state10a = False
        def returncBox10a(self):
            return self.state10a
        state10b = bool(int(rpa[10][2]))
        def cBox10bChanged(self, state10b):
             if state10b == Qt.Checked:
                 self.state10b = True
             else:
                 self.state10b = False
        def returncBox10b(self):
            return self.state10b
        state10c = bool(int(rpa[10][3]))
        def cBox10cChanged(self, state10c):
             if state10c == Qt.Checked:
                 self.state10c = True
             else:
                 self.state10c = False
        def returncBox10c(self):
            return self.state10c
        state10d = bool(int(rpa[10][4]))
        def cBox10dChanged(self, state10d):
             if state10d == Qt.Checked:
                 self.state10d = True
             else:
                 self.state10d = False
        def returncBox10d(self):
            return self.state10d
        state10e = bool(int(rpa[10][5]))
        def cBox10eChanged(self, state10e):
             if state10e == Qt.Checked:
                 self.state10e = True
             else:
                 self.state10e = False
        def returncBox10e(self):
            return self.state10e
        state10f = bool(int(rpa[10][6]))
        def cBox10fChanged(self, state10f):
             if state10f == Qt.Checked:
                 self.state10f = True
             else:
                 self.state10f = False
        def returncBox10f(self):
            return self.state10f
        state10g = bool(int(rpa[10][7]))
        def cBox10gChanged(self, state10g):
             if state10g == Qt.Checked:
                 self.state10g = True
             else:
                 self.state10g = False
        def returncBox10g(self):
            return self.state10g
    
        state11 = bool(int(rpa[11][0]))
        def cBox11Changed(self, state11):
             if state11 == Qt.Checked:
                 self.state11 = True
             else:
                 self.state11 = False
        def returncBox11(self):
            return self.state11
        state11a = bool(int(rpa[11][1]))
        def cBox11aChanged(self, state11a):
             if state11a == Qt.Checked:
                 self.state11a = True
             else:
                 self.state11a = False
        def returncBox11a(self):
            return self.state11a
        state11b = bool(int(rpa[11][2]))
        def cBox11bChanged(self, state11b):
             if state11b == Qt.Checked:
                 self.state11b = True
             else:
                 self.state11b = False
        def returncBox11b(self):
            return self.state11b
        state11c = bool(int(rpa[11][3]))
        def cBox11cChanged(self, state11c):
             if state11c == Qt.Checked:
                 self.state11c = True
             else:
                 self.state11c = False
        def returncBox11c(self):
            return self.state11c
        state11d = bool(int(rpa[11][4]))
        def cBox11dChanged(self, state11d):
             if state11d == Qt.Checked:
                 self.state11d = True
             else:
                 self.state11d = False
        def returncBox11d(self):
            return self.state11d
        state11e = bool(int(rpa[11][5]))
        def cBox11eChanged(self, state11e):
             if state11e == Qt.Checked:
                 self.state11e = True
             else:
                 self.state11e = False
        def returncBox11e(self):
            return self.state11e
        state11f = bool(int(rpa[11][6]))
        def cBox11fChanged(self, state11f):
             if state11f == Qt.Checked:
                 self.state11f = True
             else:
                 self.state11f = False
        def returncBox11f(self):
            return self.state11f
        state11g = bool(int(rpa[11][7]))
        def cBox11gChanged(self, state11g):
             if state11g == Qt.Checked:
                 self.state11g = True
             else:
                 self.state11g = False
        def returncBox11g(self):
            return self.state11g
    
        state12 = bool(int(rpa[12][0]))    
        def cBox12Changed(self, state12):
             if state12 == Qt.Checked:
                 self.state12 = True
             else:
                 self.state12 = False
        def returncBox12(self):
            return self.state12
        state12a = bool(int(rpa[12][1]))
        def cBox12aChanged(self, state12a):
             if state12a == Qt.Checked:
                 self.state12a = True
             else:
                 self.state12a = False
        def returncBox12a(self):
            return self.state12a
        state12b = bool(int(rpa[12][2]))
        def cBox12bChanged(self, state12b):
             if state12b == Qt.Checked:
                 self.state12b = True
             else:
                 self.state12b = False
        def returncBox12b(self):
            return self.state12b
        state12c = bool(int(rpa[12][3]))
        def cBox12cChanged(self, state12c):
             if state12c == Qt.Checked:
                 self.state12c = True
             else:
                 self.state12c = False
        def returncBox12c(self):
            return self.state12c
        state12d = bool(int(rpa[12][4]))
        def cBox12dChanged(self, state12d):
             if state12d == Qt.Checked:
                 self.state12d = True
             else:
                 self.state12d = False
        def returncBox12d(self):
            return self.state12d
        state12e = bool(int(rpa[12][5]))
        def cBox12eChanged(self, state12e):
             if state12e == Qt.Checked:
                 self.state12e = True
             else:
                 self.state12e = False
        def returncBox12e(self):
            return self.state12e
        state12f = bool(int(rpa[12][6]))
        def cBox12fChanged(self, state12f):
             if state12f == Qt.Checked:
                 self.state12f = True
             else:
                 self.state12f = False
        def returncBox12f(self):
            return self.state12f
        state12g = bool(int(rpa[12][7]))
        def cBox12gChanged(self, state12g):
             if state12g == Qt.Checked:
                 self.state12g = True
             else:
                 self.state12g = False
        def returncBox12g(self):
            return self.state12g
    
        state13 = bool(int(rpa[13][0]))    
        def cBox13Changed(self, state13):
             if state13 == Qt.Checked:
                 self.state13 = True
             else:
                 self.state13 = False
        def returncBox13(self):
            return self.state13
        state13a = bool(int(rpa[13][1]))
        def cBox13aChanged(self, state13a):
             if state13a == Qt.Checked:
                 self.state13a = True
             else:
                 self.state13a = False
        def returncBox13a(self):
            return self.state13a
        state13b = bool(int(rpa[13][2]))
        def cBox13bChanged(self, state13b):
             if state13b == Qt.Checked:
                 self.state13b = True
             else:
                 self.state13b = False
        def returncBox13b(self):
            return self.state13b
        state13c = bool(int(rpa[13][3]))
        def cBox13cChanged(self, state13c):
             if state13c == Qt.Checked:
                 self.state13c = True
             else:
                 self.state13c = False
        def returncBox13c(self):
            return self.state13c
        state13d = bool(int(rpa[13][4]))
        def cBox13dChanged(self, state13d):
             if state13d == Qt.Checked:
                 self.state13d = True
             else:
                 self.state13d = False
        def returncBox13d(self):
            return self.state13d
        state13e = bool(int(rpa[13][5]))
        def cBox13eChanged(self, state13e):
             if state13e == Qt.Checked:
                 self.state13e = True
             else:
                 self.state13e = False
        def returncBox13e(self):
            return self.state13e
        state13f = bool(int(rpa[13][6]))
        def cBox13fChanged(self, state13f):
             if state13f == Qt.Checked:
                 self.state13f = True
             else:
                 self.state13f = False
        def returncBox13f(self):
            return self.state13f
        state13g = bool(int(rpa[13][7]))
        def cBox13gChanged(self, state13g):
             if state13g == Qt.Checked:
                 self.state13g = True
             else:
                 self.state13g = False
        def returncBox13g(self):
            return self.state13g
     
        state14 = bool(int(rpa[14][0]))
        def cBox14Changed(self, state14):
             if state14 == Qt.Checked:
                 self.state14 = True
             else:
                 self.state14 = False
        def returncBox14(self):
            return self.state14
        state14a = bool(int(rpa[14][1]))
        def cBox14aChanged(self, state14a):
             if state14a == Qt.Checked:
                 self.state14a = True
             else:
                 self.state14a = False
        def returncBox14a(self):
            return self.state14a
        state14b = bool(int(rpa[14][2]))
        def cBox14bChanged(self, state14b):
             if state14b == Qt.Checked:
                 self.state14b = True
             else:
                 self.state14b = False
        def returncBox14b(self):
            return self.state14b
        state14c = bool(int(rpa[14][3]))
        def cBox14cChanged(self, state14c):
             if state14c == Qt.Checked:
                 self.state14c = True
             else:
                 self.state14c = False
        def returncBox14c(self):
            return self.state14c
        state14d = bool(int(rpa[14][4]))
        def cBox14dChanged(self, state14d):
             if state14d == Qt.Checked:
                 self.state14d = True
             else:
                 self.state14d = False
        def returncBox14d(self):
            return self.state14d
        state14e = bool(int(rpa[14][5]))
        def cBox14eChanged(self, state14e):
             if state14e == Qt.Checked:
                 self.state14e = True
             else:
                 self.state14e = False
        def returncBox14e(self):
            return self.state14e
        state14f = bool(int(rpa[14][6]))
        def cBox14fChanged(self, state14f):
             if state14f == Qt.Checked:
                 self.state14f = True
             else:
                 self.state14f = False
        def returncBox14f(self):
            return self.state14f
        state14g = bool(int(rpa[14][7]))
        def cBox14gChanged(self, state14g):
             if state14g == Qt.Checked:
                 self.state14g = True
             else:
                 self.state14g = False
        def returncBox14g(self):
            return self.state14g
    
        state15 = bool(int(rpa[15][0]))    
        def cBox15Changed(self, state15):
             if state15 == Qt.Checked:
                 self.state15 = True
             else:
                 self.state15 = False
        def returncBox15(self):
            return self.state15
        state15a = bool(int(rpa[15][1]))
        def cBox15aChanged(self, state15a):
             if state15a == Qt.Checked:
                 self.state15a = True
             else:
                 self.state15a = False
        def returncBox15a(self):
            return self.state15a
        state15b = bool(int(rpa[15][2]))
        def cBox15bChanged(self, state15b):
             if state15b == Qt.Checked:
                 self.state15b = True
             else:
                 self.state15b = False
        def returncBox15b(self):
            return self.state15b
        state15c = bool(int(rpa[15][3]))
        def cBox15cChanged(self, state15c):
             if state15c == Qt.Checked:
                 self.state15c = True
             else:
                 self.state15c = False
        def returncBox15c(self):
            return self.state15c
        state15d = bool(int(rpa[15][4]))
        def cBox15dChanged(self, state15d):
             if state15d == Qt.Checked:
                 self.state15d = True
             else:
                 self.state15d = False
        def returncBox15d(self):
            return self.state15d
        state15e = bool(int(rpa[15][5]))
        def cBox15eChanged(self, state15e):
             if state15e == Qt.Checked:
                 self.state15e = True
             else:
                 self.state15e = False
        def returncBox15e(self):
            return self.state15e
        state15f = bool(int(rpa[15][6]))
        def cBox15fChanged(self, state15f):
             if state15f == Qt.Checked:
                 self.state15f = True
             else:
                 self.state15f = False
        def returncBox15f(self):
            return self.state15f
        state15g = bool(int(rpa[15][7]))
        def cBox15gChanged(self, state15g):
             if state15g == Qt.Checked:
                 self.state15g = True
             else:
                 self.state15g = False
        def returncBox15g(self):
            return self.state15g
      
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return[dialog.returncBox0(),dialog.returncBox0a(),dialog.returncBox0b(),dialog.returncBox0c(),\
               dialog.returncBox0d(),dialog.returncBox0e(),dialog.returncBox0f(),dialog.returncBox0g(),\
               dialog.returncBox1(),dialog.returncBox1a(),dialog.returncBox1b(),dialog.returncBox1c(),\
               dialog.returncBox1d(),dialog.returncBox1e(),dialog.returncBox1f(),dialog.returncBox1g(),\
               dialog.returncBox2(),dialog.returncBox2a(),dialog.returncBox2b(),dialog.returncBox2c(),\
               dialog.returncBox2d(),dialog.returncBox2e(),dialog.returncBox2f(),dialog.returncBox2g(),\
               dialog.returncBox3(),dialog.returncBox3a(),dialog.returncBox3b(),dialog.returncBox3c(),\
               dialog.returncBox3d(),dialog.returncBox3e(),dialog.returncBox3f(),dialog.returncBox3g(),\
               dialog.returncBox4(),dialog.returncBox4a(),dialog.returncBox4b(),dialog.returncBox4c(),\
               dialog.returncBox4d(),dialog.returncBox4e(),dialog.returncBox4f(),dialog.returncBox4g(),\
               dialog.returncBox5(),dialog.returncBox5a(),dialog.returncBox5b(),dialog.returncBox5c(),\
               dialog.returncBox5d(),dialog.returncBox5e(),dialog.returncBox5f(),dialog.returncBox5g(),\
               dialog.returncBox6(),dialog.returncBox6a(),dialog.returncBox6b(),dialog.returncBox6c(),\
               dialog.returncBox6d(),dialog.returncBox6e(),dialog.returncBox6f(),dialog.returncBox6g(),\
               dialog.returncBox7(),dialog.returncBox7a(),dialog.returncBox7b(),dialog.returncBox7c(),\
               dialog.returncBox7d(),dialog.returncBox7e(),dialog.returncBox7f(),dialog.returncBox7g(),\
               dialog.returncBox8(),dialog.returncBox8a(),dialog.returncBox8b(),dialog.returncBox8c(),\
               dialog.returncBox8d(),dialog.returncBox8e(),dialog.returncBox8f(),dialog.returncBox8g(),\
               dialog.returncBox9(),dialog.returncBox9a(),dialog.returncBox9b(),dialog.returncBox9c(),\
               dialog.returncBox9d(),dialog.returncBox9e(),dialog.returncBox9f(),dialog.returncBox9g(),\
               dialog.returncBox10(),dialog.returncBox10a(),dialog.returncBox10b(),dialog.returncBox10c(),\
               dialog.returncBox10d(),dialog.returncBox10e(),dialog.returncBox10f(),dialog.returncBox10g(),\
               dialog.returncBox11(),dialog.returncBox11a(),dialog.returncBox11b(),dialog.returncBox11c(),\
               dialog.returncBox11d(),dialog.returncBox11e(),dialog.returncBox11f(),dialog.returncBox11g(),\
               dialog.returncBox12(),dialog.returncBox12a(),dialog.returncBox12b(),dialog.returncBox12c(),\
               dialog.returncBox12d(),dialog.returncBox12e(),dialog.returncBox12f(),dialog.returncBox12g(),\
               dialog.returncBox13(),dialog.returncBox13a(),dialog.returncBox13b(),dialog.returncBox13c(),\
               dialog.returncBox13d(),dialog.returncBox13e(),dialog.returncBox13f(),dialog.returncBox13g(),\
               dialog.returncBox14(),dialog.returncBox14a(),dialog.returncBox14b(),dialog.returncBox14c(),\
               dialog.returncBox14d(),dialog.returncBox14e(),dialog.returncBox14f(),dialog.returncBox14g(),\
               dialog.returncBox15(),dialog.returncBox15a(),dialog.returncBox15b(),dialog.returncBox15c(),\
               dialog.returncBox15d(),dialog.returncBox15e(),dialog.returncBox15f(),dialog.returncBox15g()]
 
    window = Widget()
    data = window.getData()
    mp1,mp2,mp3,mp4,mp5,mp6,mp7,mp8,mp9,mp10,mp11,mp12,mp13,mp14,mp15,mp16=('',)*16
    for menu in range(1,17):
        for pos in range(1,9):
            if menu == 1:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp1 = mp1+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp1 = mp1+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp1 = mp1+'0'
            elif menu == 2:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp2 = mp2+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp2 = mp2+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp2 = mp2+'0'
            elif menu == 3:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp3 = mp3+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp3 = mp3+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp3 = mp3+'0'
            elif menu == 4:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp4 = mp4+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp4 = mp4+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp4 = mp4+'0'
            elif menu == 5:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp5 = mp5+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp5 = mp5+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp5 = mp5+'0'
            elif menu == 6:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp6 = mp6+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp6 = mp6+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp6 = mp6+'0'
            elif menu == 7:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp7 = mp7+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp7 = mp7+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp7 = mp7+'0'
            elif menu == 8:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp8 = mp8+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp8 = mp8+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp8 = mp8+'0'
            elif menu == 9:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp9 = mp9+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp9 = mp9+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp9 = mp9+'0'
            elif menu == 10:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp10 = mp10+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp10 = mp10+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp10 = mp10+'0'
            elif menu == 11:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp11 = mp11+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp11 = mp11+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp11 = mp11+'0'
            elif menu == 12:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp12 = mp12+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp12 = mp12+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp12 = mp12+'0'                   
            elif menu == 13:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp13 = mp13+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp13 = mp13+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp13 = mp13+'0'            
            elif menu == 14:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp14 = mp14+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp14 = mp14+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp14 = mp14+'0'    
            elif menu == 15:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp15 = mp15+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp15 = mp15+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp15 = mp15+'0'
            elif menu == 16:
                if data[(menu-1)*8+(pos-1)] == True:
                   mp16 = mp16+'1'
                elif data[(menu-1)*8+(pos-1)] == False:
                   mp16 = mp16+'0'
                elif not data[(menu-1)*8+(pos-1)]:
                   mp16 = mp16+'0'
    #print(mp1,mp2,mp3,mp4,mp5,mp6,mp7,mp8,mp9,mp10,mp11,mp12,mp13,mp14,mp15,mp16)
    #print(rpa)            
    #print(data)
    ua = update(accounts).where(accounts.c.accountID == maccountnr).values(\
       p1=mp1,p2=mp2,p3=mp3,p4=mp4,p5=mp5,p6=mp6,p7=mp7,p8=mp8,p9=mp9,p10=mp10,\
       p11=mp11,p12=mp12,p13=mp13,p14=mp14,p15=mp15,p16=mp16)
    conn.execute(ua)
    updateOK(maccountnr, mvoorn,mtussen,machtern)
    zoekAccount(m_email)