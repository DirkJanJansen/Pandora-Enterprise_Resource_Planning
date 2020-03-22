from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QVBoxLayout,\
      QComboBox, QDialog, QMessageBox, QTableView
from sqlalchemy import (Table, Column, Integer, String, Float,\
                     MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Artikelen opvragen')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Artikelen opvragen')               
    msg.exec_() 

def selektie(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle('Materiaallijsten opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(220)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('         Calculatie keuze')
            k0Edit.addItem('1. Externe calculaties')
            k0Edit.addItem('2. Interne calculaties')
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
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1 , 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
    
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(cancelBtn, 2, 0, 1, 2, Qt.AlignCenter)
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
    if not data[0] or data[0][0] == ' ':
        keuze = 0
        selektie(m_email)
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    matLijst(keuze, m_email)

def matLijst(keuze, m_email):
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('werknummerID', Integer),
        Column('calculatie', Integer),
        Column('icalculatie', Integer),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('hoeveelheid', Float),
        Column('orderinkoopID', Integer),
        Column('bestelling', Float),
        Column('reserverings_datum', String),
        Column('levertijd_begin', String),
        Column('levertijd_end', String),
        Column('categorie', Integer),
        Column('verwerkt', Integer))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if keuze == 1:
        sel = select([materiaallijsten]).where(materiaallijsten.c.calculatie > 0)\
          .order_by(materiaallijsten.c.calculatie, materiaallijsten.c.artikelID)
    elif keuze == 2:
        sel = select([materiaallijsten]).where(materiaallijsten.c.icalculatie > 0)\
          .order_by(materiaallijsten.c.calculatie, materiaallijsten.c.artikelID)
    rpmatlijst = conn.execute(sel)
          
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QDialog.__init__(self, *args,)
            self.setGeometry(50, 50, 1400, 900)
            self.setWindowTitle('Materialen bestellijsten opvragen')
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
            #table_view.clicked.connect(boekBestelling)
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
  
    header = ['LijstID','Werknummer','Externe calculatie','Interne calculatie','Artikelnummer',\
              'Hoeveelheid','Inkoopordernummer','Bestelling','Reserveringsdatum',\
              'Levertijd start','Levertijd eind','Categorie','Verwerkt'] 
  
    data_list=[]
    for row in rpmatlijst:
        data_list += [(row)] 
            
    win = MyWindow(data_list, header)
    win.exec_()
    selektie(m_email)
    