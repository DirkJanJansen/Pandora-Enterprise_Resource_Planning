from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
      QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit
    
from sqlalchemy import (Table, Column, String, Float, MetaData, create_engine)
from sqlalchemy.sql import select

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request clusters')
    msg.exec_() 
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Invalid entry')
    msg.setWindowTitle('Request clusters')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
                
def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster article lines")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                              
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(400)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                 Cluster groups sort key')
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
                        
            grid.addWidget(k0Edit, 1, 0, 1, 2, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
            
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
    
            grid.addWidget(cancelBtn, 2, 0, 1 , 2, Qt.AlignCenter)
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
    if not data[0] or data[0][0] == ' ':
        ongInvoer()
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
            self.setGeometry(100, 50, 1700, 900)
            self.setWindowTitle('Request clusters')
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

    header = ['Cluster number', 'Description', 'Price', 'Unit', 'Materials', 'Wages', \
              'Services', 'Equipment', 'Hiring', 'hours\nconstruction', 'hours mounting', 'hours\nreturn welding', \
              'hours\nchief mechanic', 'hours\npower-supply', 'hours\nOCL', 'hours\ntrack laying','hours\ntrack welding', \
              'hours\nhiring', 'Trench machine', 'Press machine', 'Atlas crane', \
              'Crane big', 'Mainliner', 'Ballast scrape\nmachine', 'Wagon', 'Locomotor', \
              'Locomotive', 'Assembly\ntrolley', 'Stormobiel', 'hours\ntelecom', 'Robel train', \
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
    
    if keuze == '0':  
        sel = select([clusters]).where(clusters.c.clusterID < 'JL').order_by(clusters.c.clusterID.asc())
    else:
        sel = select([clusters]).where(clusters.c.clusterID.like(keuze+'%'))\
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
                    self.setWindowTitle("Request clusters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setFont(QFont('Arial', 10))   
                    
                    q1Edit = QLineEdit(rpsel[1])#description
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    q2Edit = QLineEdit('{:12.2f}'.format(rpsel[2])) #price
                    q2Edit.setFixedWidth(150)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    q3Edit = QLineEdit(str(rpsel[3]))#unit
                    q3Edit.setFixedWidth(150)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    q4Edit = QLineEdit('{:12.2f}'.format(rpsel[4]))#materials
                    q4Edit.setFixedWidth(150)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    q5Edit = QLineEdit('{:12.2f}'.format(rpsel[5])) #wages
                    q5Edit.setFixedWidth(150)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    q6Edit = QLineEdit('{:12.2f}'.format(rpsel[6])) #services
                    q6Edit.setFixedWidth(150)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    q7Edit = QLineEdit('{:12.2f}'.format(rpsel[7]))#equipment
                    q7Edit.setFixedWidth(150)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    q8Edit = QLineEdit('{:12.2f}'.format(rpsel[8]))#hiring
                    q8Edit.setFixedWidth(150)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    q9Edit = QLineEdit('{:12.2f}'.format(rpsel[9]))#hours construction
                    q9Edit.setFixedWidth(150)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                    
                    q10Edit = QLineEdit('{:12.2f}'.format(rpsel[10]))#hours mounting
                    q10Edit.setFixedWidth(150)
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                    
                    q11Edit = QLineEdit('{:12.2f}'.format(rpsel[11]))#hours return welding
                    q11Edit.setFixedWidth(150)
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                    
                    q12Edit = QLineEdit('{:12.2f}'.format(rpsel[12]))#hours chief mechanic
                    q12Edit.setFixedWidth(150)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)

                    q13Edit = QLineEdit('{:12.2f}'.format(rpsel[13]))#hours power-supply
                    q13Edit.setFixedWidth(150)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
                    
                    q14Edit = QLineEdit('{:12.2f}'.format(rpsel[14]))#hours OCL
                    q14Edit.setFixedWidth(150)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                       
                    q15Edit = QLineEdit('{:12.2f}'.format(rpsel[15]))#hours track laying
                    q15Edit.setFixedWidth(150)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
                    
                    q16Edit = QLineEdit('{:12.2f}'.format(rpsel[16]))#hours track welding
                    q16Edit.setFixedWidth(150)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                    
                    q17Edit = QLineEdit('{:12.2f}'.format(rpsel[17])) #hours hiring
                    q17Edit.setFixedWidth(150)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                       
                    q18Edit = QLineEdit('{:12.2f}'.format(rpsel[18])) #hours trench machine
                    q18Edit.setFixedWidth(150)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                            
                    q19Edit = QLineEdit('{:12.2f}'.format(rpsel[19])) #hours pressing machine
                    q19Edit.setFixedWidth(150)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
                    
                    q20Edit = QLineEdit('{:12.2f}'.format(rpsel[20])) # atlas crane
                    q20Edit.setFixedWidth(150)
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                    
                    q21Edit = QLineEdit('{:12.2f}'.format(rpsel[21])) #crane big
                    q21Edit.setFixedWidth(150)
                    q21Edit.setAlignment(Qt.AlignRight)
                    q21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q21Edit.setDisabled(True)

                    q22Edit = QLineEdit('{:12.2f}'.format(rpsel[22]))#mainliner
                    q22Edit.setFixedWidth(150)
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q22Edit.setDisabled(True)

                    q23Edit = QLineEdit('{:12.2f}'.format(rpsel[23])) #ballast clearing machine
                    q23Edit.setFixedWidth(150)
                    q23Edit.setAlignment(Qt.AlignRight)
                    q23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q23Edit.setDisabled(True)

                    q24Edit = QLineEdit('{:12.2f}'.format(rpsel[24])) #wagon
                    q24Edit.setFixedWidth(150)
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q24Edit.setDisabled(True)
  
                    q25Edit = QLineEdit('{:12.2f}'.format(rpsel[25])) #locomotor
                    q25Edit.setFixedWidth(150)
                    q25Edit.setAlignment(Qt.AlignRight)
                    q25Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q25Edit.setDisabled(True)

                    q26Edit = QLineEdit('{:12.2f}'.format(rpsel[26])) #locomotive
                    q26Edit.setFixedWidth(150)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q26Edit.setDisabled(True)

                    q27Edit = QLineEdit('{:12.2f}'.format(rpsel[27])) #assembly trolley
                    q27Edit.setFixedWidth(150)
                    q27Edit.setAlignment(Qt.AlignRight)
                    q27Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q27Edit.setDisabled(True)
 
                    q28Edit = QLineEdit('{:12.2f}'.format(rpsel[28])) #stormobiel
                    q28Edit.setFixedWidth(150)
                    q28Edit.setAlignment(Qt.AlignRight)
                    q28Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q28Edit.setDisabled(True)
                                 
                    q29Edit = QLineEdit('{:12.2f}'.format(rpsel[29])) #hours telecom
                    q29Edit.setFixedWidth(150)
                    q29Edit.setAlignment(Qt.AlignRight)
                    q29Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q29Edit.setDisabled(True)
                                          
                    q30Edit = QLineEdit('{:12.2f}'.format(rpsel[30])) #robel train
                    q30Edit.setFixedWidth(150)
                    q30Edit.setAlignment(Qt.AlignRight)
                    q30Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q30Edit.setDisabled(True)
                    
                    q31Edit = QLineEdit('{:12.2f}'.format(rpsel[31])) #direction
                    q31Edit.setFixedWidth(150)
                    q31Edit.setAlignment(Qt.AlignRight)
                    q31Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q31Edit.setDisabled(True)
                                    
                    q32Edit = QLineEdit('{:12.2f}'.format(rpsel[32])) # housing
                    q32Edit.setFixedWidth(150)
                    q32Edit.setAlignment(Qt.AlignRight)
                    q32Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q32Edit.setDisabled(True)
                    
                    q33Edit = QLineEdit('{:12.2f}'.format(rpsel[33])) #cable work
                    q33Edit.setFixedWidth(150)
                    q33Edit.setAlignment(Qt.AlignRight)
                    q33Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q33Edit.setDisabled(True)
                    
                    q34Edit = QLineEdit('{:12.2f}'.format(rpsel[34])) #earth moving
                    q34Edit.setAlignment(Qt.AlignRight)
                    q34Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q34Edit.setDisabled(True)
                    
                    q35Edit = QLineEdit('{:12.2f}'.format(rpsel[35])) #concrete work
                    q35Edit.setFixedWidth(150)
                    q35Edit.setAlignment(Qt.AlignRight)
                    q35Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q35Edit.setDisabled(True)
                    
                    q36Edit = QLineEdit('{:12.2f}'.format(rpsel[36])) #Transport
                    q36Edit.setFixedWidth(150)
                    q36Edit.setAlignment(Qt.AlignRight)
                    q36Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q36Edit.setDisabled(True)
                    
                    q37Edit = QLineEdit('{:12.2f}'.format(rpsel[36])) #Remaining
                    q37Edit.setFixedWidth(150)
                    q37Edit.setAlignment(Qt.AlignRight)
                    q37Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q37Edit.setDisabled(True)
                    
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
                    
                    lbl20 = QLabel('Trench machine hours')
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
                                                          
                    lbl29 = QLabel('Mounting hours')
                    lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl29, 5, 2)
                    grid.addWidget(q27Edit, 5, 3)
                    
                    lbl30 = QLabel('Stormobiel hours')
                    lbl30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl30, 6, 2)
                    grid.addWidget(q28Edit, 6, 3)
                    
                    lbl31 = QLabel('Telecom hours')
                    lbl31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl31, 17, 2)
                    grid.addWidget(q29Edit, 17, 3) 
                                        
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
                                                                                                  
                    lbl15 = QLabel('Power-supply hours')
                    lbl15.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl15, 13, 2)
                    grid.addWidget(q13Edit, 13, 3)
                 
                    lbl16 = QLabel('OCL hours')
                    lbl16.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl16, 14, 2)
                    grid.addWidget(q14Edit, 14, 3)
                    
                    lbl17 = QLabel('Track laying hours')
                    lbl17.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl17, 15, 2)
                    grid.addWidget(q15Edit, 15, 3)
                    
                    lbl18 = QLabel('Track welding hours')
                    lbl18.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl18, 16, 2)
                    grid.addWidget(q16Edit, 16, 3)
                    
                    lbl31 = QLabel('Robel train hours')
                    lbl31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl31, 7, 2)
                    grid.addWidget(q30Edit, 7, 3)
                    
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
                    grid.addWidget(lbl, 0, 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 3, 1 , 1, Qt.AlignRight)
                                                                   
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 0, 1, 4, Qt.AlignCenter)
                      
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 150, 150)
            
                    applyBtn = QPushButton('Close')
                    applyBtn.clicked.connect(self.close)
            
                    grid.addWidget(applyBtn, 21, 3, 1, 1, Qt.AlignRight| Qt.AlignBottom)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                              
            mainWin = MainWindow()
            mainWin.exec_()

    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)