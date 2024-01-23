from login import hoofdMenu
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout,\
                             QPushButton, QMessageBox, QLineEdit, QWidget,\
                             QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update, insert, and_, func

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def foutWerknr():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Order has not yet been obtained for this calculation\nOrder for Purchase cannot be printed yet!')
    msg.setWindowTitle('Work number')
    msg.exec_()
    
def calcBestaatniet():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Calculation is not present!')
    msg.setWindowTitle('Entry')
    msg.exec_()
    
def printing():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Just a moment printing is started!')
    msg.setWindowTitle('Printing')
    msg.exec_()
     
def zoekCalculatie(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Calculate / Requesting / Printing")
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
            
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            lbl1 = QLabel('Calculation number\nor Work number.')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(zkcalcEdit, 1, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 0, 1, 1,Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
             
        def zkcalcChanged(self, text):
            self.Calculatie.setText(text)
             
        def returnCalculatie(self):
            return self.Calculatie.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnCalculatie()]       

    window = Widget()
    data = window.getData()
    
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calculatie', Integer),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer),
        Column('koppelnummer', Integer))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if not data[0]:
       return(0)
    elif data[0][0] == '8' and len(data[0]) == 9:
        mcalnr = data[0]
        selcl = select([calculaties]).where(calculaties.c.koppelnummer == int(mcalnr))
        rpcl = con.execute(selcl).first()
    elif data[0] and len(data[0]) <9:
        mcalnr = data[0]
        selcl = select([calculaties]).where(calculaties.c.calculatie == int(mcalnr))
        rpcl = con.execute(selcl).first()
    else:
        calcBestaatniet()
        zoekCalculatie(m_email)
    if not rpcl:
        calcBestaatniet()
        zoekCalculatie(m_email)
    elif rpcl and (not rpcl[2]):
        opbouwRp(rpcl[0], rpcl[1], rpcl[2], rpcl[3], m_email)
    elif rpcl and rpcl[2]:
        opvragenCalc(rpcl[0], rpcl[1], rpcl[2], rpcl[3], m_email)
    
def opvragenCalc(mcalnr, mwerkomschr,mverw, mwerknr, m_email):
    class MainWindow(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.lbl = QLabel()
            self.pixmap = QPixmap('./images/logos/verbinding.jpg')
            self.lbl.setPixmap(self.pixmap)
            grid.addWidget(self.lbl , 0, 1)
    
            self.logo = QLabel()
            self.pixmap = QPixmap('./images/logos/logo.jpg')
            self.logo.setPixmap(self.pixmap)
            grid.addWidget(self.logo , 0, 3, 1, 1, Qt.AlignRight)
              
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Calculation:      '+str(mcalnr)+'\nWork number: '+str(mwerknr)), 1, 1, 1, 3)
            grid.addWidget(QLabel(mwerkomschr[0:35]), 2 , 1, 1, 3)
                                    
            self.setWindowTitle("Request calculation / printing")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                                      
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved\n   dj.jansen@casema.nl'), 7, 0, 2, 4, Qt.AlignCenter)
            
            self.toonBtn = QPushButton('Calculation\nRequest')
            self.toonBtn.clicked.connect(lambda: toonCalculatie(mcalnr, mwerknr))
            grid.addWidget(self.toonBtn, 5, 3)
            self.toonBtn.setFont(QFont("Arial",10))
            self.toonBtn.setFixedWidth(110)           
            self.toonBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.artlijstBtn = QPushButton('Article list\nRequest')
            self.artlijstBtn.clicked.connect(lambda: toonArtikellijst(mcalnr, mwerknr))
            grid.addWidget(self.artlijstBtn,5, 1, 1, 1, Qt.AlignRight)
            self.artlijstBtn.setFont(QFont("Arial",10))
            self.artlijstBtn.setFixedWidth(110)
            self.artlijstBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.dienstenBtn = QPushButton('Services + Equipment\nOrder list Requesting')
            self.dienstenBtn.clicked.connect(lambda: toonDienstenlijst(mcalnr, mwerknr))
            grid.addWidget(self.dienstenBtn, 5, 2)
            self.dienstenBtn.setFont(QFont("Arial",10))
            self.dienstenBtn.setFixedWidth(200)
            self.dienstenBtn.setStyleSheet("color: black;  background-color: gainsboro")
                             
            self.printBtn = QPushButton('Calculation\nPrinting')
            self.printBtn.clicked.connect(lambda: printCalculatie(mcalnr, mwerknr))
            grid.addWidget(self.printBtn, 4, 3)
            self.printBtn.setFont(QFont("Arial",10))
            self.printBtn.setFixedWidth(110)
            self.printBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.artprintBtn = QPushButton('Article list\nPrinting')
            self.artprintBtn.clicked.connect(lambda: printArtikellijst(mcalnr, mwerknr))
            grid.addWidget(self.artprintBtn, 4, 1, 1, 1, Qt.AlignRight)
            self.artprintBtn.setFont(QFont("Arial",10))
            self.artprintBtn.setFixedWidth(110)
            self.artprintBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.dienstenprintBtn = QPushButton('Service + Equipment\nOrder list Printing')
            self.dienstenprintBtn.clicked.connect(lambda: printDienstenlijst(mcalnr, mwerknr))
            grid.addWidget(self.dienstenprintBtn, 4, 2)
            self.dienstenprintBtn.setFont(QFont("Arial",10))
            self.dienstenprintBtn.setFixedWidth(200)
            self.dienstenprintBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
            self.terugBtn = QPushButton('B\na\nc\nk')
            self.terugBtn.clicked.connect(self.close)
            grid.addWidget(self.terugBtn, 4, 1, 5, 1, Qt.AlignTop)
            self.terugBtn.setFont(QFont("Arial", 10))
            self.terugBtn.setFixedWidth(40)
            self.terugBtn.setFixedHeight(125)
            self.terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                             
            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)
     
    mainWin = MainWindow()
    mainWin.exec_()
    zoekCalculatie(m_email)
    
