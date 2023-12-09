from login import hoofdMenu
from postcode import checkpostcode
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QDialog, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,\
                        create_engine, and_ , select)

def eigenLeverancier(m_email):
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('email', String))
    lev_accounts = Table('lev_accounts', metadata,
        Column('levaccID', Integer(), primary_key=True), 
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')))    
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
    sel = select([leveranciers]).where(and_(leveranciers.c.leverancierID ==\
          lev_accounts.c.leverancierID, lev_accounts.c.accountID ==\
          accounts.c.accountID , accounts.c.email == m_email))
    rplev = con.execute(sel)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Leveranciers opvragen')
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
  
    header = ['Leveranciernummer','Bedrijfsnaam', 'Rechtsvorm','BTWnummer',\
              'KvKnummer','Telefoonnummer','Straat', 'Huisnummer','Toevoeging',\
              'Postcode','Woonplaats']  
  
    data_list=[]
    for row in rplev:
        mstrtplts = checkpostcode(row[6], int(row[7]))
        data_list += [(row[0],row[1],row[2],row[3],row[4],row[5],mstrtplts[0],int(row[7]),\
                      row[8],row[6], mstrtplts[1])] 
        
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)  
