import datetime
from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout,\
                             QPushButton, QMessageBox, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update, and_
   
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def foutWerknr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Werkorder niet aanwezig, \nmaak eerst een werkorder aan,\nalvorens de begroting te koppelen!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()
    
def gekoppeld():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Werknummer is reeds gekoppeld!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()
        
def verwFout(mwerknr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Koppeling heeft al plaatsgevonden\nde begrote gegevens zijn eerder\nnaar werk '+str(mwerknr)+' overgezet!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()
    
def foutCalc():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Calculatie niet aanwezig!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()
        
def geenOpdracht():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Nog geen opdracht aanwezig!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()

def gegevensOk():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Transfer is gelukt!')
    msg.setWindowTitle('Koppel begroting')
    msg.exec_()
   
def zoekBegroting(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Calculatie koppelen")
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
            
            self.Werkorder = QLabel()
            zkwerknrEdit = QLineEdit()
            zkwerknrEdit.setFixedWidth(100)
            zkwerknrEdit.setFont(QFont("Arial",10))
            zkwerknrEdit.textChanged.connect(self.zkwerknrChanged)
            reg_ex = QRegExp('^[7]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, zkwerknrEdit)
            zkwerknrEdit.setValidator(input_validator)  
           
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0)
            
            lbl1 = QLabel('Calculatienummer')  
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zkcalcEdit, 3, 1)
            
            lbl2 = QLabel('Werkorder')
            lbl2.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl2, 4, 0)
            grid.addWidget(zkwerknrEdit, 4, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 2, Qt.AlignCenter)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo ,  1, 0, 1, 2, Qt.AlignRight)
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 6, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 6, 0, 1, 1,Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
        def zkcalcChanged(self, text):
            self.Calculatie.setText(text)
            
        def zkwerknrChanged(self, text):
            self.Werkorder.setText(text)
             
        def returnCalculatie(self):
            return self.Calculatie.text()
        
        def returnWerkorder(self):
            return self.Werkorder.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnCalculatie(), dialog.returnWerkorder()]       

    window = Widget()
    data = window.getData()
    if not data[0] or not data[1]:
        zoekBegroting(m_email)
    mcalnr = int(data[0])
    mwerknr = int(data[1])
    metadata = MetaData()
    icalculaties = Table('icalculaties', metadata,
        Column('icalculatie', Integer),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer, primary_key=True),
        Column('besteldatum', String),
        Column('icalculatienummer', Integer))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selcl = select([icalculaties]).where(icalculaties.c.icalculatie == mcalnr)
    rpcl = con.execute(selcl).first()
    selwrk = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
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
    msgBox.setWindowTitle("Begroting Koppelen")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText('Omschrijving: '+mwerkomschr+'\nDeze calculatie alleen koppelen\nindien gegevens definitief zijn\nDoorgaan?')
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        metadata = MetaData()
        icalculaties = Table('icalculaties', metadata,
            Column('icalcID', Integer(), primary_key=True),
            Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
            Column('koppelnummer', Integer),
            Column('werkomschrijving', String),
            Column('verwerkt', Integer),
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
            Column('montage', Float))
        orders_intern = Table('orders_intern', metadata,
            Column('werkorderID', Integer(), primary_key=True),
            Column('werkomschrijving', String),
            Column('icalculatienummer', Integer),
            Column('begroot_totaal', Float),
            Column('begr_materialen', Float),
            Column('begr_lonen', Float),
            Column('hoeveelheid', Float),
            Column('szagen', Float),
            Column('bzagen', Float),
            Column('sschaven', Float),
            Column('bschaven', Float),
            Column('ssteken', Float),
            Column('bsteken', Float),
            Column('sboren', Float), 
            Column('bboren', Float),
            Column('sfrezen', Float),
            Column('bfrezen', Float),
            Column('sdraaien_klein', Float),
            Column('bdraaien_klein', Float),
            Column('sdraaien_groot', Float),
            Column('bdraaien_groot', Float),
            Column('stappen', Float),
            Column('btappen', Float),
            Column('snube_draaien', Float),
            Column('bnube_draaien', Float),
            Column('snube_bewerken', Float),
            Column('bnube_bewerken', Float),
            Column('sknippen', Float),
            Column('bknippen', Float),
            Column('skanten', Float),
            Column('bkanten', Float),
            Column('sstansen', Float),
            Column('bstansen', Float),
            Column('slassen_co2', Float),
            Column('blassen_co2', Float),
            Column('slassen_hand', Float),
            Column('blassen_hand', Float),
            Column('sverpakken', Float),
            Column('bverpakken', Float),
            Column('sverzinken', Float),
            Column('bverzinken', Float),
            Column('smoffelen', Float),
            Column('bmoffelen', Float),
            Column('sschilderen', Float),
            Column('bschilderen', Float),
            Column('sspuiten', Float),
            Column('bspuiten', Float),
            Column('sponsen', Float),
            Column('bponsen', Float),
            Column('spersen', Float),
            Column('bpersen', Float),
            Column('sgritstralen', Float),
            Column('bgritstralen', Float),
            Column('smontage', Float),
            Column('bmontage', Float),
            Column('artikelID', Integer),
            Column('gereed', Float))
              
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selcal = select([icalculaties,orders_intern]).where(and_(icalculaties.c.icalculatie == mcalnr,\
                       icalculaties.c.verwerkt == 1, orders_intern.c.werkorderID == mwerknr))
        rpcal = con.execute(selcal)
        
        for regel in rpcal:
            updcal = update(icalculaties).where(icalculaties.c.icalculatie == mcalnr)\
             .values(koppelnummer = mwerknr, werkomschrijving = mwerkomschr, verwerkt = 2)
            con.execute(updcal)
            
            updwerk = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr)\
              .values(begroot_totaal = orders_intern.c.begroot_totaal+regel[9],\
              begr_materialen = orders_intern.c.begr_materialen+regel[10],\
              begr_lonen = orders_intern.c.begr_lonen+regel[11],\
              szagen = orders_intern.c.szagen+regel[12],\
              bzagen = orders_intern.c.bzagen+regel[13],\
              sschaven = orders_intern.c.sschaven+regel[14],\
              bschaven = orders_intern.c.bschaven+regel[15],\
              ssteken = orders_intern.c.ssteken+regel[16],\
              bsteken = orders_intern.c.bsteken+regel[17],\
              sboren = orders_intern.c.sboren+regel[18],\
              bboren = orders_intern.c.bboren+regel[19],\
              sfrezen = orders_intern.c.sfrezen+regel[20],\
              bfrezen = orders_intern.c.bfrezen+regel[21],\
              sdraaien_klein = orders_intern.c.sdraaien_klein+regel[22],\
              bdraaien_klein = orders_intern.c.bdraaien_klein+regel[23],\
              sdraaien_groot = orders_intern.c.sdraaien_groot+regel[24] ,\
              bdraaien_groot = orders_intern.c.bdraaien_groot+regel[25] ,\
              stappen = orders_intern.c.stappen+regel[26],\
              btappen = orders_intern.c.btappen+regel[27],\
              snube_draaien = orders_intern.c.snube_draaien+regel[28],\
              bnube_draaien = orders_intern.c.bnube_draaien+regel[29],\
              snube_bewerken = orders_intern.c.snube_bewerken+regel[30],\
              bnube_bewerken = orders_intern.c.bnube_bewerken+regel[31],\
              sknippen = orders_intern.c.sknippen+regel[32],\
              bknippen = orders_intern.c.bknippen+regel[33],\
              skanten = orders_intern.c.skanten+regel[34],\
              bkanten = orders_intern.c.bkanten+regel[35],\
              sstansen = orders_intern.c.sstansen+regel[36],\
              bstansen = orders_intern.c.bstansen+regel[37],\
              slassen_co2 = orders_intern.c.slassen_co2+regel[38],\
              blassen_co2 = orders_intern.c.blassen_co2+regel[39],\
              slassen_hand = orders_intern.c.slassen_hand+regel[40],\
              blassen_hand = orders_intern.c.blassen_hand+regel[41],\
              sverpakken =orders_intern.c.sverpakken+regel[42],\
              bverpakken =orders_intern.c.bverpakken+regel[43],\
              sverzinken=orders_intern.c.sverzinken+regel[44],\
              bverzinken=orders_intern.c.bverzinken+regel[45],\
              smoffelen=orders_intern.c.smoffelen+regel[46],\
              bmoffelen=orders_intern.c.bmoffelen+regel[47],\
              sschilderen=orders_intern.c.sschilderen+regel[48],\
              bschilderen=orders_intern.c.bschilderen+regel[49],\
              sspuiten=orders_intern.c.sspuiten+regel[50],\
              bspuiten=orders_intern.c.bspuiten+regel[51],\
              sponsen=orders_intern.c.sponsen+regel[52],\
              bponsen=orders_intern.c.bponsen+regel[53],\
              spersen=orders_intern.c.spersen+regel[54],\
              bpersen=orders_intern.c.bpersen+regel[55],\
              sgritstralen=orders_intern.c.sgritstralen+regel[56],\
              bgritstralen=orders_intern.c.bgritstralen+regel[57],\
              smontage=orders_intern.c.smontage+regel[58],
              bmontage=orders_intern.c.bmontage+regel[59],\
              icalculatienummer = mcalnr, hoeveelheid = regel[7])
        con.execute(updwerk)
    
        materiaallijsten = Table('materiaallijsten', metadata,
            Column('matlijstID', Integer, primary_key=True),
            Column('icalculatie', Integer),
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
            Column('artikelomschrijving', String),
            Column('art_eenheid', String),
            Column('reserveringsaldo', Float),
            Column('categorie', Integer),
            Column('bestelsaldo', Float),
            Column('artikelprijs', Float))
   
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selmat = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.\
            c.icalculatie == mcalnr, materiaallijsten.c.artikelID == artikelen.c.artikelID))
        rpmat = con.execute(selmat)
        mboekd = str(datetime.datetime.now())[0:10]
        for row in rpmat:
           updres = update(materiaallijsten).where(and_(materiaallijsten.c.icalculatie == mcalnr,\
             materiaallijsten.c.artikelID == artikelen.c.artikelID)).values(werknummerID = mwerknr,\
             reserverings_datum = mboekd, categorie = artikelen.c.categorie)
           con.execute(updres)
           updart = update(artikelen).where(and_(materiaallijsten.c.artikelID ==\
                artikelen.c.artikelID, materiaallijsten.c.icalculatie == mcalnr))\
                .values(reserveringsaldo = artikelen.c.reserveringsaldo + materiaallijsten.c.hoeveelheid)
           con.execute(updart)
        params = Table('params', metadata,
            Column('paramID', Integer, primary_key=True),
            Column('tarief', Float),
            Column('item', String))
    
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        selpar = select([params]).order_by(params.c.paramID)
        rppar = con.execute(selpar).fetchall()
        updprijs = update(artikelen).where(orders_intern.c.artikelID ==\
            artikelen.c.artikelID).values(artikelprijs = (orders_intern.c.begroot_totaal/\
                    orders_intern.c.hoeveelheid)*(1+rppar[5][1]))
        con.execute(updprijs)
        gegevensOk()
        zoekBegroting(m_email)    
    else:
        hoofdMenu(m_email)