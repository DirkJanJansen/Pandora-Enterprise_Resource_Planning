from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
    QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit   
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData,\
                         create_engine, ForeignKey)
from sqlalchemy.sql import select, insert, update, func, and_

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Enter articles per cluster')
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Enter articles per cluster')
    msg.exec_() 

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Enter articles per cluster')
    msg.exec_()

def calcBestaat():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Cluster item line exists\nexisting quantity has been replaced\nby changed quantity!')

    msg.setWindowTitle('Enter articles per cluster')
    msg.exec_()
    
def foutCluster():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Nonexistent cluster number\nCorrect!')
    msg.setWindowTitle('Enter articles per cluster')
    msg.exec_() 

def zoeken(m_email):
    import validZt
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster -> Articles range")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            self.Clusternummer = QLabel()
            clEdit = QLineEdit()
            clEdit.setFixedWidth(210)
            font = QFont("Arial",10)
            font.setCapitalization(QFont.AllUppercase)
            clEdit.setFont(font)
            reg_ex = QRegExp('^[L-Tl-t]{1}[A-Za-z]{1}[0-9]{5}')
            input_validator = QRegExpValidator(reg_ex, clEdit)
            clEdit.setValidator(input_validator)
            clEdit.textChanged.connect(self.clChanged)
                                
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(320)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                  Search articles')
            k0Edit.addItem('1. All aticles')
            k0Edit.addItem('2. Filtered bu articles numbers')
            k0Edit.addItem('3. Filtered by articles description')
            k0Edit.activated[str].connect(self.k0Changed)
    
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(210)
            zktermEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp('^.{0,20}$')
            input_validator = QRegExpValidator(reg_ex, zktermEdit)
            zktermEdit.setValidator(input_validator)
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0, 1, 2)
            
            lbl2 = QLabel('Cluster number')
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 2, 0)
            grid.addWidget(clEdit, 2, 1)
            
            grid.addWidget(k0Edit, 3, 0, 1, 2, Qt.AlignRight)
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 4, 0)
            grid.addWidget(zktermEdit, 4, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 5, 1 , 1 ,1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 5, 1, 1, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def clChanged(self, text):
            self.Clusternummer.setText(text)
              
        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
        
        def returnClusternummer(self):
            return self.Clusternummer.text()
         
        def returnKeuze(self):
            return self.Keuze.text()
        
        def returnZoekterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnClusternummer(), dialog.returnKeuze(),\
                    dialog.returnZoekterm()]       

    window = Widget()
    data = window.getData()
    zoekterm = ''
    keuze = ''
    metadata = MetaData()
    iclusters = Table('iclusters', metadata,
        Column('iclusterID', Integer, primary_key=True),
        Column('omschrijving', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selcl = select([iclusters]).where(iclusters.c.iclusterID == str(data[0]).upper())
    rpcl = con.execute(selcl).first()
    if rpcl:
        momschr = rpcl[1]
    else:
        foutCluster()
        zoeken(m_email)
    if data[0]:
        clusternr = str(data[0]).upper()
    if not data[1] or data[1][0] == ' ':
        ongInvoer()
        zoeken(m_email)
    if not data[1] or data[1][0] == ' ':
        ongInvoer()
        zoeken(m_email)
    elif data[1][0] == '1':
        keuze = '1'
    elif data[1][0] == '2' and validZt.zt(data[2], 2):
        keuze = '2'
        zoekterm = data[2]
    elif data[1][0] == '3' and data[1]:
        keuze = '3'
        zoekterm = data[2]
    else:
        ongInvoer()
        zoeken(m_email)
    toonArtikelen(keuze, zoekterm, m_email, momschr, clusternr)   
 
def toonArtikelen(keuze,zoekterm, m_email, momschr, clusternr):             
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1350, 900)
            self.setWindowTitle('Cluster Articles')
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
     
    header = ['Article number', 'Description', 'Price', 'Stock', 'Unit',\
          'Minimum\nstock', 'Order size', 'Location', 'Group', 'Category', 'Size']

    metadata = MetaData()

    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float),
        Column('locatie_magazijn', String(10)),
        Column('artikelgroep', String),
        Column('categorie', String(10)),
        Column('afmeting', String))     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == '1':
        sel = select([artikelen]).order_by(artikelen.c.artikelID)
    elif keuze == '2':
        zoekterm = zoekterm+''
        aanv = '200000000'
        suppl = '299999999'
        zoekbegin = (zoekterm+aanv)[0:9]
        zoekeind = (zoekterm+suppl)[0:9]
        sel = select([artikelen]).where(and_(artikelen.c.artikelID >= int(zoekbegin),\
                     artikelen.c.artikelID <= int(zoekeind)))\
                    .order_by(artikelen.c.artikelID)
    elif keuze == '3':
        sel = select([artikelen]).where(artikelen.c.artikelomschrijving.ilike('%'+zoekterm+'%'))\
                              .order_by(artikelen.c.artikelID)
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
        artikelnr = idx.data()
        if idx.column() == 0:
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
                                  
                    grid.addWidget(QLabel('Cluster number              '+clusternr+\
                                        '\n'+momschr[:35]), 1, 1, 1, 3)
                        
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Article number              '+str(artikelnr)), 3, 1, 1, 3)
                                  
                    self.setWindowTitle("Building clusters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setFont(QFont('Arial', 10))
               
                    self.Hoeveelheid = QLabel(self)
                    self.Hoeveelheid.setText('Amount ')
                    self.hoev = QLineEdit(self)
                    self.hoev.setFixedWidth(210)
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.hoev)
                    self.hoev.setValidator(input_validator)
                    
                    grid.addWidget(self.Hoeveelheid, 4, 1)
                    grid.addWidget(self.hoev, 4, 2)
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved\n     dj.jansen@casema.nl'), 6, 0, 1, 3, Qt.AlignCenter)
                    
                    self.applyBtn = QPushButton('Insert', self)
                    self.applyBtn.clicked.connect(self.clickMethod)
                    grid.addWidget(self.applyBtn, 5, 2, 1, 1, Qt.AlignRight)
                    self.applyBtn.setFont(QFont("Arial",10))
                    self.applyBtn.setFixedWidth(100)
                    self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    self.cancelBtn = QPushButton('Close')
                    self.cancelBtn.clicked.connect(self.close)
                    grid.addWidget(self.cancelBtn, 5, 2, 1, 2)
                    self.cancelBtn.setFont(QFont("Arial",10))
                    self.cancelBtn.setFixedWidth(100)
                    self.cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)
                                   
                def clickMethod(self):
                    mhoev = self.hoev.text()
                    if mhoev == '' or mhoev == '0':
                        return
                    mhoev = float(str(mhoev))
                    
                    metadata = MetaData()
                    
                    icluster_artikelen = Table('icluster_artikelen', metadata,
                        Column('icluster_artID', Integer, primary_key=True),
                        Column('iclusterID', None, ForeignKey('iclusters.iclusterID')),
                        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                        Column('hoeveelheid', Float))
                    artikelen = Table('artikelen', metadata,
                        Column('artikelID', Integer(), primary_key=True),
                        Column('artikelprijs', Float))
                    iclusters = Table('iclusters', metadata,
                        Column('iclusterID', Integer(), primary_key=True),
                        Column('materialen', Float))
                    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                    con = engine.connect()
                    selclart = select([icluster_artikelen]).where(and_(icluster_artikelen\
                      .c.iclusterID == clusternr, icluster_artikelen.c.artikelID == artikelnr))
                    rpclart = con.execute(selclart).first()
                    selart = select([artikelen]).where(artikelen.c.artikelID == artikelnr)
                    rpart = con.execute(selart).first()
                    martprijs = rpart[1]
                    updcl = update(iclusters).where(iclusters.c.iclusterID == clusternr).\
                      values(materialen = iclusters.c.materialen + martprijs*mhoev)
                    con.execute(updcl)
                    if rpclart:
                        updclart = update(icluster_artikelen).where(and_(icluster_artikelen.c.\
                         iclusterID == clusternr, icluster_artikelen.c.artikelID == artikelnr))\
                         .values(hoeveelheid = mhoev)
                        con.execute(updclart)
                        calcBestaat()
                    else:
                        try:
                            mclartnr = (con.execute(select([func.max(icluster_artikelen.c.\
                             icluster_artID, type_=Integer)])).scalar())
                            mclartnr += 1
                        except:
                            mclartnr = 1
                        insclart = insert(icluster_artikelen).values(icluster_artID = mclartnr,\
                        iclusterID = clusternr, artikelID = artikelnr, hoeveelheid = mhoev)
                        con.execute(insclart)
                        invoerOK()
                    self.accept()
                    
            mainWin = MainWindow()
            mainWin.exec_()
 
    win = MyWindow(data_list, header)
    win.exec_()
 