from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                QDialog, QMessageBox ,QComboBox 
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey, \
                        MetaData, create_engine, func)
from sqlalchemy.sql import select, insert, and_

def invoerGelukt():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer dienstenorder gelukt!')
    msg.setWindowTitle('Inkooporder diensten')
    msg.exec_()
    
def foutInvoer():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer. Voer gegevens opnieuw in!')
    msg.setWindowTitle('Inkooporder diensten')
    msg.exec_() 
    
def invoerBestaat():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Warning)
    msg.setText('De betreffende dienst is al verwerkt!')
    msg.setWindowTitle('Inkooporder diensten')
    msg.exec_() 

def geenRegels():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen calculatieregels van betreffende dienst aanwezig!')
    msg.setWindowTitle('Inkooporder diensten')
    msg.exec_()     
    
def sluitRegels(m_email, mlevnr, mwerknr, mregel, self):
    self.close()
    zoekLeverancier(m_email, mlevnr, mwerknr, mregel)

def foutLeverancier():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Leverancier/Werknummer\nniet gevonden!')
    msg.setWindowTitle('Inkooporder diensten')
    msg.exec_()
        
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
                 
def _11check(mlevnr):
    number = str(mlevnr)
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

def zoekLeverancier(m_email, mlevnr, mwerknr, mregel):
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True))
            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Inkooporders diensten invoeren.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                            
            self.Leveranciernummer = QLabel()
            levEdit = QLineEdit(str(mlevnr))
            levEdit.setFixedWidth(100)
            levEdit.setFont(QFont("Arial",10))
            levEdit.textChanged.connect(self.levChanged)
            reg_ex = QRegExp('^[3]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            levEdit.setValidator(input_validator)
                            
            self.Werknummer = QLabel()
            werknEdit = QLineEdit(str(mwerknr))
            werknEdit.setFixedWidth(100)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
            reg_ex = QRegExp('^[8]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            werknEdit.setValidator(input_validator)
            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Leverancier\nWerknummer\n  Diensten'), 0, 1)
    
            grid.addWidget(QLabel('Leverancier'), 1, 0)
            grid.addWidget(levEdit, 1, 1)
            
            grid.addWidget(QLabel('Werknummer'), 2, 0)
            grid.addWidget(werknEdit, 2, 1)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 3, 0, 1 ,3, Qt.AlignCenter)
       
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(120)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 1, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(120)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(600, 400, 150, 150)
    
        def levChanged(self, text):
            self.Leveranciernummer.setText(text)
            
        def werknChanged(self, text):
            self.Werknummer.setText(text)
    
        def returnLeveranciernummer(self):
            return self.Leveranciernummer.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnLeveranciernummer(), dialog.returnWerknummer()]
       
    window = Widget()
    data = window.getData()
    if data[0] and data[1] and len(data[0]) == 9 and len(data[1]) == 9\
           and _11check(data[0]) and  _11check(data[1]):
        mlevnr = int(data[0])
        mwerknr = int(data[1])
    sel = select([leveranciers, werken]).where(and_(leveranciers.c.leverancierID\
                == mlevnr, werken.c.werknummerID == mwerknr))
    rplev = conn.execute(sel).first()
    mregel = 1
    if rplev:
        inkoopRegels(m_email, rplev, mregel)
    else:
        foutLeverancier()
        zoekLeverancier(m_email, mlevnr, mwerknr , mregel)
            
def bepaalInkoopOrdernr(mregel):
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer, primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    morderinkoopnr=(conn.execute(select([func.max(orders_inkoop.c.orderinkoopID, type_=Integer)\
                                   .label('morderinkoopnr')])).scalar())
    if mregel == 1:
       morderinkoopnr=int(maak11proef(morderinkoopnr))
    return(morderinkoopnr)
   
def Inkooporder(m_email, rplev, mregel):
    mlevnr = int(rplev[0])
    mwerknr = int(rplev[6])
    mbedrnaam = rplev[1]
    mrechtsvorm = rplev[2]
    mpostcode = rplev[3]
    mhuisnr = int(rplev[4])
    if rplev[5]:
        mtoev = rplev[5]
    else:
        mtoev=''
    import postcode
    mstrplts = postcode.checkpostcode(mpostcode, mhuisnr)
    mstraat = mstrplts[0]
    mplaats = mstrplts[1]
    minkordnr = bepaalInkoopOrdernr(mregel)
    return(minkordnr, mlevnr, mbedrnaam, mrechtsvorm, mstraat, mhuisnr,\
               mtoev, mpostcode, mplaats, mwerknr)
      
