from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import  QPushButton, QWidget, QDialog, QComboBox, QLineEdit,\
                   QLabel, QGridLayout, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, and_

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request employees')               
    msg.exec_() 
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request employees')               
    msg.exec_() 

def accKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request accounts")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Search sort key')
            k0Edit.addItem('1. All employees')
            k0Edit.addItem('2. Surname')
            k0Edit.addItem('3. Per pay table number.')
            k0Edit.addItem('4. Account number.')
            k0Edit.addItem('5. Table wages/hour <.')
            k0Edit.addItem('6. Table wages/hour >.')
            k0Edit.addItem('7. Monthly wages indirect staff >.')           
            k0Edit.addItem('8. Employment (yyyy(-mm-dd))')
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
            grid.addWidget(lbl , 1, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 2, 1)
            lbl1 = QLabel('Search term')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 6, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 6, 1)
            cancelBtn.setFont(QFont("Arial", 10))
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
    toonWerknemers(keuze,zoekterm, m_email)
   
def toonWerknemers(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    werknemers = Table('werknemers', metadata,
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('werknemerID', Integer(), primary_key=True),
        Column('loonID', None, ForeignKey('lonen.loonID')), 
        Column('loontrede', Integer),
        Column('loonheffing', Float),
        Column('pensioenpremie', Float),
        Column('reservering_vakantietoeslag', Float),
        Column('werkgevers_pensioenpremie', Float),
        Column('periodieke_uitkeringen', Float),
        Column('overige_inhoudingen', Float),
        Column('overige_vergoedingen', Float),
        Column('bedrijfsauto', Float),
        Column('reiskosten_vergoeding', Float),
        Column('indienst', String),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('aanhef', String(8)),
        Column('voornaam', String(30), nullable=False), 
        Column('tussenvoegsel', String(10)),
        Column('achternaam', String(50), nullable=False),
        Column('geboortedatum', String))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('reisuur', Float),
        Column('maandloon', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    if keuze == 1:
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID)).order_by(werknemers.c.accountID)
    elif keuze == 2:
       selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, accounts.c.achternaam.\
                     ilike('%'+zoekterm+'%'))).order_by(werknemers.c.accountID)
    elif keuze == 3 and validZt.zt(zoekterm, 13):
       selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, werknemers.c.loonID == int(zoekterm))).\
                        order_by(werknemers.c.loonID, werknemers.c.accountID)
    elif keuze == 4 and validZt.zt(zoekterm, 1):
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, werknemers.c.accountID == int(zoekterm)))
    elif keuze == 5 and validZt.zt(zoekterm, 14):
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, lonen.c.tabelloon < int(zoekterm))).\
                         order_by(lonen.c.tabelloon)
    elif keuze == 6 and validZt.zt(zoekterm, 14):
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, lonen.c.tabelloon > int(zoekterm))).\
                         order_by(lonen.c.tabelloon)
    elif keuze == 7 and validZt.zt(zoekterm, 14):
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, lonen.c.maandloon > int(zoekterm))).\
                         order_by(lonen.c.tabelloon)
    elif keuze == 8 and validZt.zt(zoekterm, 10):
        selwerkn = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID == accounts.c.accountID,
                     werknemers.c.loonID == lonen.c.loonID, werknemers.c.indienst.\
                     like(zoekterm+'%'))).order_by(werknemers.c.indienst)
    else:
        ongInvoer()
        accKeuze(m_email)
        
    if conn.execute(selwerkn).fetchone():
        rpwerkn = conn.execute(selwerkn)
    else:
        geenRecord()
        accKeuze(m_email)
        
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1600, 900)
            self.setWindowTitle('Request employee data')
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
            table_view.setColumnHidden(16,True)   
            table_view.clicked.connect(showWerknemer)
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
       
    header = ['Account number', 'Employee number', 'Payscale', 'Wages step', 'Payroll tax',\
          'Pension contribution', 'Res. Holiday surcharge', 'Employer pension contribution', 'Periodic payment.',\
          'Other deductions', 'Other fees','Company car addition',\
          'Travel compensation', 'Entry into service date', 'Leave balance', 'Extra leave',\
          'Accountnumber', 'Prefix', 'First name', 'Infix', 'Surname',\
          'Date of birth', 'Pay scale', 'Table wages', 'Travel hourly wages', 'Monthly salary']    
        
    data_list=[]
    for row in rpwerkn:
        data_list += [(row)] 
        
    def showWerknemer(idx):
        maccountnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            conn = engine.connect()
            selwrknmr = select([werknemers, accounts, lonen]).where(and_(werknemers.c.accountID\
                  == maccountnr, werknemers.c.accountID == accounts.c.accountID,\
                  lonen.c.loonID == werknemers.c.loonID))
            rpwrknmr = conn.execute(selwrknmr).first()
                                                   
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Request employee data")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                        
                    self.Accountnummer = QLabel()
                    q2Edit = QLineEdit(str(maccountnr))
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setFixedWidth(100)
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
        
                    self.Loontabelnummer = QLabel()
                    q4Edit = QLineEdit(str(rpwrknmr[2]))
                    q4Edit.setFixedWidth(30)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
         
                    self.Loontrede = QLabel()
                    q5Edit = QLineEdit(str(rpwrknmr[3]))
                    q5Edit.setFixedWidth(30)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)                              
                    
                    self.Reiskostenvergoeding = QLabel()
                    q8Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[12]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                                                         
                    self.Auto = QLabel()
                    q18Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[11]))
                    q18Edit.setFixedWidth(100)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                      
                    self.Periodiekeuitkering = QLabel()
                    q12Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    self.Overigeinhoudingen = QLabel()
                    q13Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[9]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
             
                    self.Overigevergoedingen = QLabel()
                    q19Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[10]))
                    q19Edit.setFixedWidth(100)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
             
                    self.Indienst = QLabel()
                    q14Edit = QLineEdit(rpwrknmr[13])
                    q14Edit.setFixedWidth(100)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
 
                    self.Maandloon = QLabel()
                    q15Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[25]*(1+(rpwrknmr[3]*3/100))))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
          
                    self.Verlofsaldo = QLabel()
                    q16Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[14]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
         
                    self.ExtraVerlof = QLabel()
                    q17Edit = QLineEdit('{:12.2f}'.format(rpwrknmr[15]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,1 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 1, 3, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Request employee data from\n'+rpwrknmr[18]+\
                    ' '+rpwrknmr[19]+' '+rpwrknmr[20]+'\nData of birth: '+rpwrknmr[21]), 1, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Gross monthly salary'), 3, 2)
                    grid.addWidget(q15Edit, 3, 3) 
                                                        
                    grid.addWidget(QLabel('Account number'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1)
                    
                    grid.addWidget(QLabel('Wages table'), 6, 0)
                    grid.addWidget(q4Edit, 6 , 1) 
                     
                    grid.addWidget(QLabel('Wages step'), 7, 0)
                    grid.addWidget(q5Edit, 7, 1)
                                                              
                    grid.addWidget(QLabel('Travel compensation'), 4, 2)
                    grid.addWidget(q8Edit, 4, 3)
                                              
                    grid.addWidget(QLabel('Periodic payment taxed'), 5, 0)
                    grid.addWidget(q12Edit, 5, 1) 
                    
                    grid.addWidget(QLabel('Other deductions tax-free'), 5, 2)
                    grid.addWidget(q13Edit, 5, 3) 
                    
                    grid.addWidget(QLabel('Addition Company car'), 4, 0)
                    grid.addWidget(q18Edit, 4, 1) 
                                   
                    grid.addWidget(QLabel('Other Fees\non-taxed'), 6, 2)
                    grid.addWidget(q19Edit, 6, 3) 
               
                    grid.addWidget(QLabel('Date of entry into service'), 8, 0)
                    grid.addWidget(q14Edit, 8, 1) 
                    
                    grid.addWidget(QLabel('Leave balance in hours'), 7, 2)
                    grid.addWidget(q16Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Extra leave in hours'), 8, 2)
                    grid.addWidget(q17Edit, 8, 3)
                    
                    grid.addWidget(QLabel('Hourly wages'), 9, 0)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[23])), 9, 1, 1, 1, Qt.AlignRight) 
                    grid.addWidget(QLabel('Travel hourly wages'), 9, 2)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[24])), 9, 3, 1, 1, Qt.AlignRight)
                    grid.addWidget(QLabel('Pension contribution'), 10, 0)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[5])), 10, 1, 1, 1, Qt.AlignRight) 
                    grid.addWidget(QLabel('Reservation holiday allowance'), 10, 2)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[6])), 10, 3, 1, 1, Qt.AlignRight)
                    grid.addWidget(QLabel('Employer pension contribution'), 11, 0)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[7])), 11, 1, 1, 1, Qt.AlignRight) 
                    grid.addWidget(QLabel('Payroll tax'), 11, 2)
                    grid.addWidget(QLabel('{:12.2f}'.format(rpwrknmr[4])), 11, 3, 1, 1, Qt.AlignRight)
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 350, 300)
                                               
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 12, 3)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_()
                                   
    win = MyWindow(data_list, header)
    win.exec_()
    accKeuze(m_email)