def opbouwRp(mcalnr, mwerkomschr, mverw, mwerknr, m_email):
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float),
        Column('calculatie', Integer),
        Column('materialen', Float))
    cluster_artikelen = Table('cluster_artikelen', metadata,
        Column('cluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelprijs', Float))
    
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('tarieffactor', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selmat=select([calculaties, cluster_artikelen, artikelen]).where(and_(\
            calculaties.c.calculatie == mcalnr,\
            calculaties.c.clusterID == cluster_artikelen.c.clusterID,\
            cluster_artikelen.c.artikelID == artikelen.c.artikelID))
    rpmat = con.execute(selmat)
    for rij in rpmat:
        updcalmat = update(calculaties).where(and_(calculaties.c.calculatie ==\
           mcalnr, calculaties.c.clusterID == rij[1],\
           cluster_artikelen.c.artikelID == rij[9])).values(\
           materialen = calculaties.c.materialen+rij[2]*rij[8]*rij[10]*(1+rppar[6][1]))
        con.execute(updcalmat)
   
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('omschrijving', String),
        Column('werkomschrijving', String),
        Column('calcID', Integer(), primary_key=True),
        Column('calculatie', Integer),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('verwerkt', Integer),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
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
        Column('uren_inhuur', Float),
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
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float))
    clusters = Table('clusters', metadata,
        Column('clusterID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
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
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float))
    cluster_artikelen = Table('cluster_artikelen', metadata,
        Column('cluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_eenheid', String))
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('calculatie', Integer),
        Column('hoeveelheid', Float),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('artikelprijs', Float),
        Column('subtotaal', Float),
        Column('resterend', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcalc = select([calculaties, clusters]).where(and_(calculaties.c\
       .calculatie == int(mcalnr), calculaties.c.clusterID == clusters.c.clusterID))
    rpcalc = con.execute(selcalc)
    selclart = select([cluster_artikelen,artikelen]).where(and_(cluster_artikelen.c.\
      artikelID == artikelen.c.artikelID, calculaties.c.clusterID ==\
      cluster_artikelen.c.clusterID, calculaties.c.calculatie == (int(mcalnr))))\
      .order_by(cluster_artikelen.c.clusterID, cluster_artikelen.c.artikelID)
    rpclart = con.execute(selclart)
    for record in rpcalc:
        updcalc = update(calculaties).where(and_(calculaties.c.calculatie == record[3],\
           calculaties.c.clusterID == clusters.c.clusterID)).values(verwerkt = 1, \
           uren_constr = calculaties.c.uren_constr+clusters.c.uren_constr*calculaties.c.hoeveelheid,\
           uren_mont = calculaties.c.uren_mont+clusters.c.uren_mont*calculaties.c.hoeveelheid,\
           uren_retourlas = calculaties.c.uren_retourlas+clusters.c.uren_retourlas*calculaties.c.hoeveelheid,\
           uren_telecom = calculaties.c.uren_telecom+clusters.c.uren_telecom*calculaties.c.hoeveelheid,\
           uren_bfi = calculaties.c.uren_bfi+clusters.c.uren_bfi*calculaties.c.hoeveelheid,\
           uren_voeding = calculaties.c.uren_voeding+clusters.c.uren_voeding*calculaties.c.hoeveelheid,\
           uren_bvl = calculaties.c.uren_bvl+clusters.c.uren_bvl*calculaties.c.hoeveelheid,\
           uren_spoorleg = calculaties.c.uren_spoorleg+clusters.c.uren_spoorleg*calculaties.c.hoeveelheid,\
           uren_spoorlas = calculaties.c.uren_spoorlas+clusters.c.uren_spoorlas*calculaties.c.hoeveelheid,\
           uren_inhuur = calculaties.c.uren_inhuur+clusters.c.uren_inhuur*calculaties.c.hoeveelheid,\
           sleuvengraver = calculaties.c.sleuvengraver+clusters.c.sleuvengraver*calculaties.c.hoeveelheid,\
           persapparaat = calculaties.c.persapparaat+clusters.c.persapparaat*calculaties.c.hoeveelheid,\
           atlaskraan = calculaties.c.atlaskraan+clusters.c.atlaskraan*calculaties.c.hoeveelheid,\
           kraan_groot = calculaties.c.kraan_groot+clusters.c.kraan_groot*calculaties.c.hoeveelheid,\
           mainliner = calculaties.c.mainliner+clusters.c.mainliner*calculaties.c.hoeveelheid,\
           hormachine = calculaties.c.hormachine+clusters.c.hormachine*calculaties.c.hoeveelheid,\
           wagon = calculaties.c.wagon+clusters.c.wagon*calculaties.c.hoeveelheid,\
           locomotor = calculaties.c.locomotor+clusters.c.locomotor*calculaties.c.hoeveelheid,\
           locomotief = calculaties.c.locomotief+clusters.c.locomotief*calculaties.c.hoeveelheid,\
           montagewagen = calculaties.c.montagewagen+clusters.c.montagewagen*calculaties.c.hoeveelheid,\
           stormobiel = calculaties.c.stormobiel+clusters.c.stormobiel*calculaties.c.hoeveelheid,\
           robeltrein = calculaties.c.robeltrein+clusters.c.robeltrein*calculaties.c.hoeveelheid)
        con.execute(updcalc)
        updcal1 = update(calculaties).where(and_(calculaties.c.calculatie == record[3],\
           calculaties.c.clusterID == clusters.c.clusterID)).values(\
        lonen = calculaties.c.uren_constr+clusters.c.uren_constr*rppar[8][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_mont+clusters.c.uren_mont*rppar[9][1]+\
           calculaties.c.uren_retourlas+clusters.c.uren_retourlas*rppar[15][1]+\
           calculaties.c.uren_telecom+clusters.c.uren_telecom*rppar[18][1]+\
           calculaties.c.uren_bfi+clusters.c.uren_bfi*rppar[10][1]+\
           calculaties.c.uren_voeding+clusters.c.uren_voeding*rppar[11][1]+\
           calculaties.c.uren_bvl+clusters.c.uren_bvl*rppar[12][1]+\
           calculaties.c.uren_spoorleg+clusters.c.uren_spoorleg*rppar[13][1]+\
           calculaties.c.uren_spoorlas+clusters.c.uren_spoorlas*rppar[14][1],
       inhuur = calculaties.c.uren_inhuur+clusters.c.uren_inhuur*rppar[7][1]*rppar[7][3],
       materieel = calculaties.c.sleuvengraver+clusters.c.sleuvengraver*rppar[19][1]*rppar[19][3]+\
           calculaties.c.persapparaat+clusters.c.persapparaat*rppar[20][1]*rppar[20][3]+\
           calculaties.c.atlaskraan+clusters.c.atlaskraan*rppar[21][1]*rppar[21][3]+\
           calculaties.c.kraan_groot+clusters.c.kraan_groot*rppar[22][1]*rppar[22][3]+\
           calculaties.c.mainliner+clusters.c.mainliner*rppar[23][1]*rppar[23][3]+\
           calculaties.c.hormachine+clusters.c.hormachine*rppar[24][1]*rppar[24][3]+
           calculaties.c.wagon+clusters.c.wagon*rppar[25][1]*rppar[25][3]+\
           calculaties.c.locomotor+clusters.c.locomotor*rppar[26][1]*rppar[26][3]+\
           calculaties.c.locomotief+clusters.c.locomotief*rppar[27][1]*rppar[27][3]+\
           calculaties.c.montagewagen+clusters.c.montagewagen*rppar[28][1]*rppar[28][3]+\
           calculaties.c.stormobiel+clusters.c.stormobiel*rppar[29][1]*rppar[29][3]+\
           calculaties.c.robeltrein+clusters.c.robeltrein*rppar[30][1]*rppar[30][3],\
           diensten = calculaties.c.leiding+clusters.c.leiding+\
           calculaties.c.huisvesting+clusters.c.huisvesting+\
           calculaties.c.kabelwerk+clusters.c.kabelwerk+\
           calculaties.c.grondverzet+clusters.c.grondverzet+\
           calculaties.c.betonwerk+clusters.c.betonwerk+\
           calculaties.c.vervoer+clusters.c.vervoer+\
           calculaties.c.overig+clusters.c.overig)
        con.execute(updcal1)
        for row in rpclart:
            selart = select([materiaallijsten.c.artikelID, materiaallijsten.c.calculatie]).where(and_(materiaallijsten.\
                c.artikelID == row[1], materiaallijsten.c.calculatie == record[3]))
            rpart = con.execute(selart).first()
            if rpart:
                updmatlijst = update(materiaallijsten).where(and_(materiaallijsten.c.\
                  artikelID == row[1], materiaallijsten.c.calculatie == record[3]))\
                 .values(hoeveelheid = materiaallijsten.c.hoeveelheid+(record[5]*row[3]),\
                artikelprijs = row[6]*(1+rppar[6][1]), subtotaal = materiaallijsten.\
                c.subtotaal+record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(updmatlijst)
            elif not rpart:
                try:
                    mmatlijstnr = (con.execute(select([func.max(materiaallijsten.c.matlijstID,\
                        type_=Integer)])).scalar())
                    mmatlijstnr += 1
                except:
                    mmatlijstnr = 1
                insmatlijst = insert(materiaallijsten).values(matlijstID = mmatlijstnr,\
                    calculatie = record[3], artikelID = row[1],\
                    hoeveelheid = record[5]*row[3], resterend = record[5]*row[3],\
                    artikelprijs = row[6]*(1+rppar[6][1]),\
                    subtotaal = record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(insmatlijst)
        selber = select([calculaties.c.calcID, calculaties.c.calculatie])\
                           .where(calculaties.c.calculatie == mcalnr)
        rpselber = con.execute(selber)
        for regel in rpselber:
            updber = update(calculaties).where(calculaties.c.calculatie==mcalnr)\
             .values(prijs=calculaties.c.materialen+calculaties.c.materieel+\
              calculaties.c.lonen+calculaties.c.diensten, werkomschrijving = mwerkomschr)
            con.execute(updber)
    opvragenCalc(mcalnr, mwerkomschr, mverw, mwerknr, m_email)
                        
def printCalculatie(mcalnr, mwerknr):
    from sys import platform
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
        Column('werkomschrijving', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpcal = con.execute(selcal)
    
    mblad = 1
    rgl = 0
    mmat = 0
    mlon = 0
    mmater = 0
    minh = 0
    mtotaal = 0
    for row in rpcal:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename = '.\\forms\\Extern_Clustercalculaties\\clustercalculation_'+str(row[3])+'-'+str(row[2])+'.txt'
            else:
                filename = './forms/Extern_Clustercalculaties/clustercalculation_'+str(row[3])+'-'+str(row[2])+'.txt'
            kop=\
    ('Work number: '+str(mwerknr)+' '+'{:<24s}'.format(str(row[12]))+'  Calculation: '+str(row[3])+'  Date: '+str(datetime.datetime.now())[0:10]+'  Page : '+str(mblad)+'\n'+
    '=====================================================================================================\n'+
    'Cluster  Clustername           Unit Number    Materials      Wages  Equipment   Services      Amount \n'+
    '=====================================================================================================\n')
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<9s}'.format(row[1])+'{:<22.21s}'.format(row[4])+'{:<6s}'.format(row[6])+'{:5.2f}'.format(row[5])+'  '+'{:11.2f}'.format(row[8])+'{:11.2f}'.format(row[9])+'{:11.2f}'.format(row[11])+'{:11.2f}'.format(row[10])+'{:12.2f}'.format(row[7])+'\n')
        mmat = mmat+row[8]
        mlon = mlon+row[9]
        mmater = mmater+row[11]
        minh = minh+row[10]
        mtotaal = mtotaal+row[7]
        rgl += 1
    tail =(\
    '-------------------------------------------------------------------------------------------------------\n'+
    'Totals                                      '+'{:11.2f}'.format(mmat)+'{:11.2f}'.format(mlon)+'{:11.2f}'.format(mmater)+'{:11.2f}'.format(minh)+'{:12.2f}'.format(mtotaal)+'\n'
    '=======================================================================================================\n')
    open(filename,'a').write(tail)
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
                     
def printArtikellijst(mcalnr, mwerknr):
    from sys import platform
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('calculatie', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('subtotaal', Float))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('art_eenheid', String),
         Column('locatie_magazijn', String))
    calculaties = Table('calculaties', metadata,
        Column('calculatie', Integer),
        Column('koppelnummer', Integer))
                                    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selmat = select([materiaallijsten, artikelen])\
      .where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.calculatie == mcalnr)).order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)
    selkop = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpkop = con.execute(selkop).first()
    mblad = 1
    rgl = 0
    for row in rpmat:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename =  filename = '.\\forms\\Extern_Clustercalculaties\\material_list_'+str(rpkop[0])+'-'+str(rpkop[1])+'.txt'
            else:
                filename =  filename = './forms/Extern_Clustercalculaties/material_list_'+str(rpkop[0])+'-'+str(rpkop[1])+'.txt'
            kop=\
    ('Work number:   '+str(mwerknr)+'  Calculation: '+str(rpkop[0])+'   Date: '+str(datetime.datetime.now())[0:10]+'  Page :  '+str(mblad)+'\n'+
    '=============================================================================================\n'+
    'Articlenr  Cluster                             Unit          Price      Number               \n'+
    '=============================================================================================\n')
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<11d}'.format(row[6])+'{:<37.35s}'.format(row[7])+'{:<8.6s}'.format(row[8])+'{:10.2f}'.format(row[3])+'  '+'{:10.2f}'.format(row[4])+'\n')
        rgl += 1
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
    
