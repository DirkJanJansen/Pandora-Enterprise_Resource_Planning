from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton,\
     QMessageBox, QLineEdit, QGridLayout, QDialog, QCheckBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, \
                            ForeignKey, create_engine, Boolean)
from sqlalchemy.sql import select, update, func
         
def _11check(mcontr):
    number = str(mcontr)
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

def foutAccount():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Foutief accountnummer opgegeven,\n en/of account niet geldig voor deze bewerking!')
        msg.setWindowTitle('Mutaties diensten werken')
        msg.exec_()
              
def foutWerk():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Foutief werknummer opgegeven!')
        msg.setWindowTitle('Mutaties diensten werken')
        msg.exec_()
        
def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Werknummer is afgemeld,\nboekingen niet meer mogelijk!')
    msg.setWindowTitle('Mutaties uren werken')
    msg.exec_()
    
def geenKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen kostensoort keuze gemaakt')
    msg.setWindowTitle('Mutaties uren werken')               
    msg.exec_()
    
def ongDatum():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Ongeldige datum ingevoerd')
    msg.setWindowTitle('Mutaties uren werken')               
    msg.exec_()
    
def geenUren():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Geen uren ingevoerd!')
    msg.setWindowTitle('Mutaties uren werken')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)  

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
        \t\t\t\t\t\t\t\t\t\t 
                                        Informatie over te muteren uren.  
                                         
        De module start met de volgende variabele gegevens:
        Accountnummer: leeg veld in te vullen met accountnummer van de werknemer.
        Werknummer: leeg veld in te vullen met het werknummer, waarvoor wordt gewerkt.
        Aanwezig/Afwezig: kies hier de soort uren, waarvoor de boeking moet worden gedaan,
        bv. 100% reguliere uren, 125% overwerk, 150% overwerk, 200% overwerk, 
        of een van de diverse genoemde afwezigheidsuren voor verlof ziekte enz.
        Aantal uren: Uren die zijn gewerkt op de dag van de werkzaamheden.
        Datum werkzaamheden:  datum van de huidige dag in het formaat jjjj-mm-dd
        Button 'Muteren' Standaard button met tekst 'Muteren'
        Bij het aanpassen of invullen van de velden 'Accountnummer', 'Werknummer' en
        'Datum werkzaamheden', zal het systeem bij opkomen van de velden de laatst
        ingetoetste gegevens onthouden, zodat een snelle invoer mogelijk is.
        De keuze Aanwezig/Afwezig zal standaard ingevuld worden met 100% uren,
        omdat dit de meest voorkomende keuze zal zijn.
        Bij het intoetsen van de gegevens zal  bij een juiste invoer de knop
        'Muteren' groen kleuren. Bij een foutieve of niet gelukte invoer zal de 
        knop 'Muteren' rood kleuren, in dit geval dient een korrektie te worden 
        gemaakt, omdat de invoer niet is geboekt!
   
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

