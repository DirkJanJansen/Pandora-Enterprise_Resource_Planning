from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
  QDialog, QMessageBox, QComboBox, QWidget, QTableView, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QAbstractTableModel
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine, select, update, false, and_)

def refresh(keuze, zoekterm, m_email, self):
    self.close()
    toonAfdrachten(keuze, zoekterm, m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearchterm!')
    msg.setWindowTitle('Contributions payments')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def betalingGelukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Payment is booked!')
    msg.setWindowTitle('Contributions payments')
    msg.exec_()

def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Contributions payments")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
                              
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(250)
            k0Edit.setFont(QFont("Arial", 10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Request/Pay contributions')
            k0Edit.addItem('1. Sorted by period')
            k0Edit.addItem('2. Filtered by time period')
            k0Edit.addItem('3. Filtered by not payed')
            k0Edit.addItem('4. Filtered by authority')
            k0Edit.addItem('5. Filtered by booking date')
            k0Edit.addItem('6. Filtered by counter sales')
            k0Edit.addItem('7. Filtered by online orders')
            
            k0Edit.activated[str].connect(self.k0Changed)
    
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(150)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 1)
            lbl1 = QLabel('Sear term')
            grid.addWidget(lbl1, 2, 1)
            grid.addWidget(zktermEdit, 2, 1, 1, 1, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(closeBtn, 3, 1)
            closeBtn.setFont(QFont("Arial", 10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
               
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
    toonAfdrachten(keuze, zoekterm, m_email)
    
def toonAfdrachten(keuze, zoekterm, m_email):         
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Contributions Requesting/Paying')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0, 1, 16)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 15, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Refresh')
            freshBtn.clicked.connect(lambda: refresh(keuze, zoekterm, m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 14, 1, 1, Qt.AlignRight)
        
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 13, 1, 1, Qt.AlignRight)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 0, 1, 16, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(10, 30, 1900, 900)
            self.setLayout(grid)
    
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
        
    header = ['Contrib. number', 'Type contribution', 'Amount        ', 'Booking date', 'Pay date',\
              'Pay status', 'Authority','Employer', 'Work number', 'Work order',\
              'Account number', 'Payment over period', 'Supplier order', 'OrderID']
    metadata = MetaData()   
    afdrachten = Table('afdrachten', metadata,
        Column('afdrachtID', Integer(), primary_key=True),
        Column('soort', String),
        Column('bedrag', Float),
        Column('boekdatum', String),
        Column('betaaldatum', String),
        Column('betaalstatus', String),
        Column('instantie', String),
        Column('werknemerID', Integer),
        Column('werknummerID', Integer),
        Column('werkorderID', Integer),
        Column('rekeningnummer', String),
        Column('periode', String),
        Column('inkoopordernummer', Integer),
        Column('ovbestelID', Integer))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
       selafdr = select([afdrachten]).order_by(afdrachten.c.periode,\
                       afdrachten.c.instantie).order_by(afdrachten.c.afdrachtID)
       rpafdr = con.execute(selafdr)
    elif keuze == 2:
        selafdr = select([afdrachten]).where(afdrachten.c.periode.like(zoekterm+'%'))
        rpafdr = con.execute(selafdr)
    elif keuze == 3:
        selafdr = select([afdrachten]).where(afdrachten.c.betaalstatus == false()).\
          order_by(afdrachten.c.periode, afdrachten.c.instantie)
        rpafdr = con.execute(selafdr)
    elif keuze == 4:
        selafdr = select([afdrachten]).where(afdrachten.c.instantie.ilike('%'+zoekterm+'%')).\
          order_by(afdrachten.c.periode, afdrachten.c.instantie)
        rpafdr = con.execute(selafdr)
    elif keuze == 5:
        selafdr = select([afdrachten]).where(afdrachten.c.boekdatum.like(zoekterm+'%')).\
          order_by(afdrachten.c.boekdatum)
        rpafdr = con.execute(selafdr)
    elif keuze == 6:
        selafdr = select([afdrachten]).where(and_(afdrachten.c.ovbestelID<500000000,\
          afdrachten.c.ovbestelID>0)).order_by(afdrachten.c.ovbestelID)
        rpafdr = con.execute(selafdr)
    elif keuze == 7:
        selafdr = select([afdrachten]).where(afdrachten.c.ovbestelID>499999999).\
          order_by(afdrachten.c.ovbestelID)
        rpafdr = con.execute(selafdr)
    else:
        ongInvoer()
        zoeken(m_email)
   
    data_list=[]
    for row in rpafdr:
        data_list += [(row)]
        
    def showSelection(idx):
        mafdrnr = idx.data()
        if idx.column() == 0:
            mbetaald = str(datetime.datetime.now())[0:10]
            metadata = MetaData()   
            afdrachten = Table('afdrachten', metadata,
                Column('afdrachtID', Integer(), primary_key=True),
                Column('soort', String),
                Column('bedrag', Float),
                Column('boekdatum', String),
                Column('betaaldatum', String),
                Column('betaalstatus', Boolean),
                Column('instantie', String),
                Column('werknemerID', Integer),
                Column('werknummerID', Integer),
                Column('werkorderID', Integer),
                Column('rekeningnummer', String),
                Column('periode', String),
                Column('inkoopordernummer', Integer),
                Column('ovbestelID', Integer))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selbet = select([afdrachten]).where(afdrachten.c.afdrachtID == mafdrnr)
            rpbet = con.execute(selbet).first()
                  
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Pay contribution bill")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignCenter)
                    
                    self.Soort = QLabel()
                    q1Edit = QLineEdit(rpbet[1])
                    q1Edit.setFixedWidth(250)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    self.Bedrag = QLabel()
                    q2Edit = QLineEdit(str(round(float(rpbet[2]),2)))
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setFixedWidth(150)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    self.Boekdatum = QLabel(mbetaald)
                    q3Edit = QLineEdit(str(rpbet[3]))
                    q3Edit.setFixedWidth(150)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    self.Betaaldatum = QLabel()
                    q4Edit = QLineEdit(str(rpbet[4]))
                    q4Edit.setFixedWidth(150)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                                 
                    self.Instantie = QLabel()
                    q5Edit = QLineEdit(rpbet[6])
                    q5Edit.setFixedWidth(250)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    self.Werknemer = QLabel()
                    q6Edit = QLineEdit(str(rpbet[7]))
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setFixedWidth(150)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    self.Werknummer = QLabel()
                    q7Edit = QLineEdit(str(rpbet[8]))
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setFixedWidth(150)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    self.Werkorder = QLabel()
                    q8Edit = QLineEdit(str(rpbet[9]))
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setFixedWidth(150)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    self.Rekeningnummer = QLabel()
                    q9Edit = QLineEdit(str(rpbet[10]))
                    q9Edit.setFixedWidth(250)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                    
                    self.Periode = QLabel()
                    q10Edit = QLineEdit(str(rpbet[11]))
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setFixedWidth(150)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                    
                    self.Inkooporder = QLabel()
                    q11Edit = QLineEdit(str(rpbet[12]))
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.setFixedWidth(150)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                                                  
                    self.Verkooporder = QLabel()
                    q12Edit = QLineEdit(str(rpbet[13]))
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setFixedWidth(150)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)    
                
                    lbl1 = QLabel('Contribution number')
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(str(mafdrnr))
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Type')
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q1Edit, 2, 1)
                                                         
                    lbl4 = QLabel('Amount')
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q2Edit, 3, 1)
                    
                    lbl5 = QLabel('Booking date')
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q3Edit, 4, 1)
                    
                    lbl6 = QLabel('Pay date')
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q4Edit, 5, 1)
                    
                    cBox = QCheckBox('Pay')
                    cBox.stateChanged.connect(self.cBoxChanged)
                    grid.addWidget(cBox, 5, 2)
                    if len(rpbet[4])==10:
                       cBox.setEnabled(False)
                    
                    lbl7 = QLabel('Authority')
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q5Edit, 6, 1, 1, 2)
                    
                    lbl8 = QLabel('Employee')
                    lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl8, 7, 0)
                    grid.addWidget(q6Edit, 7, 1)
                    
                    lbl9 = QLabel('Work number')
                    lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl9, 8, 0)
                    grid.addWidget(q7Edit, 8, 1)
                    
                    lbl10 = QLabel('Work order')
                    lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl10, 9, 0)
                    grid.addWidget(q8Edit, 9, 1)
                    
                    lbl20 = QLabel('Account number')
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 10, 0)
                    grid.addWidget(q9Edit, 10, 1, 1, 2)
                      
                    lbl21 = QLabel('Period')
                    lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl21, 11, 0)
                    grid.addWidget(q10Edit, 11, 1)
                    
                    lbl22 = QLabel('Supplier order')
                    lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl22, 12, 0)
                    grid.addWidget(q11Edit, 12, 1)
                       
                    lbl23 = QLabel('OrderID')
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 13, 0)
                    grid.addWidget(q12Edit, 13, 1)
                   
                    btlBtn = QPushButton('Paying')
                    btlBtn.clicked.connect(self.accept)
            
                    grid.addWidget(btlBtn, 14, 2, 1 , 1, Qt.AlignRight)
                    btlBtn.setFont(QFont("Arial",10))
                    btlBtn.setFixedWidth(100)
                    btlBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    sluitBtn = QPushButton('Close')
                    sluitBtn.clicked.connect(self.close)
            
                    grid.addWidget(sluitBtn, 14, 1, 1, 1, Qt.AlignRight)
                    sluitBtn.setFont(QFont("Arial",10))
                    sluitBtn.setFixedWidth(100)
                    sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 2, Qt.AlignCenter)
                                 
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)
                                               
                state = False  
                def cBoxChanged(self, state):
                    if state == Qt.Checked:
                        self.state = True
                        
                def returncBox(self):
                      return self.state
                       
                @staticmethod
                def getData(parent=None):
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returncBox()] 
            
            mainWin = MainWindow()
            data = mainWin.getData()
                 
            if data[0]:
                mstatus = True
            else:
                return()
            if mstatus:
                  updafdr = update(afdrachten).where(afdrachten.c.afdrachtID == mafdrnr).\
                   values(betaaldatum = mbetaald, betaalstatus = mstatus)
                  con.execute(updafdr)
                  betalingGelukt()
                  con.close
        
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)