from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QDialog, QLabel,\
         QGridLayout, QPushButton, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData,\
                         create_engine)
from sqlalchemy.sql import select, update

def refresh(keuze, m_email, self):
    self.close()
    toonIclusters(keuze, m_email)
    
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Je gegevens zijn aangepast!')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Clusters invoeren!')
    msg.exec_()

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Clusters invoeren')
    msg.exec_()
    
def calcBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculatieregel bestaat al\nen is verrekend met\ningebrachte hoeveelheid!')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Clusters invoeren')
    msg.exec_()   

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
        
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen cluster gevonden\nmaak een andere selektie\nof maak een nieuwe cluster s.v.p.!')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Clusters invoeren')               
    msg.exec_() 
    
def ongKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Ongeldige keuze')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Clusters invoeren')               
    msg.exec_() 
        
def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster selektie")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                              
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(300)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('          Sorteersleutel Clustergroepen')
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
            grid.addWidget(lbl , 1, 0, 1, 2)
                        
            grid.addWidget(k0Edit, 3, 0, 1, 3, Qt.AlignRight)
                        
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 2, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Clusters')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 5, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(cancelBtn, 5, 1, 1, 1,Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
        def k0Changed(self, text):
            self.Keuze.setText(text)
                    
        def returnk0(self):
            return self.Keuze.text()
                   
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0()]       

    window = Widget()
    data = window.getData()
    keuze = ''
    if not data[0]:
        ongKeuze()
        zoeken(m_email)
    elif data[0][0] == '0':
        keuze = ''
    elif data[0]:
        keuze = data[0][0]
    toonIclusters(keuze, m_email)  
  
