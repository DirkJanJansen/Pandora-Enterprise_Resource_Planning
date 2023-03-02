from collections import Counter
from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QGridLayout, QDialog, QLineEdit,\
                        QMessageBox, QPushButton, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon, QMovie
from PyQt5.QtCore import Qt, QRegExp, QSize
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

def updateOK(self):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setFont(QFont("Arial",10))
    msg.setText('De bevoegdheden van: \n'+self.mvoorn+' '+self.mtussen+' '+self.machtern+'\nzijn aangepast!')
    msg.setWindowTitle('AUTHORISATIE')
    msg.exec_()

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
            accEdit = QLineEdit('1')
            accEdit.setFixedWidth(100)
            accEdit.setFont(QFont("Arial",10))
            accEdit.textChanged.connect(self.accChanged)
            reg_ex = QRegExp('^[1]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, accEdit)
            accEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
               
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
    if rpacc:
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
    con = engine.connect()
    sel = select([accounts]).where(accounts.c.accountID == maccountnr)
    rpa = con.execute(sel).first()

    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Aanpassen Bevoegdheden")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(15)
            
            self.mvoorn = mvoorn
            self.mtussen = mtussen
            self.machtern = machtern
            
            self.astr = rpa[0]+rpa[1]+rpa[2]+rpa[3]+rpa[4]+rpa[5]+rpa[6]+rpa[7]\
                 +rpa[8]+rpa[9]+rpa[10]+rpa[11]+rpa[12]+rpa[13]+rpa[14]+rpa[15]
            
            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 6)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 16, 1, 4, Qt.AlignRight)
            
            accEdit = QLineEdit(str(maccountnr))
            accEdit.setFixedWidth(100)
            accEdit.setFont(QFont("Arial",10))
            accEdit.setStyleSheet('color: black')
            accEdit.setDisabled(True)  
    
            grid.addWidget(QLabel(mvoorn+' '+mtussen+' '+machtern), 0, 8, 1, 9, Qt.AlignTop)     
            grid.addWidget(QLabel('Accountnummer'), 0, 8, 1, 10, Qt.AlignBottom)
            grid.addWidget(accEdit, 0, 7, 1, 10, Qt.AlignCenter | Qt.AlignBottom) 
            
            grid.addWidget(QLabel('Menu'), 2, 1, 1, 2, Qt.AlignRight)
            grid.addWidget(QLabel('S'), 2, 3)
            grid.addWidget(QLabel('B'), 2, 4)
            grid.addWidget(QLabel('I'), 2, 5)
            grid.addWidget(QLabel('W'), 2, 6)
            grid.addWidget(QLabel('P'), 2, 7)
            grid.addWidget(QLabel('O'), 2, 8)
            grid.addWidget(QLabel('R'), 2, 9)
            
            grid.addWidget(QLabel('Menu'), 2, 11, 1, 2, Qt.AlignRight)  
            grid.addWidget(QLabel('S'), 2, 13)
            grid.addWidget(QLabel('B'), 2, 14)
            grid.addWidget(QLabel('I'), 2, 15)
            grid.addWidget(QLabel('W'), 2, 16)
            grid.addWidget(QLabel('P'), 2, 17)
            grid.addWidget(QLabel('O'), 2, 18)
            grid.addWidget(QLabel('R'), 2, 19)
            
            lbl0 = QLabel('Accounts')
            lbl0.setFixedWidth(115) 
            grid.addWidget(lbl0, 3 , 0)
            lbl1 = QLabel('Leveranciers')
            lbl1.setFixedWidth(115) 
            grid.addWidget(lbl1, 4 , 0)
            lbl2 = QLabel('Werknemers')
            lbl2.setFixedWidth(115) 
            grid.addWidget(lbl2, 5 , 0)
            lbl3 = QLabel('Inkoop')
            lbl3.setFixedWidth(115) 
            grid.addWidget(lbl3, 6 , 0)
            lbl4 = QLabel('Verkoop')
            lbl4.setFixedWidth(115) 
            grid.addWidget(lbl4, 7 , 0)
            lbl5 = QLabel('Magazijn')
            lbl5.setFixedWidth(115) 
            grid.addWidget(lbl5, 8 , 0)
            lbl6 = QLabel('Werken Intern')
            lbl6.setFixedWidth(115) 
            grid.addWidget(lbl6, 9 , 0)
            lbl7 = QLabel('Werken Extern')
            lbl7.setFixedWidth(115) 
            grid.addWidget(lbl7, 10 , 0)
            lbl8 = QLabel('Calculatie Interne Werken')
            lbl8.setFixedWidth(200) 
            grid.addWidget(lbl8, 3 , 11)
            lbl9 = QLabel('Calculatie Externe Werken')
            lbl9.setFixedWidth(200) 
            grid.addWidget(lbl9, 4 , 11)
            lbl10 = QLabel('Loonadminstratie')
            lbl10.setFixedWidth(200) 
            grid.addWidget(lbl10, 5 , 11)
            lbl11 = QLabel('Boekhouding')
            lbl11.setFixedWidth(200) 
            grid.addWidget(lbl11, 6 , 11)
            lbl12 = QLabel('Voorraadmanagement')
            lbl12.setFixedWidth(200) 
            grid.addWidget(lbl12, 7 , 11)
            lbl13 = QLabel('Managementinformatie')
            lbl13.setFixedWidth(200) 
            grid.addWidget(lbl13, 8 , 11)
            lbl14 = QLabel('Onderhoud')
            lbl14.setFixedWidth(200) 
            grid.addWidget(lbl14, 9 , 11)
            lbl15 = QLabel('Herprinten formulieren')
            lbl15.setFixedWidth(200) 
            grid.addWidget(lbl15, 10 , 11)
            
            self.xlist=[]
            for x in range(0,121):
               cBox = QCheckBox()
               val = self.astr[x]   
               if val == '1':
                   cBox.setChecked(True)
               else:
                   cBox.setChecked(False)
               if x < 64:
                   grid.addWidget(cBox, int(x/8+3), x%8+2)
               else:
                   grid.addWidget(cBox, int(x/8-5), x%8+12)
               cBox.clicked.connect(lambda checked , mindex = x : getindex(mindex))
                                              
            def getindex(mindex):
                #compile list with changes
                self.xlist.append(mindex)
                                         
            def writeValues(self):
                #remove unnessary paired changes (enable, disable) or (disable, enable) and sort
                self.xlist = [value for value, count in Counter(self.xlist).items() if count%2 == 1]
                self.xlist.sort()
                for x in self.xlist:
                    if self.astr[x] == '0':
                        self.astr=self.astr[0:x]+'1'+self.astr[x+1:]
                    else:
                        self.astr=self.astr[0:x]+'0'+self.astr[x+1:]
                                                           
                updper=update(accounts).where(accounts.c.accountID==maccountnr).values\
                 (p1=self.astr[0:8],
                  p2=self.astr[8:16],
                  p3=self.astr[16:24],
                  p4=self.astr[24:32],
                  p5=self.astr[32:40],
                  p6=self.astr[40:48],
                  p7=self.astr[48:56],
                  p8=self.astr[56:64],
                  p9=self.astr[64:72],
                  p10=self.astr[72:80],
                  p11=self.astr[80:88],
                  p12=self.astr[88:96],
                  p13=self.astr[96:104],
                  p14=self.astr[104:112],
                  p15=self.astr[112:120],
                  p16=self.astr[120:128])
                con.execute(updper)
                updateOK(self)
                self.close()
                                                                          
            applyBtn = QPushButton('Opslaan')
            applyBtn.clicked.connect(lambda: writeValues(self))
                       
            grid.addWidget(applyBtn, 12, 16, 1, 4, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: winSluit(self, m_email))
            
            grid.addWidget(cancelBtn, 12, 12, 1, 4)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
            
            grid.addWidget(infoBtn, 12, 10, 1, 4, Qt.AlignCenter)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 18, Qt.AlignCenter)
                 
            self.setLayout(grid)
            self.setGeometry(500, 200, 150, 100)
       
    win = Widget()
    win.exec_()
  
    zoekAccount(m_email)