def printDienstenlijst(mcalnr, mwerknr):
    if mwerknr == 0:
        return(foutWerknr())
    from sys import platform
    metadata = MetaData()               
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('werkomschrijving', String),
        Column('calculatie', Integer),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float), 
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
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String))
                                           
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()  
        
    selcal = select([calculaties]).where(calculaties.c.koppelnummer == mwerknr).\
     order_by(calculaties.c.clusterID)
    rpcal = con.execute(selcal)
    
    mblad = 1
    rgl = 0
    m_uren = 0
    mtotaal = 0
    
    header = ['Hiring','Trench machine','Pressing machine','Atlas crane','Crane big',\
          'Mainliner','Ballast\nscrapper machine','Wagon','Locomotor','Locomotive','Assemble Trolley',\
          'Stormobiel','Robel train','Direction','Housing','Cable work',\
          'Earth moving','Concrete work','Transport','Remaining']
    
    for row in rpcal:
        if row[8] == 0:
            return(foutWerknr())
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename = '.\\forms\\Extern_Clustercalculaties_Diensten\\clustercalculation_'+str(row[2]).replace(' ', '_')+'.txt'
            else:
                filename = './forms/Extern_Clustercalculaties_Diensten/clustercalculation_'+str(row[2]).replace(' ', '_')+'.txt'
            kop=\
    ('Order list internal for purchase orders / reservations Services and Equipment,\nWork number: '+str(mwerknr)+' '+'{:<24s}'.format(str(row[2]))+' Calculation: '+str(row[3])+\
     '  Date: '+str(datetime.datetime.now())[0:10]+'  Page : '+str(mblad)+'\n'+
    '=====================================================================================================\n'+
    'Cluster Cluster description     Number Unit   Description-Service    hours-sub Amount-Sub  Del.period\n'+
    '=====================================================================================================\n')
            if rgl == 0:                 
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
        for k in range(14, 34):
            dienst = header[k-14]
            if k == 14:
                uren = row[k]
                bedrag = row[k]*rppar[7][1]
                #print(row[k],rppar[7][1], rppar[7][2], dienst, '\n')
            elif k < 27:
                uren = row[k]
                bedrag = row[k]*rppar[k+4][1]
                #print(row[k], rppar[k+4][1],rppar[k+4][2], dienst, '\n')
            else:
                bedrag = row[k]
                #print(row[k], dienst, '\n')
                  
            if row[k]:
                open(filename,'a').write('{:<8s}'.format(row[4])+'{:<21.22s}'.format(row[1])+\
                 '{:6.2f}'.format(row[5])+' {:6s}'.format(row[6])+'  {:<18s}'.format(dienst)+\
                 '{:12.2f}'.format(uren)+'{:12.2f}'.format(bedrag)+' {:10s}'.format(' Agree'+'\n'))
                if k < 27:
                    m_uren= m_uren+row[k]
                    mtotaal = mtotaal+row[k]*rppar[k+5][1]
                else:
                    mtotaal = mtotaal+row[k]
        rgl += 1
    tail =(\
    '-----------------------------------------------------------------------------------------------------\n'+
    'Totals                                                          '+'{:11.2f}'.format(m_uren)+'{:12.2f}'.format(mtotaal)+'\n'+
    '=====================================================================================================\n')    
    open(filename,'a').write(tail)
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()

