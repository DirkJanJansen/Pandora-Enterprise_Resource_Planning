from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QVBoxLayout,\
      QComboBox, QDialog, QLineEdit, QMessageBox, QTableView
from sqlalchemy import (Table, Column, Integer, Float, String, MetaData, ForeignKey,\
                       create_engine)
from sqlalchemy.sql import select, and_

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Provide/print materials')
    msg.exec_() 
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request articles')
    msg.exec_()
  
def mutatieKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request article mutations")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(240)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('       Search sort key')
            k0Edit.addItem('1. All mutations')
            k0Edit.addItem('2. Work(s) (Description)')
            k0Edit.addItem('3. Supplier(s) (Name)')
            k0Edit.addItem('4. Sale orders')
            k0Edit.addItem('5. Internal work orders')
            k0Edit.addItem('6. By yyyy(-mm(-dd))')
            k0Edit.addItem('7. Counter sales orders')
            
            k0Edit.activated[str].connect(self.k0Changed)
                            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(240)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                                  
            grid.addWidget(k0Edit, 1, 1)
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved  dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
                      
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(110)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk0(self):
            return self.Keuze.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzkterm()]       

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
    toonMutaties(keuze, zoekterm, m_email)

def toonMutaties(keuze, zoekterm, m_email):
    import validZt
    metadata = MetaData()
    artikelmutaties = Table('artikelmutaties', metadata,
        Column('mutatieID', Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('hoeveelheid', Float),
        Column('boekdatum', String),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('ovbestelID', None, ForeignKey('klanten.klantID')),
        Column('werkorderID', None, ForeignKey('orders_intern.werkorderID')),
        Column('tot_mag_prijs', Float),
        Column('btw_hoog', Float),
        Column('baliebonID', Integer))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('werkomschrijving', String))
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer, primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer, primary_key=True),
        Column('bedrijfsnaam',  String))
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True))
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer, primary_key=True))
                    
    engine = create_engine('postgresql://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if keuze == 1:
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving,artikelen.c\
           .artikelprijs]).where(artikelen.c.artikelID==artikelmutaties.c.artikelID)
    elif keuze == 2:
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving, artikelen.c\
           .artikelprijs,werken.c.werknummerID, werken.c.werkomschrijving])\
           .where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
            artikelmutaties.c.werknummerID == werken.c.werknummerID,\
            werken.c.werkomschrijving.ilike('%'+zoekterm+'%'))).\
         order_by(artikelmutaties.c.werknummerID, artikelmutaties.c.artikelID)
    elif keuze == 3:
        sel = select ([artikelmutaties, artikelen.c.artikelomschrijving,artikelen.c\
           .artikelprijs, leveranciers.c.leverancierID,leveranciers.c.bedrijfsnaam]).\
            where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
            artikelmutaties.c.orderinkoopID==orders_inkoop.c.orderinkoopID,\
            orders_inkoop.c.leverancierID == leveranciers.c.leverancierID, leveranciers.c.\
            bedrijfsnaam.ilike('%'+zoekterm+'%'))).order_by(leveranciers.c.leverancierID,\
            artikelmutaties.c.artikelID)
    elif keuze == 4:
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving,artikelen.c\
           .artikelprijs]).where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
            artikelmutaties.c.ovbestelID==orders_verkoop.c.ovbestelID)).\
            order_by(artikelmutaties.c.ovbestelID, artikelmutaties.c.artikelID)
    elif keuze == 5:
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving, artikelen.c\
           .artikelprijs])\
          .where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
          artikelmutaties.c.werkorderID==orders_intern.c.werkorderID)).\
           order_by(artikelmutaties.c.werkorderID, artikelmutaties.c.artikelID)
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving,artikelen.c\
         .artikelprijs]).where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
         artikelmutaties.c.boekdatum.like(zoekterm+'%'))).order_by(artikelmutaties.c.boekdatum)
    elif keuze == 7:
        sel = select([artikelmutaties, artikelen.c.artikelomschrijving,artikelen.c\
         .artikelprijs]).where(and_(artikelen.c.artikelID==artikelmutaties.c.artikelID,\
         artikelmutaties.c.baliebonID > 0)).order_by(artikelmutaties.c.baliebonID)
    else:
        ongInvoer()
        mutatieKeuze(m_email)
 
    if conn.execute(sel).fetchone():     
        rp = conn.execute(sel)
    else:
        geenRecord()
        mutatieKeuze(m_email)
         
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QDialog.__init__(self, *args,)
            self.setGeometry(50, 50, 1800, 900)
            self.setWindowTitle('Request articles mutations')
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
            #table_view.clicked.connect(showAccount)
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
  
    header = ['Mutation number','Article number', 'Amount','Booking date', 'Work number', 'Order purchase number',\
              'Sales order number','Internal order number', 'Total warehouse price', 'VAT high',\
              'Counter receipt number', 'Article description', 'Article price']
    if keuze == 2:
        header1 = ['Work number','Work description']
        header.extend(header1)
    elif keuze == 3:
        header2 = ['Supplier number', 'Company name']
        header.extend(header2)
  
    data_list=[]
    for row in rp:
        data_list += [(row)] 
    
    win = MyWindow(data_list, header)
    win.exec_()
    mutatieKeuze(m_email)