from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
     QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit
   
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, and_

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Icluster-artikelen opvragen')               
    msg.exec_() 
    
def geenRegels():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Er zijn nog geen artikelregels aanwezig voor dit cluster!')
    msg.setWindowTitle('Cluster-artikelen opvragen')               
    msg.exec_()
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Icluster-artikelen opvragen')               
    msg.exec_()
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
                
def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster artikelregels")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                              
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(340)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('            Sorteersleutel Clustergroepen')
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
                        
            grid.addWidget(k0Edit, 1, 0, 1, 2, Qt.AlignRight)
           
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignRight)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
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
    zoekterm = ''
    if not data[0] or data[0][0] == ' ':
        ongInvoer()
        zoeken(m_email)
    elif data[0]:
        zoekterm = data[0][0]
    toonIclusterartikelen(zoekterm, m_email)
    
def  toonIclusterartikelen(zoekterm, m_email):
    import validZt                     
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1800, 900)
            self.setWindowTitle('Artikelen per cluster opvragen')
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
              
    header = ['Clusternr', 'Omschrijving', 'Prijs', 'Eenheid', 'Materialen', 'Lonen',\
              'Diensten', 'Materiëel', 'Inhuur', 'Zagen', 'Schaven','Steken',\
              'Boren', 'Frezen', 'Draaien-klein', 'Draaien-groot', 'Tappen',\
              'Nube-draaien', 'Nube-bewerken', 'Knippen', 'Kanten',\
              'Stansen', 'Lassen-CO2', 'Lassen-Hand', 'Verpakken', 'Verzinken',\
              'Moffelen', 'Schilderen', 'Spuiten', 'Ponsen','Persen','Gritstralen']
    
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
        Column('inhuur', Float),
        Column('zagen', Float),
        Column('schaven', Float),
        Column('steken', Float),
        Column('boren', Float),
        Column('frezen', Float),
        Column('draaien_klein', Float),
        Column('draaien_groot', Float),
        Column('tappen', Float),
        Column('nube_draaien', Float),
        Column('nube_bewerken', Float),
        Column('knippen', Float),
        Column('kanten', Float),
        Column('stansen', Float),
        Column('lassen_co2', Float),
        Column('lassen_hand', Float),
        Column('verpakken', Float),
        Column('verzinken', Float),
        Column('moffelen', Float),
        Column('schilderen', Float),
        Column('spuiten', Float),
        Column('ponsen', Float),
        Column('persen', Float),
        Column('gritstralen', Float))
       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
     
    if zoekterm == '0':
        sel = select([iclusters]).order_by(iclusters.c.iclusterID)
    elif validZt.zt(zoekterm, 25):
        sel = select([iclusters]).where(iclusters.c.iclusterID.ilike(zoekterm+'%'))\
                              .order_by(iclusters.c.iclusterID)
    else:
        ongInvoer()
        zoeken(m_email)
        
    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
        zoeken(m_email)
 
    data_list=[]
    for row in rp:
        data_list += [(row)]
    
    def showSelection(idx):
        clusternr = str(idx.data())
        if idx.column() == 0:
            metadata = MetaData()
            iclusters = Table('iclusters', metadata,
                Column('iclusterID', Integer, primary_key=True),
                Column('omschrijving', String))
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer, primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float))
            icluster_artikelen = Table('icluster_artikelen', metadata,
                Column('icluster_artID', Integer, primary_key=True),
                Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
                Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                Column('hoeveelheid', Float))
    
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcl = select([icluster_artikelen, iclusters, artikelen]).where(and_\
             (icluster_artikelen.c.iclusterID == clusternr, icluster_artikelen.c.iclusterID==\
              iclusters.c.iclusterID, icluster_artikelen.c.artikelID == artikelen.c.artikelID))
            if con.execute(selcl).fetchone():
                rpsel = con.execute(selcl)
            else:
                geenRegels()
                return
            regel = 0
            for row in rpsel:
                regel += 1
                class MainWindow(QDialog):
                    def __init__(self):
                        QDialog.__init__(self)
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                        self.setWindowTitle("Opvragen artikelregels per cluster")
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        
                        self.setFont(QFont('Arial', 10))   
                        
                        q1Edit = QLineEdit(str(row[5]))
                        q1Edit.setFixedWidth(400)
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q1Edit.setDisabled(True)
                        
                        q6Edit = QLineEdit(str(row[2]))
                        q6Edit.setFixedWidth(150)
                        q6Edit.setAlignment(Qt.AlignRight)
                        q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q6Edit.setDisabled(True)
                                       
                        q2Edit = QLineEdit('{:12.2f}'.format(row[8]))
                        q2Edit.setFixedWidth(150)
                        q2Edit.setAlignment(Qt.AlignRight)
                        q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q2Edit.setDisabled(True)
                         
                        q3Edit = QLineEdit('{:12.2f}'.format(row[3]))
                        q3Edit.setFixedWidth(150)
                        q3Edit.setAlignment(Qt.AlignRight)
                        q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q3Edit.setDisabled(True)
                        
                        q5Edit = QLineEdit(str(row[7]))
                        q5Edit.setFixedWidth(400)
                        q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q5Edit.setDisabled(True)
                                               
                        grid = QGridLayout()
                        grid.setSpacing(20)
                        
                        lbl1 = QLabel('Clusternummer')  
                        lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl1, 1, 0)
                        
                        lbl2 = QLabel(clusternr)
                        grid.addWidget(lbl2, 1, 1)
                        
                        lbl9 = QLabel('Regelnummer: ')
                        lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl9, 1, 2)
                        
                        lbl10 = QLabel(str(regel))
                        grid.addWidget(lbl10, 1, 3)
                               
                        lbl3 = QLabel('Clusteromschrijving')  
                        lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl3, 2, 0)
                        grid.addWidget(q1Edit, 2, 1, 1, 3) 
                        
                        lbl8 = QLabel('Artikelnummer')  
                        lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl8, 3, 0)
                        grid.addWidget(q6Edit, 3, 1)
                                                                
                        lbl4 = QLabel('Artikelprijs')  
                        lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl4, 4, 0)
                        grid.addWidget(q2Edit, 4, 1)
                        
                        lbl5 = QLabel('Hoeveelheid\nArtikelen per cluster')  
                        lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl5, 5, 0)
                        grid.addWidget(q3Edit, 5, 1)
                       
                        lbl7 = QLabel('Artikelomschrijving')  
                        lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        grid.addWidget(lbl7, 6, 0)
                        grid.addWidget(q5Edit, 6, 1, 1, 3)
                      
                        lbl = QLabel()
                        pixmap = QPixmap('./images/logos/verbinding.jpg')
                        lbl.setPixmap(pixmap)
                        grid.addWidget(lbl, 0, 0, 1, 2)
                        
                        logo = QLabel()
                        pixmap = QPixmap('./images/logos/logo.jpg')
                        logo.setPixmap(pixmap)
                        grid.addWidget(logo , 0, 3, 1 , 1, Qt.AlignRight)
                                                         
                        grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 4, Qt.AlignCenter)
                          
                        self.setLayout(grid)
                        self.setGeometry(500, 300, 150, 150)
                
                        applyBtn = QPushButton('Regels')
                        applyBtn.clicked.connect(self.accept)
                
                        grid.addWidget(applyBtn, 7, 3, 1, 1, Qt.AlignRight)
                        applyBtn.setFont(QFont("Arial",10))
                        applyBtn.setFixedWidth(100)
                        applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                                                          
                mainWin = MainWindow()
                mainWin.exec_()    
    
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)