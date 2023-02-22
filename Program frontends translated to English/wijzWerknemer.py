from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                             QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        ForeignKey,  MetaData, create_engine)
from sqlalchemy.sql import select, and_, update

def geenBetaalgeg():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No payment details found for this period!')
    msg.setWindowTitle('Payment details!')
    msg.exec_()
    
def wijzSluit(self, m_email):
    self.close()
    zoekWerknemer(m_email)
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def info():
    class Widget(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Informatie vervangend werk")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont("Arial", 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
            
            lblinfo = QLabel('Replacement work.')
            grid.addWidget(lblinfo, 0, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgb(45, 83, 115); font: 25pt Comic Sans MS")
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            lblinfo = QLabel(
        '''
        If an employee needs to perform substitute work in another discipline,
        the new wage table number of this discipline must be filled in
        in the Pay table field. 
        The Orig field will then retain the old pay table number, with which his or her\t
        wages are determined. 
        The work wages data for transfer to the works is calculated with the changed
        wage table number. 
        When resuming the original work, the wage table number to be changed back to
        the contents of the Orig field so that both fields be equal again and the
        original situation has been restored.
       
        ''')
                
            grid.addWidget(lblinfo, 1, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF") 
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn,  3, 0, 1, 4, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setMinimumWidth(650)
            self.setGeometry(550, 300, 900, 150)
            
    window = Widget()
    window.exec_()
    
def foutWerknemer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Employee not found!')
    msg.setWindowTitle('EMPLOYEE')
    msg.exec_()
               
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Your data have been adjusted!')
    msg.setWindowTitle('DATA!')
    msg.exec_()

def _11check(minput):
    number = str(minput)
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
    
def zoekWerknemer(m_email):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify employee data.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    
            self.setFont(QFont('Arial', 10))
    
            self.Werknemer = QLabel()
            werknemerEdit = QLineEdit()
            werknemerEdit.setFixedWidth(100)
            werknemerEdit.setFont(QFont("Arial",10))
            werknemerEdit.textChanged.connect(self.werknemerChanged)
            reg_ex = QRegExp('^[1]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, werknemerEdit)
            werknemerEdit.setValidator(input_validator)
                                         
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
     
            grid.addWidget(QLabel('Account-employee'), 1, 0)
            grid.addWidget(werknemerEdit, 1, 1)
                       
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'),3,0,1,2, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(400, 300, 150, 150)
    
        def werknemerChanged(self, text):
            self.Werknemer.setText(text)
         
        def returnWerknemer(self):
            return self.Werknemer.text()
        
  
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnWerknemer()]
    
    window = Widget()
    data = window.getData()
    if data[0]:
        maccountnr = data[0]
    else:
        foutWerknemer()
        return(0, 0)
                
    metadata = MetaData()

    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')))
   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([werknemers]).where(werknemers.c.accountID == maccountnr)
    rpwerkn = conn.execute(sel).first()
    
    if (len(str(maccountnr)) == 9 and _11check(maccountnr) and rpwerkn):
        maccountnr = rpwerkn[1]
        mwerknmr = rpwerkn[0]
        updateWerknemer(m_email, mwerknmr)
    else:
        foutWerknemer()
        zoekWerknemer(m_email)

def updateWerknemer(m_email, mwerknmr):
    metadata = MetaData()   
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')), 
        Column('loontrede', Integer),
        Column('reiskosten_vergoeding', Float),
        Column('periodieke_uitkeringen', Float),
        Column('overige_inhoudingen', Float),
        Column('overige_vergoedingen', Float),
        Column('bedrijfsauto', Float),
        Column('indienst', String),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float),
        Column('wnrloonID', Integer))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('reisuur', Float),
        Column('maandloon', Float)) 
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('soort', String),
        Column('meerwerkstatus', Boolean),
        Column('bruto_loonbedrag', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('voornaam', String),
        Column('achternaam', String),
        Column('geboortedatum', String))
         
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([werknemers, lonen, wrkwnrln, accounts]).where(and_\
      (werknemers.c.werknemerID == mwerknmr, werknemers.c.loonID ==\
       lonen.c.loonID, accounts.c.accountID == werknemers.c.accountID))
    rpwerkn = conn.execute(sel).first()
    mwerknmr = rpwerkn[0]
    maccountnr = rpwerkn[1]
    mloonnr = rpwerkn[2]
    if not rpwerkn[12]:
        mwnrloonnr = mloonnr
    else:
        mwnrloonnr = rpwerkn[12]
    mtrede = rpwerkn[3]*0.03
    mreisk = rpwerkn[4]
    mauto = rpwerkn[8]      
    mperiodiek = rpwerkn[5]
    moveriginh = rpwerkn[6]
    moverigverg = rpwerkn[7]
    mindienst = rpwerkn[9]
    mverlofsaldo = rpwerkn[10]
    mextraverlof = rpwerkn[11]
    mvoorn = rpwerkn[25]
    machtern = rpwerkn[26]
    mgeboren = rpwerkn[27]
        
    if rpwerkn[2] < 37:
        mbruto = rpwerkn[14]*520/3*(1+mtrede)
        muurl = rpwerkn[14]*(1+mtrede)
    else:
        mbruto =  rpwerkn[16]*(1+mtrede)
        muurl = mbruto*3/520
    if rpwerkn[14]:
        mreisuurl = round(rpwerkn[14],2)
    else:
        mreisuurl = 0
                                         
    class Widget(QDialog):
         def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify employee data")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                  
            self.setFont(QFont('Arial', 10))
                
            self.Accountnummer = QLabel()
            q2Edit = QLineEdit(str(maccountnr))
            q2Edit.setFixedWidth(100)
            q2Edit.setAlignment(Qt.AlignRight)
            q2Edit.setDisabled(True)
            q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q2Edit.textChanged.connect(self.q2Changed)
                        
            self.Loontabelnummer = QLabel()
            q4Edit = QLineEdit(str(mloonnr))
            q4Edit.setFixedWidth(30)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^[0-9]{1,2}$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.wnrTabelnummer = QLabel()
            o4Edit = QLineEdit(str(mwnrloonnr))
            o4Edit.setFixedWidth(30)
            o4Edit.setFont(QFont("Arial",10))
            o4Edit.textChanged.connect(self.o4Changed)
            reg_ex = QRegExp("^[0-9]{1,2}$")
            input_validator = QRegExpValidator(reg_ex, o4Edit)
            o4Edit.setValidator(input_validator)
            
            self.Loontrede = QLabel()
            q5Edit = QLineEdit(str(int(mtrede/0.03)))
            q5Edit.setFixedWidth(30)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp("^[0-9]{1,2}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
                                     
            self.Reiskostenvergoeding = QLabel()
            q8Edit = QLineEdit(str(round(mreisk,2)))
            q8Edit.setFixedWidth(100)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.setAlignment(Qt.AlignRight)
            q8Edit.textChanged.connect(self.q8Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
                                              
            self.Auto = QLabel()
            q18Edit = QLineEdit(str(round(mauto,2)))
            q18Edit.setFixedWidth(100)
            q18Edit.setFont(QFont("Arial",10))
            q18Edit.setAlignment(Qt.AlignRight)
            q18Edit.textChanged.connect(self.q18Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q18Edit)
            q18Edit.setValidator(input_validator)
             
            self.Periodiekeuitkering = QLabel()
            q12Edit = QLineEdit(str(round(mperiodiek,2)))
            q12Edit.setFixedWidth(100)
            q12Edit.setAlignment(Qt.AlignRight)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.setAlignment(Qt.AlignRight)
            q12Edit.textChanged.connect(self.q12Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q12Edit)
            q12Edit.setValidator(input_validator)
            
            self.Overigeinhoudingen = QLabel()
            q13Edit = QLineEdit(str(round(moveriginh,2)))
            q13Edit.setFixedWidth(100)
            q13Edit.setAlignment(Qt.AlignRight)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setAlignment(Qt.AlignRight)
            q13Edit.textChanged.connect(self.q13Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q13Edit)
            q13Edit.setValidator(input_validator)
  
            self.Overigevergoedingen = QLabel()
            q19Edit = QLineEdit(str(round(moverigverg,2)))
            q19Edit.setFixedWidth(100)
            q19Edit.setAlignment(Qt.AlignRight)
            q19Edit.setFont(QFont("Arial",10))
            q19Edit.setAlignment(Qt.AlignRight)
            q19Edit.textChanged.connect(self.q19Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q19Edit)
            q19Edit.setValidator(input_validator)
    
            self.Indienst = QLabel()
            q14Edit = QLineEdit(mindienst)
            q14Edit.setFixedWidth(100)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.textChanged.connect(self.q14Changed)
            reg_ex = QRegExp('^[1-2]{1}[09]{1}[0-9]{2}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q14Edit)
            q14Edit.setValidator(input_validator)
                        
            self.Brutoloon = QLabel()
            q15Edit = QLineEdit('{:12.2f}'.format(mbruto))
            q15Edit.setDisabled(True)
            q15Edit.setFixedWidth(100)
            q15Edit.setAlignment(Qt.AlignRight)
            q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q15Edit.textChanged.connect(self.q15Changed)
            
            self.Verlofsaldo = QLabel()
            q16Edit = QLineEdit('{:12.2f}'.format(mverlofsaldo))
            q16Edit.setDisabled(True)
            q16Edit.setFixedWidth(100)
            q16Edit.setAlignment(Qt.AlignRight)
            q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q16Edit.textChanged.connect(self.q16Changed)

            self.ExtraVerlof = QLabel()
            q17Edit = QLineEdit(str(round(mextraverlof,2)))
            q17Edit.setFixedWidth(100)
            q17Edit.setAlignment(Qt.AlignRight)
            q17Edit.setFont(QFont("Arial",10))
            q17Edit.textChanged.connect(self.q17Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q17Edit)
            q17Edit.setValidator(input_validator)
             
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,1 , 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 4, 1, 1, Qt.AlignCenter)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Modify employee data from\n'+mvoorn+\
                ' '+machtern+'\nDate of birth: '+mgeboren), 1, 1, 1, 3)
            
            grid.addWidget(QLabel('Gross monthly salary'), 3, 2)
            grid.addWidget(q15Edit, 3, 3) 
                                                
            grid.addWidget(QLabel('Accountnumber'), 3, 0)
            grid.addWidget(q2Edit, 3, 1)
            
            grid.addWidget(QLabel('Wage table'), 6, 0)
            grid.addWidget(q4Edit, 6 , 1) 
            
            grid.addWidget(QLabel('Orig'), 6, 1, 1, 1, Qt.AlignCenter)
            grid.addWidget(o4Edit, 6, 1, 1, 1, Qt.AlignRight)
             
            grid.addWidget(QLabel('Wage step'), 7, 0)
            grid.addWidget(q5Edit, 7, 1)
                                                      
            grid.addWidget(QLabel('Travel compensation'), 4, 2)
            grid.addWidget(q8Edit, 4, 3)
                                      
            grid.addWidget(QLabel('Periodic payment taxed'), 5, 0)
            grid.addWidget(q12Edit, 5, 1) 
            
            grid.addWidget(QLabel('Other deductions tax-free'), 5, 2)
            grid.addWidget(q13Edit, 5, 3) 
            
            grid.addWidget(QLabel('Addition Company car'), 4, 0)
            grid.addWidget(q18Edit, 4, 1) 
                           
            grid.addWidget(QLabel('Other Fees\nnon-taxed'), 6, 2)
            grid.addWidget(q19Edit, 6, 3) 
       
            grid.addWidget(QLabel('Date of entry into service'), 8, 0)
            grid.addWidget(q14Edit, 8, 1) 
            
            grid.addWidget(QLabel('Leave balance in hours'), 7, 2)
            grid.addWidget(q16Edit, 7, 3)
            
            grid.addWidget(QLabel('Extra leave in hours'), 8, 2)
            grid.addWidget(q17Edit, 8, 3)
            
            grid.addWidget(QLabel('Hourly wage'), 9, 0)
            grid.addWidget(QLabel(str(round(muurl, 2))), 9, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Travel hourly wage'), 9, 2)
            grid.addWidget(QLabel(str(round(mreisuurl, 2))), 9, 3)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 1, 1, 2)
            self.setLayout(grid)
            self.setGeometry(400, 250, 350, 300)
                         
            applyBtn = QPushButton('Modify')
            applyBtn.clicked.connect(self.accept)
                       
            grid.addWidget(applyBtn, 10, 4)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: wijzSluit(self, m_email))
        
            grid.addWidget(cancelBtn, 9, 4)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
        
            grid.addWidget(infoBtn, 8, 4)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                
         def q2Changed(self, text):
            self.Accountnummer.setText(text)
                       
         def q4Changed(self, text):
            self.Loontabelnummer.setText(text)

         def o4Changed(self, text):
            self.wnrTabelnummer.setText(text)
            
         def q5Changed(self, text):
            self.Loontrede.setText(text)
                              
         def q8Changed(self, text):
            self.Reiskostenvergoeding.setText(text)
        
         def q12Changed(self, text):
            self.Periodiekeuitkering.setText(text)
            
         def q13Changed(self, text):
            self.Overigeinhoudingen.setText(text)
            
         def q14Changed(self, text):
            self.Indienst.setText(text)
        
         def q15Changed(self, text):
            self.Brutoloon.setText(text)
            
         def q16Changed(self, text):
            self.Verlofsaldo.setText(text)
            
         def q17Changed(self, text):
            self.ExtraVerlof.setText(text)
       
         def q18Changed(self, text):
            self.Auto.setText(text)
            
         def q19Changed(self, text):
            self.Overigevergoedingen.setText(text)
            
         def returnAccountnummer(self):
            return self.Accountnummer.text()
        
         def returnLoontabelnummer(self):
            return self.Loontabelnummer.text()
        
         def returnWnrLoonnummer(self):
            return self.wnrTabelnummer.text()
    
         def returnLoontrede(self):
            return self.Loontrede.text()
     
         def returnReiskostenvergoeding(self):
            return self.Reiskostenvergoeding.text()
                              
         def returnPeriodiekeuitkering(self):
            return self.Periodiekeuitkering.text()
    
         def returnOverigeinhoudingen(self):
            return self.Overigeinhoudingen.text()   
 
         def returnIndienst(self):
            return self.Indienst.text()   
    
         def returnBrutoloon(self):
            return self.Brutoloon.text() 
        
         def returnVerlofsaldo(self):
            return self.Verlofsaldo.text() 

         def returnExtraVerlof(self):
            return self.ExtraVerlof.text() 
        
         def returnAuto(self):
            return self.Auto.text() 
        
         def returnOverigevergoedingen(self):
            return self.Overigevergoedingen.text() 
                
         @staticmethod
         def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnAccountnummer(), dialog.returnLoontabelnummer(),\
               dialog.returnWnrLoonnummer(),dialog.returnLoontrede(),\
               dialog.returnReiskostenvergoeding(), dialog.returnPeriodiekeuitkering(),\
               dialog.returnOverigeinhoudingen(),dialog.returnIndienst(),\
               dialog.returnBrutoloon(), dialog.returnVerlofsaldo(),\
               dialog.returnExtraVerlof(), dialog.returnAuto(), dialog.returnOverigevergoedingen()]   

    window = Widget()
    data = window.getData()
    if data[1]:
        mloontabel = int(data[1])
    else:
        mloontabel = rpwerkn[2]
    if data[2]:
        mwnrloonnr = int(data[2])
    elif not rpwerkn[12]:
        mwnrloonnr = rpwerkn[2]
    elif not data[2]: 
        mwnrloonnr = rpwerkn[12]
    if data[3]:
        mtrede = int(data[2])
    else:
        mtrede = rpwerkn[3]
    if data[4]:
        mreisk = float(data[3])
    else:
        mreisk = rpwerkn[4]
    if data[5]:
        mperiod = float(data[4])
    else:
        mperiod = rpwerkn[5]
    if data[6]:
        moverig = float(data[5])
    else:
        moverig = rpwerkn[6]
    if data[7]:
        mindienst = data[6]
    else:
        mindienst = rpwerkn[9]
    if data[9]:
        mextraverlof = data[9]
    else:
        mextraverlof = rpwerkn[11]
    if data[10]:
        mauto = data[10]
    else:
        mauto = rpwerkn[8]
    if data[12]:
        movverg = data[11]
    else:
        movverg = rpwerkn[7]
        
    u = update(werknemers).where(werknemers.c.werknemerID == mwerknmr).\
    values(loonID = mloontabel, wnrloonID = mwnrloonnr, loontrede = mtrede, reiskosten_vergoeding = mreisk,\
        periodieke_uitkeringen=mperiod, overige_inhoudingen=moverig,\
        indienst = mindienst, extraverlof = mextraverlof, bedrijfsauto = mauto,\
        overige_vergoedingen = movverg)  
    conn.execute(u)
    conn.close()
    updateOK()
    zoekWerknemer(m_email)