def toonIclusters(keuze, m_email) :            
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Cluster Calculatie')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))

            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0, 1, 16)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 15, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(keuze, m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 14, 1, 1, Qt.AlignRight)
        
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 13, 1, 1, Qt.AlignRight)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 0, 1, 16, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(50, 50, 1800, 900)
            self.setLayout(grid)

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
             
    header = ['Clusternr','Omschrijving','Prijs','Eenheid','Materialen','Lonen',\
              'Diensten','Materiëel','Inhuur','St.zagen','Zagen','St.schaven','Schaven',\
              'St.steken','Steken','St.boren','Boren','St.frezen','Frezen','St.draaien klein',\
              'Draaien klein','St.draaien_groot','Draaien groot','St.tappen','Tappen',\
              'St.nube draaien','Nube draaien','St.nube bewerken','Nube bewerken',\
              'St.knippen','Knippen','St.kanten','Kanten','St.stansen','Stansen',\
              'St.lassen co2','Lassen co2','St.lassen hand','Lassen hand','St.verpakken',\
              'Verpakken','St.verzinken','Verzinken','St.moffelen','Moffelen','St.schilderen',\
              'Schilderen','St.spuiten','Spuiten','St.ponsen','Ponsen','St.persen',\
              'Persen','St.gritstralen','Gritstralen','St.montage','Montage']
    
    metadata = MetaData()
    iclusters = Table('iclusters', metadata,
        Column('iclusterID', String, primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
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
    
    sel = select([iclusters]).where(iclusters.c.iclusterID.ilike(keuze+'%'))\
                          .order_by(iclusters.c.iclusterID)

    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
        zoeken(m_email)
        
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        clusternr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcl = select([iclusters]).where(iclusters.c.iclusterID == clusternr)
            rpsel = con.execute(selcl).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Wijzigen Cluster")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                    
                    self.Omschrijving = QLabel()
                    q1Edit = QLineEdit(rpsel[1])
                    q1Edit.setFixedWidth(400)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.textChanged.connect(self.q1Changed) 
                    reg_ex = QRegExp("^.{0,49}$")
                    input_validator = QRegExpValidator(reg_ex, q1Edit)
                    q1Edit.setValidator(input_validator)
                                    
                    self.Prijs = QLabel()
                    q2Edit = QLineEdit(str(round(float(rpsel[2]),2)))
                    q2Edit.setFixedWidth(150)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.textChanged.connect(self.q2Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)
                     
                    self.Eenheid = QLabel()
                    q3Edit = QLineEdit(str(rpsel[3]))
                    q3Edit.setFixedWidth(150)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.textChanged.connect(self.q3Changed) 
                    reg_ex = QRegExp("^.{0,10}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                    
                    self.Materialen = QLabel()
                    q4Edit = QLineEdit(str(round(float(rpsel[4]),2)))
                    q4Edit.setFixedWidth(150)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.textChanged.connect(self.q4Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                    q4Edit.setDisabled(True)
                    
                    self.Lonen = QLabel()
                    q5Edit = QLineEdit(str(round(float(rpsel[5]),2)))
                    q5Edit.setFixedWidth(150)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.textChanged.connect(self.q5Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q5Edit)
                    q5Edit.setValidator(input_validator)
                    q5Edit.setDisabled(True)
                    
                    self.Diensten = QLabel()
                    q6Edit = QLineEdit(str(round(float(rpsel[6]),2)))
                    q6Edit.setFixedWidth(150)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.textChanged.connect(self.q6Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q6Edit)
                    q6Edit.setValidator(input_validator)
                    q6Edit.setDisabled(True)
                    
                    self.Materiëel = QLabel()
                    q7Edit = QLineEdit(str(round(float(rpsel[7]),2)))
                    q7Edit.setFixedWidth(150)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.textChanged.connect(self.q7Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q7Edit)
                    q7Edit.setValidator(input_validator)
                    q7Edit.setDisabled(True)
                    
                    self.Inhuur = QLabel()
                    q8Edit = QLineEdit(str(round(float(rpsel[8]),2)))
                    q8Edit.setFixedWidth(150)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.textChanged.connect(self.q8Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q8Edit)
                    q8Edit.setValidator(input_validator)
                    q8Edit.setDisabled(True)
                      
                    self.Szagen = QLabel()
                    q9Edit = QLineEdit(str(round(float(rpsel[9]),2)))
                    q9Edit.setFixedWidth(150)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.textChanged.connect(self.q9Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q9Edit)
                    q9Edit.setValidator(input_validator)
                    
                    self.Zagen = QLabel()
                    q10Edit = QLineEdit(str(round(float(rpsel[10]),2)))
                    q10Edit.setFixedWidth(150)
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setFont(QFont("Arial",10))
                    q10Edit.textChanged.connect(self.q10Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q10Edit)
                    q10Edit.setValidator(input_validator)
                    
                    self.Sschaven = QLabel()
                    q11Edit = QLineEdit(str(round(float(rpsel[11]),2)))
                    q11Edit.setFixedWidth(150)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.textChanged.connect(self.q11Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q11Edit)
                    q11Edit.setValidator(input_validator)
                    
                    self.Schaven = QLabel()
                    q12Edit = QLineEdit(str(round(float(rpsel[12]),2)))
                    q12Edit.setFixedWidth(150)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.textChanged.connect(self.q12Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q12Edit)
                    q12Edit.setValidator(input_validator)
                    
                    self.Ssteken = QLabel()
                    q13Edit = QLineEdit(str(round(float(rpsel[13]),2)))
                    q13Edit.setFixedWidth(150)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.textChanged.connect(self.q13Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q13Edit)
                    q13Edit.setValidator(input_validator)
                    
                    self.Steken = QLabel()
                    q14Edit = QLineEdit(str(round(float(rpsel[14]),2)))
                    q14Edit.setFixedWidth(150)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.textChanged.connect(self.q14Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q14Edit)
                    q14Edit.setValidator(input_validator)
                    
                    self.Sboren = QLabel()
                    q15Edit = QLineEdit(str(round(float(rpsel[15]),2)))
                    q15Edit.setFixedWidth(150)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setFont(QFont("Arial",10))
                    q15Edit.textChanged.connect(self.q15Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q15Edit)
                    q15Edit.setValidator(input_validator)
                                   
                    self.Boren = QLabel()
                    q16Edit = QLineEdit(str(round(float(rpsel[16]),2)))
                    q16Edit.setFixedWidth(150)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.textChanged.connect(self.q16Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q16Edit)
                    q16Edit.setValidator(input_validator)
                    
                    self.Sfrezen = QLabel()
                    q17Edit = QLineEdit(str(round(float(rpsel[17]),2)))
                    q17Edit.setFixedWidth(150)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setFont(QFont("Arial",10))
                    q17Edit.textChanged.connect(self.q17Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q17Edit)
                    q17Edit.setValidator(input_validator)
                    
                    self.Frezen = QLabel()
                    q18Edit = QLineEdit(str(round(float(rpsel[18]),2)))
                    q18Edit.setFixedWidth(150)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setFont(QFont("Arial",10))
                    q18Edit.textChanged.connect(self.q18Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q18Edit)
                    q18Edit.setValidator(input_validator)  
                    
                    self.Sdraaien_klein = QLabel()
                    q19Edit = QLineEdit(str(round(float(rpsel[19]),2)))
                    q19Edit.setFixedWidth(150)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setFont(QFont("Arial",10))
                    q19Edit.textChanged.connect(self.q19Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q19Edit)
                    q19Edit.setValidator(input_validator)
                         
                    self.Draaien_klein = QLabel()
                    q20Edit = QLineEdit(str(round(float(rpsel[20]),2)))
                    q20Edit.setFixedWidth(150)
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setFont(QFont("Arial",10))
                    q20Edit.textChanged.connect(self.q20Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q20Edit)
                    q20Edit.setValidator(input_validator)
                    
                    self.Sdraaien_groot = QLabel()
                    q21Edit = QLineEdit(str(round(float(rpsel[21]),2)))
                    q21Edit.setFixedWidth(150)
                    q21Edit.setAlignment(Qt.AlignRight)
                    q21Edit.setFont(QFont("Arial",10))
                    q21Edit.textChanged.connect(self.q21Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q21Edit)
                    q21Edit.setValidator(input_validator)
                    
                    self.Draaien_groot = QLabel()
                    q22Edit = QLineEdit(str(round(float(rpsel[22]),2)))
                    q22Edit.setFixedWidth(150)
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.setFont(QFont("Arial",10))
                    q22Edit.textChanged.connect(self.q22Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q22Edit)
                    q22Edit.setValidator(input_validator)
                    
                    self.Stappen = QLabel()
                    q23Edit = QLineEdit(str(round(float(rpsel[23]),2)))
                    q23Edit.setFixedWidth(150)
                    q23Edit.setAlignment(Qt.AlignRight)
                    q23Edit.setFont(QFont("Arial",10))
                    q23Edit.textChanged.connect(self.q23Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q23Edit)
                    q23Edit.setValidator(input_validator)
                       
                    self.Tappen = QLabel()
                    q24Edit = QLineEdit(str(round(float(rpsel[24]),2)))
                    q24Edit.setFixedWidth(150)
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setFont(QFont("Arial",10))
                    q24Edit.textChanged.connect(self.q24Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q24Edit)
                    q24Edit.setValidator(input_validator)
                    
                    self.Snube_draaien = QLabel()
                    q25Edit = QLineEdit(str(round(float(rpsel[25]),2)))
                    q25Edit.setFixedWidth(150)
                    q25Edit.setAlignment(Qt.AlignRight)
                    q25Edit.setFont(QFont("Arial",10))
                    q25Edit.textChanged.connect(self.q25Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q25Edit)
                    q25Edit.setValidator(input_validator)
                    
                    self.Nube_draaien = QLabel()
                    q26Edit = QLineEdit(str(round(float(rpsel[26]),2)))
                    q26Edit.setFixedWidth(150)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setFont(QFont("Arial",10))
                    q26Edit.textChanged.connect(self.q26Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q26Edit)
                    q26Edit.setValidator(input_validator)
                    
                    self.Snube_bewerken = QLabel()
                    q27Edit = QLineEdit(str(round(float(rpsel[27]),2)))
                    q27Edit.setFixedWidth(150)
                    q27Edit.setAlignment(Qt.AlignRight)
                    q27Edit.setFont(QFont("Arial",10))
                    q27Edit.textChanged.connect(self.q27Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q27Edit)
                    q27Edit.setValidator(input_validator)
                    
                    self.Nube_bewerken = QLabel()
                    q28Edit = QLineEdit(str(round(float(rpsel[28]),2)))
                    q28Edit.setFixedWidth(150)
                    q28Edit.setAlignment(Qt.AlignRight)
                    q28Edit.setFont(QFont("Arial",10))
                    q28Edit.textChanged.connect(self.q28Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q28Edit)
                    q28Edit.setValidator(input_validator)
                    
                    self.Sknippen = QLabel()
                    q29Edit = QLineEdit(str(round(float(rpsel[29]),2)))
                    q29Edit.setFixedWidth(150)
                    q29Edit.setAlignment(Qt.AlignRight)
                    q29Edit.setFont(QFont("Arial",10))
                    q29Edit.textChanged.connect(self.q29Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q29Edit)
                    q29Edit.setValidator(input_validator)
                       
                    self.Knippen = QLabel()
                    q30Edit = QLineEdit(str(round(float(rpsel[30]),2)))
                    q30Edit.setFixedWidth(150)
                    q30Edit.setAlignment(Qt.AlignRight)
                    q30Edit.setFont(QFont("Arial",10))
                    q30Edit.textChanged.connect(self.q30Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q30Edit)
                    q30Edit.setValidator(input_validator)
                    
                    self.Skanten = QLabel()
                    q31Edit = QLineEdit(str(round(float(rpsel[31]),2)))
                    q31Edit.setFixedWidth(150)
                    q31Edit.setAlignment(Qt.AlignRight)
                    q31Edit.setFont(QFont("Arial",10))
                    q31Edit.textChanged.connect(self.q31Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q31Edit)
                    q31Edit.setValidator(input_validator)
                            
                    self.Kanten = QLabel()
                    q32Edit = QLineEdit(str(round(float(rpsel[32]),2)))
                    q32Edit.setFixedWidth(150)
                    q32Edit.setAlignment(Qt.AlignRight)
                    q32Edit.setFont(QFont("Arial",10))
                    q32Edit.textChanged.connect(self.q32Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q32Edit)
                    q32Edit.setValidator(input_validator)
                    
                    self.Sstansen = QLabel()
                    q33Edit = QLineEdit(str(round(float(rpsel[33]),2)))
                    q33Edit.setFixedWidth(150)
                    q33Edit.setAlignment(Qt.AlignRight)
                    q33Edit.setFont(QFont("Arial",10))
                    q33Edit.textChanged.connect(self.q33Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q33Edit)
                    q33Edit.setValidator(input_validator)
                    
                    self.Stansen = QLabel()
                    q34Edit = QLineEdit(str(round(float(rpsel[34]),2)))
                    q34Edit.setFixedWidth(150)
                    q34Edit.setAlignment(Qt.AlignRight)
                    q34Edit.setFont(QFont("Arial",10))
                    q34Edit.textChanged.connect(self.q34Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q34Edit)
                    q34Edit.setValidator(input_validator)
                    
                    self.Slassen_CO2 = QLabel()
                    q35Edit = QLineEdit(str(round(float(rpsel[35]),2)))
                    q35Edit.setFixedWidth(150)
                    q35Edit.setAlignment(Qt.AlignRight)
                    q35Edit.setFont(QFont("Arial",10))
                    q35Edit.textChanged.connect(self.q35Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q35Edit)
                    q35Edit.setValidator(input_validator)
                    
                    self.Lassen_CO2 = QLabel()
                    q36Edit = QLineEdit(str(round(float(rpsel[36]),2)))
                    q36Edit.setFixedWidth(150)
                    q36Edit.setAlignment(Qt.AlignRight)
                    q36Edit.setFont(QFont("Arial",10))
                    q36Edit.textChanged.connect(self.q36Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q36Edit)
                    q36Edit.setValidator(input_validator)
                    
                    self.Slassen_hand = QLabel()
                    q37Edit = QLineEdit(str(round(float(rpsel[37]),2)))
                    q37Edit.setFixedWidth(150)
                    q37Edit.setAlignment(Qt.AlignRight)
                    q37Edit.setFont(QFont("Arial",10))
                    q37Edit.textChanged.connect(self.q37Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q37Edit)
                    q37Edit.setValidator(input_validator)
                    
                    self.Lassen_hand = QLabel()
                    q38Edit = QLineEdit(str(round(float(rpsel[38]),2)))
                    q38Edit.setFixedWidth(150)
                    q38Edit.setAlignment(Qt.AlignRight)
                    q38Edit.setFont(QFont("Arial",10))
                    q38Edit.textChanged.connect(self.q38Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q38Edit)
                    q38Edit.setValidator(input_validator)
                    
                    self.Sverpakken = QLabel()
                    q39Edit = QLineEdit(str(round(float(rpsel[39]),2)))
                    q39Edit.setFixedWidth(150)
                    q39Edit.setFont(QFont("Arial",10))
                    q39Edit.setAlignment(Qt.AlignRight)
                    q39Edit.textChanged.connect(self.q39Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q39Edit)
                    q39Edit.setValidator(input_validator)
                    
                    self.Verpakken = QLabel()
                    q40Edit = QLineEdit(str(round(float(rpsel[40]),2)))
                    q40Edit.setFixedWidth(150)
                    q40Edit.setFont(QFont("Arial",10))
                    q40Edit.setAlignment(Qt.AlignRight)
                    q40Edit.textChanged.connect(self.q40Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q40Edit)
                    q40Edit.setValidator(input_validator)
                    
                    self.Sverzinken = QLabel()
                    q41Edit = QLineEdit(str(round(float(rpsel[41]),2)))
                    q41Edit.setFixedWidth(150)
                    q41Edit.setFont(QFont("Arial",10))
                    q41Edit.setAlignment(Qt.AlignRight)
                    q41Edit.textChanged.connect(self.q41Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q41Edit)
                    q41Edit.setValidator(input_validator)
                    
                    self.Verzinken = QLabel()
                    q42Edit = QLineEdit(str(round(float(rpsel[42]),2)))
                    q42Edit.setFixedWidth(150)
                    q42Edit.setAlignment(Qt.AlignRight)
                    q42Edit.setFont(QFont("Arial",10))
                    q42Edit.textChanged.connect(self.q42Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q42Edit)
                    q42Edit.setValidator(input_validator)
                    
                    self.Smoffelen = QLabel()
                    q43Edit = QLineEdit(str(round(float(rpsel[43]),2)))
                    q43Edit.setFixedWidth(150)
                    q43Edit.setAlignment(Qt.AlignRight)
                    q43Edit.setFont(QFont("Arial",10))
                    q43Edit.textChanged.connect(self.q43Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q43Edit)
                    q43Edit.setValidator(input_validator)
                    
                    self.Moffelen = QLabel()
                    q44Edit = QLineEdit(str(round(float(rpsel[44]),2)))
                    q44Edit.setFixedWidth(150)
                    q44Edit.setAlignment(Qt.AlignRight)
                    q44Edit.setFont(QFont("Arial",10))
                    q44Edit.textChanged.connect(self.q44Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q44Edit)
                    q44Edit.setValidator(input_validator)
                    
                    self.Sschilderen = QLabel()
                    q45Edit = QLineEdit(str(round(float(rpsel[45]),2)))
                    q45Edit.setFixedWidth(150)
                    q45Edit.setAlignment(Qt.AlignRight)
                    q45Edit.setFont(QFont("Arial",10))
                    q45Edit.textChanged.connect(self.q45Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q45Edit)
                    q45Edit.setValidator(input_validator)
        
                    self.Schilderen = QLabel()
                    q46Edit = QLineEdit(str(round(float(rpsel[46]),2)))
                    q46Edit.setFixedWidth(150)
                    q46Edit.setAlignment(Qt.AlignRight)
                    q46Edit.setFont(QFont("Arial",10))
                    q46Edit.textChanged.connect(self.q46Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q46Edit)
                    q46Edit.setValidator(input_validator)
                    
                    self.Sspuiten = QLabel()
                    q47Edit = QLineEdit(str(round(float(rpsel[47]),2)))
                    q47Edit.setFixedWidth(150)
                    q47Edit.setAlignment(Qt.AlignRight)
                    q47Edit.setFont(QFont("Arial",10))
                    q47Edit.textChanged.connect(self.q47Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q47Edit)
                    q47Edit.setValidator(input_validator)
                    
                    self.Spuiten = QLabel()
                    q48Edit = QLineEdit(str(round(float(rpsel[48]),2)))
                    q48Edit.setFixedWidth(150)
                    q48Edit.setAlignment(Qt.AlignRight)
                    q48Edit.setFont(QFont("Arial",10))
                    q48Edit.textChanged.connect(self.q48Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q48Edit)
                    q48Edit.setValidator(input_validator)
                    
                    self.Sponsen = QLabel()
                    q49Edit = QLineEdit(str(round(float(rpsel[49]),2)))
                    q49Edit.setFixedWidth(150)
                    q49Edit.setAlignment(Qt.AlignRight)
                    q49Edit.setFont(QFont("Arial",10))
                    q49Edit.textChanged.connect(self.q49Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q49Edit)
                    q49Edit.setValidator(input_validator)
                    
                    self.Ponsen = QLabel()
                    q50Edit = QLineEdit(str(round(float(rpsel[50]),2)))
                    q50Edit.setFixedWidth(150)
                    q50Edit.setAlignment(Qt.AlignRight)
                    q50Edit.setFont(QFont("Arial",10))
                    q50Edit.textChanged.connect(self.q50Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q50Edit)
                    q50Edit.setValidator(input_validator)
                    
                    self.Spersen = QLabel()
                    q51Edit = QLineEdit(str(round(float(rpsel[51]),2)))
                    q51Edit.setFixedWidth(150)
                    q51Edit.setAlignment(Qt.AlignRight)
                    q51Edit.setFont(QFont("Arial",10))
                    q51Edit.textChanged.connect(self.q51Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q51Edit)
                    q51Edit.setValidator(input_validator)
                    
                    self.Persen = QLabel()
                    q52Edit = QLineEdit(str(round(float(rpsel[52]),2)))
                    q52Edit.setFixedWidth(150)
                    q52Edit.setAlignment(Qt.AlignRight)
                    q52Edit.setFont(QFont("Arial",10))
                    q52Edit.textChanged.connect(self.q52Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q52Edit)
                    q52Edit.setValidator(input_validator)
                    
                    self.Sgritstralen = QLabel()
                    q53Edit = QLineEdit(str(round(float(rpsel[53]),2)))
                    q53Edit.setFixedWidth(150)
                    q53Edit.setAlignment(Qt.AlignRight)
                    q53Edit.setFont(QFont("Arial",10))
                    q53Edit.textChanged.connect(self.q53Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q53Edit)
                    q53Edit.setValidator(input_validator)
                    
                    self.Gritstralen = QLabel()
                    q54Edit = QLineEdit(str(round(float(rpsel[54]),2)))
                    q54Edit.setFixedWidth(150)
                    q54Edit.setAlignment(Qt.AlignRight)
                    q54Edit.setFont(QFont("Arial",10))
                    q54Edit.textChanged.connect(self.q54Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q54Edit)
                    q54Edit.setValidator(input_validator) 
                    
                    self.Smontage = QLabel()
                    q55Edit = QLineEdit(str(round(float(rpsel[55]),2)))
                    q55Edit.setFixedWidth(150)
                    q55Edit.setFont(QFont("Arial",10))
                    q55Edit.setAlignment(Qt.AlignRight)
                    q55Edit.textChanged.connect(self.q55Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q55Edit)
                    q55Edit.setValidator(input_validator)
                                     
                    self.Montage = QLabel()
                    q56Edit = QLineEdit(str(round(float(rpsel[56]),2)))
                    q56Edit.setFixedWidth(150)
                    q56Edit.setAlignment(Qt.AlignRight)
                    q56Edit.setFont(QFont("Arial",10))
                    q56Edit.textChanged.connect(self.q56Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q56Edit)
                    q56Edit.setValidator(input_validator)   
                                                                          
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Clusternummer')  
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(clusternr)
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Omschrijving')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 1, 2)
                    grid.addWidget(q1Edit, 1, 3, 1, 3) # RowSpan 1 ,ColumnSpan 3
                                                         
                    lbl4 = QLabel('Prijs')  
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 2, 0)
                    grid.addWidget(q2Edit, 2, 1)
                    
                    lbl5 = QLabel('Eenheid')  
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 2, 2)
                    grid.addWidget(q3Edit, 2, 3)
                    
                    lbl6 = QLabel('Materialen')  
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 2, 4)
                    grid.addWidget(q4Edit, 2, 5)
                    
                    lbl7 = QLabel('Lonen')  
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 2, 6)
                    grid.addWidget(q5Edit, 2, 7)
                    
                    lbl8 = QLabel('Diensten')  
                    lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl8, 3, 0)
                    grid.addWidget(q6Edit, 3, 1)
                    
                    lbl9 = QLabel('Materiëel')  
                    lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl9, 3, 2)
                    grid.addWidget(q7Edit, 3, 3)
                    
                    lbl10 = QLabel('Inhuur')  
                    lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl10, 3, 4)
                    grid.addWidget(q8Edit, 3, 5)
                    
                    lbl11 = QLabel('St.zagen')  
                    lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl11, 4, 0)
                    grid.addWidget(q9Edit, 4, 1)
                    
                    lbl12 = QLabel('Zagen')  
                    lbl12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl12, 4, 2)
                    grid.addWidget(q10Edit, 4, 3)
                    
                    lbl13 = QLabel('St.schaven')  
                    lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl13, 4, 4)
                    grid.addWidget(q11Edit, 4, 5)
                      
                    lbl14 = QLabel('Schaven')  
                    lbl14.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl14, 4, 6)
                    grid.addWidget(q12Edit, 4, 7)
                    
                    lbl15 = QLabel('St.steken')  
                    lbl15.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl15, 5, 0)
                    grid.addWidget(q13Edit, 5, 1)
                    
                    lbl16 = QLabel('Steken')  
                    lbl16.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl16, 5, 2)
                    grid.addWidget(q14Edit, 5, 3)
                    
                    lbl17 = QLabel('St.boren')  
                    lbl17.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl17, 5, 4)
                    grid.addWidget(q15Edit, 5, 5)
                    
                    lbl18 = QLabel('Boren')  
                    lbl18.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl18, 5, 6)
                    grid.addWidget(q16Edit, 5, 7)
                    
                    lbl19 = QLabel('St.frezen')  
                    lbl19.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl19, 6, 0)
                    grid.addWidget(q17Edit, 6, 1)
                    
                    lbl20 = QLabel('Frezen')  
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 6, 2)
                    grid.addWidget(q18Edit, 6, 3)
                    
                    lbl21 = QLabel('St.draaien-klein')  
                    lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl21, 6, 4)
                    grid.addWidget(q19Edit, 6, 5)
                    
                    lbl22 = QLabel('Draaien-klein')  
                    lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl22, 6, 6)
                    grid.addWidget(q20Edit, 6, 7)
                    
                    lbl23 = QLabel('St.draaien-groot')  
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 7, 0)
                    grid.addWidget(q21Edit, 7, 1)
                    
                    lbl26 = QLabel('Draaien-groot')  
                    lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl26, 7, 2)
                    grid.addWidget(q22Edit, 7, 3)
                    
                    lbl27 = QLabel('St.tappen')  
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 7, 4)
                    grid.addWidget(q23Edit, 7, 5)
                    
                    lbl28 = QLabel('Tappen')  
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 7, 6)
                    grid.addWidget(q24Edit, 7, 7)
                    
                    lbl27 = QLabel('St.nube_draaien')  
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 8, 0)
                    grid.addWidget(q25Edit, 8, 1)
                    
                    lbl28 = QLabel('Nube_draaien')  
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 8, 2)
                    grid.addWidget(q26Edit, 8, 3)
                    
                    lbl29 = QLabel('St.nube-bewerken')  
                    lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl29, 8, 4)
                    grid.addWidget(q27Edit, 8, 5)
                    
                    lbl30 = QLabel('Nube-bewerken')  
                    lbl30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl30, 8, 6)
                    grid.addWidget(q28Edit, 8, 7)
                    
                    lbl31 = QLabel('St.knippen')  
                    lbl31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl31, 9, 0)
                    grid.addWidget(q29Edit, 9, 1)
                    
                    lbl32 = QLabel('Knippen')  
                    lbl32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl32, 9, 2)
                    grid.addWidget(q30Edit, 9, 3)
                    
                    lbl33 = QLabel('St.kanten')  
                    lbl33.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl33, 9, 4)
                    grid.addWidget(q31Edit, 9, 5)
                    
                    lbl34 = QLabel('Kanten')  
                    lbl34.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl34, 9, 6)
                    grid.addWidget(q32Edit, 9, 7)
                    
                    lbl35 = QLabel('St.stansen')  
                    lbl35.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl35, 10, 0)
                    grid.addWidget(q33Edit, 10, 1)
                    
                    lbl36 = QLabel('Stansen')  
                    lbl36.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl36, 10, 2)
                    grid.addWidget(q34Edit, 10, 3)
                    
                    lbl37 = QLabel('St.Lassen-Co2')  
                    lbl37.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl37, 10, 4)
                    grid.addWidget(q35Edit, 10, 5)
                    
                    lbl38 = QLabel('Lassen-Co2')  
                    lbl38.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl38, 10, 6)
                    grid.addWidget(q36Edit, 10, 7)
                    
                    lbl39 = QLabel('St.Lassen-hand')  
                    lbl39.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl39, 11, 0)
                    grid.addWidget(q37Edit, 11, 1)
                    
                    lbl40 = QLabel('Lassen-hand')  
                    lbl40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl40, 11, 2)
                    grid.addWidget(q38Edit, 11, 3)
                    
                    lbl41 = QLabel('St.Verpakken')  
                    lbl41.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl41, 11, 4)
                    grid.addWidget(q39Edit, 11, 5)
                        
                    lbl42 = QLabel('Verpakken')  
                    lbl42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl42, 11, 6)
                    grid.addWidget(q40Edit, 11, 7)
                    
                    lbl43 = QLabel('St.Verzinken')  
                    lbl43.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl43, 12, 0)
                    grid.addWidget(q41Edit, 12, 1)
                    
                    lbl44 = QLabel('Verzinken')  
                    lbl44.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl44, 12, 2)
                    grid.addWidget(q42Edit, 12, 3)
                    
                    lbl45 = QLabel('St.Moffelen')  
                    lbl45.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl45, 12, 4)
                    grid.addWidget(q43Edit, 12, 5)
                    
                    lbl46 = QLabel('Moffelen')  
                    lbl46.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl46, 12, 6)
                    grid.addWidget(q44Edit, 12, 7)
                    
                    lbl47 = QLabel('St.Schilderen')  
                    lbl47.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl47, 13, 0)
                    grid.addWidget(q45Edit, 13, 1)
                    
                    lbl48 = QLabel('Schilderen')  
                    lbl48.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl48, 13, 2)
                    grid.addWidget(q46Edit, 13, 3)
                    
                    lbl49 = QLabel('St.Spuiten')  
                    lbl49.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl49, 13, 4)
                    grid.addWidget(q47Edit, 13, 5)
                                                              
                    lbl50 = QLabel('Spuiten')  
                    lbl50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl50, 13, 6)
                    grid.addWidget(q48Edit, 13, 7)
                    
                    lbl51 = QLabel('St.Ponsen')
                    lbl51.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl51, 14, 0)
                    grid.addWidget(q49Edit, 14, 1)
                 
                    lbl52 = QLabel('Ponsen')
                    lbl52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl52, 14, 2)
                    grid.addWidget(q50Edit, 14, 3)
                    
                    lbl53 = QLabel('St.Persen')  
                    lbl53.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl53, 14, 4)
                    grid.addWidget(q51Edit, 14, 5)
                    
                    lbl54 = QLabel('Persen')  
                    lbl54.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl54, 14, 6)
                    grid.addWidget(q52Edit, 14, 7)
                    
                    lbl55 = QLabel('St.Gritstralen')  
                    lbl55.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl55, 15, 0)
                    grid.addWidget(q53Edit, 15, 1)
                    
                    lbl56 = QLabel('Gritstralen')  
                    lbl56.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl56, 15, 2)
                    grid.addWidget(q54Edit, 15, 3)
                    
                    lbl57 = QLabel('St.Montage')  
                    lbl57.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl57, 15, 4)
                    grid.addWidget(q55Edit, 15, 5)
                    
                    lbl58 = QLabel('Montage')  
                    lbl58.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl58, 15, 6)
                    grid.addWidget(q56Edit, 15, 7)
                          
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl, 0, 0, 1, 1, Qt.AlignRight)
                                     
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 7, 1 , 1, Qt.AlignRight)
                    
                    grid.addWidget(QLabel('Wijzigen Cluster'), 0, 1, 1, 8, Qt.AlignCenter)
                                                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 17, 0, 1, 8, Qt.AlignCenter)
                      
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 150, 150)
            
                    applyBtn = QPushButton('Wijzig')
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 16, 7, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(90)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 16, 6, 1, 2, Qt.AlignCenter)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(90)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                               
                def q1Changed(self,text):
                    self.Omschrijving.setText(text)
            
                def q2Changed(self,text):
                    self.Prijs.setText(text)
            
                def q3Changed(self,text):
                    self.Eenheid.setText(text)
             
                def q4Changed(self,text):
                    self.Materialen.setText(text)
                    
                def q5Changed(self,text):
                    self.Lonen.setText(text)
                    
                def q6Changed(self,text):
                    self.Diensten.setText(text)
                    
                def q7Changed(self,text):
                    self.Materiëel.setText(text)
                    
                def q8Changed(self,text):
                    self.Inhuur.setText(text)
                
                def q9Changed(self,text):
                    self.Szagen.setText(text)
                    
                def q10Changed(self,text):
                    self.Zagen.setText(text)
                       
                def q11Changed(self,text):
                    self.Sschaven.setText(text)
                    
                def q12Changed(self,text):
                    self.Schaven.setText(text)
                    
                def q13Changed(self,text):
                    self.Ssteken.setText(text)
                    
                def q14Changed(self,text):
                    self.Steken.setText(text)
                    
                def q15Changed(self,text):
                    self.Sboren.setText(text)
                    
                def q16Changed(self,text):
                    self.Boren.setText(text)
                    
                def q17Changed(self,text):
                    self.Sfrezen.setText(text)
                    
                def q18Changed(self,text):
                    self.Frezen.setText(text)
                    
                def q19Changed(self,text):
                    self.Sdraaien_klein.setText(text)
                    
                def q20Changed(self,text):
                    self.Draaien_klein.setText(text)
                    
                def q21Changed(self,text):
                    self.Sdraaien_groot.setText(text)
                    
                def q22Changed(self,text):
                    self.Draaien_groot.setText(text)
                    
                def q23Changed(self,text):
                    self.Stappen.setText(text)
                    
                def q24Changed(self,text):
                    self.Tappen.setText(text)
                    
                def q25Changed(self,text):
                    self.Snube_draaien.setText(text)
                    
                def q26Changed(self,text):
                    self.Nube_draaien.setText(text)
                    
                def q27Changed(self,text):
                    self.Snube_bewerken.setText(text)
                    
                def q28Changed(self,text):
                    self.Nube_bewerken.setText(text)
                    
                def q29Changed(self,text):
                    self.Sknippen.setText(text)
                    
                def q30Changed(self,text):
                    self.Knippen.setText(text)
                    
                def q31Changed(self,text):
                    self.Skanten.setText(text)
               
                def q32Changed(self,text):
                    self.Kanten.setText(text)
                    
                def q33Changed(self,text):
                    self.Sstansen.setText(text)
                                     
                def q34Changed(self,text):
                    self.Stansen.setText(text)   
                    
                def q35Changed(self,text):
                    self.Slassen_CO2.setText(text)

                def q36Changed(self,text):
                    self.Lassen_CO2.setText(text) 

                def q37Changed(self,text):
                    self.Slassen_hand.setText(text)

                def q38Changed(self,text):
                    self.Lassen_hand.setText(text)  

                def q39Changed(self,text):
                    self.Sverpakken.setText(text)  

                def q40Changed(self,text):
                    self.Verpakken.setText(text)  

                def q41Changed(self,text):
                    self.Sverzinken.setText(text)  

                def q42Changed(self,text):
                    self.Verzinken.setText(text)  

                def q43Changed(self,text):
                    self.Smoffelen.setText(text)  

                def q44Changed(self,text):
                    self.Moffelen.setText(text)  

                def q45Changed(self,text):
                    self.Sschilderen.setText(text)  

                def q46Changed(self,text):
                    self.Schilderen.setText(text)  

                def q47Changed(self,text):
                    self.Sspuiten.setText(text) 

                def q48Changed(self,text):
                    self.Spuiten.setText(text) 

                def q49Changed(self,text):
                    self.Sponsen.setText(text) 

                def q50Changed(self,text):
                    self.Ponsen.setText(text) 

                def q51Changed(self,text):
                    self.Spersen.setText(text) 

                def q52Changed(self,text):
                    self.Persen.setText(text) 

                def q53Changed(self,text):
                    self.Sgritstralen.setText(text) 

                def q54Changed(self,text):
                    self.Gritstralen.setText(text)  

                def q55Changed(self,text):
                    self.Smontage.setText(text)  

                def q56Changed(self,text):
                    self.Montage.setText(text)                                
             
                def returnq1(self):
                    return self.Omschrijving.text()
                
                def returnq2(self):
                    return self.Prijs.text()
                
                def returnq3(self):
                    return self.Eenheid.text()
                
                def returnq4(self):
                    return self.Materialen.text()
            
                def returnq5(self):
                    return self.Lonen.text()
            
                def returnq6(self):
                    return self.Diensten.text()
                
                def returnq7(self):
                    return self.Materiëel.text()
                      
                def returnq8(self):
                    return self.Inhuur.text()
                
                def returnq9(self):
                    return self.Szagen.text()
                
                def returnq10(self):
                    return self.Zagen.text()
                
                def returnq11(self):
                    return self.Sschaven.text()
                
                def returnq12(self):
                    return self.Schaven.text()
                
                def returnq13(self):
                    return self.Ssteken.text()
                
                def returnq14(self):
                    return self.Steken.text()
                
                def returnq15(self):
                    return self.Sboren.text()
                
                def returnq16(self):
                    return self.Boren.text()
                
                def returnq17(self):
                    return self.Sfrezen.text()
                
                def returnq18(self):
                    return self.Frezen.text()
                
                def returnq19(self):
                    return self.Sdraaien_klein.text()
                
                def returnq20(self):
                    return self.Draaien_klein.text()
                
                def returnq21(self):
                    return self.Sdraaien_groot.text()
                
                def returnq22(self):
                    return self.Draaien_groot.text()
                
                def returnq23(self):
                    return self.Stappen.text()
              
                def returnq24(self):
                    return self.Tappen.text()
                
                def returnq25(self):
                    return self.Snube_draaien.text()
                
                def returnq26(self):
                    return self.Nube_draaien.text()
              
                def returnq27(self):
                    return self.Snube_bewerken.text()
                
                def returnq28(self):
                    return self.Nube_bewerken.text()
                
                def returnq29(self):
                    return self.Sknippen.text()
        
                def returnq30(self):
                    return self.Knippen.text()
                
                def returnq31(self):
                    return self.Skanten.text()
                
                def returnq32(self):
                    return self.Kanten.text()
                
                def returnq33(self):
                    return self.Sstansen.text()
                
                def returnq34(self):
                    return self.Stansen.text()
                
                def returnq35(self):
                    return self.Slassen_CO2.text()
                
                def returnq36(self):
                    return self.Lassen_CO2.text()
                
                def returnq37(self):
                    return self.Slassen_hand.text()
                
                def returnq38(self):
                    return self.Lassen_hand.text()
                
                def returnq39(self):
                    return self.Sverpakken.text()
                
                def returnq40(self):
                    return self.Verpakken.text()
                
                def returnq41(self):
                    return self.Sverzinken.text()
                
                def returnq42(self):
                    return self.Verzinken.text()
                
                def returnq43(self):
                    return self.Smoffelen.text()
                
                def returnq44(self):
                    return self.Moffelen.text()
                
                def returnq45(self):
                    return self.Sschilderen.text()
                
                def returnq46(self):
                    return self.Schilderen.text()
                
                def returnq47(self):
                    return self.Sspuiten.text()
                
                def returnq48(self):
                    return self.Spuiten.text()
                
                def returnq49(self):
                    return self.Sponsen.text()
                
                def returnq50(self):
                    return self.Ponsen.text()
                
                def returnq51(self):
                    return self.Spersen.text()
                
                def returnq52(self):
                    return self.Persen.text()
                
                def returnq53(self):
                    return self.Sgritstralen.text()
                
                def returnq54(self):
                    return self.Gritstralen.text()
                
                def returnq55(self):
                    return self.Smontage.text()
                
                def returnq56(self):
                    return self.Montage.text()
                                              
                @staticmethod
                def getData(parent=None):
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                            dialog.returnq4(), dialog.returnq5(), dialog.returnq6(),\
                            dialog.returnq7(), dialog.returnq8(), dialog.returnq9(),\
                            dialog.returnq10(), dialog.returnq11(), dialog.returnq12(),\
                            dialog.returnq13(), dialog.returnq14(), dialog.returnq15(),\
                            dialog.returnq16(), dialog.returnq17(), dialog.returnq18(),\
                            dialog.returnq19(), dialog.returnq20(), dialog.returnq21(),\
                            dialog.returnq22(), dialog.returnq23(), dialog.returnq24(),\
                            dialog.returnq25(), dialog.returnq26(), dialog.returnq27(),\
                            dialog.returnq28(), dialog.returnq29(), dialog.returnq30(),\
                            dialog.returnq31(), dialog.returnq32(), dialog.returnq33(),\
                            dialog.returnq34(), dialog.returnq35(), dialog.returnq36(),\
                            dialog.returnq37(), dialog.returnq38(), dialog.returnq39(),\
                            dialog.returnq40(), dialog.returnq41(), dialog.returnq42(),\
                            dialog.returnq43(), dialog.returnq44(), dialog.returnq45(),\
                            dialog.returnq46(), dialog.returnq47(), dialog.returnq48(),\
                            dialog.returnq49(), dialog.returnq50(), dialog.returnq51(),\
                            dialog.returnq52(), dialog.returnq53(), dialog.returnq54(),\
                            dialog.returnq55(), dialog.returnq56()]
                            
            mainWin = MainWindow()
            data = mainWin.getData()
            
            chflag = 0
            for k in range(0, 56):
                if data[k]:
                    chflag = 1
            if chflag == 0:
                return
            if data[0]:
                ms0 = str(data[0])
            else:
                ms0 = rpsel[1]
            if data[2]:
                mf2 = data[2]
            else:
                mf2= rpsel[3]  
            if data[3]:
                mf3 = float(data[3])
            else:
                mf3= rpsel[4]
            if data[5]:
                mf5 = float(data[5])
            else:
                mf5= rpsel[6]
            if data[8]:
                mf8 = float(data[8])
            else:
                mf8 = rpsel[9]
            if data[9]:
                mf9 = float(data[9])
            else:
                mf9= rpsel[10]
            if data[10]:
                mf10 = float(data[10])
            else:
                mf10= rpsel[11]     
            if data[11]:
                mf11 = float(data[11])
            else:
                mf11= rpsel[12]     
            if data[12]:
                mf12 = float(data[12])
            else:
                mf12= rpsel[13]
            if data[13]:
                mf13 = float(data[13])
            else:
                mf13= rpsel[14]
            if data[14]:
                mf14 = float(data[14])
            else:
                mf14= rpsel[15]
            if data[15]:
                mf15 = float(data[15])
            else:
                mf15= rpsel[16]
            if data[16]:
                mf16 = float(data[16])
            else:
                mf16= rpsel[17]
            if data[17]:
                mf17 = float(data[17])
            else:
                mf17 = rpsel[18]
            if data[18]:
                mf18 = float(data[18])
            else:
                mf18= rpsel[19]
            if data[19]:
                mf19 = float(data[19])
            else:
                mf19= rpsel[20]
            if data[20]:
                mf20 = float(data[20])
            else:
                mf20= rpsel[21]
            if data[21]:
                mf21 = float(data[21])
            else:
                mf21= rpsel[22]
            if data[22]:
                mf22 = data[22]
            else:
                mf22= rpsel[23]
            if data[23]:
                mf23 = float(data[23])
            else:
                mf23= rpsel[24]
            if data[24]:
                mf24 = float(data[24])
            else:
                mf24 = rpsel[25]
            if data[25]:
                mf25 = float(data[25])
            else:
                mf25 = rpsel[26]
            if data[26]:
                mf26 = float(data[26])
            else:
                mf26 = rpsel[27]
            if data[27]:
                mf27 = float(data[27])
            else:
                mf27 = rpsel[28]
            if data[28]:
                mf28 = float(data[28])
            else:
                mf28 = rpsel[29]
            if data[29]:
                mf29 = float(data[29])
            else:
                mf29 = rpsel[30]
            if data[30]:
                mf30 = float(data[30])
            else:
                mf30 = rpsel[31]
            if data[31]:
                mf31 = float(data[31])
            else:
                mf31 = rpsel[32]
            if data[32]:
                mf32 = float(data[32])
            else:
                mf32 = rpsel[33]
            if data[33]:
                mf33 = float(data[33])
            else:
                mf33 = rpsel[34]
            if data[34]:
                mf34 = float(data[34])
            else:
                mf34 = rpsel[35]
            if data[35]:
                mf35 = float(data[35])
            else:
                mf35 = rpsel[36]
            if data[36]:
                mf36 = float(data[36])
            else:
                mf36 = rpsel[37]
            if data[37]:
                mf37 = float(data[37])
            else:
                mf37 = rpsel[38]
            if data[38]:
                mf38 = float(data[38])
            else:
                mf38 = rpsel[39]
            if data[39]:
                mf39 = float(data[39])
            else:
                mf39 = rpsel[40]    
            if data[40]:
                mf40 = float(data[40])
            else:
                mf40 = rpsel[41]
            if data[41]:
                mf41 = float(data[41])
            else:
                mf41 = rpsel[42]
            if data[42]:
                mf42 = float(data[42])
            else:
                mf42 = rpsel[43]
            if data[43]:
                mf43 = float(data[43])
            else:
                mf43 = rpsel[44]
            if data[44]:
                mf44 = float(data[44])
            else:
                mf44 = rpsel[45]
            if data[45]:
                mf45 = float(data[45])
            else:
                mf45 = rpsel[46]
            if data[46]:
                mf46 = float(data[46])
            else:
                mf46 = rpsel[47]
            if data[47]:
                mf47 = float(data[47])
            else:
                mf47 = rpsel[48]
            if data[48]:
                mf48 = float(data[48])
            else:
                mf48 = rpsel[49]
            if data[49]:
                mf49 = float(data[49])
            else:
                mf49 = rpsel[50]
            if data[50]:
                mf50 = float(data[50])
            else:
                mf50 = rpsel[51]
            if data[51]:
                mf51 = float(data[51])
            else:
                mf51 = rpsel[52]
            if data[52]:
                mf52 = float(data[52])
            else:
                mf52 = rpsel[53]
            if data[53]:
                mf53 = float(data[53])
            else:
                mf53 = rpsel[54]
            if data[54]:
                mf54 = float(data[54])
            else:
                mf54 = rpsel[55]
            if data[55]:
                mf55 = float(data[55])
            else:
                mf55 = rpsel[56]
                
            metadata = MetaData()       
            params = Table('params', metadata,
                Column('paramID', Integer, primary_key=True),
                Column('tarief', Float),
                Column('item', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
                                                                 
            upd = update(iclusters).where(iclusters.c.iclusterID == clusternr).values(\
                omschrijving=ms0, eenheid=mf2, materialen=mf3, diensten = mf5,\
                szagen=mf8,zagen=mf9,sschaven=mf10,schaven=mf11,ssteken=mf12,steken=mf13,\
                sboren=mf14,boren=mf15,sfrezen=mf16,frezen=mf17,sdraaien_klein=mf18,\
                draaien_klein=mf19,sdraaien_groot=mf20,draaien_groot=mf21,stappen=mf22,\
                tappen=mf23,snube_draaien=mf24,nube_draaien=mf25,snube_bewerken=mf26,\
                nube_bewerken=mf27,sknippen=mf28,knippen=mf29,skanten=mf30,kanten=mf31,\
                sstansen=mf32,stansen=mf33,slassen_co2=mf34,lassen_co2=mf35,\
                slassen_hand=mf36,lassen_hand=mf37,sverpakken=mf38,verpakken=mf39,\
                sverzinken=mf40,verzinken=mf41,smoffelen=mf42,moffelen=mf43,sschilderen=mf44,\
                schilderen=mf45,sspuiten=mf46,spuiten=mf47,sponsen=mf48,ponsen=mf49,\
                spersen=mf50,persen=mf51,sgritstralen=mf52,gritstralen=mf53,smontage=mf54,\
                montage=mf55)
            con.execute(upd)
            upd1 = update(iclusters).where(iclusters.c.iclusterID == clusternr).values(\
                lonen=iclusters.c.zagen*rppar[72][1]+iclusters.c.szagen*rppar[72][1]/50\
                +iclusters.c.schaven*rppar[73][1]+iclusters.c.sschaven*rppar[73][1]/50\
                +iclusters.c.steken*rppar[74][1]+iclusters.c.ssteken*rppar[74][1]/50\
                +iclusters.c.boren*rppar[75][1]+iclusters.c.sboren*rppar[75][1]/50\
                +iclusters.c.frezen*rppar[76][1]+iclusters.c.sfrezen*rppar[76][1]/50\
                +iclusters.c.draaien_klein*rppar[77][1]+iclusters.c.sdraaien_klein*rppar[77][1]/50\
                +iclusters.c.draaien_groot*rppar[78][1]+iclusters.c.sdraaien_groot*rppar[78][1]/50\
                +iclusters.c.tappen*rppar[79][1]+iclusters.c.stappen*rppar[79][1]/50\
                +iclusters.c.nube_draaien*rppar[80][1]+iclusters.c.snube_draaien*rppar[80][1]/50\
                +iclusters.c.nube_bewerken*rppar[81][1]+iclusters.c.snube_bewerken*rppar[81][1]/50\
                +iclusters.c.knippen*rppar[82][1]+iclusters.c.sknippen*rppar[82][1]/50\
                +iclusters.c.kanten*rppar[83][1]+iclusters.c.skanten*rppar[83][1]/50\
                +iclusters.c.stansen*rppar[84][1]+iclusters.c.sstansen*rppar[84][1]/50\
                +iclusters.c.lassen_co2*rppar[85][1]+iclusters.c.slassen_co2*rppar[85][1]/50\
                +iclusters.c.lassen_hand*rppar[86][1]+iclusters.c.slassen_hand*rppar[86][1]/50\
                +iclusters.c.verpakken*rppar[87][1]+iclusters.c.sverpakken*rppar[86][1]/50\
                +iclusters.c.verzinken*rppar[88][1]+iclusters.c.sverzinken*rppar[88][1]/50\
                +iclusters.c.moffelen*rppar[89][1]+iclusters.c.smoffelen*rppar[89][1]/50\
                +iclusters.c.schilderen*rppar[90][1]+iclusters.c.sschilderen*rppar[90][1]/50\
                +iclusters.c.spuiten*rppar[91][1]+iclusters.c.spuiten*rppar[91][1]/50\
                +iclusters.c.ponsen*rppar[92][1]+iclusters.c.sponsen*rppar[92][1]/50\
                +iclusters.c.persen*rppar[93][1]+iclusters.c.spersen*rppar[93][1]/50\
                +iclusters.c.gritstralen*rppar[94][1]+iclusters.c.sgritstralen*rppar[94][1]/50\
                +iclusters.c.montage*rppar[95][1]+iclusters.c.smontage*rppar[95][1]/50)
            con.execute(upd1)
            upd3 = update(iclusters).where(iclusters.c.iclusterID == clusternr).values(\
                         prijs = mf3+mf5+iclusters.c.lonen+iclusters.c.materieel+iclusters.c.inhuur)
            con.execute(upd3)
            invoerOK()
     
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)