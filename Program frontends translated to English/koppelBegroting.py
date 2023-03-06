import datetime
from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout,\
                             QPushButton, QMessageBox, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update,  and_

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def foutWerknr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Work number is incorrect!')
    msg.setWindowTitle('Link budget')
    msg.exec_()
    
def gekoppeld():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Work number is already linked!')
    msg.setWindowTitle('Link budget')
    msg.exec_()
    
def verwFout(mwerknr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Link has already taken place\nthe budgeted data has previously been transferred to work '+str(mwerknr)+'!')
    msg.setWindowTitle('Link budget')
    msg.exec_()
    
def foutCalc():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Calculation is not found!')
    msg.setWindowTitle('Link budget')
    msg.exec_()
        
def geenOpdracht():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No order yet!')
    msg.setWindowTitle('Link budget')
    msg.exec_()

def gegevensOk():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Transfer was successful!')
    msg.setWindowTitle('Link budget')
    msg.exec_()

def zoekBegroting(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Link calculation")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                                      
            self.Calculatie = QLabel()
            zkcalcEdit = QLineEdit()
            zkcalcEdit.setFixedWidth(100)
            zkcalcEdit.setFont(QFont("Arial",10))
            zkcalcEdit.textChanged.connect(self.zkcalcChanged)
            reg_ex = QRegExp('^[1-9]{1}[0-9]{0,8}$')
            input_validator = QRegExpValidator(reg_ex, zkcalcEdit)
            zkcalcEdit.setValidator(input_validator)  
            
            self.Werknummer = QLabel()
            zkwerknrEdit = QLineEdit()
            zkwerknrEdit.setFixedWidth(100)
            zkwerknrEdit.setFont(QFont("Arial",10))
            zkwerknrEdit.textChanged.connect(self.zkwerknrChanged)
            reg_ex = QRegExp('^[8]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, zkwerknrEdit)
            zkwerknrEdit.setValidator(input_validator)  
           
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            lbl1 = QLabel('Calculation number')
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zkcalcEdit, 3, 1)
            
            lbl2 = QLabel('Work umber')
            lbl2.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl2, 4, 0)
            grid.addWidget(zkwerknrEdit, 4, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 2, Qt.AlignRight)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 2, Qt.AlignRight)
   
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 6, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 6, 0, 1, 1,Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
             
        def zkcalcChanged(self, text):
            self.Calculatie.setText(text)
            
        def zkwerknrChanged(self, text):
            self.Werknummer.setText(text)
             
        def returnCalculatie(self):
            return self.Calculatie.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnCalculatie(), dialog.returnWerknummer()]       

    window = Widget()
    data = window.getData()
    if not data[0] or not data[1]:
        zoekBegroting(m_email)
    mcalnr = int(data[0])
    mwerknr = int(data[1])
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calculatie', Integer),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('opdracht_datum', String),
        Column('calculatienummer', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selcl = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpcl = con.execute(selcl).first()
    selwrk = select([werken]).where(werken.c.werknummerID == mwerknr)
    rpwerk = con.execute(selwrk).first()
    if not rpcl:
        foutCalc()
        zoekBegroting(m_email)
    if not rpwerk:
        foutWerknr()
        zoekBegroting(m_email)
    mcalnr = rpcl[0]
    mwerkomschr = rpcl[1]
    mverw = rpcl[2]
    verder = False
    if rpcl and mverw == 1:
        verder = True
    elif rpcl and mverw > 1:
        verwFout(mwerknr)
        zoekBegroting(m_email)
    if rpwerk and rpwerk[1] == '':
        geenOpdracht()
        zoekBegroting(m_email)
    elif rpwerk[2] > 0:
        gekoppeld()
        zoekBegroting(m_email)
    elif rpwerk and rpwerk[1] and verder:
        koppelCalc(mcalnr, mwerknr,mwerkomschr, m_email)
   
def koppelCalc(mcalnr, mwerknr, mwerkomschr, m_email):
    msgBox=QMessageBox()
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Link budget")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText('Description: '+mwerkomschr+'\nThis calculation only linking\nthen all data is definitive\nProceed?')
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        metadata = MetaData()
        calculaties = Table('calculaties', metadata,
            Column('calcID', Integer(), primary_key=True),
            Column('clusterID', None, ForeignKey('clusters.clusterID')),
            Column('koppelnummer', Integer),
            Column('calculatie', Integer),
            Column('omschrijving', String),
            Column('hoeveelheid', Float),
            Column('eenheid', String),
            Column('prijs', Float),
            Column('materialen', Float),
            Column('lonen', Float),
            Column('diensten', Float),
            Column('materieel', Float),
            Column('inhuur', Float),
            Column('uren_constr', Float),
            Column('uren_mont', Float),
            Column('uren_retourlas', Float),
            Column('uren_telecom', Float),
            Column('uren_bfi', Float),
            Column('uren_voeding', Float),
            Column('uren_bvl', Float),
            Column('uren_spoorleg', Float),
            Column('uren_spoorlas', Float),
            Column('uren_inhuur', Float),
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
            Column('werkomschrijving', String),
            Column('verwerkt', Integer),
            Column('leiding', Float),
            Column('huisvesting', Float),
            Column('kabelwerk', Float),
            Column('grondverzet', Float),
            Column('betonwerk', Float),
            Column('vervoer', Float),
            Column('overig', Float))
        werken = Table('werken', metadata,
            Column('werknummerID', Integer(), primary_key=True),
            Column('aanneemsom', Float),
            Column('begr_materialen', Float),
            Column('begr_materieel', Float),
            Column('begr_inhuur', Float),
            Column('begr_constr_uren', Float),
            Column('begr_mont_uren', Float),
            Column('begr_retourlas_uren', Float),
            Column('begr_telecom_uren', Float),
            Column('begr_bfi_uren', Float),
            Column('begr_voeding_uren', Float),
            Column('begr_bvl_uren', Float),
            Column('begr_spoorleg_uren', Float),
            Column('begr_spoorlas_uren', Float),
            Column('begr_lonen', Float),
            Column('werkomschrijving', String),
            Column('calculatienummer', Integer),
            Column('begr_leiding', Float),
            Column('begr_huisv', Float),
            Column('begr_kabelwerk', Float),
            Column('begr_grondverzet', Float),
            Column('begr_beton_bvl', Float),
            Column('begr_vervoer', Float),
            Column('begr_overig', Float))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selcal = select([calculaties,werken]).where(and_(calculaties.c.calculatie == mcalnr,\
                       werken.c.werknummerID == mwerknr))
        rpcal = con.execute(selcal)
        for regel in rpcal:
            updcal = update(calculaties).where(calculaties.c.calculatie == mcalnr)\
             .values(koppelnummer = regel[37], werkomschrijving = regel[52], verwerkt = 2)
            con.execute(updcal)
            
            updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
              .values(aanneemsom = werken.c.aanneemsom+regel[7],\
              begr_materialen = werken.c.begr_materialen+regel[8],\
              begr_materieel = werken.c.begr_materieel+regel[11],\
              begr_lonen = werken.c.begr_lonen+regel[9],\
              begr_inhuur = werken.c.begr_inhuur+regel[12],\
              begr_constr_uren = werken.c.begr_constr_uren+regel[13],\
              begr_mont_uren = werken.c.begr_mont_uren+regel[14],\
              begr_retourlas_uren = werken.c.begr_retourlas_uren+regel[15],\
              begr_telecom_uren = werken.c.begr_telecom_uren + regel[16],\
              begr_bfi_uren = werken.c.begr_bfi_uren + regel[17],\
              begr_voeding_uren = werken.c.begr_voeding_uren + regel[18],\
              begr_bvl_uren = werken.c.begr_bvl_uren + regel[19] ,\
              begr_spoorleg_uren = werken.c.begr_spoorleg_uren + regel[20],\
              begr_spoorlas_uren = werken.c.begr_spoorlas_uren + regel[21],\
              begr_leiding = werken.c.begr_leiding + regel[37],\
              begr_huisv = werken.c.begr_huisv + regel[38],\
              begr_kabelwerk = werken.c.begr_kabelwerk + regel[39],\
              begr_grondverzet = werken.c.begr_grondverzet + regel[40],\
              begr_beton_bvl = werken.c.begr_beton_bvl + regel[41],\
              begr_vervoer = werken.c.begr_vervoer + regel[42],\
              begr_overig = werken.c.begr_overig + regel[43],\
              calculatienummer = mcalnr)
            con.execute(updwerk)
            
        materiaallijsten = Table('materiaallijsten', metadata,
            Column('matlijstID', Integer, primary_key=True),
            Column('calculatie', Integer),
            Column('hoeveelheid', Float),
            Column('artikelID', None, ForeignKey('artikelen.artikelID')),
            Column('werknummerID', Integer),
            Column('orderinkoopID', Integer),
            Column('reserverings_datum', String),
            Column('levertijd_begin', String),
            Column('levertijd_end', String),
            Column('categorie', Integer))
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer(), primary_key=True),
            Column('reserveringsaldo', Float),
            Column('categorie', Integer),
            Column('bestelsaldo', Float))
   
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selmat = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.\
            c.calculatie == mcalnr, materiaallijsten.c.artikelID == artikelen.c.artikelID))
        rpmat = con.execute(selmat)
        mboekd = str(datetime.datetime.now())[0:10]
        for row in rpmat:
           updres = update(materiaallijsten).where(and_(materiaallijsten.c.calculatie == mcalnr,\
             materiaallijsten.c.artikelID == artikelen.c.artikelID)).values(werknummerID = mwerknr,\
             reserverings_datum = mboekd, categorie = artikelen.c.categorie)
           con.execute(updres)
           updart = update(artikelen).where(and_(materiaallijsten.c.artikelID ==\
                artikelen.c.artikelID, materiaallijsten.c.calculatie == mcalnr))\
                .values(reserveringsaldo = artikelen.c.reserveringsaldo + materiaallijsten.c.hoeveelheid)
           con.execute(updart)
        gegevensOk()
        zoekBegroting(m_email)
    else:
        hoofdMenu(m_email)