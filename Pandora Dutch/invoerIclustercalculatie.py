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
            self.setWindowTitle("Informatie ERP Systeem Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Informatie ERP Pandora')
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

        Informatie over clustercalculatie maken en koppelen naar werkorder.
        
        De volgorde van het aanmaken en koppelen van een calculatie is:
                      
        Menu Calculatie interne werken
        6. Calculatie maken of wijzigen.
           Accepteer het eerste vrije nummer hetgeen door het systeem wordt ingevuld.\t
           Wijzigen is alleen mogelijk indien de calculatie nog niet is gekoppeld
           aan een werkordernummer. Kies in dit geval een bestaand calculatienummer.
        7. Calculatie/Artikellijst - opvragen/berekenen/printen
           Hiermee worden de calculatiegegevens en /of de artikelgegevens opgevraagd
           berekend of geprint. De berekening geschiedt na het starten van de module.
        
        Menu Interne Werken
        1. Invoeren Werkopdrachten
           Werkordernummer wordt ingevuld. Invoeren omschrijving, start werk
           Artikelnummer halffabrikaat en hoeveelheid. Omschrijving en hoeveelheid
           dienen identiek te zijn aan de gegevens van de calculatie. Artikelnummer
           halffabrikaat verwijst naar het artikelnummer van het gereedprodukt.
           Maak zonodig dit artikelnummer eerst aan, indien het nog niet bestaat.
           
        Menu Calculatie interne werken   
        8. Calculatie koppelen produktie.
           De koppeling van de calculatie met het werknummer wordt gemaakt en de
           artikelgegevens en werktarieven worden overgezet naar de werkorder.
        
        Menu Interne Werken
        3. Opvragen werkopdrachten Printen Werkbrief.
            Print hierna de Werkbrief voor de produktie van de artikelen.
           
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

def gerCalnr(mcalnr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculatienummer '+str(mcalnr)+'  is aangemaakt!')
    msg.setWindowTitle('Clustercalculatie invoeren')               
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Clustercalculatie invoeren')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Clustercalculatie invoeren')               
    msg.exec_() 

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt')
    msg.setWindowTitle('Clustercalculatie invoeren')
    msg.exec_()

def calcBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculatieregel bestaat al\nen is verrekend met\ningebrachte hoeveelheid!')
    msg.setWindowTitle('Clustercalculatie invoeren')
    msg.exec_() 
    
def calcGekoppeld():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Calculatie is al gekoppeld aan werk\nwijzigen is niet meer mogelijk!')
    msg.setWindowTitle('Clustercalculatie invoeren')
    msg.exec_() 
    
def schoonCalculatie(mcalnr, m_email):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Calculatie Aanpassen")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText("Deze calculatie bestaat al\nwilt u deze calculatie aanpassen?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
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
       materiaallijsten = Table('materiaallijsten', metadata,
           Column('matlijstID', Integer, primary_key=True),
           Column('icalculatie', Integer))
        
       engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
       con = engine.connect()
       updcal = update(icalculaties).where(icalculaties.c.icalculatie == mcalnr).values\
         (prijs=0, materialen=0, lonen=0,diensten=0,materieel=0,inhuur=0,szagen=0,\
          zagen=0,sschaven=0,schaven=0,ssteken=0,steken=0,sboren=0,boren=0,sfrezen=0,\
          frezen=0,sdraaien_klein=0,draaien_klein=0,sdraaien_groot=0,draaien_groot=0,\
          stappen=0,tappen=0,snube_draaien=0,nube_draaien=0,snube_bewerken=0,\
          nube_bewerken=0,sknippen=0,knippen=0,skanten=0,kanten=0,sstansen=0,stansen=0,\
          slassen_co2=0,lassen_co2=0,slassen_hand=0,lassen_hand=0,sverpakken=0,\
          verpakken=0,sverzinken=0,verzinken=0,smoffelen=0,moffelen=0,sschilderen=0,\
          schilderen=0,sspuiten=0,spuiten=0,sponsen=0,ponsen=0,spersen=0,persen=0,\
          sgritstralen=0,gritstralen=0,smontage=0,montage=0,verwerkt=0)
       con.execute(updcal)
       delmat = delete(materiaallijsten).where(materiaallijsten.c.icalculatie==mcalnr)
       con.execute(delmat)
    else:
       zoeken(m_email)
    
def zoeken(m_email):
    metadata = MetaData()
    icalculaties = Table('icalculaties', metadata,
       Column('icalcID', Integer(), primary_key=True),
       Column('icalculatie', Integer),
       Column('verwerkt', Integer))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mcalnr = con.execute(select([func.max(icalculaties.c.icalculatie,\
            type_=Integer).label('mcalnr')])).scalar()
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Calculatie intern werk maken / wijzigen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
             
            self.Calculatie = QLabel()
            kEdit = QLineEdit(str(mcalnr+1))
            kEdit.setFixedWidth(100)
            kEdit.setAlignment(Qt.AlignRight)
            kEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp('^[0-9]{1,9}$')
            input_validator = QRegExpValidator(reg_ex, kEdit)
            kEdit.setValidator(input_validator)
            kEdit.textChanged.connect(self.kChanged)
                   
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(340)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('         Sorteersleutel Clustergroepen')
            k0Edit.addItem('0. Alle Clusters')
            k0Edit.addItem('LA-LK. Bewerkte onderdelen')
            k0Edit.addItem('MA-MK. Bouten en Moeren')
            k0Edit.addItem('NA-NK. Gietwerk bewerking')
            k0Edit.addItem('OA-OK. Laswerk samengesteld')
            k0Edit.addItem('PA-PK. Plaatwerk samengesteld')
            k0Edit.addItem('RA-RK. Kunstof onderdelen')
            k0Edit.addItem('SA-SK. Prefab Montagedelen')
            k0Edit.addItem('TA-TK. Samengestelde Onderdelen')
            k0Edit.activated[str].connect(self.k0Changed)
           
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            grid.addWidget(k0Edit, 2, 0, 1, 2, Qt.AlignRight)
            
            lbl2 = QLabel('Calculatie')  
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 1, 0)
            grid.addWidget(kEdit, 1, 1,)
                         
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 0, 1, 2,Qt.AlignCenter)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            infoBtn = QPushButton('Informatie')
            infoBtn.clicked.connect(lambda: info())
    
            grid.addWidget(infoBtn, 3, 0)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
         
        def kChanged(self, text):
            self.Calculatie.setText(text)   
            
        def k0Changed(self, text):
            self.Keuze.setText(text)
                  
        def returnk(self):
            return self.Calculatie.text()
        
        def returnk0(self):
            return self.Keuze.text()
  
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnk()]       

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
    scontr = select([icalculaties]).where(icalculaties.c.icalculatie == mcalnr)
    rpcontr = con.execute(scontr).first()
    if rpcontr and rpcontr[2] == 2:
        calcGekoppeld()
        zoeken(m_email)
    elif rpcontr and rpcontr[2] == 1:
       schoonCalculatie(mcalnr, m_email)
    toonIclusters(m_email, keuze , mcalnr)
 