def toonCalculatie(mcalnr, mwerknr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Cluster calculation')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.hideColumn(1)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(ShowSelection)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['ID','Cluster','Work description','Calculation','Cluster number',\
              'Processed','Amount','Unit', 'Link number', 'Total price','Materials',\
              'Wages','Services','Equipment', 'Hiring','Hours\nConstruction','Hours\nMounting',\
              'Hours\nReturn welding', 'Hours\nTelecom', 'Hours\nChief mechanic','Hours\nPower-supply',\
              'Hours\nOCL','Hours\nTrack laying','Hours\nTrack welding','Hours\nHiring',\
              'Hours\nTrench machine','Hours\nPressing machine', 'Hours\nAtlas crane',\
              'Hours\nCrane big','Hours\nMainliner','Hours\nBallast scrape machine','Hours\nWagon',\
              'Hours\nLocomotor','Hours\nLocomotive','Hours\nAssemble trolley','Hours\nStormobiel',\
              'Hours\nRobel train','Direction', 'Housing','Cable work', 'Earth moving',\
              'Concrete work', 'Transport', 'Remaining']

    metadata = MetaData()               
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('werkomschrijving', String),
        Column('calculatie', Integer),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('verwerkt', Integer),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
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
        Column('uren_inhuur', Float),
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
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float))
                                               
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([calculaties]).where(calculaties.c.calculatie == mcalnr).\
     order_by(calculaties.c.clusterID)
    rpcal = con.execute(selcal)
      
    data_list=[]
    for row in rpcal:
        data_list += [(row)]
        
    def ShowSelection(idx):
        mcalnr = idx.data()
        if  idx.column() == 0:

            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcal = select([calculaties]).where(calculaties.c.calcID == mcalnr)
            rpcal = con.execute(selcal).first()
                                                      
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(10)
                    
                    self.setWindowTitle("Request cluster calculation")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Request cluster calculation'),0, 0, 1, 6, Qt.AlignCenter)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 5, 1, 1, Qt.AlignRight)                
                    index = 3
                    for item in header:
                        horpos = index%3
                        verpos = index
                        if index%3 == 1:
                            verpos = index - 1
                        elif index%3 == 2:
                            verpos = index -2
                        self.lbl = QLabel(header[index-3])
                        
                        self.Gegevens = QLabel()
                        if type(rpcal[index-3]) == float:
                            q1Edit = QLineEdit('{:12.2f}'.format(rpcal[index-3]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        elif type(rpcal[index-3]) == int:
                            q1Edit = QLineEdit(str(rpcal[index-3]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        else:
                            q1Edit = QLineEdit(str(rpcal[index-3]))
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        if verpos == 3 and horpos > 0:
                            q1Edit.setFixedWidth(300)
                        else:
                            q1Edit.setFixedWidth(120)
                        q1Edit.setDisabled(True)
                        grid.addWidget(self.lbl, verpos, horpos+horpos%3)
                        grid.addWidget(q1Edit, verpos, horpos+horpos%3+1)
                        
                        index +=1
                        
                    terugBtn = QPushButton('Close')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, verpos+1, 5, 1 , 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100) 
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), verpos+2, 0, 1, 6, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(300, 100, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
            mainWin.raise_()
            mainWin.activateWindow()
            
    win = MyWindow(data_list, header)
    win.exec_()
    
def toonDienstenlijst(mcalnr, mwerknr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Cluster calculation')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.hideColumn(1)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(showDienst)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
        
    header = ['ID','Cluster','Work description','Calculation','Cluster number',\
      'Processed','Amount','Unit', 'Link number', 'Total price','Materials',\
      'Wages','Services','Equipment', 'Hiring','Direction', 'Housing','Cable work',\
      'Earth moving','Concrete work', 'Transport', 'Remaining', 'Hiring','Pressing machine',\
      'Trench machine', 'Atlas crane', 'Crane big', 'Mainliner', 'Ballast scrape machine',\
      'Wagon', 'Locomotor', 'Locomotive', 'Assemble trolley', 'Stormobiel', 'Robel train']

    metadata = MetaData()               
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('werkomschrijving', String),
        Column('calculatie', Integer),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('verwerkt', Integer),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('leiding', Float),
        Column('huisvesting', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('betonwerk', Float),
        Column('vervoer', Float),
        Column('overig', Float),
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
        Column('robeltrein', Float))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selparams = select([params]).where(and_(params.c.paramID < 32,\
                     params.c.paramID > 19)).order_by(params.c.paramID)
    rpparams = con.execute(selparams).fetchall()
                                           
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([calculaties]).where(calculaties.c.calculatie == mcalnr).\
     order_by(calculaties.c.clusterID)
    rpcal = con.execute(selcal)
      
    data_list=[]
    for row in rpcal:
        data_list += [(row)]
    
    def showDienst(idx):
        calcnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            seldienst = select([calculaties]).where(calculaties.c.calcID==calcnr)
            rpcalc = con.execute(seldienst).first()
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Request works external calculation data services")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                         
                    self.setFont(QFont('Arial', 10))
                       
                    q1Edit = QLineEdit(str(rpcalc[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setDisabled(True)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    
                    q2Edit = QLineEdit(rpcalc[1])
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        
                    q3Edit = QLineEdit(rpcalc[2])
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    q4Edit = QLineEdit(str(rpcalc[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
           
                    q5Edit = QLineEdit(str(rpcalc[4]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)                              
                    
                    q8Edit = QLineEdit(str(rpcalc[5]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    q9Edit = QLineEdit('{:12.2f}'.format(rpcalc[6]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                                                         
                    q11Edit = QLineEdit(rpcalc[7])
                    q11Edit.setFixedWidth(100)
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                      
                    q12Edit = QLineEdit(str(rpcalc[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    q13Edit = QLineEdit('{:12.2f}'.format(rpcalc[9]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
             
                    q19Edit = QLineEdit('{:12.2f}'.format(rpcalc[10]))
                    q19Edit.setFixedWidth(100)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
             
                    q14Edit = QLineEdit('{:12.2f}'.format(rpcalc[11]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                                    
                    q15Edit = QLineEdit('{:12.2f}'.format(rpcalc[12]))
                    q15Edit.setDisabled(True)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                   
                    q16Edit = QLineEdit('{:12.2f}'.format(rpcalc[13]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                                            
                    q17Edit = QLineEdit('{:12.2f}'.format(rpcalc[15]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    q20Edit = QLineEdit('{:12.2f}'.format(rpcalc[16]))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                    
                    q21Edit = QLineEdit('{:12.2f}'.format(rpcalc[17]))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setAlignment(Qt.AlignRight)
                    q21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q21Edit.setDisabled(True)
    
                    q22Edit = QLineEdit('{:12.2f}'.format(rpcalc[18]))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q22Edit.setDisabled(True)
    
                    q23Edit = QLineEdit('{:12.2f}'.format(rpcalc[19]))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setAlignment(Qt.AlignRight)
                    q23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q23Edit.setDisabled(True)
                    
                    q24Edit = QLineEdit('{:12.2f}'.format(rpcalc[20]))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q24Edit.setDisabled(True)
                                                  
                    q26Edit = QLineEdit('{:12.2f}'.format(rpcalc[21]))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q26Edit.setDisabled(True)
                    
                    q27Edit = QLineEdit('{:12.2f}'.format(rpcalc[14]))
                    q27Edit.setFixedWidth(100)
                    q27Edit.setAlignment(Qt.AlignRight)
                    q27Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q27Edit.setDisabled(True)
                    
                    q28Edit = QLineEdit('{:12.2f}'.format(rpcalc[23]*rpparams[0][1]))
                    q28Edit.setFixedWidth(100)
                    q28Edit.setAlignment(Qt.AlignRight)
                    q28Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q28Edit.setDisabled(True)
                    
                    q29Edit = QLineEdit('{:12.2f}'.format(rpcalc[24]*rpparams[1][1]))
                    q29Edit.setFixedWidth(100)
                    q29Edit.setAlignment(Qt.AlignRight)
                    q29Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q29Edit.setDisabled(True)
                    
                    q30Edit = QLineEdit('{:12.2f}'.format(rpcalc[25]*rpparams[2][1]))
                    q30Edit.setFixedWidth(100)
                    q30Edit.setAlignment(Qt.AlignRight)
                    q30Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q30Edit.setDisabled(True)
                    
                    q31Edit = QLineEdit('{:12.2f}'.format(rpcalc[26]*rpparams[3][1]))
                    q31Edit.setFixedWidth(100)
                    q31Edit.setAlignment(Qt.AlignRight)
                    q31Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q31Edit.setDisabled(True)
                    
                    q32Edit = QLineEdit('{:12.2f}'.format(rpcalc[27]*rpparams[4][1]))
                    q32Edit.setFixedWidth(100)
                    q32Edit.setAlignment(Qt.AlignRight)
                    q32Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q32Edit.setDisabled(True)
                    
                    q33Edit = QLineEdit('{:12.2f}'.format(rpcalc[28]*rpparams[5][1]))
                    q33Edit.setFixedWidth(100)
                    q33Edit.setAlignment(Qt.AlignRight)
                    q33Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q33Edit.setDisabled(True)
                    
                    q34Edit = QLineEdit('{:12.2f}'.format(rpcalc[29]*rpparams[6][1]))
                    q34Edit.setFixedWidth(100)
                    q34Edit.setAlignment(Qt.AlignRight)
                    q34Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q34Edit.setDisabled(True)
                    
                    q35Edit = QLineEdit('{:12.2f}'.format(rpcalc[30]*rpparams[7][1]))
                    q35Edit.setFixedWidth(100)
                    q35Edit.setAlignment(Qt.AlignRight)
                    q35Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q35Edit.setDisabled(True)
                    
                    q36Edit = QLineEdit('{:12.2f}'.format(rpcalc[31]*rpparams[8][1]))
                    q36Edit.setFixedWidth(100)
                    q36Edit.setAlignment(Qt.AlignRight)
                    q36Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q36Edit.setDisabled(True)
                    
                    q37Edit = QLineEdit('{:12.2f}'.format(rpcalc[32]*rpparams[9][1]))
                    q37Edit.setFixedWidth(100)
                    q37Edit.setAlignment(Qt.AlignRight)
                    q37Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q37Edit.setDisabled(True)
                    
                    q38Edit = QLineEdit('{:12.2f}'.format(rpcalc[33]*rpparams[10][1]))
                    q38Edit.setFixedWidth(100)
                    q38Edit.setAlignment(Qt.AlignRight)
                    q38Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q38Edit.setDisabled(True)
                  
                    q39Edit = QLineEdit('{:12.2f}'.format(rpcalc[34]*rpparams[10][1]))
                    q39Edit.setFixedWidth(100)
                    q39Edit.setAlignment(Qt.AlignRight)
                    q39Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q39Edit.setDisabled(True)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    grid.addWidget(QLabel('Request calculation data from\nServices external works'), 0, 1, 1, 3)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 6, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                     
                    grid.addWidget(QLabel('CalcID'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1) 
                    
                    grid.addWidget(QLabel('Cluster description'), 2, 0)
                    grid.addWidget(q3Edit, 2, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Cluster'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1, 1, 3) 
               
                    grid.addWidget(QLabel('Calculation'), 4, 0)
                    grid.addWidget(q4Edit, 4, 1) 
                     
                    grid.addWidget(QLabel('ClusterID'), 4, 2)
                    grid.addWidget(q5Edit, 4, 3)
                                                              
                    grid.addWidget(QLabel('Processed'), 5, 0)
                    grid.addWidget(q8Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Amount'), 5, 2)
                    grid.addWidget(q9Edit, 5, 3)
                                                
                    grid.addWidget(QLabel('Unit'), 6, 0)
                    grid.addWidget(q11Edit, 6, 1)
                    
                    grid.addWidget(QLabel('Work number'), 6, 2)
                    grid.addWidget(q12Edit, 6, 3)
                    
                    grid.addWidget(QLabel('Price'), 7, 0)
                    grid.addWidget(q13Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Materials'), 7,  2)
                    grid.addWidget(q19Edit, 7, 3)
                                
                    grid.addWidget(QLabel('Wages'), 8, 0)
                    grid.addWidget(q14Edit, 8, 1) 
                        
                    grid.addWidget(QLabel('Services\nTotal'), 8, 2)
                    grid.addWidget(q15Edit, 8, 3)
                                                     
                    grid.addWidget(QLabel('Equipment'), 9, 0)
                    grid.addWidget(q16Edit, 9, 1)                           
                                                 
                    grid.addWidget(QLabel('Direction'), 11, 0)
                    grid.addWidget(q17Edit, 11, 1) 
                                               
                    grid.addWidget(QLabel('Housing'), 11, 2)
                    grid.addWidget(q20Edit, 11, 3)
                   
                    grid.addWidget(QLabel('Cable work'), 12, 0)
                    grid.addWidget(q21Edit, 12, 1)
                                        
                    grid.addWidget(QLabel('Earth moving'), 12, 2)
                    grid.addWidget(q22Edit, 12, 3)
                     
                    grid.addWidget(QLabel('Concrete work'), 13, 0)
                    grid.addWidget(q23Edit, 13, 1)
                                        
                    grid.addWidget(QLabel('Transport'), 13, 2)
                    grid.addWidget(q24Edit, 13, 3)
                                        
                    grid.addWidget(QLabel('Remaining'), 14, 0)
                    grid.addWidget(q26Edit, 14, 1)
                    
                    lblsoort = QLabel('Equipment type')
                    lbluren = QLabel('Hours')
                    lblbedrag = QLabel('Amount')
                    
                    grid.addWidget(lblsoort, 1, 4)
                    grid.addWidget(lbluren, 1, 5)
                    grid.addWidget(lblbedrag, 1, 6)
                    
                    grid.addWidget(QLabel('Hiring'), 2, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[22])), 2, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q27Edit, 2, 6)
                    
                    grid.addWidget(QLabel('Trench machine'), 3, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[23])), 3, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q28Edit, 3, 6)
                    
                    grid.addWidget(QLabel('Pressing machine'), 4, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[24])), 4, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q29Edit, 4, 6)
                    
                    grid.addWidget(QLabel('Atlas crane'), 5, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[25])), 5, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q30Edit, 5, 6)
                    
                    grid.addWidget(QLabel('Crane big'), 6, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[26])), 6, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q31Edit, 6, 6)
                    
                    grid.addWidget(QLabel('Mainliner'), 7, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[27])), 7, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q32Edit, 7, 6)
                    
                    grid.addWidget(QLabel('Ballast clearing machine'), 8, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[28])), 8, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q33Edit, 8, 6)
                    
                    grid.addWidget(QLabel('Wagon'), 9, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[29])), 9, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q34Edit, 9, 6)
                    
                    grid.addWidget(QLabel('Locomotor'), 10, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[30])), 10, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q35Edit, 10, 6)
                    
                    grid.addWidget(QLabel('Locomotive'), 11, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[31])), 11, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q36Edit, 11, 6)
                    
                    grid.addWidget(QLabel('Assemble trolley'), 12, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[32])), 12, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q37Edit, 12, 6)
                    
                    grid.addWidget(QLabel('Stormobiel'), 13, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[33])), 13, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q38Edit, 13, 6)
                    
                    grid.addWidget(QLabel('Robel train'), 14, 4)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpcalc[34])), 14, 5, 1, 1, Qt.AlignRight)
                    grid.addWidget(q39Edit, 14, 6)
                                                                              
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 7, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(500, 50, 350, 300)
                                                                            
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 15, 6, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_() 
            
    win = MyWindow(data_list, header)
    win.exec_()

def toonArtikellijst(mcalnr, mwerknr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1200, 900)
            self.setWindowTitle('Materials list')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                    Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.setColumnHidden(6, True)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(showSelart)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None

    header = ['Article number','Description','Reservation balance','ListID','Calculation',\
              'Work number','Purchase order number', 'Article number','Article price',\
              'Amount','Call-off','Remaining','Subtotal','Reservation date',\
              'Delivery end','Delivery start','Category']

    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('calculatie', Integer),
         Column('werknummerID', Integer),
         Column('orderinkoopID', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('afroep', Float),
         Column('resterend', Float),
         Column('subtotaal', Float),
         Column('reserverings_datum', String),
         Column('levertijd_end', String),
         Column('levertijd_begin', String),
         Column('categorie', Integer))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('reserveringsaldo', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    selmat = select([artikelen,materiaallijsten]).where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
         materiaallijsten.c.artikelID == artikelen.c.artikelID,\
         materiaallijsten.c.calculatie == mcalnr))\
         .order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)

    data_list=[]
    for row in rpmat:
        data_list += [(row)]

    def showSelart(idx):
        martnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()

            selmat = select([artikelen, materiaallijsten]).where(\
                 and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                 materiaallijsten.c.artikelID == int(martnr),\
                 materiaallijsten.c.calculatie == mcalnr))\
                 .order_by(materiaallijsten.c.artikelID)
            rpmat = con.execute(selmat).first()

            header = ['Article number','Description','Reservation balance','ListID','Calculation',\
              'Work number','Purchase order number','Article number','Article price',\
              'Amount','Call-off','Remaining','Subtotal','Reservation date',\
              'Delivery end','Delivery start', 'Category']

            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)

                    grid = QGridLayout()
                    grid.setSpacing(20)

                    self.setWindowTitle("Request Articles Cluster calculation")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

                    self.setFont(QFont('Arial', 10))

                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)

                    grid.addWidget(QLabel('Request Articles calculation'),0, 1, 1, 2)

                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 3, 1, 1, Qt.AlignRight)
                    index = 1
                    for item in header:
                        self.lbl = QLabel(header[index-1])
                        self.Gegevens = QLabel()
                        if index == 1:
                            if type(rpmat[index-1]) == float:
                                q1Edit = QLineEdit('{:12.2f}'.format(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            elif type(rpmat[index-1]) == int:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            else:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setFixedWidth(100)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, 1, 0)
                            grid.addWidget(q1Edit, index, 1, 1, 2)
                        elif index == 2:
                            q1Edit = QLineEdit(str(rpmat[index-1]))
                            q1Edit.setFixedWidth(400)
                            q1Edit.setDisabled(True)
                            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            grid.addWidget(self.lbl, 2, 0)
                            grid.addWidget(q1Edit, index, 1, 1, 3)
                        elif index%2 == 0:
                            if type(rpmat[index-1]) == float:
                                q1Edit = QLineEdit('{:12.2f}'.format(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            elif type(rpmat[index-1]) == int:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            else:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, index, 0)
                            grid.addWidget(q1Edit, index, 1)
                        else:
                            if type(rpmat[index-1]) == float:
                                q1Edit = QLineEdit('{:12.2f}'.format(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            elif type(rpmat[index-1]) == int:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            else:
                                q1Edit = QLineEdit(str(rpmat[index-1]))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, index+1, 2)
                            grid.addWidget(q1Edit, index+1, 3)
                        index += 1

                    terugBtn = QPushButton('Close')
                    terugBtn.clicked.connect(self.accept)

                    grid.addWidget(terugBtn, index+1, 3, 1, 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100)
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+2, 0, 1, 4, Qt.AlignCenter)

                    self.setLayout(grid)
                    self.setGeometry(400, 200, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
            
    win = MyWindow(data_list, header)
    win.exec_()   