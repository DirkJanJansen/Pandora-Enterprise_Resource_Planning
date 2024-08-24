import datetime
from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
     QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit
    
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, insert, func, update, delete, and_

def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information ERP System Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Information ERP Pandora')
            grid.addWidget(lblinfo, 0, 0, 1, 2, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 20pt Comic Sans MS")
            
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

        Information about creating cluster calculation en linking towards worknumber.
        
        The order of creating and linking a calculation is:
         
        Menu Calculation external works
        6. Create or change calculation.
           Accept the first free number entered by the system.\t
           Changes are only possible if the calculation is not yet linked to a
           work number. In this case, choose an existing calculation number.
        7. Calculation/Item list - request/calculate/printing
           With this choice the calculation data and/or the article data is 
           calculated or printed. The calculation takes place after starting the module.
                   
        Menu external works
        1. Enter working numbers 
           If work number does not yet exist, first enter work number, otherwise link.
           
        Menu Calculation external works 
        8. Calculation linking production.
           The link of the calculation with the working number is made and the
           articles data and work rates are transferred to the work number. 

        
        7. Then print out the calculation and the article list list for production.
            Printing of the order list for purchasing of "Services and Equipment" 
            is only possible when the order for the worknumber is obtained. 
            Activate the box "order" of the concerning worknumber.
  
     ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()

def gerCalnr(mcalnr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculation number '+str(mcalnr)+'  is created!')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_() 

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_()

def calcBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculation line already exists\nand is settled with\nspecified quantity!')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_() 
    
def calcGekoppeld():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Calculation is already linked to work\nchange is no longer possible!')
    msg.setWindowTitle('Insert cluster calculation')
    msg.exec_() 
    
def schoonCalculatie(mcalnr, m_email):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Calculation adjust")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText("This calculation exists already\ndo you want to adjust this calculation?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
       metadata = MetaData()
       calculaties = Table('calculaties', metadata,
           Column('calcID', Integer(), primary_key=True),
           Column('calculatie', Integer),
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
           Column('verwerkt', Integer))
       materiaallijsten = Table('materiaallijsten', metadata,
           Column('matlijstID', Integer, primary_key=True),
           Column('calculatie', Integer))
        
       engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
       con = engine.connect()
       updcal = update(calculaties).where(calculaties.c.calculatie == mcalnr).values\
         (prijs=0, materialen=0, lonen=0,diensten=0,materieel=0,inhuur=0,uren_constr=0,\
         uren_mont=0,uren_retourlas=0,uren_telecom=0,uren_bfi=0,uren_voeding=0,\
         uren_bvl=0,uren_spoorleg=0,uren_spoorlas=0,uren_inhuur=0,sleuvengraver=0,\
         persapparaat=0,atlaskraan=0,kraan_groot=0,mainliner=0,hormachine=0,\
         wagon=0,locomotor=0,locomotief=0,montagewagen=0,stormobiel=0,robeltrein=0,\
         verwerkt=0, werkomschrijving = '')
       con.execute(updcal)
       delmat = delete(materiaallijsten).where(materiaallijsten.c.calculatie==mcalnr)
       con.execute(delmat)
    else:
        zoeken(m_email)
    
def zoeken(m_email):
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
       Column('calcID', Integer(), primary_key=True),
       Column('calculatie', Integer),
       Column('verwerkt', Integer),
       Column('werkomschrijving', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
        mcalnr = con.execute(select([func.max(calculaties.c.calculatie,\
            type_=Integer)])).scalar()
    except:
        mcalnr = 0

    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Create / change calculation of external work")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            self.Calculatie = QLabel()
            kEdit = QLineEdit(str(mcalnr+1))
            kEdit.setFixedWidth(100)
            kEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp('^[1-9]{1}[0-9]{0,9}$')
            input_validator = QRegExpValidator(reg_ex, kEdit)
            kEdit.setValidator(input_validator)
            kEdit.textChanged.connect(self.kChanged)

            self.Werkomschrijving = QLabel()
            k1Edit = QLineEdit()
            k1Edit.setFixedWidth(300)
            k1Edit.setFont(QFont("Arial", 10))
            k1Edit.textChanged.connect(self.k1Changed)
                   
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(400)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                 Cluster Groups Sort Key')
            k0Edit.addItem('0. All clusters')
            k0Edit.addItem('AA-AL. Rails + welding assets')
            k0Edit.addItem('BA-BK. Beams + mounting')
            k0Edit.addItem('CA-CK. Level crossing + level crossing protection')
            k0Edit.addItem('DA-DK. Crushed stone + earth moving')
            k0Edit.addItem('EA-EK. Switch + track constructions')
            k0Edit.addItem('FA-FK. Underground infrastructure')
            k0Edit.addItem('GA-GK. Train control + signals')
            k0Edit.addItem('HA-HK. OCL + support structure')
            k0Edit.addItem('JA-JK. Power supplies + substations')
            k0Edit.activated[str].connect(self.k0Changed)
           
            grid = QGridLayout()
            grid.setSpacing(20)
                           
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)

            lbl2 = QLabel('Calculation')
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            lbl3 = QLabel('Workdescr.')
            grid.addWidget(lbl2, 1, 0)
            grid.addWidget(kEdit, 1, 1,)
            grid.addWidget(lbl3, 2, 0)
            grid.addWidget(k1Edit, 2, 1)

            grid.addWidget(k0Edit, 3, 0, 1, 2, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
              
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
   
            grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 4, 0, 1, 2,Qt.AlignCenter)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
    
            grid.addWidget(infoBtn, 4, 0)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
         
        def kChanged(self, text):
            self.Calculatie.setText(text)   
            
        def k0Changed(self, text):
            self.Keuze.setText(text)

        def k1Changed(self, text):
            self.Werkomschrijving.setText(text)
                  
        def returnk(self):
            return self.Calculatie.text()
        
        def returnk0(self):
            return self.Keuze.text()

        def returnk1(self):
            return self.Werkomschrijving.text()
  
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnk(), dialog.returnk1()]

    window = Widget()
    data = window.getData()
    keuze = ''
    if not data[0] or data[0][0] == ' ':
       ongInvoer()
       zoeken(m_email)
    elif data[0]:
        keuze = data[0][0]
    if data[1] == '' or int(data[1]) > mcalnr:
       mcalnr += 1
       gerCalnr(mcalnr)
    elif data[1]:
         mcalnr = int(data[1])
    if data[2]:
        mwerkomschr = data[2]
    scontr = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpcontr = con.execute(scontr).first()

    if rpcontr and rpcontr[2] == 2:
        calcGekoppeld()
        zoeken(m_email)
    elif rpcontr and rpcontr[2] == 1:
       schoonCalculatie(mcalnr, m_email)
    toonClusters(m_email, keuze , mcalnr, mwerkomschr)
    
def toonClusters(m_email, keuze, mcalnr, mwerkomschr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 900, 900)
            self.setWindowTitle('Cluster calculation external work')
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
            table_view.clicked.connect(showSelection)
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
             
    header = ['Cluster number', 'Description', 'Price', 'Unit', 'Materials', 'Wages',\
              'Services', 'Equipment', 'Hiring']
    
    metadata = MetaData()
    clusters = Table('clusters', metadata,
        Column('clusterID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    if keuze == '0':
        sel = select([clusters]).order_by(clusters.c.clusterID)
    elif keuze:
        sel = select([clusters]).where(clusters.c.clusterID.ilike(keuze+'%'))\
                              .order_by(clusters.c.clusterID)
  
    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
     
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        clusternr = str(idx.data())
        if idx.column() == 0:
            metadata = MetaData()
            clusters = Table('clusters', metadata,
                Column('clusterID', Integer(), primary_key=True),
                Column('omschrijving', String))
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcl = select([clusters]).where(clusters.c.clusterID == clusternr.upper())
            rpcl = con.execute(selcl).first()
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
                    grid.addWidget(QLabel('Calculation number:          '+str(mcalnr)), 1, 1, 1, 3)
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Cluster number               '+str(clusternr)+\
                           '\n'+rpcl[1]), 2, 1, 1, 3)
                               
                    self.setWindowTitle("Create cluster calculation  external work")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setFont(QFont('Arial', 10))
                                       
                    self.Hoeveelheid = QLabel(self)
                    self.Hoeveelheid.setText('Amount ')
                    self.hoev = QLineEdit(self)
                    self.hoev.setFixedWidth(100)
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.hoev)
                    self.hoev.setValidator(input_validator)
                    
                    grid.addWidget(self.Hoeveelheid, 3, 1)
                    grid.addWidget(self.hoev, 3, 2)
                    
                    grid.addWidget(QLabel(' \u00A9 2017 all rights reserved\n     dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
                    
                    self.cancelBtn = QPushButton('Close')
                    self.cancelBtn.clicked.connect(self.close)
                    grid.addWidget(self.cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
                    self.cancelBtn.setFont(QFont("Arial",10))
                    self.cancelBtn.setFixedWidth(100)
                    self.cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                             
                    self.applyBtn = QPushButton('Insert', self)
                    self.applyBtn.clicked.connect(self.clickMethod)
                    grid.addWidget(self.applyBtn, 4, 2, 1, 1, Qt.AlignRight)
                    self.applyBtn.setFont(QFont("Arial",10))
                    self.applyBtn.setFixedWidth(100)
                    self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)

                def clickMethod(self):
                    mhoev = self.hoev.text()
                    if mhoev == '' or mhoev == ' ':
                        return
                    mhoev = float(str(mhoev))

                    metadata = MetaData()
                    clusters = Table('clusters', metadata,
                          Column('clusterID', Integer(), primary_key=True),
                          Column('omschrijving', String),
                          Column('eenheid', String),
                          Column('prijs', Float))
                    calculaties = Table('calculaties', metadata,
                          Column('calcID', Integer(), primary_key=True),
                          Column('clusterID', None, ForeignKey('clusters.clusterID')),
                          Column('omschrijving', String),
                          Column('hoeveelheid', Float),
                          Column('eenheid', String),
                          Column('prijs', Float),
                          Column('calculatie', Integer),
                          Column('calculatiedatum', String),
                          Column('werkomschrijving', String))

                    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                    con = engine.connect()
                    sel = select([clusters.c.clusterID, clusters.c.omschrijving, clusters.c.eenheid, \
                                  clusters.c.prijs]).where(clusters.c.clusterID == clusternr)
                    rpsel = con.execute(sel).first()
                    momschr = rpsel[1]
                    meenh = rpsel[2]
                    mprijs = rpsel[3]
                    mcaldat = str(datetime.datetime.now())[0:10]

                    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                    con = engine.connect()
                    selcalc = select([calculaties.c.clusterID, calculaties. \
                                     c.calculatie]).where(and_(calculaties.c.clusterID == clusternr, \
                                                                calculaties.c.calculatie == mcalnr))
                    rpcalc = con.execute(selcalc).first()
                    if rpcalc:
                        calcBestaat()
                        upd = update(calculaties) \
                            .where(and_(calculaties.c.clusterID == clusternr, \
                                        calculaties.c.calculatie == mcalnr)).values \
                            (hoeveelheid=calculaties.c.hoeveelheid + mhoev, \
                             calculatiedatum=mcaldat, werkomschrijving = mwerkomschr)
                        con.execute(upd)
                    else:
                        mcalnrnr = (con.execute(select([func.max(calculaties.c.calcID, \
                                                                 type_=Integer).label('mcalnrnr')])).scalar())
                        mcalnrnr += 1
                        ins = insert(calculaties).values(calcID=mcalnrnr, \
                              clusterID=clusternr, hoeveelheid=mhoev, \
                              omschrijving=momschr, eenheid=meenh, prijs=mprijs, \
                              calculatie=mcalnr, calculatiedatum=mcaldat, werkomschrijving = mwerkomschr)
                        con.execute(ins)
                        invoerOK()
                    self.accept()
                    
            mainWin = MainWindow()
            mainWin.exec_()

    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)