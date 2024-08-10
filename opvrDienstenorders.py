from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import  QLabel, QPushButton, QWidget, QGridLayout,\
     QComboBox, QDialog, QLineEdit, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, ForeignKey,  Integer, String, MetaData,\
                       create_engine, Float)
from sqlalchemy.sql import select, and_ 

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request service orders')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request service orders')               
    msg.exec_() 

def inkooporderKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request Purchase Order Services")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(330)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                Search sort key')
            k0Edit.addItem('1. All service orders sorted by work number')
            k0Edit.addItem('2. Filtered by company name')
            k0Edit.addItem('3. Filtered by external work name')
            k0Edit.addItem('4. Filtered by external work number')
            k0Edit.addItem('5. Filtered on purchase order number.')
            k0Edit.addItem('6. Delivery date yyyy(-mm(-dd))')
            k0Edit.activated[str].connect(self.k0Changed)
                            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(220)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 0, 1, 3, Qt.AlignRight)
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1, 1, 1, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
         
            grid.addWidget(applyBtn, 3, 1, 1, 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(110)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))   
            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(110)
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
    opvrDienstorders(keuze,zoekterm, m_email)
    
def opvrDienstorders(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer(), primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
        Column('besteldatum', String),
        Column('goedgekeurd', String),
        Column('betaald', String),
        Column('afgemeld', String))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String))
    orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
        Column('orddienstlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('werkomschr', String),
        Column('omschrijving', String),
        Column('aanneemsom', Float),
        Column('plan_start', String),
        Column('werk_start', String),
        Column('plan_gereed', String),
        Column('werk_gereed', String),
        Column('acceptatie_gereed', Float),
        Column('acceptatie_datum', String),
        Column('meerminderwerk', Float),
        Column('regel', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('werkomschrijving', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
 
    if keuze == 1:
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken]).\
         where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
           leverancierID, orders_inkoop_diensten.c.werknummerID == werken.c.\
           werknummerID, orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.\
           orderinkoopID)).order_by(orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 2:
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
        .where(and_(orders_inkoop_diensten.c.orderinkoopID==orders_inkoop.c.orderinkoopID,\
          orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
          orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
          leveranciers.c.bedrijfsnaam.ilike('%'+zoekterm+'%'))).order_by\
           (orders_inkoop.c.leverancierID, orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 3:
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          werken.c.werkomschrijving.ilike('%'+zoekterm+'%'))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 4 and validZt.zt(zoekterm, 8):
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          werken.c.werknummerID == int(zoekterm))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 5 and validZt.zt(zoekterm, 4):
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
            orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_diensten.c.orderinkoopID == int(zoekterm))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_diensten.c.plan_gereed.like(zoekterm+'%'))).order_by\
         (orders_inkoop_diensten.c.plan_gereed, orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    else:
        ongInvoer()
        inkooporderKeuze(m_email)
        
    if con.execute(sel).fetchone():
        rpinkorders = con.execute(sel)
    else:
        geenRecord()
        inkooporderKeuze(m_email)
                                     
    class Window(QDialog):
       def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1600, 900)
            self.setWindowTitle('Request purchase orders services')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnHidden(2,True)
            table_view.setColumnHidden(14,True)
            table_view.setColumnHidden(15,True)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showOrder)
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
       
    header = ['Order purchasing\nservice number','Order purchase number', 'Work number','Type of service', 'Serve description', 'Contract price',\
          'Planned start', 'Real start','Planned ready', 'Real ready', 'Acceptance ready', 'Acceptance date', 'More-less work',\
          'Line number', 'Order purchase number','Supplier', 'Order date', 'Approved', 'Payed',\
          'Unsubscribed','Supplier number', 'Supplier name' ,'Legal status','Work number','Work description']
        
    data_list=[]
    for row in rpinkorders:
        data_list += [(row)] 
        
    def showOrder(idx):
        mordinkdnst = idx.data()
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        if idx.column() == 0:
            selorddnst = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
                .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
                leverancierID, orders_inkoop_diensten.c.werknummerID == werken.c.\
                werknummerID, orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.\
                orderinkoopID, orders_inkoop_diensten.c.orddienstlevID == mordinkdnst))
            rporddnst = con.execute(selorddnst).first() 
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Request purchase orders services")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                        
                    self.Orderinkoopdienst = QLabel()
                    q2Edit = QLineEdit(str(rporddnst[14]))
                    q2Edit.setFixedWidth(90)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
        
                    self.Leveranciernummer = QLabel()
                    q4Edit = QLineEdit(str(rporddnst[15]))
                    q4Edit.setFixedWidth(90)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
         
                    self.Besteldatum = QLabel()
                    q5Edit = QLineEdit(str(rporddnst[16]))
                    q5Edit.setFixedWidth(90)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)                              
                    
                    self.Goedgekeurd = QLabel()
                    q8Edit = QLineEdit(str(rporddnst[17]))
                    q8Edit.setFixedWidth(90)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                                                         
                    self.Betaald = QLabel()
                    q18Edit = QLineEdit(str(rporddnst[18]))
                    q18Edit.setFixedWidth(90)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                      
                    self.Afgemeld = QLabel()
                    q12Edit = QLineEdit(str(rporddnst[19]))
                    q12Edit.setFixedWidth(90)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    self.Leveranciernummer = QLabel()
                    q13Edit = QLineEdit(str(rporddnst[20]))
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setFixedWidth(100)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
             
                    self.Bedrijfsnaam = QLabel()
                    q19Edit = QLineEdit(str(rporddnst[21]))
                    q19Edit.setFixedWidth(380)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
             
                    self.Rechtsvorm = QLabel()
                    q14Edit = QLineEdit(str(rporddnst[22]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                                    
                    self.Werknummer = QLabel()
                    q15Edit = QLineEdit(str(rporddnst[23]))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
          
                    self.Werkomschrijving = QLabel()
                    q16Edit = QLineEdit(str(rporddnst[24]))
                    q16Edit.setFixedWidth(390)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
         
                    self.Dienstomschrijving = QLabel()
                    q17Edit = QLineEdit(str(rporddnst[4]))
                    q17Edit.setFixedWidth(390)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    self.Dienstsoort = QLabel()
                    q11Edit = QLineEdit(str(rporddnst[3]))
                    q11Edit.setFixedWidth(390)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                    
                    self.Aanneemsom = QLabel()
                    q20Edit = QLineEdit('{:12.2f}'.format(rporddnst[5]))
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setFixedWidth(100)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                    
                    self.Planstart = QLabel()
                    q21Edit = QLineEdit(str(rporddnst[6]))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q21Edit.setDisabled(True)
    
                    self.Werkelijkstart = QLabel()
                    q22Edit = QLineEdit(str(rporddnst[7]))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q22Edit.setDisabled(True)
    
                    self.Plangereed = QLabel()
                    q23Edit = QLineEdit(str(rporddnst[8]))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q23Edit.setDisabled(True)
                    
                    self.Werkelijkgereed = QLabel()
                    q24Edit = QLineEdit(str(rporddnst[9]))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q24Edit.setDisabled(True)
                    
                    self.AcceptatieaantaL = QLabel()
                    q25Edit = QLineEdit('{:12.2f}'.format(rporddnst[10]))
                    q25Edit.setFixedWidth(100)
                    q25Edit.setAlignment(Qt.AlignRight)
                    q25Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q25Edit.setDisabled(True)
                    
                    self.Acceptatiedatum = QLabel()
                    q26Edit = QLineEdit(str(rporddnst[11]))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q26Edit.setDisabled(True)
                    
                    self.Meerminderwerk = QLabel()
                    q27Edit = QLineEdit('{:12.2f}'.format(rporddnst[12]))
                    q27Edit.setFixedWidth(100)
                    q27Edit.setAlignment(Qt.AlignRight)
                    q27Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q27Edit.setDisabled(True) 
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 5, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    
                    lbl1 = QLabel('Order data')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(QLabel('Order purchase number'), 2, 0)
                    grid.addWidget(q2Edit, 2, 1) 
                                                        
                    grid.addWidget(QLabel('Supplier number'), 2, 2)
                    grid.addWidget(q4Edit, 2, 3)
                    
                    grid.addWidget(QLabel('Order date'), 2, 4)
                    grid.addWidget(q5Edit, 2 , 5) 
                     
                    grid.addWidget(QLabel('Approved'), 3, 0)
                    grid.addWidget(q8Edit, 3, 1)
                                                              
                    grid.addWidget(QLabel('Payed'), 3, 2)
                    grid.addWidget(q18Edit, 3, 3)
                                              
                    grid.addWidget(QLabel('Unsubscribed'), 3, 4)
                    grid.addWidget(q12Edit, 3, 5)
     
                    lbl2 = QLabel('Order line data'+' - line number: '+str(rporddnst[13]))
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")               
                    grid.addWidget(lbl2, 5, 0, 1, 4)
                    grid.addWidget(QLabel('Supplier number'), 6, 0)
                    grid.addWidget(q13Edit, 6, 1) 
                    
                    grid.addWidget(QLabel('Company name'), 7, 0)
                    grid.addWidget(q19Edit, 7, 1, 1, 4) 
                                   
                    grid.addWidget(q14Edit, 7, 4) 
               
                    grid.addWidget(QLabel('Work number'), 8, 0)
                    grid.addWidget(q15Edit, 8, 1) 
                                                           
                    grid.addWidget(QLabel('Work description'), 9, 0)
                    grid.addWidget(q16Edit, 9, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Service description'), 10, 0)
                    grid.addWidget(q17Edit, 10, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Type of service'), 11, 0)
                    grid.addWidget(q11Edit, 11, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Contract price'), 12, 0)
                    grid.addWidget(q20Edit, 12, 1)
                                    
                    grid.addWidget(QLabel('Planned start'), 12, 2)
                    grid.addWidget(q21Edit, 12, 3)
                    
                    grid.addWidget(QLabel('Real start'), 12, 4)
                    grid.addWidget(q22Edit, 12, 5)
                    
                    grid.addWidget(QLabel('Planned ready'), 13, 0)
                    grid.addWidget(q23Edit, 13, 1)
                    
                    grid.addWidget(QLabel('Real ready'), 13, 2)
                    grid.addWidget(q24Edit, 13, 3)
                    
                    grid.addWidget(QLabel('Acceptance ready'), 14,  0)
                    grid.addWidget(q25Edit, 14, 1)
                    
                    grid.addWidget(QLabel('Acceptance date'), 14, 2)
                    grid.addWidget(q26Edit, 14, 3)
                   
                    grid.addWidget(QLabel('More-less work\nprovisional sum'), 14, 4)
                    grid.addWidget(q27Edit, 14, 5)
                                                                            
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 0, 1, 6, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 350, 300)
                                               
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 15, 5, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_()
                                   
    win = Window(data_list, header)
    win.exec_()
    inkooporderKeuze(m_email)