def inkoopRegels(m_email, rplev, mregel):
    minkgeg = Inkooporder(m_email, rplev, mregel)
    minkordnr = minkgeg[0]
    mlevnr = minkgeg[1]
    mwerknr = minkgeg[9]
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Bestelregels inkooporder diensten inbrengen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                       
            self.Inkoopordernummer = QLabel()
            inkorderEdit = QLineEdit(str(minkordnr))
            inkorderEdit.setDisabled(True)
            inkorderEdit.setAlignment(Qt.AlignRight)
            inkorderEdit.setFixedWidth(100)
            inkorderEdit.setFont(QFont("Arial",10))
            inkorderEdit.textChanged.connect(self.inkorderChanged) 
        
            self.Werknummer = QLabel()
            werknEdit = QLineEdit(str(mwerknr))
            werknEdit.setFixedWidth(100)
            werknEdit.setAlignment(Qt.AlignRight)
            werknEdit.setDisabled(True)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
                            
            self.Diensten= QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(250)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('   Keuze Diensten / Materieel') 
            k0Edit.addItem('1. Inhuur')
            k0Edit.addItem('2. Leiding')
            k0Edit.addItem('3. Huisvesting')
            k0Edit.addItem('4. Kabelwerk')
            k0Edit.addItem('5. Grondverzet')
            k0Edit.addItem('6. Betonwerk')
            k0Edit.addItem('7. Vervoer')
            k0Edit.addItem('8. Overig')
            k0Edit.addItem('A. Sleuvengraver')
            k0Edit.addItem('B. Persapparaat')
            k0Edit.addItem('C. Atlaskraan')
            k0Edit.addItem('D. Kraan groot')
            k0Edit.addItem('E. Mainliner')
            k0Edit.addItem('F. Hormachine')
            k0Edit.addItem('G. Wagon')
            k0Edit.addItem('H. Locomotor')
            k0Edit.addItem('J. Locomotief')
            k0Edit.addItem('K. Montagewagen')
            k0Edit.addItem('L. Stormobiel') 
            k0Edit.addItem('M. Robeltrein') 
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.OrderregelPrijs = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setFixedWidth(130)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            q1Edit.setDisabled(True)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
             
            self.Omschrijving = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(400)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp("^.{0,50}$")
            input_validator = QRegExpValidator(reg_ex,q2Edit)
            q2Edit.setValidator(input_validator)    
        
            self.GeplandeStart = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setCursorPosition(0)
            q3Edit.setFixedWidth(130)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)  
            
            self.GeplandGereed = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setCursorPosition(0)
            q4Edit.setFixedWidth(130)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)  
                        
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,1, 0)
            
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Bestelling voor\nLeverancier: '+str(minkgeg[1])\
            +',\n'+minkgeg[2]+' '+minkgeg[3]+',\n'+minkgeg[4]+' '+str(minkgeg[5])\
            +minkgeg[6]+',\n'+minkgeg[7]+' '+minkgeg[8]+'.\nOrderregel '+str(mregel)), 1, 1, 1, 3)
                                             
            lbl1 = QLabel('Ordernummer')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 5, 0)
            grid.addWidget(inkorderEdit, 5, 1)
            
            grid.addWidget(QLabel('Werknummer'), 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(werknEdit, 6, 1)  
 
            lbl8 = QLabel('Soort Order  *')
            lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl8, 7, 0)
            grid.addWidget(k0Edit, 7, 1)
             
            '''
            lbl4 = QLabel('Aanneemsom')  
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 8, 0)
            grid.addWidget(q1Edit, 8, 1)
            '''
            
            lbl5 = QLabel('Omschrijving  *')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 9, 0)
            grid.addWidget(q2Edit, 9, 1, 1 , 3)
            
            lbl6 = QLabel('Geplande Start jjjj-mm-dd  *')  
            lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl6, 10, 0)
            grid.addWidget(q3Edit, 10, 1)
            
            lbl7 = QLabel('Gepland Gereed jjjj-mm-dd  *')  
            lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl7, 11, 0)
            grid.addWidget(q4Edit, 11, 1)
            grid.addWidget(QLabel('* Verplichte Invoer'), 11, 2, 1, 2)
                   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
         
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 3, 1 , 1, Qt.AlignRight)
                       
            self.setLayout(grid)
            self.setGeometry(600, 150, 150, 150)
    
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 12, 3, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(lambda: sluitRegels(m_email, mlevnr, mwerknr, mregel, self))
    
            grid.addWidget(sluitBtn, 12, 2)
            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                                        
        def inkorderChanged(self, text):
            self.Inkoopordernummer.setText(text)
            
        def werknChanged(self, text):
            self.Werknummer.setText(text)
         
        def q1Changed(self,text):
            self.OrderregelPrijs.setText(text)
            
        def q2Changed(self,text):
            self.Omschrijving.setText(text)
        
        def q3Changed(self,text):
            self.GeplandeStart.setText(text)
            
        def q4Changed(self,text):
            self.GeplandGereed.setText(text)
                  
        def k0Changed(self,text):
            self.Diensten.setText(text)  
                       
        def returninkorder(self):
            return self.Inkoopordernummer.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()    
                 
        def returnq1(self):
            return self.Omschrijving.text()
        
        def returnq2(self):
            return self.OrderregelPrijs.text()
        
        def returnq3(self):
            return self.GeplandeStart.text()
        
        def returnq4(self):
            return self.GeplandGereed.text()
                      
        def returnk0(self):
            return self.Diensten.text() 
       
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnq1(),\
                    dialog.returnq2(), dialog.returnq3(), dialog.returnq4()]  
   
    window = Widget()
    data = window.getData()
         
    if data[0] and data[1] and data[3] and data[4]:
        soort = data[0]
        momschr = data[1]
        geplstart = data[3]
        geplgereed = data[4]
    else:
        foutInvoer()
        inkoopRegels(m_email, rplev, mregel)
          
    metadata = MetaData()
    orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
        Column('orddienstlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('werkomschr', String),
        Column('omschrijving', String),
        Column('aanneemsom', Float),
        Column('plan_start', String),
        Column('werk_start', String),
        Column('plan_gereed', String),
        Column('werk_gereed', String),
        Column('acceptatie_gereed', Float),
        Column('acceptatie_datum', String),
        Column('regel', Integer))
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True), 
        Column('koppelnummer', Integer),
        Column('inhuur', Float),            
        Column('uren_inhuur', Float),
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float),
        Column('sleuvengraver', Float),
        Column('persapparaat', Float),
        Column('atlaskraan', Float),
        Column('kraan_groot', Float),
        Column('mainliner', Float),
        Column('hormachine', Float),
        Column('wagon', Float),
        Column('locomotor', Float),
        Column('locomotief', Float),
        Column('montagewagen', Float),
        Column('stormobiel', Float),
        Column('robeltrein', Float),
        Column('verwerkt', Integer))
    params_services = Table('params_services', metadata,
                            Column('servicesID', Integer, primary_key=True),
                            Column('hourly_tariff', Float),
                            Column('item', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    selpar = select([params_services]).order_by(params_services.c.servicesID)
    rppar = conn.execute(selpar).fetchall()
   
    selcal = select([calculaties]).where(calculaties.c.koppelnummer == mwerknr)
    seldienst = select([orders_inkoop_diensten]).where(and_(orders_inkoop_diensten.c.werknummerID == mwerknr,\
      orders_inkoop_diensten.c.werkomschr.like(soort+'%')))
    rpdienst = conn.execute(seldienst).first()
    rpcal = conn.execute(selcal)
                    
    if mregel == 1 and data[0] and not rpdienst:
        datum = str(datetime.datetime.now())
        mbestdatum = (datum[0:4]+'-'+datum[8:10]+'-'+datum[5:7])
        metadata = MetaData()
        orders_inkoop = Table('orders_inkoop', metadata,
            Column('orderinkoopID', Integer(), primary_key=True),
            Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')),
            Column('besteldatum', String),
            Column('status', Integer))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        mbestdatum = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
        ins = insert(orders_inkoop).values(orderinkoopID = minkordnr, leverancierID =\
                    mlevnr, besteldatum = mbestdatum, status = 1)
        conn.execute(ins)

    flag = 0    
    if soort[0] == '1' and not rpdienst:
        minh_uren = 0
        minhuur = 0
        for row in rpcal:
            if row[2]:
                minh_uren += row[3]
                minhuur += row[2]
                flag = 1
        if flag:
            try:
                mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
                mdienstnr += 1
            except:
                mdienstnr = 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(minh_uren,2))+' uren', omschrijving = momschr,\
                 aanneemsom = minhuur,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '2' and not rpdienst: 
        mleiding = 0
        for row in rpcal:
            if row[4]:
                mleiding += row[4]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort, omschrijving = momschr, aanneemsom = mleiding,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '3' and not rpdienst:
        mhuisvesting = 0
        for row in rpcal:
            if row[5]:
                mhuisvesting += row[5]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort, omschrijving = momschr, aanneemsom = mhuisvesting,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '4' and not rpdienst:
        mkabelwerk = 0
        for row in rpcal:
            if row[6]:
                mkabelwerk += row[6]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort , omschrijving = momschr, aanneemsom = mkabelwerk ,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '5' and not rpdienst:
        mgrondverzet = 0
        for row in rpcal:
            if row[7]:
                mgrondverzet += row[7]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort , omschrijving = momschr, aanneemsom = mgrondverzet,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '6' and not rpdienst:
        mbetonwerk = 0
        for row in rpcal:
            if row[8]:
                mbetonwerk += row[8]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort, omschrijving = momschr, aanneemsom = mbetonwerk,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '7' and not rpdienst:
        mvervoer = 0
        for row in rpcal:
            if row[9]:
                mvervoer += row[9]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort, omschrijving = momschr, aanneemsom = mvervoer,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == '8' and not rpdienst:
        moverig = 0
        for row in rpcal:
            if row[10]:
                moverig += row[10]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort, omschrijving = momschr, aanneemsom = moverig,\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'A' and not rpdienst:
        msleuf = 0
        for row in rpcal:
            if row[11]:
                msleuf += row[11]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(msleuf,2))+' uren', omschrijving = momschr,\
                 aanneemsom = msleuf*rppar[0][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'B' and not rpdienst:
        mpers = 0 
        for row in rpcal:
            if row[12]:
                mpers += row[12]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mpers,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mpers*rppar[1][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'C' and not rpdienst:
        matlas = 0 
        for row in rpcal:
            if row[13]:
                matlas += row[13]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(matlas,2))+' uren', omschrijving = momschr,\
                 aanneemsom = matlas*rppar[2][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'D' and not rpdienst:
        mkrgroot = 0
        for row in rpcal:
            if row[14]:
                mkrgroot += row[14]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mkrgroot,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mkrgroot*rppar[3][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'E' and not rpdienst:
        mmainliner = 0
        for row in rpcal:
            if row[15]:
                mmainliner += row[15]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mmainliner,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mmainliner*rppar[4][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'F' and not rpdienst:
        mhor = 0
        for row in rpcal:
            if row[16]:
                mhor += row[16]
                flag = 1 
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mhor,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mhor*rppar[5][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'G' and not rpdienst:
        mwagon = 0
        for row in rpcal:
            if row[17]:
                mwagon += row[17]
                flag = 1 
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mwagon,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mwagon*rppar[6][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'H' and not rpdienst:
        mlmotor = 0
        for row in rpcal:
            if row[18]:
                mlmotor += row[18]
                flag = 1 
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mlmotor,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mlmotor*rppar[7][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'J' and not rpdienst:
        mlmotief = 0
        for row in rpcal:
            if row[19]:
                mlmotief += row[19]
                flag = 1 
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mlmotief,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mlmotief*rppar[8][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'K' and not rpdienst:
        mmont = 0
        for row in rpcal:
            if row[20]:
                mmont += row[20]
                flag = 1 
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mmont,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mmont*rppar[9][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'L' and not rpdienst:
        mstorm = 0
        for row in rpcal:
            if row[21]:
                mstorm += row[21]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mstorm,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mstorm*rppar[10][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif soort[0] == 'M' and not rpdienst:
        mrobel = 0
        for row in rpcal:
            if row[22]:
                mrobel += row[22]
                flag = 1
        if flag:
            mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
                type_=Integer).label('mdienstnr')])).scalar())
            mdienstnr += 1
            insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
                 orderinkoopID = minkordnr, werknummerID = mwerknr,\
                 werkomschr = soort+' '+str(round(mrobel,2))+' uren', omschrijving = momschr,\
                 aanneemsom = mrobel*rppar[11][1],\
                 plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
            conn.execute(insrgl)
            mregel += 1
            invoerGelukt()
    elif rpdienst:
        invoerBestaat()
    if flag == 0 and not rpdienst:
        geenRegels()
    conn.close
    inkoopRegels(m_email, rplev, mregel)