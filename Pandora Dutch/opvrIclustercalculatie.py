from login import hoofdMenu
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout,\
          QPushButton, QMessageBox, QLineEdit, QWidget, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update, insert, and_, func

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def calcBestaatniet():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Calculatie is niet aanwezig!')
    msg.setWindowTitle('INVOEREN')
    msg.exec_()
    
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('AFDRUKKEN')
    msg.exec_()
     
def zoekCalculatie(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Calculeren / Opvragen / Printen")
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
            
            lbl1 = QLabel('Calculatienummer\nof werkorder.')  
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
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
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
    icalculaties = Table('icalculaties', metadata,
        Column('icalculatie', Integer),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer),
        Column('koppelnummer', Integer))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    if not data[0]:
       return(0)
    elif data[0][0]=='7'and len(data[0]) == 9:
        mcalnr = data[0]
        selcl = select([icalculaties]).where(icalculaties.c.koppelnummer == int(mcalnr))
        rpcl = con.execute(selcl).first()
    elif data[0] and len(data[0]) <9:
        mcalnr = data[0]
        selcl = select([icalculaties]).where(icalculaties.c.icalculatie == int(mcalnr))
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
            grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)
              
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Calculatie: '+str(mcalnr)+'\nWerknummer: '+str(mwerknr)), 1, 1, 1, 3)
            grid.addWidget(QLabel(mwerkomschr[0:35]), 2 , 1, 1, 3)
                                   
            self.setWindowTitle("Calculatie opvragen / printen") 
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                                      
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved\n   dj.jansen@casema.nl'), 6, 0, 2, 3, Qt.AlignCenter)
                             
            self.printBtn = QPushButton('Calculatie\nPrinten')
            self.printBtn.clicked.connect(lambda: printCalculatie(mcalnr, mwerknr))
            grid.addWidget(self.printBtn, 4, 2)
            self.printBtn.setFont(QFont("Arial",10))
            self.printBtn.setFixedWidth(100)
            self.printBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.artprintBtn = QPushButton('Artikellijst\nPrinten')
            self.artprintBtn.clicked.connect(lambda: printArtikellijst(mcalnr, mwerknr))
            grid.addWidget(self.artprintBtn, 4, 1, 1, 1, Qt.AlignRight)
            self.artprintBtn.setFont(QFont("Arial",10))
            self.artprintBtn.setFixedWidth(100)
            self.artprintBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.toonBtn = QPushButton('Calculatie\nOpvragen')
            self.toonBtn.clicked.connect(lambda: toonCalculatie(mcalnr, mwerknr))
            grid.addWidget(self.toonBtn, 5, 2)
            self.toonBtn.setFont(QFont("Arial",10))
            self.toonBtn.setFixedWidth(100)
            self.toonBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
            self.artlijstBtn = QPushButton('Artikellijst\nOpvragen')
            self.artlijstBtn.clicked.connect(lambda: toonArtikellijst(mcalnr, mwerknr))
            grid.addWidget(self.artlijstBtn,5, 1, 1, 1, Qt.AlignRight)
            self.artlijstBtn.setFont(QFont("Arial",10))
            self.artlijstBtn.setFixedWidth(100)
            self.artlijstBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
            self.terugBtn = QPushButton('T\ne\nr\nu\ng')
            self.terugBtn.clicked.connect(self.close)
            grid.addWidget(self.terugBtn, 4, 1, 5, 1, Qt.AlignTop)
            self.terugBtn.setFont(QFont("Arial", 10))
            self.terugBtn.setFixedWidth(40)
            self.terugBtn.setFixedHeight(115)
            self.terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                             
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
                
    mainWin = MainWindow()
    mainWin.exec_()
    zoekCalculatie(m_email)
   
