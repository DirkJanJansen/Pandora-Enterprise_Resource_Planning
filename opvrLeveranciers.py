from login import hoofdMenu
from postcode import checkpostcode
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import  QLabel, QPushButton, QWidget, QGridLayout,\
       QComboBox, QDialog, QLineEdit, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine)
from sqlalchemy.sql import select, desc

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request suppliers')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\nplease make another selection!')
    msg.setWindowTitle('Request suppliers')               
    msg.exec_() 
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def leveranciersKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Suppliers Overview.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Times', 10))
    
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(230)
            k4Edit.setFont(QFont("Arial", 10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem(' Search sort key')
            k4Edit.addItem('1. All Supplers.')
            k4Edit.addItem('2. Company name.')
            k4Edit.addItem('3. Supplernumber.')
            k4Edit.activated[str].connect(self.k4Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(220)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                           
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k4Edit, 2, 1)
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 2,Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 4, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 4, 1)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
        def k4Changed(self, text):
            self.Keuze4.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk4(self):
            return self.Keuze4.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk4(), dialog.returnzkterm()]       

    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonLeveranciers(keuze, zoekterm, m_email)

def toonLeveranciers(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('btwnummer', String),
        Column('kvknummer', String),
        Column('telnr', String),
        Column('postcode', String),  
        Column('huisnummer', String),
        Column('toevoeging', String))
                          
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
         sel = select([leveranciers]).order_by(desc(leveranciers.c.leverancierID)) 
    elif keuze == 2:
         sel = select([leveranciers]).where(leveranciers.c.bedrijfsnaam.ilike('%'+zoekterm+'%'))
    elif keuze == 3 and validZt.zt(zoekterm, 3):
        zoekterm = int(zoekterm)
        sel = select([leveranciers]).where(leveranciers.c.leverancierID == zoekterm)
    else:
        ongInvoer()
        leveranciersKeuze(m_email)
        
    if con.execute(sel).fetchone():
        rplev = con.execute(sel)
    else:
        geenRecord()
        leveranciersKeuze(m_email)
     
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Request Suppliers')
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
            #table_view.clicked.connect(showLeverancier)
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
  
    header = ['Supplier number','Company name', 'Legal Status','VAT umber',\
              'KvK number','Telephone number','Street', 'House number','Suffix',\
              'Zipcode','Residence']  
  
    data_list=[]
    for row in rplev:
        mstrtplts = checkpostcode(row[6], int(row[7]))
        data_list += [(row[0],row[1],row[2],row[3],row[4],row[5],mstrtplts[0],int(row[7]),\
                      row[8],row[6], mstrtplts[1])] 
        
    win = MyWindow(data_list, header)
    win.exec_()
    leveranciersKeuze(m_email)  