def toonIclusters(m_email, keuze, mcalnr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 900, 900)
            self.setWindowTitle('Clustercalculatie intern werk')
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
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
 
    header = ['Clusternr', 'Omschrijving', 'Prijs', 'Eenheid', 'Materialen', 'Lonen',\
              'Diensten', 'Materiëel', 'Inhuur']
    
    metadata = MetaData()
    
    iclusters = Table('iclusters', metadata,
        Column('iclusterID', Integer(), primary_key=True),
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
        sel = select([iclusters]).order_by(iclusters.c.iclusterID)
    elif keuze:
        sel = select([iclusters]).where(iclusters.c.iclusterID.ilike(keuze+'%'))\
                              .order_by(iclusters.c.iclusterID)
  
    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
        toonIclusters(m_email)
        
    data_list=[]
    for row in rp:
        data_list += [(row)]

    def showSelection(idx):
        clusternr = str(idx.data())
        if idx.column() == 0:
            metadata = MetaData()
            iclusters = Table('iclusters', metadata,
                Column('iclusterID', Integer(), primary_key=True),
                Column('omschrijving', String))
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcl = select([iclusters]).where(iclusters.c.iclusterID == clusternr.upper())
            rpcl = con.execute(selcl).first()
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)
                      
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Calculatienummer:          '+str(mcalnr)), 1, 1, 1, 3)
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Clusternummer               '+str(clusternr)+\
                           '\n'+rpcl[1]), 2, 1, 1, 3)
                               
                    self.setWindowTitle("Clustercalculatie intern werk maken") 
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setFont(QFont('Arial', 10))
                                       
                    self.Hoeveelheid = QLabel(self)
                    self.Hoeveelheid.setText('Hoeveelheid ')
                    self.hoev = QLineEdit(self)
                    self.hoev.setFixedWidth(100)
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.hoev)
                    self.hoev.setValidator(input_validator)
                    
                    grid.addWidget(self.Hoeveelheid, 3, 1)
                    grid.addWidget(self.hoev, 3, 2)
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
                    
                    self.applyBtn = QPushButton('Invoeren', self)
                    self.applyBtn.clicked.connect(self.clickMethod)
                    grid.addWidget(self.applyBtn, 4, 2, 1, 1, Qt.AlignRight)
                    self.applyBtn.setFont(QFont("Arial",10))
                    self.applyBtn.setFixedWidth(100) 
                    self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    self.cancelBtn = QPushButton('Sluiten')
                    self.cancelBtn.clicked.connect(self.close)
                    grid.addWidget(self.cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
                    self.cancelBtn.setFont(QFont("Arial",10))
                    self.cancelBtn.setFixedWidth(100)
                    self.cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
      
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)
                       
                def clickMethod(self):
                    mhoev=self.hoev.text()
                    if mhoev == '' or mhoev == ' ':
                        return
                    mhoev = float(str(mhoev))
                                    
                    metadata = MetaData()
                    iclusters = Table('iclusters', metadata,
                       Column('iclusterID', Integer(), primary_key=True),
                       Column('omschrijving', String),
                       Column('eenheid', String),
                       Column('prijs', Float))
                    icalculaties = Table('icalculaties', metadata,
                       Column('icalcID', Integer(), primary_key=True),
                       Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
                       Column('omschrijving', String),
                       Column('hoeveelheid', Float),
                       Column('eenheid', String),
                       Column('prijs', Float),
                       Column('icalculatie', Integer),
                       Column('calculatiedatum', String))
                     
                    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                    con = engine.connect()
                    sel = select([iclusters.c.iclusterID, iclusters.c.omschrijving, iclusters.c.eenheid,\
                        iclusters.c.prijs]).where(iclusters.c.iclusterID == clusternr)
                    rpsel = con.execute(sel).first()
                    momschr = rpsel[1]
                    meenh = rpsel[2]
                    mprijs = rpsel[3]
                    mcaldat = str(datetime.datetime.now())[0:10]
                                                     
                    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                    con = engine.connect()
                    selcalc = select([icalculaties.c.iclusterID, icalculaties.\
                     c.icalculatie]).where(and_(icalculaties.c.iclusterID == clusternr,\
                     icalculaties.c.icalculatie == mcalnr))
                    rpcalc = con.execute(selcalc).first()
                    if rpcalc:
                        calcBestaat()
                        upd = update(icalculaties)\
                         .where(and_(icalculaties.c.iclusterID == clusternr,\
                             icalculaties.c.icalculatie == mcalnr)).values\
                            (hoeveelheid = icalculaties.c.hoeveelheid + mhoev,\
                             calculatiedatum = mcaldat)
                        con.execute(upd)
                    else:
                        mcalnrnr = (con.execute(select([func.max(icalculaties.c.icalcID,\
                            type_=Integer).label('mcalnrnr')])).scalar())
                        mcalnrnr += 1
                        ins = insert(icalculaties).values(icalcID = mcalnrnr,\
                                iclusterID = clusternr, hoeveelheid = mhoev,\
                                omschrijving = momschr, eenheid = meenh, prijs = mprijs,\
                                icalculatie = mcalnr, calculatiedatum = mcaldat)
                        con.execute(ins)
                        invoerOK()
                    self.accept()
                    
            mainWin = MainWindow()
            mainWin.exec_()
   
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)