def opbouwRp(mcalnr, mwerkomschr, mverw, mwerknr, m_email):
    metadata = MetaData()
    icalculaties = Table('icalculaties', metadata,
        Column('icalcID', Integer(), primary_key=True),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('hoeveelheid', Float),
        Column('icalculatie', Integer),
        Column('materialen', Float))
    icluster_artikelen = Table('icluster_artikelen', metadata,
        Column('icluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelprijs', Float))

    params_finance = Table('params_finance', metadata,
         Column('financeID', Integer, primary_key=True),
         Column('factor', Float),
         Column('item', String))

    params_hours = Table('params_hours', metadata,
         Column('rateID', Integer, primary_key=True),
         Column('hourly_tariff', Float),
         Column('item', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params_finance]).order_by(params_finance.c.financeID)
    rppar = con.execute(selpar).fetchall()
    selpar1 = select([params_hours]).order_by(params_hours.c.rateID)
    rppar1 = con.execute(selpar1).fetchall()
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selmat=select([icalculaties, icluster_artikelen, artikelen]).where(and_(\
            icalculaties.c.icalculatie == mcalnr,\
            icalculaties.c.iclusterID == icluster_artikelen.c.iclusterID,\
            icluster_artikelen.c.artikelID == artikelen.c.artikelID))
    rpmat = con.execute(selmat)
    for rij in rpmat:
        updcalmat = update(icalculaties).where(and_(icalculaties.c.icalculatie ==\
           mcalnr, icalculaties.c.iclusterID == rij[1],\
           icluster_artikelen.c.artikelID == rij[9])).values(\
           materialen = icalculaties.c.materialen+rij[2]*rij[8]*rij[10]*(1+rppar[6][1]))
        con.execute(updcalmat)
   
    metadata = MetaData()
    icalculaties = Table('icalculaties', metadata,
        Column('icalcID', Integer(), primary_key=True),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('koppelnummer', Integer),
        Column('icalculatie', Integer),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('szagen', Float),
        Column('zagen', Float),
        Column('sschaven', Float),
        Column('schaven', Float),
        Column('ssteken', Float),
        Column('steken', Float),
        Column('sboren', Float),
        Column('boren', Float),
        Column('sfrezen', Float),
        Column('frezen', Float),
        Column('sdraaien_klein', Float),
        Column('draaien_klein', Float),
        Column('sdraaien_groot', Float),
        Column('draaien_groot', Float),
        Column('stappen', Float),
        Column('tappen', Float),
        Column('snube_draaien', Float),
        Column('nube_draaien', Float),
        Column('snube_bewerken', Float),
        Column('nube_bewerken', Float),
        Column('sknippen', Float),
        Column('knippen', Float),
        Column('skanten', Float),
        Column('kanten', Float),
        Column('sstansen', Float),
        Column('stansen', Float),
        Column('slassen_co2', Float),
        Column('lassen_co2', Float),
        Column('slassen_hand', Float),
        Column('lassen_hand', Float),
        Column('sverpakken', Float),
        Column('verpakken', Float),
        Column('sverzinken', Float),
        Column('verzinken', Float),
        Column('smoffelen', Float),
        Column('moffelen', Float),
        Column('sschilderen', Float),
        Column('schilderen', Float),
        Column('sspuiten', Float),
        Column('spuiten', Float),
        Column('sponsen', Float),
        Column('ponsen', Float),
        Column('spersen', Float),
        Column('persen', Float),
        Column('sgritstralen', Float),
        Column('gritstralen', Float),
        Column('smontage', Float),
        Column('montage', Float),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
    iclusters = Table('iclusters', metadata,
        Column('iclusterID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('szagen', Float),
        Column('zagen', Float),
        Column('sschaven', Float),
        Column('schaven', Float),
        Column('ssteken', Float),
        Column('steken', Float),
        Column('sboren', Float),
        Column('boren', Float),
        Column('sfrezen', Float),
        Column('frezen', Float),
        Column('sdraaien_klein', Float),
        Column('draaien_klein', Float),
        Column('sdraaien_groot', Float),
        Column('draaien_groot', Float),
        Column('stappen', Float),
        Column('tappen', Float),
        Column('snube_draaien', Float),
        Column('nube_draaien', Float),
        Column('snube_bewerken', Float),
        Column('nube_bewerken', Float),
        Column('sknippen', Float),
        Column('knippen', Float),
        Column('skanten', Float),
        Column('kanten', Float),
        Column('sstansen', Float),
        Column('stansen', Float),
        Column('slassen_co2', Float),
        Column('lassen_co2', Float),
        Column('slassen_hand', Float),
        Column('lassen_hand', Float),
        Column('sverpakken', Float),
        Column('verpakken', Float),
        Column('sverzinken', Float),
        Column('verzinken', Float),
        Column('smoffelen', Float),
        Column('moffelen', Float),
        Column('sschilderen', Float),
        Column('schilderen', Float),
        Column('sspuiten', Float),
        Column('spuiten', Float),
        Column('sponsen', Float),
        Column('ponsen', Float),
        Column('spersen', Float),
        Column('persen', Float),
        Column('sgritstralen', Float),
        Column('gritstralen', Float),
        Column('smontage', Float),
        Column('montage', Float))
    icluster_artikelen = Table('icluster_artikelen', metadata,
        Column('icluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_eenheid', String))
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('icalculatie', Integer),
        Column('hoeveelheid', Float),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('artikelprijs', Float),
        Column('subtotaal', Float),
        Column('resterend', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcalc = select([icalculaties, iclusters]).where(and_(icalculaties.c\
       .icalculatie == int(mcalnr), icalculaties.c.iclusterID == iclusters.c.iclusterID))
    rpcalc = con.execute(selcalc)
    selclart = select([icluster_artikelen,artikelen]).where(and_(icluster_artikelen.c.\
      artikelID == artikelen.c.artikelID, icalculaties.c.iclusterID ==\
      icluster_artikelen.c.iclusterID, icalculaties.c.icalculatie == (int(mcalnr))))\
      .order_by(icluster_artikelen.c.iclusterID, icluster_artikelen.c.artikelID)
    rpclart = con.execute(selclart)
    for record in rpcalc:
        updcalc = update(icalculaties).where(and_(icalculaties.c.icalculatie == record[3],\
           icalculaties.c.iclusterID == iclusters.c.iclusterID)).values(verwerkt = 1,\
           zagen = (icalculaties.c.zagen+iclusters.c.zagen)*icalculaties.c.hoeveelheid,\
           szagen = icalculaties.c.szagen+iclusters.c.szagen,\
           schaven = (icalculaties.c.schaven+iclusters.c.schaven)*icalculaties.c.hoeveelheid,\
           sschaven = icalculaties.c.sschaven+iclusters.c.schaven,\
           steken = (icalculaties.c.steken+iclusters.c.steken)*icalculaties.c.hoeveelheid,\
           ssteken = icalculaties.c.ssteken+iclusters.c.steken,\
           boren = (icalculaties.c.boren+iclusters.c.boren)*icalculaties.c.hoeveelheid,\
           sboren = icalculaties.c.sboren+iclusters.c.sboren,\
           frezen = (icalculaties.c.frezen+iclusters.c.frezen)*icalculaties.c.hoeveelheid,\
           sfrezen = icalculaties.c.sfrezen+iclusters.c.sfrezen,\
           draaien_klein = (icalculaties.c.draaien_klein+iclusters.c.draaien_klein)*icalculaties.c.hoeveelheid,\
           sdraaien_klein = icalculaties.c.sdraaien_klein+iclusters.c.sdraaien_klein,\
           draaien_groot = (icalculaties.c.draaien_groot+iclusters.c.draaien_groot)*icalculaties.c.hoeveelheid,\
           sdraaien_groot = icalculaties.c.sdraaien_groot+iclusters.c.sdraaien_groot,\
           tappen = (icalculaties.c.tappen+iclusters.c.tappen)*icalculaties.c.hoeveelheid,\
           stappen = icalculaties.c.stappen+iclusters.c.stappen,\
           nube_draaien = (icalculaties.c.nube_draaien+iclusters.c.nube_draaien)*icalculaties.c.hoeveelheid,\
           snube_draaien = icalculaties.c.snube_draaien+iclusters.c.snube_draaien,\
           nube_bewerken = (icalculaties.c.nube_bewerken+iclusters.c.nube_bewerken)*icalculaties.c.hoeveelheid,\
           snube_bewerken = icalculaties.c.snube_bewerken+iclusters.c.snube_bewerken,\
           knippen = (icalculaties.c.knippen+iclusters.c.knippen)*icalculaties.c.hoeveelheid,\
           sknippen = icalculaties.c.sknippen+iclusters.c.sknippen,\
           kanten = (icalculaties.c.kanten+iclusters.c.kanten)*icalculaties.c.hoeveelheid,\
           skanten = icalculaties.c.skanten+iclusters.c.skanten,\
           stansen = (icalculaties.c.stansen+iclusters.c.stansen)*icalculaties.c.hoeveelheid,\
           sstansen = icalculaties.c.sstansen+iclusters.c.sstansen,\
           lassen_co2 = (icalculaties.c.lassen_co2+iclusters.c.lassen_co2)*icalculaties.c.hoeveelheid,\
           slassen_co2 = icalculaties.c.slassen_co2+iclusters.c.slassen_co2,\
           lassen_hand = (icalculaties.c.lassen_hand+iclusters.c.lassen_hand)*icalculaties.c.hoeveelheid,\
           slassen_hand = icalculaties.c.slassen_hand+iclusters.c.slassen_hand,\
           verpakken = (icalculaties.c.verpakken+iclusters.c.verpakken)*icalculaties.c.hoeveelheid,\
           sverpakken = icalculaties.c.sverpakken+iclusters.c.sverpakken,\
           verzinken = (icalculaties.c.verzinken+iclusters.c.verzinken)*icalculaties.c.hoeveelheid,\
           sverzinken = icalculaties.c.sverzinken+iclusters.c.sverzinken,\
           moffelen = (icalculaties.c.moffelen+iclusters.c.moffelen)*icalculaties.c.hoeveelheid,\
           smoffelen = icalculaties.c.smoffelen+iclusters.c.smoffelen,\
           schilderen = (icalculaties.c.schilderen+iclusters.c.schilderen)*icalculaties.c.hoeveelheid,\
           sschilderen = icalculaties.c.sschilderen+iclusters.c.sschilderen,\
           spuiten = (icalculaties.c.spuiten+iclusters.c.spuiten)*icalculaties.c.hoeveelheid,\
           sspuiten = icalculaties.c.sspuiten+iclusters.c.sspuiten,\
           ponsen = (icalculaties.c.ponsen+iclusters.c.ponsen)*icalculaties.c.hoeveelheid,\
           sponsen = icalculaties.c.sponsen+iclusters.c.sponsen,\
           persen = (icalculaties.c.persen+iclusters.c.persen)*icalculaties.c.hoeveelheid,\
           spersen = icalculaties.c.spersen+iclusters.c.spersen,\
           gritstralen = (icalculaties.c.gritstralen+iclusters.c.gritstralen)*icalculaties.c.hoeveelheid,\
           sgritstralen = icalculaties.c.sgritstralen+iclusters.c.sgritstralen,\
           montage = (icalculaties.c.montage+iclusters.c.montage)*icalculaties.c.hoeveelheid,\
           smontage = icalculaties.c.smontage+iclusters.c.smontage,\
           lonen = (icalculaties.c.zagen+iclusters.c.zagen)*rppar1[11][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.szagen+iclusters.c.szagen)*rppar1[11][1]+\
           (icalculaties.c.schaven+iclusters.c.schaven)*rppar1[12][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sschaven+iclusters.c.sschaven)*rppar1[12][1]+\
           (icalculaties.c.steken+iclusters.c.steken)*rppar1[13][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.ssteken+iclusters.c.ssteken)*rppar1[13][1]+\
           (icalculaties.c.boren+iclusters.c.boren)*rppar1[14][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sboren+iclusters.c.sboren)*rppar1[14][1]+\
           (icalculaties.c.frezen+iclusters.c.frezen)*rppar1[15][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sfrezen+iclusters.c.sfrezen)*rppar1[15][1]+\
           (icalculaties.c.draaien_klein+iclusters.c.draaien_klein)*rppar1[16][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sdraaien_klein+iclusters.c.sdraaien_klein)*rppar1[16][1]+\
           (icalculaties.c.draaien_groot+iclusters.c.draaien_groot)*rppar1[17][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sdraaien_groot+iclusters.c.sdraaien_groot)*rppar1[17][1]+\
           (icalculaties.c.tappen+iclusters.c.tappen)*rppar1[18][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.stappen+iclusters.c.stappen)*rppar1[18][1]+\
           (icalculaties.c.nube_draaien+iclusters.c.nube_draaien)*rppar1[19][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.snube_draaien+iclusters.c.snube_draaien)*rppar1[19][1]+\
           (icalculaties.c.nube_bewerken+iclusters.c.nube_bewerken)*rppar1[20][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.snube_bewerken+iclusters.c.snube_bewerken)*rppar1[20][1]+\
           (icalculaties.c.knippen+iclusters.c.knippen)*rppar1[21][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sknippen+iclusters.c.sknippen)*rppar1[21][1]+\
           (icalculaties.c.kanten+iclusters.c.kanten)*rppar1[22][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.skanten+iclusters.c.skanten)*rppar1[22][1]+\
           (icalculaties.c.stansen+iclusters.c.stansen)*rppar1[23][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sstansen+iclusters.c.sstansen)*rppar1[23][1]+\
           (icalculaties.c.lassen_co2+iclusters.c.lassen_co2)*rppar1[24][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.slassen_co2+iclusters.c.slassen_co2)*rppar1[24][1]+\
           (icalculaties.c.lassen_hand+iclusters.c.lassen_hand)*rppar1[25][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.slassen_hand+iclusters.c.slassen_hand)*rppar1[25][1]+\
           (icalculaties.c.verpakken+iclusters.c.verpakken)*rppar1[26][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sverpakken+iclusters.c.sverpakken)*rppar1[26][1]+\
           (icalculaties.c.verzinken+iclusters.c.verzinken)*rppar1[27][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sverzinken+iclusters.c.sverzinken)*rppar1[27][1]+\
           (icalculaties.c.moffelen+iclusters.c.moffelen)*rppar1[28][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.smoffelen+iclusters.c.smoffelen)*rppar1[28][1]+\
           (icalculaties.c.schilderen+iclusters.c.schilderen)*rppar1[29][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sschilderen+iclusters.c.sschilderen)*rppar1[29][1]+\
           (icalculaties.c.spuiten+iclusters.c.spuiten)*rppar1[30][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sspuiten+iclusters.c.sspuiten)*rppar1[30][1]+\
           (icalculaties.c.ponsen+iclusters.c.ponsen)*rppar1[31][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sponsen+iclusters.c.sponsen)*rppar1[31][1]+\
           (icalculaties.c.persen+iclusters.c.persen)*rppar1[32][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.spersen+iclusters.c.spersen)*rppar1[32][1]+\
           (icalculaties.c.gritstralen+iclusters.c.gritstralen)*rppar1[33][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.sgritstralen+iclusters.c.sgritstralen)*rppar1[33][1]+\
           (icalculaties.c.montage+iclusters.c.montage)*rppar1[34][1]*icalculaties.c.hoeveelheid+\
           (icalculaties.c.smontage+iclusters.c.smontage)*rppar1[34][1])

        con.execute(updcalc)
        for row in rpclart:
            selart = select([materiaallijsten.c.artikelID, materiaallijsten.c.icalculatie]).where(and_(materiaallijsten.\
                c.artikelID == row[1], materiaallijsten.c.icalculatie == record[3]))
            rpart = con.execute(selart).first()
            if rpart:
                updmatlijst = update(materiaallijsten).where(and_(materiaallijsten.c.\
                  artikelID == row[1], materiaallijsten.c.icalculatie == record[3]))\
                 .values(hoeveelheid = materiaallijsten.c.hoeveelheid+(record[5]*row[3]),\
                artikelprijs = row[6]*(1+rppar[6][1]), subtotaal = materiaallijsten.\
                c.subtotaal+record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(updmatlijst)
            elif not rpart:
                mmatlijstnr = (con.execute(select([func.max(materiaallijsten.c.matlijstID,\
                        type_=Integer).label('mmatlijstnr')])).scalar())
                mmatlijstnr += 1
                insmatlijst = insert(materiaallijsten).values(matlijstID = mmatlijstnr,\
                    icalculatie = record[3], artikelID = row[1],\
                    hoeveelheid = record[5]*row[3], resterend = record[5]*row[3],\
                    artikelprijs = row[6]*(1+rppar[6][1]),\
                    subtotaal = record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(insmatlijst)
        selber = select([icalculaties.c.icalcID, icalculaties.c.icalculatie])\
                           .where(icalculaties.c.icalculatie == mcalnr)
        rpselber = con.execute(selber)
        for regel in rpselber:
            updber = update(icalculaties).where(icalculaties.c.icalculatie==mcalnr)\
             .values(prijs=icalculaties.c.materialen+icalculaties.c.lonen,\
              werkomschrijving = mwerkomschr)
            con.execute(updber)
    opvragenCalc(mcalnr, mwerkomschr, mverw, mwerknr, m_email)
                        
def printCalculatie(mcalnr, mwerknr):
    from sys import platform
    metadata = MetaData()
    icalculaties = Table('icalculaties', metadata,
        Column('icalcID', Integer(), primary_key=True),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('koppelnummer', Integer),
        Column('icalculatie', Integer),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('werkomschrijving', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([icalculaties]).where(icalculaties.c.icalculatie == mcalnr)
    rpcal = con.execute(selcal)
    
    mblad = 1
    rgl = 0
    mmat = 0
    mlon = 0
    mtotaal = 0
    for row in rpcal:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename = '.\\forms\\Intern_Clustercalculaties\\clustercalculatie-'+str(row[3])+'-'+str(mwerknr)+'.txt'
            else:
                filename = './forms/Intern_Clustercalculaties/clustercalculatie-'+str(row[3])+'-'+str(mwerknr)+'.txt' 
            kop=\
    ('Werkorder: '+ str(mwerknr)+' '+'{:<24.24s}'.format(str(row[10]))+'  Calculatie: '+str(row[3])+'  Datum: '+str(datetime.datetime.now())[0:10]+'  Blad : '+str(mblad)+'\n'+
    '================================================================================================\n'+
    'Cluster  Omschrijving       Eenheid Aantal  Materialen       Lonen                       Bedrag\n'+
    '================================================================================================\n')
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<9s}'.format(row[1])+'{:<23.21}'.format(row[4])+'{:<5s}'.format(row[6])+'{:5.2f}'.format(row[5])+'{:12.2f}'.format(row[8])+'{:12.2f}'.format(row[9])+'                 '+'{:12.2f}'.format(row[7])+'\n')
        mmat = mmat+row[8]
        mlon = mlon+row[9]
        mtotaal = mtotaal+row[7]
        rgl += 1
    tail =(\
    '-------------------------------------------------------------------------------------------------\n'+
    'Totalen                                   '+'{:12.2f}'.format(mmat)+'{:12.2f}'.format(mlon)+'                 '+'{:12.2f}'.format(mtotaal)+'\n'
    '=================================================================================================\n')    
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
         Column('icalculatie', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('subtotaal', Float))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('art_eenheid', String),
         Column('locatie_magazijn', String))
    icalculaties = Table('icalculaties', metadata,
        Column('icalculatie', Integer),
        Column('koppelnummer', Integer))
                                    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selmat = select([materiaallijsten, artikelen])\
      .where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.icalculatie == mcalnr)).order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)
    selkop = select([icalculaties]).where(icalculaties.c.icalculatie == mcalnr)
    rpkop = con.execute(selkop).first()
    mblad = 1
    rgl = 0
    for row in rpmat:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename =  filename = '.\\forms\\Intern_Clustercalculaties\\materiaallijst-'+str(rpkop[0])+'-'+str(mwerknr)+'.txt'
            else:
                filename =  filename = './forms/Intern_Clustercalculaties/materiaallijst-'+str(rpkop[0])+'-'+str(mwerknr)+'.txt'
            kop=\
    ('Werkorder:   '+ str(mwerknr)+'  Calculatie: '+str(rpkop[0])+'   Datum: '+str(datetime.datetime.now())[0:10]+'  Blad :  '+str(mblad)+'\n'+
    '=============================================================================================\n'+
    'Artikelnr  Omschrijving                        Eenheid       Prijs      Aantal               \n'+
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
        
def toonCalculatie(mcalnr, mwerknr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1800, 900)
            self.setWindowTitle('Clustercalculatie')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
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
             
    header = ['ID','Calculatie','Clusternr', 'Omschrijving','Werkomschrijving','Verwerkt',
      'Hoeveelheid','Eenheid','Koppelnummer','Totaalprijs','Materialen', 'Lonen',\
      'Materieel','Diensten','Inhuur','St.zagen','Zagen','St.schaven','Schaven',\
      'St.steken','Steken','St.boren','Boren','St.frezen','Frezen','St.draaien klein',\
      'Draaien klein','St.draaien_groot','Draaien groot','St.tappen','Tappen',\
      'St.nube draaien','Nube draaien','St.nube bewerken','Nube bewerken',\
      'St.knippen','Knippen','St.kanten','Kanten','St.stansen','Stansen',\
      'St.lassen co2','Lassen co2','St.lassen hand','Lassen hand','St.verpakken',\
      'Verpakken','St.verzinken','Verzinken','St.moffelen','Moffelen','St.schilderen',\
      'Schilderen','St.spuiten','Spuiten','St.ponsen','Ponsen','St.persen',\
      'Persen','St.gritstralen','Gritstralen','St.montage','Montage']

    metadata = MetaData()               
    icalculaties = Table('icalculaties', metadata,
        Column('icalcID', Integer(), primary_key=True),
        Column('icalculatie', Integer),
        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
        Column('omschrijving', String),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('materieel', Float),
        Column('diensten', Float),
        Column('inhuur', Float),
        Column('szagen', Float),
        Column('zagen', Float),
        Column('sschaven', Float),
        Column('schaven', Float),
        Column('ssteken', Float),
        Column('steken', Float),
        Column('sboren', Float),
        Column('boren', Float),
        Column('sfrezen', Float),
        Column('frezen', Float),
        Column('sdraaien_klein', Float),
        Column('draaien_klein', Float),
        Column('sdraaien_groot', Float),
        Column('draaien_groot', Float),
        Column('stappen', Float),
        Column('tappen', Float),
        Column('snube_draaien', Float),
        Column('nube_draaien', Float),
        Column('snube_bewerken', Float),
        Column('nube_bewerken', Float),
        Column('sknippen', Float),
        Column('knippen', Float),
        Column('skanten', Float),
        Column('kanten', Float),
        Column('sstansen', Float),
        Column('stansen', Float),
        Column('slassen_co2', Float),
        Column('lassen_co2', Float),
        Column('slassen_hand', Float),
        Column('lassen_hand', Float),
        Column('sverpakken', Float),
        Column('verpakken', Float),
        Column('sverzinken', Float),
        Column('verzinken', Float),
        Column('smoffelen', Float),
        Column('moffelen', Float),
        Column('sschilderen', Float),
        Column('schilderen', Float),
        Column('sspuiten', Float),
        Column('spuiten', Float),
        Column('sponsen', Float),
        Column('ponsen', Float),
        Column('spersen', Float),
        Column('persen', Float),
        Column('sgritstralen', Float),
        Column('gritstralen', Float),
        Column('smontage', Float),
        Column('montage', Float))
                                                 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([icalculaties]).where(icalculaties.c.icalculatie == mcalnr).\
     order_by(icalculaties.c.iclusterID)
    rpcal = con.execute(selcal)
          
    data_list=[]
    for row in rpcal:
        data_list += [(row)]
        
    def ShowSelection(idx):
        mcalnr = idx.data()
        if  idx.column() == 0:
                     
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcal = select([icalculaties]).where(icalculaties.c.icalcID == mcalnr)
            rpcal = con.execute(selcal).first()
            
            header = ['ID','Calculatie','Clusternr', 'Omschrijving','Werkomschrijving',\
              'Verwerkt','Hoeveelheid','Eenheid', 'Koppelnr', 'Totaalprijs','Materialen',\
              'Lonen','Materieel', 'Diensten', 'Inhuur','St.zagen','Zagen','St.schaven',\
              'Schaven','St.steken','Steken','St.boren','Boren','St.frezen','Frezen',\
              'St.draaien klein','Draaien klein','St.draaien_groot','Draaien groot',\
              'St.tappen','Tappen','St.nube draaien','Nube draaien','St.nube bewerken',\
              'Nube bewerken','St.knippen','Knippen','St.kanten','Kanten','St.stansen',\
              'Stansen','St.lassen co2','Lassen co2','St.lassen hand','Lassen hand',\
              'St.verpakken','Verpakken','St.verzinken','Verzinken','St.moffelen',\
              'Moffelen','St.schilderen','Schilderen','St.spuiten','Spuiten','St.ponsen',\
              'Ponsen','St.persen','Persen','St.gritstralen','Gritstralen','St.montage','Montage']
                              
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Opvragen Clustercalculatie")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Opvragen Clustercalculatie'),0, 0, 1, 9, Qt.AlignCenter)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 9, 1, 1, Qt.AlignRight)                
                    index = 0
                    for item in header:
                        horpos = index%5
                        if index%5 == 0:
                            verpos = index 
                        elif index%5 == 1:
                            verpos = index-1
                        elif index%5 == 2:
                            verpos = index-2
                        elif index%5 == 3:
                            verpos = index -3
                        elif index%5 == 4:
                            verpos = index-4
                        self.lbl = QLabel(header[index])
                        
                        self.Gegevens = QLabel()
                        if type(rpcal[index]) == float :
                            q1Edit = QLineEdit('{:12.2f}'.format(rpcal[index]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        elif  type(rpcal[index]) == int:
                            q1Edit = QLineEdit(str(rpcal[index]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        else:
                            q1Edit = QLineEdit(str(rpcal[index]))
                        q1Edit.setFixedWidth(150)
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        grid.addWidget(self.lbl, verpos+2, horpos+horpos%5)
                        grid.addWidget(q1Edit, verpos+2, horpos+horpos%5+1)
                        q1Edit.setDisabled(True)
    
                        index +=1
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, verpos+3, 9, 1 , 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100) 
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), verpos+4, 0, 1, 9, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(100, 100, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
             
    win = MyWindow(data_list, header)
    win.exec_()
            
def toonArtikellijst(mcalnr, mwerknr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1700, 900)
            self.setWindowTitle('Materiaallijst')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                    Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnHidden(4, True)
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
             
    header = ['Artikelnr','Omschrijving','Reserveringsaldo','LijstID','Calculatie',\
              'Werknummer','Orderinkoopnummer', 'Artikelnr','ArtikelPrijs',\
              'Hoeveelheid','Afroep','Resterend','Subtotaal','Reserveringdatum',\
              'Levering eind','Levering begin','Categorie']
                   
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('icalculatie', Integer),
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
    
    selmat = select([artikelen, materiaallijsten]).where(and_(materiaallijsten.c.artikelID\
       == artikelen.c.artikelID, materiaallijsten.c.artikelID == artikelen.c.artikelID,\
       materiaallijsten.c.icalculatie == mcalnr))\
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
                
            selmat = select([artikelen, materiaallijsten]).where(and_(\
                 materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                 materiaallijsten.c.artikelID == int(martnr),\
                 materiaallijsten.c.icalculatie == mcalnr))\
                 .order_by(materiaallijsten.c.artikelID)
            rpmat = con.execute(selmat).first()
             
            header = ['Artikelnr','Omschrijving','Reserveringsaldo','LijstID',\
               'Calculatie','Werknummer','Orderinkoopnummer', 'Artikelnr',\
               'ArtikelPrijs','Hoeveelheid','Afroep','Resterend','Subtotaal',\
               'Reserveringdatum','Levering eind','Levering begin', 'Categorie']
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Opvragen Artikelen Clustercalculatie")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Opvragen Artikelen Calculatie'),0, 1, 1, 2)
            
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
                            q1Edit .setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setFixedWidth(100)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, 1, 0)
                            grid.addWidget(q1Edit, index, 1, 1, 2)
                        elif index == 2:
                            q1Edit = QLineEdit(str(rpmat[index-1]))
                            q1Edit.setFixedWidth(400)
                            q1Edit.setDisabled(True)
                            q1Edit .setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
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
                            q1Edit.setDisabled(True)
                            q1Edit .setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
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
                            q1Edit .setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, index+1, 2)
                            grid.addWidget(q1Edit, index+1, 3)
                        index += 1
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, index+1, 3, 1, 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100)  
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+2, 0, 1, 4, Qt.AlignCenter)                           
                    
                    self.setLayout(grid)
                    self.setGeometry(400, 200, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
      
    win = MyWindow(data_list, header)
    win.exec_()   