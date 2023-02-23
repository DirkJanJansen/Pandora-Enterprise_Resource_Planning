from login import hoofdMenu
from validZt import zt
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QTableView, QVBoxLayout,\
                             QPushButton, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, and_

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearchterm!')
    msg.setWindowTitle('Request reservations')               
    msg.exec_()
    
def foutBestel():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Order has been executed before!')
    msg.setWindowTitle('Request reservations')               
    msg.exec_()
    
def foutOrder():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Invalid purchase order number!')
    msg.setWindowTitle('Request reservations')               
    msg.exec_()
   
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request reservations')               
    msg.exec_() 
    
def updateOk():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Adjustments have been made')
    msg.setWindowTitle('Request reservations')
    msg.exec_()

def resKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request reservations")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(350)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                   Search sort key')
            k0Edit.addItem('1. All reservations')
            k0Edit.addItem('2. Sorted by date of reservation')
            k0Edit.addItem('3. Sorted by start delivery')
            k0Edit.addItem('4. Filtered by articlenumber')
            k0Edit.addItem('5. Filtered by worknumber / workorder')
            k0Edit.addItem('6. Filtered by ordered items')
            k0Edit.addItem('7. Filtered by items to order')
            k0Edit.addItem('8. Filtered by categorynumber')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(210)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 0 ,1, 2, Qt.AlignRight)
            lbl1 = QLabel('Searchterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1 , 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
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
    toonReserveringen(keuze,zoekterm, m_email)

def toonReserveringen(keuze, zoekterm, m_email):
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('werknummerID', Integer),
        Column('calculatie', Integer),
        Column('icalculatie', Integer),
        Column('orderinkoopID', Integer),
        Column('hoeveelheid', Float),
        Column('reserverings_datum', String),
        Column('levertijd_begin', String),
        Column('levertijd_end', String),
        Column('categorie', Integer))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('categorie', String(10)),
        Column('bestelsaldo', Float),
        Column('reserveringsaldo', Float))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    if keuze == 1:
        sel = select([materiaallijsten, artikelen]).where(materiaallijsten.c.artikelID == \
          artikelen.c.artikelID).order_by(materiaallijsten.c.artikelID)
    elif keuze == 2:
        sel = select([materiaallijsten, artikelen]).where(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID).order_by(materiaallijsten.c.reserverings_datum)
    elif keuze == 3:
        sel = select([materiaallijsten, artikelen]).where(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID).order_by(materiaallijsten.c.levertijd_begin)
    elif keuze == 4 and zt(zoekterm, 2):
        sel = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID, materiaallijsten.c.artikelID ==  int(zoekterm)))
    elif keuze == 5 and zt(zoekterm, 21):
        sel = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID, materiaallijsten.c.werknummerID == int(zoekterm)))
    elif keuze == 6:
        sel = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID,materiaallijsten.c.orderinkoopID > 0)).order_by(materiaallijsten.c.artikelID)
    elif keuze == 7:
         sel = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.c.artikelID ==\
           artikelen.c.artikelID,materiaallijsten.c.orderinkoopID == 0)).order_by(materiaallijsten.c.artikelID)
    elif keuze == 8 and str(zoekterm).isnumeric() and len(str(zoekterm)) == 1:
        sel = select([materiaallijsten,artikelen]).where(and_(materiaallijsten.c.artikelID ==\
          artikelen.c.artikelID, materiaallijsten.c.categorie == zoekterm)).order_by(artikelen.c.artikelID)
    else:
        ongInvoer()
        resKeuze(m_email)
    
    if con.execute(sel).fetchone():    
        rpres = con.execute(sel)
    else:
        geenRecord()
        resKeuze(m_email)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QDialog.__init__(self, *args,)
            self.setGeometry(100, 50, 1600, 900)
            self.setWindowTitle('Request reservations')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.horizontalHeader().setSectionsMovable(True)
            table_view.setColumnHidden(11,True)
            table_view.setColumnHidden(15,True)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showReservering)
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
       
    header = ['MatlistID','Articlenumber','Worknumber','Calculation','Icalculation',\
              'Purchaseordernumber','Quantity','Reservation date','Delivery time start',\
              'Delivery time end','Category', 'Articlenumber','Article description',\
              'Article price','Article stock','Category','Order balance','Reservation balance']  
        
    data_list=[]
    for row in rpres:
        data_list += [(row)]
        
    def showReservering(idx):
        mresnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([materiaallijsten, artikelen]).where(and_(materiaallijsten.c.artikelID ==\
                artikelen.c.artikelID, materiaallijsten.c.matlijstID == mresnr))
            rpres = con.execute(sel).first()
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                
                    self.setWindowTitle("Request reserverations")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                    self.setFont(QFont('Arial', 10))
                               
                    self.ResID = QLabel()
                    q1Edit = QLineEdit(str(rpres[0]))
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setFixedWidth(100)
                    q1Edit.setDisabled(True)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                
                    self.Artikelnummer = QLabel()
                    q2Edit = QLineEdit(str(rpres[1]))
                    q2Edit.setFixedWidth(100)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                    
                    self.Artikelomschrijving = QLabel()
                    q3Edit = QLineEdit(str(rpres[12]))
                    q3Edit.setFixedWidth(400)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    self.Artikelvoorraad = QLabel()
                    q18Edit = QLineEdit('{:12.2f}'.format(rpres[14]))
                    q18Edit.setFixedWidth(100)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True) 
                                    
                    self.Werknummer = QLabel()
                    q4Edit = QLineEdit(str(rpres[2]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    self.Calculatie = QLabel()
                    q5Edit = QLineEdit(str(rpres[3]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    self.Icalculatie = QLabel()
                    q10Edit = QLineEdit(str(rpres[4]))
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setFixedWidth(100)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                                 
                    self.Inkooporder = QLabel()
                    q6Edit = QLineEdit(str(rpres[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                  
                    self.Hoeveelheid = QLabel()
                    q17Edit = QLineEdit('{:12.2f}'.format(rpres[6]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                                     
                    self.Reserveringsaldo = QLabel()
                    q7Edit = QLineEdit('{:12.2f}'.format(rpres[17]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                                   
                    self.Reserveringdatum = QLabel()
                    q8Edit = QLineEdit(str(rpres[7]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    self.Levering_start= QLabel()
                    q9Edit = QLineEdit(str(rpres[8]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
  
                    self.Levering_eind = QLabel()
                    q11Edit = QLineEdit(str(rpres[9]))
                    q11Edit.setFixedWidth(100)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                           
                    self.Categorie = QLabel()
                    q13Edit = QLineEdit(str(rpres[10]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
                    
                    self.Artikelprijs = QLabel()
                    q14Edit = QLineEdit('{:12.2f}'.format(rpres[13]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                    
                    self.Bestelsaldo = QLabel()
                    q16Edit = QLineEdit('{:12.2f}'.format(rpres[16]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                                         
                    grid = QGridLayout()
                    grid.setSpacing(20)
                
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl , 0, 0)
                
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight) 
                  
                    grid.addWidget(QLabel('MatlistID'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                
                    grid.addWidget(QLabel('Articlenumber'), 2, 0)
                    grid.addWidget(q2Edit, 2, 1)
                    
                    grid.addWidget(QLabel('Worknumber'), 2, 2)
                    grid.addWidget(q4Edit, 2, 3)
                    
                    grid.addWidget(QLabel('Calculation'), 3, 0)
                    grid.addWidget(q5Edit, 3, 1)
                    
                    grid.addWidget(QLabel('Icalculation'), 3, 2)
                    grid.addWidget(q10Edit, 3, 3)
                
                    grid.addWidget(QLabel('Article description'), 4, 0)
                    grid.addWidget(q3Edit, 4 ,1, 1, 3) 
                                             
                    grid.addWidget(QLabel('Purchase order number'), 5, 0)
                    grid.addWidget(q6Edit, 5, 1)
                                                      
                    grid.addWidget(QLabel('Quantity'), 5, 2)
                    grid.addWidget(q17Edit, 5, 3)
                    
                    grid.addWidget(QLabel('Article stock'), 6, 0)
                    grid.addWidget(q18Edit, 6, 1)
                
                    grid.addWidget(QLabel('Reservation balance'), 6, 2)
                    grid.addWidget(q7Edit, 6, 3)
                
                    grid.addWidget(QLabel('Reservation date'), 7, 0)
                    grid.addWidget(q8Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Order balance'), 7, 2)
                    grid.addWidget(q16Edit, 7, 3)
                
                    grid.addWidget(QLabel('Delivery start'), 8, 0)
                    grid.addWidget(q9Edit, 8, 1) 
                                                          
                    grid.addWidget(QLabel('Delivery end'), 8, 2)
                    grid.addWidget(q11Edit, 8, 3)
                    
                    grid.addWidget(QLabel('Category'), 9,0)
                    grid.addWidget(q13Edit, 9, 1)
                    
                    grid.addWidget(QLabel('Article price'), 9, 2)
                    grid.addWidget(q14Edit, 9, 3)
                                     
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 4, Qt.AlignCenter)
                       
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 10, 3, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial", 10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                  
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 350, 300)
                    
            window = Widget()
            window.exec_()
                                
    win = MyWindow(data_list, header)
    win.exec_()
    resKeuze(m_email)    