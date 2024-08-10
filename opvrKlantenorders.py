from login import hoofdMenu
from datetime import datetime 
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QStyledItemDelegate,\
      QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, \
                            ForeignKey, create_engine, DateTime, select)
                    
def geenOrders():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No orders present!')
    msg.setWindowTitle('Request order overview')               
    msg.exec_()
    
def bestellingen(m_email):
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False))
    klanten = Table('klanten', metadata,
        Column('klantID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')))
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True),
        Column('klantID', None, ForeignKey('klanten.klantID')),
        Column('ovbesteldatum', DateTime(), default=datetime.now),
        Column('datum_betaald', String))
    orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
        Column('ovaID', Integer, primary_key=True),
        Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('ovaantal', Integer),
        Column('ovleverdatum', DateTime()),
        Column('verkoopprijs', Float),
        Column('retour',Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('artikelomschrijving', String(50)),
        Column('thumb_artikel', String(70)))
          
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    sel = select([accounts.c.accountID, accounts.c.email]).\
            where(accounts.c.email == m_email)
    rpaccount = con.execute(sel).first()
    maccountnr = rpaccount[0]
    maccountnr = int(maccountnr)
    m_email = rpaccount[1]
    con = engine.connect()
    columns = [orders_verkoop.c.ovbestelID,\
        orders_verkoop.c.ovbesteldatum, orders_verkoop.c.datum_betaald,\
        orders_verkoop_artikelen.c.ovleverdatum,\
        orders_verkoop_artikelen.c.ovaantal, artikelen.c.artikelID,\
        artikelen.c.artikelomschrijving, orders_verkoop_artikelen.c.verkoopprijs,\
        artikelen.c.thumb_artikel, orders_verkoop_artikelen.c.retour]
    bestellingen = select(columns).where(accounts.c.email == m_email)
    bestellingen = bestellingen.select_from(accounts.join(klanten)\
               .join(orders_verkoop).join(orders_verkoop_artikelen)\
               .join(artikelen)).order_by(orders_verkoop_artikelen.c.ovbestelID, orders_verkoop_artikelen.c.artikelID)
    
    if con.execute(bestellingen).fetchone():
        rp_bestellingen = con.execute(bestellingen)
    else:
        geenOrders()
        hoofdMenu(m_email)
    toonBest(rp_bestellingen, m_email)
        
def toonBest(rp_bestellingen, m_email):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Order overview')
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
            table_view.setColumnWidth(8, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.setItemDelegateForColumn(8, showImage(self))
            #table_view.clicked.connect(showBestelling)
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

    class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap)) 
   
    header = ['Order','Order date', 'Pay date','Delivery date', 'Quantity',\
              'Article number','Description','Selling price', 'Image', 'Return']
    
    data_list=[]
    for row in rp_bestellingen:
        data_list += [(row)]
               
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)