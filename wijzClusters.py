from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QDialog, QLabel,\
       QGridLayout, QPushButton, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData,\
                         create_engine, select, update)

def refresh(keuze, m_email, self):
    self.close()
    toonClusters(keuze, m_email)
    
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Your data have been adjusted!')
    msg.setWindowTitle('Modify clusters')
    msg.exec_()

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Modify clusters')
    msg.exec_()
    
def calcBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Calculation line already exists\nen is settled with\nentered quantity!')
    msg.setWindowTitle('Modify clusters')
    msg.exec_()   

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No cluster found\ncreate another selection\nof create a new cluster please!')
    msg.setFont(QFont("Arial",10))
    msg.setWindowTitle('Modify clusters')
    msg.exec_() 
    
def ongKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Invalid choice!')
    msg.setWindowTitle('Modify clusters')
    msg.exec_() 
                
def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster selektion")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                              
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
                        
            grid.addWidget(k0Edit, 1, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 2, 1, 1, 1,Qt.AlignCenter)
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
    toonClusters(keuze, m_email)  
  
def toonClusters(keuze, m_email):              
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Cluster Calculation')
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
            
            freshBtn = QPushButton('Refresh')
            freshBtn.clicked.connect(lambda: refresh(keuze, m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 14, 1, 1, Qt.AlignRight)
        
            sluitBtn = QPushButton('Close')
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
             
    header = ['Cluster number', 'Description', 'Price', 'Unit', 'Materials', 'Wages',\
              'Services', 'Equipment', 'Hiring', 'hours\nconstruction', 'hours mounting','hours\nreturn welding',\
              'hours\nchief mechanic', 'hours\npower-supply', 'hours\nOCL', 'hours\ntrack laying', 'hours\ntrack welding',\
              'hours\nhiring', 'Trencher', 'Press machine', 'Atlas crane',\
              'Crane big', 'Mainliner', 'Ballast scrape\nmachine', 'Wagon', 'Locomotor',\
              'Locomotive', 'Assembly\ntrolley', 'Stormobiel', 'hours\ntelecom', 'Robel train',\
              'Direction', 'Housing', 'Cable work', 'Earth moving', 'Concrete work', 'Transport', 'Remaining']
    
    metadata = MetaData()
    clusters = Table('clusters', metadata,
        Column('clusterID', String, primary_key=True),
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
        Column('uren_telecom', Float),
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
        
    sel = select([clusters]).where(clusters.c.clusterID.ilike(keuze+'%'))\
                              .order_by(clusters.c.clusterID)

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
            selcl = select([clusters]).where(clusters.c.clusterID == clusternr)
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
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.textChanged.connect(self.q1Changed) 
                    reg_ex = QRegExp("^.{0,49}$")
                    input_validator = QRegExpValidator(reg_ex, q1Edit)
                    q1Edit.setValidator(input_validator)
                                    
                    self.Prijs = QLabel()
                    q2Edit = QLineEdit(('{:12.2f}'.format(rpsel[2])))
                    q2Edit.setFixedWidth(150)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setDisabled(True)
                     
                    self.Eenheid = QLabel()
                    q3Edit = QLineEdit(str(rpsel[3]))
                    q3Edit.setFixedWidth(150)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.textChanged.connect(self.q3Changed) 
                    reg_ex = QRegExp("^.{0,10}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                    
                    self.Materialen = QLabel()
                    q4Edit = QLineEdit('{:12.2f}'.format(rpsel[4]))
                    q4Edit.setFixedWidth(150)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setDisabled(True)
                    
                    self.Lonen = QLabel()
                    q5Edit = QLineEdit('{:12.2f}'.format(rpsel[5]))
                    q5Edit.setFixedWidth(150)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setDisabled(True)
                    
                    self.Diensten = QLabel()
                    q6Edit = QLineEdit('{:12.2f}'.format(rpsel[6]))
                    q6Edit.setFixedWidth(150)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    self.Materiëel = QLabel()
                    q7Edit = QLineEdit('{:12.2f}'.format(rpsel[7]))
                    q7Edit.setFixedWidth(150)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setValidator(input_validator)
                    q7Edit.setDisabled(True)
                    
                    self.Inhuur = QLabel()
                    q8Edit = QLineEdit('{:12.2f}'.format(rpsel[8]))
                    q8Edit.setFixedWidth(150)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setDisabled(True)
                                   
                    self.Construktieuren = QLabel()
                    q9Edit = QLineEdit(str(round(float(rpsel[9]),2)))
                    q9Edit.setFixedWidth(150)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.textChanged.connect(self.q9Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q9Edit)
                    q9Edit.setValidator(input_validator)
                    
                    self.Montageuren = QLabel()
                    q10Edit = QLineEdit(str(round(float(rpsel[10]),2)))
                    q10Edit.setFixedWidth(150)
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setFont(QFont("Arial",10))
                    q10Edit.textChanged.connect(self.q10Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q10Edit)
                    q10Edit.setValidator(input_validator)
                    
                    self.Retourlasuren = QLabel()
                    q11Edit = QLineEdit(str(round(float(rpsel[11]),2)))
                    q11Edit.setFixedWidth(150)
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.textChanged.connect(self.q11Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q11Edit)
                    q11Edit.setValidator(input_validator)
                    
                    self.BFIuren = QLabel()
                    q12Edit = QLineEdit(str(round(float(rpsel[12]),2)))
                    q12Edit.setFixedWidth(150)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.textChanged.connect(self.q12Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q12Edit)
                    q12Edit.setValidator(input_validator)
                    
                    self.Telecomuren = QLabel()
                    q29Edit = QLineEdit(str(round(float(rpsel[29]),2)))
                    q29Edit.setFixedWidth(150)
                    q29Edit.setAlignment(Qt.AlignRight)
                    q29Edit.setFont(QFont("Arial",10))
                    q29Edit.textChanged.connect(self.q29Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q29Edit)
                    q29Edit.setValidator(input_validator)      
                         
                    self.Voedinguren = QLabel()
                    q13Edit = QLineEdit(str(round(float(rpsel[13]),2)))
                    q13Edit.setFixedWidth(150)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.textChanged.connect(self.q13Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q13Edit)
                    q13Edit.setValidator(input_validator)
                    
                    self.Bvluren = QLabel()
                    q14Edit = QLineEdit(str(round(float(rpsel[14]),2)))
                    q14Edit.setFixedWidth(150)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.textChanged.connect(self.q14Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q14Edit)
                    q14Edit.setValidator(input_validator)
                       
                    self.Spoorleguren = QLabel()
                    q15Edit = QLineEdit(str(round(float(rpsel[15]),2)))
                    q15Edit.setFixedWidth(150)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setFont(QFont("Arial",10))
                    q15Edit.textChanged.connect(self.q15Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q15Edit)
                    q15Edit.setValidator(input_validator)
                    
                    self.Spoorlasuren = QLabel()
                    q16Edit = QLineEdit(str(round(float(rpsel[16]),2)))
                    q16Edit.setFixedWidth(150)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.textChanged.connect(self.q16Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q16Edit)
                    q16Edit.setValidator(input_validator)
                    
                    self.Inhuururen = QLabel()
                    q17Edit = QLineEdit(str(round(float(rpsel[17]),2)))
                    q17Edit.setFixedWidth(150)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setFont(QFont("Arial",10))
                    q17Edit.textChanged.connect(self.q17Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q17Edit)
                    q17Edit.setValidator(input_validator)
                       
                    self.Sleuvengraver = QLabel()
                    q18Edit = QLineEdit(str(round(float(rpsel[18]),2)))
                    q18Edit.setFixedWidth(150)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setFont(QFont("Arial",10))
                    q18Edit.textChanged.connect(self.q18Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q18Edit)
                    q18Edit.setValidator(input_validator)
                            
                    self.Persapparaat = QLabel()
                    q19Edit = QLineEdit(str(round(float(rpsel[19]),2)))
                    q19Edit.setFixedWidth(150)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setFont(QFont("Arial",10))
                    q19Edit.textChanged.connect(self.q19Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q19Edit)
                    q19Edit.setValidator(input_validator)
                    
                    self.Atlaskraan = QLabel()
                    q20Edit = QLineEdit(str(round(float(rpsel[20]),2)))
                    q20Edit.setFixedWidth(150)
                    q20Edit.setFont(QFont("Arial",10))
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.textChanged.connect(self.q20Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q20Edit)
                    q20Edit.setValidator(input_validator)
                    
                    self.Kraan_groot = QLabel()
                    q21Edit = QLineEdit(str(round(float(rpsel[21]),2)))
                    q21Edit.setFixedWidth(150)
                    q21Edit.setFont(QFont("Arial",10))
                    q21Edit.setAlignment(Qt.AlignRight)
                    q21Edit.textChanged.connect(self.q21Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q21Edit)
                    q21Edit.setValidator(input_validator)
                    
                    self.Mainliner = QLabel()
                    q22Edit = QLineEdit(str(round(float(rpsel[22]),2)))
                    q22Edit.setFixedWidth(150)
                    q22Edit.setFont(QFont("Arial",10))
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.textChanged.connect(self.q22Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q22Edit)
                    q22Edit.setValidator(input_validator)
                    
                    self.Hormachine = QLabel()
                    q23Edit = QLineEdit(str(round(float(rpsel[23]),2)))
                    q23Edit.setFixedWidth(150)
                    q23Edit.setAlignment(Qt.AlignRight)
                    q23Edit.setFont(QFont("Arial",10))
                    q23Edit.textChanged.connect(self.q23Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q23Edit)
                    q23Edit.setValidator(input_validator)
                    
                    self.Wagon = QLabel()
                    q24Edit = QLineEdit(str(round(float(rpsel[24]),2)))
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setFixedWidth(150)
                    q24Edit.setFont(QFont("Arial",10))
                    q24Edit.textChanged.connect(self.q24Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q24Edit)
                    q24Edit.setValidator(input_validator)
                    
                    self.Locomotor = QLabel()
                    q25Edit = QLineEdit(str(round(float(rpsel[25]),2)))
                    q25Edit.setFixedWidth(150)
                    q25Edit.setAlignment(Qt.AlignRight)
                    q25Edit.setFont(QFont("Arial",10))
                    q25Edit.textChanged.connect(self.q25Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q25Edit)
                    q25Edit.setValidator(input_validator)
        
                    self.Locomotief = QLabel()
                    q26Edit = QLineEdit(str(round(float(rpsel[26]),2)))
                    q26Edit.setFixedWidth(150)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setFont(QFont("Arial",10))
                    q26Edit.textChanged.connect(self.q26Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q26Edit)
                    q26Edit.setValidator(input_validator)
                    
                    self.Stormobiel = QLabel()
                    q27Edit = QLineEdit(str(round(float(rpsel[27]),2)))
                    q27Edit.setFixedWidth(150)
                    q27Edit.setAlignment(Qt.AlignRight)
                    q27Edit.setFont(QFont("Arial",10))
                    q27Edit.textChanged.connect(self.q27Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q27Edit)
                    q27Edit.setValidator(input_validator)
                    
                    self.Montagewagen = QLabel()
                    q28Edit = QLineEdit(str(round(float(rpsel[28]),2)))
                    q28Edit.setFixedWidth(150)
                    q28Edit.setAlignment(Qt.AlignRight)
                    q28Edit.setFont(QFont("Arial",10))
                    q28Edit.textChanged.connect(self.q28Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q28Edit)
                    q28Edit.setValidator(input_validator)
                    
                    self.Robeltrein = QLabel()
                    q30Edit = QLineEdit(str(round(float(rpsel[30]),2)))
                    q30Edit.setFixedWidth(150)
                    q30Edit.setFont(QFont("Arial",10))
                    q30Edit.setAlignment(Qt.AlignRight)
                    q30Edit.textChanged.connect(self.q30Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q30Edit)
                    q30Edit.setValidator(input_validator)
                    
                    self.Leiding = QLabel()
                    q31Edit = QLineEdit(str(round(float(rpsel[31]),2)))
                    q31Edit.setFixedWidth(150)
                    q31Edit.setFont(QFont("Arial",10))
                    q31Edit.setAlignment(Qt.AlignRight)
                    q31Edit.textChanged.connect(self.q31Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q31Edit)
                    q31Edit.setValidator(input_validator)
                    
                    self.Huisvesting = QLabel()
                    q32Edit = QLineEdit(str(round(float(rpsel[32]),2)))
                    q32Edit.setFixedWidth(150)
                    q32Edit.setFont(QFont("Arial",10))
                    q32Edit.setAlignment(Qt.AlignRight)
                    q32Edit.textChanged.connect(self.q32Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q32Edit)
                    q32Edit.setValidator(input_validator)
                                    
                    self.Kabelwerk = QLabel()
                    q33Edit = QLineEdit(str(round(float(rpsel[33]),2)))
                    q33Edit.setFixedWidth(150)
                    q33Edit.setFont(QFont("Arial",10))
                    q33Edit.setAlignment(Qt.AlignRight)
                    q33Edit.textChanged.connect(self.q33Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q33Edit)
                    q33Edit.setValidator(input_validator)
                    
                    self.Grondverzet = QLabel()
                    q34Edit = QLineEdit(str(round(float(rpsel[34]),2)))
                    q34Edit.setFixedWidth(150)
                    q34Edit.setFont(QFont("Arial",10))
                    q34Edit.setAlignment(Qt.AlignRight)
                    q34Edit.textChanged.connect(self.q34Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q34Edit)
                    q34Edit.setValidator(input_validator)
                    
                    self.Betonwerk = QLabel()
                    q35Edit = QLineEdit(str(round(float(rpsel[35]),2)))
                    q35Edit.setFixedWidth(150)
                    q35Edit.setFont(QFont("Arial",10))
                    q35Edit.setAlignment(Qt.AlignRight)
                    q35Edit.textChanged.connect(self.q35Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q35Edit)
                    q35Edit.setValidator(input_validator)
                    
                    self.Vervoer = QLabel()
                    q36Edit = QLineEdit(str(round(float(rpsel[36]),2)))
                    q36Edit.setFixedWidth(150)
                    q36Edit.setFont(QFont("Arial",10))
                    q36Edit.setAlignment(Qt.AlignRight)
                    q36Edit.textChanged.connect(self.q36Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q36Edit)
                    q36Edit.setValidator(input_validator)
                    
                    self.Overig = QLabel()
                    q37Edit = QLineEdit(str(round(float(rpsel[37]),2)))
                    q37Edit.setFixedWidth(150)
                    q37Edit.setFont(QFont("Arial",10))
                    q37Edit.setAlignment(Qt.AlignRight)
                    q37Edit.textChanged.connect(self.q37Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q37Edit)
                    q37Edit.setValidator(input_validator)
                    
                    grid = QGridLayout()
                    grid.setSpacing(10)
                    
                    lbl1 = QLabel('Cluster number')
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(clusternr)
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Description')
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q1Edit, 2, 1, 1, 3) # RowSpan 1 ,ColumnSpan 3
                                                         
                    lbl4 = QLabel('Price')
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q2Edit, 3, 1)
                    
                    lbl5 = QLabel('Unit')
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q3Edit, 4, 1)
                    
                    lbl6 = QLabel('Materials')
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q4Edit, 5, 1)
                    
                    lbl7 = QLabel('Wages')
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q5Edit, 6, 1)
                    
                    lbl8 = QLabel('Services')
                    lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl8, 7, 0)
                    grid.addWidget(q6Edit, 7, 1)
                    
                    lbl9 = QLabel('Equipment')
                    lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl9, 8, 0)
                    grid.addWidget(q7Edit, 8, 1)
                    
                    lbl10 = QLabel('Hiring')
                    lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl10, 9, 0)
                    grid.addWidget(q8Edit, 9, 1)
                    
                    lbl20 = QLabel('Trenching hours')
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 10, 0)
                    grid.addWidget(q18Edit, 10, 1)
                      
                    lbl21 = QLabel('Pressing machine hours')
                    lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl21, 11, 0)
                    grid.addWidget(q19Edit, 11, 1)
                    
                    lbl22 = QLabel('Atlas crane hours')
                    lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl22, 12, 0)
                    grid.addWidget(q20Edit, 12, 1)
                    
                    lbl23 = QLabel('Crane big hours')
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 13, 0)
                    grid.addWidget(q21Edit, 13, 1)
                    
                    lbl24 = QLabel('Mainliner hours')
                    lbl24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl24, 14, 0)
                    grid.addWidget(q22Edit, 14, 1)
                    
                    lbl25 = QLabel('Ballast clearing hours')
                    lbl25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl25, 15, 0)
                    grid.addWidget(q23Edit, 15, 1)
                    
                    lbl26 = QLabel('Wagon hours')
                    lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl26, 16, 0)
                    grid.addWidget(q24Edit, 16, 1)
                    
                    lbl27 = QLabel('Locomotor hours')
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 3, 2)
                    grid.addWidget(q25Edit, 3, 3)
                    
                    lbl28 = QLabel('Locomotive hours')
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 4, 2)
                    grid.addWidget(q26Edit, 4, 3)
                    
                    lbl29 = QLabel('Stormobiel hours')
                    lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl29, 5, 2)
                    grid.addWidget(q27Edit, 5, 3)
                    
                    lbl30 = QLabel('Assembly trolley hours')
                    lbl30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl30, 6, 2)
                    grid.addWidget(q28Edit, 6, 3)
                    
                    lbl31 = QLabel('Robel train hours')
                    lbl31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl31, 7, 2)
                    grid.addWidget(q30Edit, 7, 3)
                    
                    lbl19 = QLabel('Hiring hours')
                    lbl19.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl19, 8, 2)
                    grid.addWidget(q17Edit, 8, 3)      
                    
                    lbl11 = QLabel('Construction hours')
                    lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl11, 9, 2)
                    grid.addWidget(q9Edit, 9, 3)
                        
                    lbl12 = QLabel('Mounting hours')
                    lbl12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl12, 10, 2)
                    grid.addWidget(q10Edit, 10, 3)
                    
                    lbl13 = QLabel('Return welding hours')
                    lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl13, 11, 2)
                    grid.addWidget(q11Edit, 11, 3)
                    
                    lbl14 = QLabel('Chief mechanic hours')
                    lbl14.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl14, 12, 2)
                    grid.addWidget(q12Edit, 12, 3)
                    
                    lbl19 = QLabel('Telecom hours')
                    lbl19.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl19, 13, 2)
                    grid.addWidget(q29Edit, 13, 3)
                                                              
                    lbl15 = QLabel('Power-supply hours')
                    lbl15.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl15, 14, 2)
                    grid.addWidget(q13Edit, 14, 3)
                 
                    lbl16 = QLabel('OCL hours')
                    lbl16.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl16, 15, 2)
                    grid.addWidget(q14Edit, 15, 3)
                    
                    lbl17 = QLabel('Track laying hours')
                    lbl17.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl17, 16, 2)
                    grid.addWidget(q15Edit, 16, 3)
                    
                    lbl18 = QLabel('Track welding hours')
                    lbl18.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl18, 17, 2)
                    grid.addWidget(q16Edit, 17, 3)
                    
                    lbl32 = QLabel('Direction')
                    lbl32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl32, 17, 0)
                    grid.addWidget(q31Edit, 17, 1)
                    
                    lbl33 = QLabel('Housing')
                    lbl33.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl33, 18, 0)
                    grid.addWidget(q32Edit, 18, 1)
                    
                    lbl34 = QLabel('Cable work')
                    lbl34.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl34, 18, 2)
                    grid.addWidget(q33Edit, 18, 3)
                    
                    lbl35 = QLabel('Earth moving')
                    lbl35.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl35, 19, 0)
                    grid.addWidget(q34Edit, 19, 1)
                    
                    lbl36 = QLabel('Concrete work')
                    lbl36.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl36, 19, 2)
                    grid.addWidget(q35Edit, 19, 3)
                
                    lbl37 = QLabel('Transport')
                    lbl37.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl37, 20, 0)
                    grid.addWidget(q36Edit, 20, 1)
                    
                    lbl38 = QLabel('Remaining')
                    lbl38.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl38, 20, 2)
                    grid.addWidget(q37Edit, 20, 3)
          
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl, 0, 0, 1, 1, Qt.AlignRight)
                                     
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 3, 1 , 1, Qt.AlignRight)
                    
                    grid.addWidget(QLabel('Modify cluster'), 0, 1, 1, 2, Qt.AlignCenter)
                                                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 1, 1, 3)
                      
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 150, 150)
            
                    applyBtn = QPushButton('Modify')
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 21, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)
            
                    grid.addWidget(closeBtn, 21, 2, 1, 2, Qt.AlignCenter)
                    closeBtn.setFont(QFont("Arial",10))
                    closeBtn.setFixedWidth(100)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                             
                def q1Changed(self,text):
                    self.Omschrijving.setText(text)
            
                def q3Changed(self,text):
                    self.Eenheid.setText(text)
                             
                def q9Changed(self,text):
                    self.Construktieuren.setText(text)
                    
                def q10Changed(self,text):
                    self.Montageuren.setText(text)
                       
                def q11Changed(self,text):
                    self.Retourlasuren.setText(text)
                    
                def q12Changed(self,text):
                    self.BFIuren.setText(text)
                    
                def q13Changed(self,text):
                    self.Voedinguren.setText(text)
                    
                def q14Changed(self,text):
                    self.Bvluren.setText(text)
                    
                def q15Changed(self,text):
                    self.Spoorleguren.setText(text)
                    
                def q16Changed(self,text):
                    self.Spoorlasuren.setText(text)
                    
                def q17Changed(self,text):
                    self.Inhuururen.setText(text)
                    
                def q18Changed(self,text):
                    self.Sleuvengraver.setText(text)
                    
                def q19Changed(self,text):
                    self.Persapparaat.setText(text)
                    
                def q20Changed(self,text):
                    self.Atlaskraan.setText(text)
                    
                def q21Changed(self,text):
                    self.Kraan_groot.setText(text)
                    
                def q22Changed(self,text):
                    self.Mainliner.setText(text)
                    
                def q23Changed(self,text):
                    self.Hormachine.setText(text)
                    
                def q24Changed(self,text):
                    self.Wagon.setText(text)
                    
                def q25Changed(self,text):
                    self.Locomotor.setText(text)
                    
                def q26Changed(self,text):
                    self.Locomotief.setText(text)
                    
                def q27Changed(self,text):
                    self.Stormobiel.setText(text)
                    
                def q28Changed(self,text):
                    self.Montagewagen.setText(text)
                    
                def q29Changed(self,text):
                    self.Telecomuren.setText(text)
                    
                def q30Changed(self,text):
                    self.Robeltrein.setText(text)
               
                def q31Changed(self,text):
                    self.Leiding.setText(text)
                    
                def q32Changed(self,text):
                    self.Huisvesting.setText(text)
                    
                def q33Changed(self,text):
                    self.Kabelwerk.setText(text)
                    
                def q34Changed(self,text):
                    self.Grondverzet.setText(text)
                    
                def q35Changed(self,text):
                    self.Betonwerk.setText(text)
                    
                def q36Changed(self,text):
                    self.Vervoer.setText(text)
                    
                def q37Changed(self,text):
                    self.Overig.setText(text)
                             
                def returnq1(self):
                    return self.Omschrijving.text()
                                
                def returnq3(self):
                    return self.Eenheid.text()
                                
                def returnq9(self):
                    return self.Construktieuren.text()
                
                def returnq10(self):
                    return self.Montageuren.text()
                
                def returnq11(self):
                    return self.Retourlasuren.text()
                
                def returnq12(self):
                    return self.BFIuren.text()
                
                def returnq13(self):
                    return self.Voedinguren.text()
                
                def returnq14(self):
                    return self.Bvluren.text()
                
                def returnq15(self):
                    return self.Spoorleguren.text()
                
                def returnq16(self):
                    return self.Spoorlasuren.text()
                
                def returnq17(self):
                    return self.Inhuururen.text()
                
                def returnq18(self):
                    return self.Sleuvengraver.text()
                
                def returnq19(self):
                    return self.Persapparaat.text()
                
                def returnq20(self):
                    return self.Atlaskraan.text()
                
                def returnq21(self):
                    return self.Kraan_groot.text()
                
                def returnq22(self):
                    return self.Mainliner.text()
                
                def returnq23(self):
                    return self.Hormachine.text()
              
                def returnq24(self):
                    return self.Wagon.text()
                
                def returnq25(self):
                    return self.Locomotor.text()
                
                def returnq26(self):
                    return self.Locomotief.text()
              
                def returnq27(self):
                    return self.Stormobiel.text()
                
                def returnq28(self):
                    return self.Montagewagen.text()
                
                def returnq29(self):
                    return self.Telecomuren.text()
        
                def returnq30(self):
                    return self.Robeltrein.text()
                
                def returnq31(self):
                    return self.Leiding.text()
                
                def returnq32(self):
                    return self.Huisvesting.text()
                
                def returnq33(self):
                    return self.Kabelwerk.text()
                
                def returnq34(self):
                    return self.Grondverzet.text()
                
                def returnq35(self):
                    return self.Betonwerk.text()
                
                def returnq36(self):
                    return self.Vervoer.text()
                
                def returnq37(self):
                    return self.Overig.text()
                                       
                @staticmethod
                def getData(parent=None):
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returnq1(), dialog.returnq3(), dialog.returnq9(),\
                            dialog.returnq10(), dialog.returnq11(), dialog.returnq12(),\
                            dialog.returnq13(), dialog.returnq14(), dialog.returnq15(),\
                            dialog.returnq16(), dialog.returnq17(), dialog.returnq18(),\
                            dialog.returnq19(), dialog.returnq20(), dialog.returnq21(),\
                            dialog.returnq22(), dialog.returnq23(), dialog.returnq24(),\
                            dialog.returnq25(), dialog.returnq26(), dialog.returnq27(),\
                            dialog.returnq28(), dialog.returnq29(), dialog.returnq30(),\
                            dialog.returnq31(), dialog.returnq32(), dialog.returnq33(),\
                            dialog.returnq34(), dialog.returnq35(), dialog.returnq36(),\
                            dialog.returnq37()]  
                                       
            mainWin = MainWindow()
            data = mainWin.getData()
     
            chflag = 0
            for k in range(0,31):
                if data[k]:
                    chflag = 1
            if chflag == 0:
                return
            if data[0]:
                ms0 = str(data[0])
            else:
                ms0 = rpsel[1]
            if data[1]:
                mf1 = data[1]
            else:
                mf1 = rpsel[3]  
            if data[2]:
                mf2 = float(data[2])
            else:
                mf2= rpsel[9]
            if data[3]:
                mf3 = data[3]
            else:
                mf3 = rpsel[10]
            if data[4]:
                mf4 = float(data[4])
            else:
                mf4= rpsel[11]
            if data[5]:
                mf5 = float(data[5])
            else:
                mf5 = rpsel[12]
            if data[6]:
                mf6 = float(data[6])
            else:
                mf6 = rpsel[13]
            if data[7]:
                mf7 = float(data[7])
            else:
                mf7 = rpsel[14]
            if data[8]:
                mf8 = float(data[8])
            else:
                mf8= rpsel[15]
            if data[9]:
                mf9 = float(data[9])
            else:
                mf9= rpsel[16]
            if data[10]:
                mf10 = float(data[10])
            else:
                mf10= rpsel[17]     
            if data[11]:
                mf11 = float(data[11])
            else:
                mf11= rpsel[18]     
            if data[12]:
                mf12 = float(data[12])
            else:
                mf12= rpsel[19]
            if data[13]:
                mf13 = float(data[13])
            else:
                mf13= rpsel[20]
            if data[14]:
                mf14 = float(data[14])
            else:
                mf14= rpsel[21]
            if data[15]:
                mf15 = float(data[15])
            else:
                mf15= rpsel[22]
            if data[16]:
                mf16 = float(data[16])
            else:
                mf16= rpsel[23]
            if data[17]:
                mf17 = float(data[17])
            else:
                mf17 = rpsel[24]
            if data[18]:
                mf18 = float(data[18])
            else:
                mf18= rpsel[25]
            if data[19]:
                mf19 = float(data[19])
            else:
                mf19= rpsel[26]
            if data[20]:
                mf20 = float(data[20])
            else:
                mf20= rpsel[27]
            if data[21]:
                mf21 = float(data[21])
            else:
                mf21= rpsel[28]
            if data[22]:
                mf22 = data[22]
            else:
                mf22= rpsel[29]
            if data[23]:
                mf23 = float(data[23])
            else:
                mf23= rpsel[30]
            if data[24]:
                mf24 = float(data[24])
            else:
                mf24 = rpsel[31]
            if data[25]:
                mf25 = float(data[25])
            else:
                mf25 = rpsel[32]
            if data[26]:
                mf26 = float(data[26])
            else:
                mf26 = rpsel[33]
            if data[27]:
                mf27 = float(data[27])
            else:
                mf27 = rpsel[34]
            if data[28]:
                mf28 = float(data[28])
            else:
                mf28 = rpsel[35]
            if data[29]:
                mf29 = float(data[29])
            else:
                mf29 = rpsel[36]
            if data[30]:
                mf30 = float(data[30])
            else:
                mf30 = rpsel[37]
                   
            metadata = MetaData()
            params_hours = Table('params_hours', metadata,
                Column('rateID', Integer, primary_key=True),
                Column('hourly_tariff', Float),
                Column('item', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params_hours]).order_by(params_hours.c.rateID)
            rppar = con.execute(selpar).fetchall()

            metadata = MetaData()
            params_services = Table('params_services', metadata,
                                 Column('servicesID', Integer, primary_key=True),
                                 Column('hourly_tariff', Float),
                                 Column('item', String))

            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar1 = select([params_services]).order_by(params_services.c.servicesID)
            rppar1 = con.execute(selpar1).fetchall()

            upd1 = update(clusters).where(clusters.c.clusterID == clusternr).values(
                omschrijving=ms0, eenheid=mf1, uren_constr = mf2,\
                uren_mont=mf3, uren_retourlas=mf4, uren_bfi=mf5, uren_voeding=mf6,\
                uren_bvl=mf7, uren_spoorleg=mf8, uren_spoorlas=mf9, uren_inhuur=mf10,\
                sleuvengraver=mf11, persapparaat=mf12, atlaskraan=mf13, kraan_groot=mf14,\
                mainliner=mf15, hormachine=mf16, wagon=mf17,locomotor=mf18,locomotief=mf19,\
                montagewagen=mf20, stormobiel=mf21, uren_telecom=mf22, robeltrein=mf23,
                leiding=mf24, huisvesting=mf25, kabelwerk=mf26,grondverzet=mf27,\
                betonwerk=mf28,vervoer=mf29, overig=mf30)
            con.execute(upd1)
            upd2 = update(clusters).where(clusters.c.clusterID == clusternr).values(\
                lonen=clusters.c.uren_constr*rppar[1][1]+clusters.c.uren_mont*rppar[2][1]\
                 +clusters.c.uren_retourlas*rppar[8][1]+clusters.c.uren_bfi*rppar[3][1]\
                 +clusters.c.uren_voeding*rppar[4][1]+clusters.c.uren_bvl*rppar[5][1]\
                 +clusters.c.uren_spoorleg*rppar[6][1]+clusters.c.uren_spoorlas*rppar[7][1]\
                 +clusters.c.uren_telecom*rppar[10][1],\
                materieel=clusters.c.sleuvengraver*rppar1[0][1]+clusters.c.persapparaat\
                 *rppar1[1][1]+clusters.c.atlaskraan*rppar1[2][1]+clusters.c.kraan_groot\
                 *rppar1[3][1]+clusters.c.mainliner*rppar1[4][1]+clusters.c.hormachine\
                 *rppar1[5][1]+clusters.c.wagon*rppar1[6][1]+clusters.c.locomotor\
                 *rppar1[7][1]+clusters.c.locomotief*rppar1[8][1]+clusters.c.montagewagen\
                 *rppar1[9][1]+clusters.c.stormobiel*rppar1[10][1]+clusters.c.robeltrein\
                 *rppar1[11][1], inhuur=clusters.c.uren_inhuur*rppar[0][1])
            con.execute(upd2)
            upd3 = update(clusters).where(clusters.c.clusterID == clusternr).values(\
                    diensten = clusters.c.inhuur+clusters.c.leiding+clusters.c.huisvesting+\
                    clusters.c.kabelwerk+clusters.c.grondverzet+clusters.c.betonwerk+\
                    clusters.c.vervoer+clusters.c.overig)
            con.execute(upd3)
            upd4 = update(clusters).where(clusters.c.clusterID == clusternr).values(\
                    prijs = clusters.c.lonen+clusters.c.materialen+clusters.c.diensten+\
                    clusters.c.materieel)
            con.execute(upd4)
            invoerOK()
        
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)