def urenMut(maccountnr, mwerknr, mboekd, merror, m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Muteren uren")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Account = QLabel()
            zkaccEdit = QLineEdit(str(maccountnr))
            zkaccEdit.setFixedWidth(150)
            zkaccEdit.setFont(QFont("Arial",10))
            zkaccEdit.textChanged.connect(self.zkaccChanged)
            reg_ex = QRegExp("^[1]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, zkaccEdit)
            zkaccEdit.setValidator(input_validator)
            
            self.Werknummer = QLabel()
            zkwerknEdit = QLineEdit(str(mwerknr))
            zkwerknEdit.setFixedWidth(150)
            zkwerknEdit.setFont(QFont("Arial",10))
            zkwerknEdit.textChanged.connect(self.zkwerknChanged) 
            reg_ex = QRegExp("^[8]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, zkwerknEdit)
            zkwerknEdit.setValidator(input_validator)
     
            self.Soort = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(150)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('100%')
            k0Edit.addItem('125%')
            k0Edit.addItem('150%')
            k0Edit.addItem('200%')
            k0Edit.addItem('Reis')
            k0Edit.addItem('Verlof')
            k0Edit.addItem('Extra verlof')
            k0Edit.addItem('Ziekte')
            k0Edit.addItem('Feestdag')
            k0Edit.addItem('Dokter')
            k0Edit.addItem('Geoorl. verzuim')
            k0Edit.addItem('Ong. verzuim')
            k0Edit.activated[str].connect(self.k0Changed) 
                        
            self.Werkuren = QLabel()
            urenEdit = QLineEdit()
            urenEdit.setFixedWidth(150)
            urenEdit.setFont(QFont("Arial",10))
            urenEdit.textChanged.connect(self.urenChanged) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, urenEdit)
            urenEdit.setValidator(input_validator)
            
            self.Boekdatum = QLabel()
            boekdatumEdit = QLineEdit(mboekd)
            boekdatumEdit.setFixedWidth(150)
            boekdatumEdit.setFont(QFont("Arial",10))
            boekdatumEdit.textChanged.connect(self.boekdatumChanged) 
            reg_ex = QRegExp("^[2]{1}[0-1]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, boekdatumEdit)
            boekdatumEdit.setValidator(input_validator)
           
            grid = QGridLayout()
            grid.setSpacing(20)
                                
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0 , 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)       

            lblt = QLabel(' Muteren uren (werken - lonen) niet cumulatief')
            grid.addWidget(lblt , 6, 0, 1, 3, Qt.AlignCenter)
                  
            grid.addWidget(QLabel('  \u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 8, 0, 1, 3, Qt.AlignCenter)
                                              
            lbl1 = QLabel('Accountnummer')  
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(zkaccEdit, 1, 1)
           
            lbl2 = QLabel('Werknummer')  
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 2, 0)
            grid.addWidget(zkwerknEdit,2, 1)
            
            lbl4 = QLabel('Aanwezig/Afwezig')  
            lbl4.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl4, 3, 0)
            grid.addWidget(k0Edit, 3, 1)
     
            lbl3 = QLabel('Aantal uren')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 4, 0)
            grid.addWidget(urenEdit, 4, 1)
        
            lbl5 = QLabel('Datum Werkzaamheden')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 5, 0)
            grid.addWidget(boekdatumEdit,5, 1)
                      
            cBox = QCheckBox('Meerwerk')
            cBox.stateChanged.connect(self.cBoxChanged)
            grid.addWidget(cBox, 3, 2)
                                     
            applyBtn = QPushButton('Muteren')
            applyBtn.clicked.connect(self.accept)
    
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            if merror == 1:
                applyBtn.setStyleSheet("color: black; background-color: #00CC66")
            elif  merror == 2:
                applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            else:
                applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(applyBtn,7, 2 , 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 7, 1, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
                 
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info()) 
    
            grid.addWidget(infoBtn, 7, 0, 1, 1, Qt.AlignRight)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black; background-color: gainsboro") 
                                  
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
           
        def zkaccChanged(self, text):
            self.Account.setText(text)
            
        def zkwerknChanged(self, text):
            self.Werknummer.setText(text)
            
        def k0Changed(self,text):
            self.Soort.setText(text)
            
        def urenChanged(self,text):
            self.Werkuren.setText(text)
            
        def boekdatumChanged(self, text):
            self.Boekdatum.setText(text)
                    
        state = False  
        def cBoxChanged(self, state):
             if state == Qt.Checked:
                 self.state = True
      
        def returnzkacc(self):
            return self.Account.text()
        
        def returnzkwerkn(self):
            return self.Werknummer.text()
        
        def returnk0(self):
            return self.Soort.text()
        
        def returnuren(self):
            return self.Werkuren.text()
             
        def returnboekdatum(self):
            return self.Boekdatum.text()
    
        def returncBox(self):
            return self.state
           
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnzkacc(), dialog.returnzkwerkn(),dialog.returnk0(),\
                    dialog.returnuren(), dialog.returncBox(), dialog.returnboekdatum()]  
      
    window = Widget()
    data = window.getData()
    muren = 0
    mu125 = 0
    mu150 = 0
    mu200 = 0
    mreis = 0
    mmeerw100 = 0
    mmeerw125 = 0
    mmeerw150 = 0
    mmeerw200 = 0
    mverlof = 0
    mextraverlof = 0
    mziek = 0
    mfeest = 0
    mdokter = 0
    mgverzuim = 0
    moverzuim = 0
     
    if data[0] and len(data[0]) == 9 and _11check(data[0]):
        maccountnr = int(data[0])
    elif not data[0] and len(str(maccountnr)) == 9 and _11check(maccountnr):
        maccountnr = int(maccountnr)
    else:
       foutAccount()
       return('', mwerknr, mboekd, merror, m_email)
    if data[1] and len(data[1])== 9  and _11check(data[1]):
        mwerknr = int(data[1])
    elif not data[1] and len(str(mwerknr)) == 9 and _11check(mwerknr):
        mwerknr = int(mwerknr) 
    else:
        foutWerk()
        return(maccountnr, '', mboekd, merror, m_email)
                
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('voortgangstatus', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
    rpwerk = con.execute(selwerk).first()
     
    if data[2]:
        keuze = data[2]
    elif data[2] == '':
        keuze = '100%'
    else:
        geenKeuze()
        return(maccountnr, mwerknr, mboekd, merror, m_email)
    if data[4]:
        mstatus = True
    else:
        mstatus = False
    if data[5]:
        mboekd = data[5]
        if len(mboekd) != 10 or int(mboekd[0:4]) < 2020 or int(mboekd\
             [0:4]) > 2099 or int(mboekd[5:7]) >12 or int(mboekd[8:10]) > 31:
            ongDatum()
            return(maccountnr, mwerknr, mboekd, merror, m_email)
    else:
        mboekd =  mboekd
     
    if rpwerk[1] == 'H':
        mwerknr = 1
        werkGereed()
        return(maccountnr, mwerknr, mboekd, merror, m_email)
    elif not data[3] or data[3] == '0' or data[3] == '.':
        merror = 2
        return(maccountnr, mwerknr, mboekd, merror,m_email)
    elif data[3] and keuze == '100%' and mstatus:
        mmeerw100 = float(data[3])
    elif data[3] and keuze == '100%':
        muren = float(data[3])
    elif data[3] and keuze == '125%' and mstatus:
        mmeerw125 = float(data[3])
    elif data[3] and keuze == '125%':
        mu125 = float(data[3])
    elif data[3] and keuze == '150%' and mstatus:
        mmeerw150 = float(data[3])
    elif data[3] and keuze == '150%':
        mu150 = float(data[3])
    elif data[3] and keuze == '200%' and mstatus:
        mmeerw200 = float(data[3])
    elif data[3] and keuze == '200%':
        mu200 = float(data[3])
    elif data[3] and keuze == 'Reis':
        mreis = float(data[3])
    elif data[3] and keuze == 'Verlof':
        mverlof = float(data[3])
        mstatus = False
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(verlofsaldo = werknemers.c.verlofsaldo - mverlof)
        con.execute(upd) 
    elif data[3] and keuze == 'Extra verlof':
        mextraverlof = float(data[3])
        mstatus = False
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(extraverlof = werknemers.c.extraverlof - mextraverlof)
        con.execute(upd)       
    elif data[3] and keuze == 'Ziekte':
        mziek = float(data[3])
    elif data[3] and keuze == 'Feestdag':
        mfeest = float(data[3])
        mstatus = False
    elif data[3] and keuze == 'Dokter':
        mdokter = float(data[3])
        mstatus = False
    elif data[3] and keuze == 'Geoorl. verzuim':
        mgverzuim = float(data[3]) 
        mstatus = False
    elif data[3] and keuze == 'Ong. verzuim':
        moverzuim = float(data[3])  
        mstatus = False
    else:
        merror = 2
        return(maccountnr, mwerknr, mboekd, merror, m_email)
                         
    metadata = MetaData()
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('werknummerID',Integer),       
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('tabelloon', Float),
        Column('reisloon', Float),
        Column('bruto_loonbedrag', Float),
        Column('meerwerkstatus', Boolean),
        Column('soort', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('wnrloonID', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('kosten_lonen', Float),
        Column('voortgangstatus', String),
        Column('statusweek', String(6)),
        Column('werk_constr_uren', Float),
        Column('werk_mont_uren', Float),
        Column('werk_retourlas_uren', Float),
        Column('werk_telecom_uren', Float),
        Column('werk_bfi_uren', Float),
        Column('werk_bvl_uren', Float),
        Column('werk_spoorleg_uren', Float),
        Column('werk_spoorlas_uren', Float),
        Column('werk_reis_uren', Float),
        Column('meerminderwerk', Float),
        Column('werk_voeding_uren', Float))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur', Float),
        Column('reisuur', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mw = select([werknemers]).where(werknemers.c.accountID == maccountnr)
    result = con.execute(mw).first()
    if not result:
        foutAccount()
        return(maccountnr, mwerknr, mboekd, merror, m_email)
    mwrkwnruren=(con.execute(select([func.max(wrkwnrln.c.wrkwnrurenID, type_=Integer)\
                                   .label('mwrkwnruren')])).scalar())
    wrkgr = result[2]
    wrkgr2 = result[3]
    loonsel = select([lonen]).where(lonen.c.loonID == wrkgr)
    loonsel2 = select([lonen]).where(lonen.c.loonID == wrkgr2)
    loonres = con.execute(loonsel).first()
    loonres2 = con.execute(loonsel2).first()
    muurloon = loonres2[1]
    mwerkuur = loonres[2]
    mreisuur = loonres[3]
    mwrku125 = mwerkuur*1.25
    mwrku150 = mwerkuur*1.5
    mwrku200 = mwerkuur*2
    loonk = (muren*mwerkuur)+(mreis*mreisuur)+(mu125*mwrku125)+(mu150*mwrku150)+\
             (mu200*mwrku200)+(mmeerw100*mwerkuur)+(mmeerw125*mwerkuur)+(mmeerw150*\
             mwerkuur)+(mmeerw200*mwerkuur)
    meerk = (mmeerw100*mwerkuur)+(mmeerw125*mwrku125)+\
            (mmeerw150*mwrku150)+(mmeerw200*mwrku200)
    lonen = (muren*muurloon)+(mu125*muurloon*1.25)+(mu150*muurloon*1.5)+(mu200\
             *muurloon*2)+(mreis*mreisuur)+(mmeerw100*muurloon)+\
             (mmeerw125*muurloon*1.25)+(mmeerw150*muurloon*1.5)+\
             (mmeerw200*muurloon*2)+(mverlof*muurloon)+(mextraverlof*muurloon)+\
             (mziek*muurloon)+(mfeest*muurloon)+(mdokter*muurloon)+\
             (mgverzuim*muurloon)+(moverzuim*muurloon)
     
    inswrkwnrln = wrkwnrln.insert().values(
    wrkwnrurenID = mwrkwnruren+1,
    werknemerID = result[0],
    boekdatum = mboekd,
    aantaluren = muren+mu125+mu150+mu200+mreis+mmeerw100+mmeerw125+mmeerw150+\
      mmeerw200+mverlof+mextraverlof+mziek+mfeest+mdokter+mgverzuim+moverzuim,
    soort = keuze,
    werknummerID = mwerknr,
    tabelloon = muurloon,
    reisloon = mreisuur,
    bruto_loonbedrag = lonen,
    meerwerkstatus = mstatus,
    loonID = wrkgr2)

    if con.execute(inswrkwnrln):
        merror = 1
    else:
        merror = 2
        return(maccountnr, mwerknr, mboekd, merror, m_email) 
                 
    if wrkgr < 5:
        stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
        values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_constr_uren = werken.c.werk_constr_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
        con.execute(stmt)
    elif wrkgr < 9:   
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_mont_uren = werken.c.werk_mont_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 13:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_retourlas_uren = werken.c.werk_retourlas_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 17:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_telecom_uren = werken.c.werk_telecom_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
                meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 21:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_bfi_uren = werken.c.werk_bfi_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 25:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_bvl_uren = werken.c.werk_bvl_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
                meerminderwerk = werken.c.meerminderwerk + meerk)
          con.xecute(stmt)
    elif wrkgr < 29:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_spoorleg_uren = werken.c.werk_spoorleg_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 33:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_mont_uren = werken.c.werk_spoorlas_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    elif wrkgr < 37:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_voeding_uren = werken.c.werk_voeding_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
    con.close   
    return(maccountnr, mwerknr, mboekd, merror, m_email) 
