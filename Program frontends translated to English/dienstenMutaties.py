from login import hoofdMenu
import datetime

from PyQt5.QtCore import Qt, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox,\
     QMessageBox, QLineEdit, QGridLayout, QDialog, QComboBox, QWidget, QTableView
from sqlalchemy import (Table, Column, String,  Integer, Float, MetaData, \
                            ForeignKey, create_engine, insert, select, update, func, and_, or_)

def refresh(keuze, zoekterm, m_email, self):
    self.close()
    toonMutaties(keuze,zoekterm, m_email)

def _11check(mcontr):
    number = str(mcontr)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False
           
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Entry')
    msg.exec_()
    
def foutCombinatie():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Warning)
        msg.setText('The combination of purchase order,\ncost type and order line\n does not occur!')
        msg.setWindowTitle('Entry incorrect')
        msg.exec_()
       
def foutInkooporder():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Incorrect purchase order\nopted!')
        msg.setWindowTitle('Entry incorrect')
        msg.exec_()
               
def foutWerk():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Incorrect work number\nopted!')
        msg.setWindowTitle('Entry incorrect')
        msg.exec_()
 
def geenSoort():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No cost type chosen')
    msg.setWindowTitle('Entry incorrect')
    msg.exec_()
       
def geenRegel():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No line number entered')
    msg.setWindowTitle('Entry incorrect')
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Publishing/printing materials')
    msg.exec_() 
  
def geenKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No cost type\nchoice made')
    msg.setWindowTitle('Entry incorrect')
    msg.exec_()    
    
def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Work number is unsubscribed,\n bookings no longer possible!')
    msg.setWindowTitle('Data!')
    msg.exec_()
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearchterm!')
    msg.setWindowTitle('Request articles')
    msg.exec_()
    
def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def mutatieKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Request changes services-portal accounting")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Search sort key')
            k0Edit.addItem('1. All services')
            k0Edit.addItem('2. Worknumber')
            k0Edit.addItem('3. Workdescription')
            k0Edit.addItem('4. Suppliernumber')
            k0Edit.addItem('5. Companyname')
            k0Edit.addItem('6. By salesorder')
            k0Edit.addItem('7. Cost type (1-9)')
            
            k0Edit.activated[str].connect(self.k0Changed)
                            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(230)
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
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3 , Qt.AlignCenter)
   
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
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

def toonMutaties(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
        Column('orddienstlevID', Integer, primary_key=True),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('acceptatie_gereed', Float),
        Column('acceptatie_datum', String),
        Column('werkomschr', String),
        Column('omschrijving', String),
        Column('meerminderwerk', Integer),
        Column('aanneemsom', Float),
        Column('regel', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('werkomschrijving', String(50)))
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer, primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer, primary_key=True),
        Column('bedrijfsnaam',  String),
        Column('rechtsvorm', String))
                    
    engine = create_engine('postgresql://postgres@localhost/bisystem')
    conn = engine.connect()
   
    if keuze == 1:
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
           .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID))\
            .order_by(werken.c.werknummerID)
    elif keuze == 2 and validZt.zt(zoekterm, 8):
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
           werken.c.werknummerID== int(zoekterm)))
    elif keuze == 3:
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
           werken.c.werkomschrijving.ilike('%'+zoekterm+'%')))\
           .order_by(werken.c.werknummerID)
    elif keuze == 4 and validZt.zt(zoekterm, 3):
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
           leveranciers.c.leverancierID == int(zoekterm)))
    elif keuze == 5:
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
           leveranciers.c.bedrijfsnaam.ilike('%'+zoekterm+'%')))
    elif keuze == 6 and validZt.zt(zoekterm, 5):
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
            orders_inkoop.c.orderinkoopID== int(zoekterm)))
    elif keuze == 7 and validZt.zt(zoekterm, 16):
        sel = select([orders_inkoop_diensten, werken, orders_inkoop, leveranciers])\
         .where(and_(werken.c.werknummerID==orders_inkoop_diensten.c.werknummerID,\
            leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,\
            orders_inkoop.c.orderinkoopID==orders_inkoop_diensten.c.orderinkoopID,\
           orders_inkoop_diensten.c.werkomschr.like(zoekterm+'%')))\
           .order_by(orders_inkoop_diensten.c.werkomschr)
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
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Mutate costs services')
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
            table_view.setColumnHidden(13, True)
            table_view.setColumnHidden(7, True)
            table_view.clicked.connect(dienstenMut)
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
            self.setGeometry(50, 50, 1800, 900)
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
  
    header = ['Mutation number','Work number', 'Order PurchaseID','Amount booking', 'Booking date', 'Category',\
              'Category-Description','VAT-high', 'Contract price', 'Line number', 'Work number', 'Description',\
              'Order PurchaseID', 'SupplierID', 'SupplierID','Company name', 'Legal status']
    
    data_list=[]
    for row in rp:
        data_list += [(row)] 
    
    def dienstenMut(idx):
        mordinkdnst = idx.data()
        metadata = MetaData()
        orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
            Column('orddienstlevID', Integer, primary_key=True),
            Column('werknummerID', None, ForeignKey('werken.werknummerID')),
            Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
            Column('acceptatie_gereed', Float),
            Column('acceptatie_datum', String),
            Column('werkomschr', String),
            Column('omschrijving', String),
            Column('meerminderwerk', Integer),
            Column('aanneemsom', Float),
            Column('regel', Integer))
        
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        if idx.column() == 0:
            selorddnst = select([orders_inkoop_diensten]).where(orders_inkoop_diensten.c.\
            orddienstlevID == mordinkdnst)
            rporddnst = con.execute(selorddnst).first() 
            mwerknr = rporddnst[1]
            msoort = rporddnst[5]
            momschr = rporddnst[6]
            mregel = rporddnst[9]
            minkordernr = rporddnst[2]
          
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Mutate costs services")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            
                    self.setFont(QFont('Arial', 10))
                                
                    self.Werknummer = QLabel()
                    zkwerknEdit = QLineEdit(str(mwerknr))
                    zkwerknEdit.setAlignment(Qt.AlignRight)
                    zkwerknEdit.setFixedWidth(150)
                    zkwerknEdit.setFont(QFont("Arial",10))
                    zkwerknEdit.setDisabled(True)
                       
                    self.Inkoopordernummer = QLabel()
                    q1Edit = QLineEdit(str(minkordernr))
                    q1Edit.setFixedWidth(150)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.setDisabled(True)
                    
                    self.Soort = QLabel()
                    k0Edit = QLineEdit(str(msoort))
                    k0Edit.setFixedWidth(200)
                    k0Edit.setFont(QFont("Arial",10))
                    k0Edit.setDisabled(True)
                    
                    self.Bedrag = QLabel()
                    q2Edit = QLineEdit()
                    q2Edit.setFixedWidth(150)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.textChanged.connect(self.q2Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)      
            
                    self.Regel = QLabel()
                    q3Edit = QLineEdit(str(mregel))
                    q3Edit.setFixedWidth(40)
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                 
                    self.Omschrijving = QLabel()
                    q4Edit = QLineEdit(str(momschr))
                    q4Edit.setFixedWidth(400)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.textChanged.connect(self.q4Changed) 
                    reg_ex = QRegExp("^.{0,40}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q4Edit.setValidator(input_validator)
                                               
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                  
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)       
               
                    lblt = QLabel('Mutations (costs third parties) not cumulative.\nFor \'Close\' do not enter an amount.')
                    grid.addWidget(lblt , 8, 0, 1, 3, Qt.AlignCenter)
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 9, 0, 1, 3, Qt.AlignCenter )
                      
                    lbl1 = QLabel('  More/less work = Checkbox active')
                    grid.addWidget(lbl1, 7 , 1)
                    
                    lbl2 = QLabel('Work number')
                    lbl2.setAlignment(Qt.AlignRight)
                    grid.addWidget(lbl2, 1, 0)
                    grid.addWidget(zkwerknEdit,1, 1)
                    
                    q1 = QLabel('Purchase order number')
                    q1.setAlignment(Qt.AlignRight)
                    grid.addWidget(q1, 3, 0)
                    grid.addWidget(q1Edit,3, 1)  
                    
                    lbl3 = QLabel('Discipline')  
                    lbl3.setAlignment(Qt.AlignRight)
                    grid.addWidget(lbl3, 4, 0)
                    grid.addWidget(k0Edit, 4, 1)
                    
                    lbl4 = QLabel('Description')
                    lbl4.setAlignment(Qt.AlignRight)
                    grid.addWidget(lbl4, 5, 0)
                    grid.addWidget(q4Edit, 5, 1, 1, 3)   
                    
                    lbl5 = QLabel('Amount')
                    lbl5.setAlignment(Qt.AlignRight)
                    grid.addWidget(lbl5, 6, 0)
                    grid.addWidget(q2Edit,6, 1)
                    
                    lbl6 = QLabel('         Order line')
                    grid.addWidget(lbl6, 4, 2)
                    grid.addWidget(q3Edit, 4, 2, 1, 2)
                                       
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)
                               
                    applyBtn = QPushButton('Mutate\nClose')
                    applyBtn.clicked.connect(self.accept)
    
                    grid.addWidget(applyBtn, 8, 2, 1 , 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                 
                    cBox = QCheckBox('     More/less work')
                    cBox.stateChanged.connect(self.cBoxChanged)
                    grid.addWidget(cBox, 6, 2)
                      
                def q2Changed(self,text):
                    self.Bedrag.setText(text)
                    
                def q4Changed(self,text):
                    self.Omschrijving.setText(text)
                    
                state = False 
                def cBoxChanged(self, state):
                    if state == Qt.Checked :
                        self.state = True
                    if state == Qt.Unchecked:
                        self.state = False
                                           
                def returnq2(self):
                    return self.Bedrag.text()
        
                def returnq4(self):
                    return self.Omschrijving.text()
                           
                def returncBox(self):
                    return self.state
                                 
                @staticmethod
                def getData(parent=None):
                    dialog = Widget(parent)
                    dialog.exec_()
                    return [dialog.returnq2(), dialog.returnq4(), dialog.returncBox()]
                 
            window = Widget()
            data = window.getData()
            if data[0]:
                mbedrag = float(data[0])
            elif not data[0] or data[0] == '0':
                return()
            if data[1]:
                momschr = data[1]
            else:
                momschr = rporddnst[6]
            if data[2]:
                mmmwerk = True
            else:
                mmmwerk = False
             
            metadata = MetaData()
            werken = Table('werken', metadata,
                Column('werknummerID', Integer(), primary_key=True),
                Column('kosten_materieel', Float),
                Column('kosten_huisv', Float),
                Column('kosten_leiding', Float),
                Column('kosten_overig', Float),
                Column('kosten_vervoer', Float),
                Column('kosten_inhuur', Float),
                Column('beton_bvl', Float),
                Column('kabelwerk', Float),
                Column('grondverzet', Float),
                Column('meerminderwerk', Float),
                Column('voortgangstatus',  String))
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
            rpwerk = con.execute(selwerk).first()
            
            if rpwerk[11] == 'H':
                werkGereed()
                return('', minkordernr, mregel)
                 
            metadata = MetaData()
            dienstenmutaties = Table('dienstenmutaties', metadata,
                Column('mutatieID', Integer, primary_key=True),
                Column('werknummerID', None, ForeignKey('werken.werknummerID')),
                Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                Column('leverancierID', Float),
                Column('werkomschr', String),
                Column('boekbedrag', Float),
                Column('boekdatum', Float),
                Column('btw_hoog', Float),
                Column('btw_laag', Float),
                Column('regel', Integer),
                Column('omschrijving', String))
            orders_inkoop  = Table('orders_inkoop', metadata,
                Column('orderinkoopID', Integer, primary_key=True),
                Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')))
            orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
                Column('orddienstlevID', Integer, primary_key=True),
                Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                Column('acceptatie_gereed', Float),
                Column('acceptatie_datum', String),
                Column('werkomschr', String),
                Column('regel', Integer),
                Column('meerminderwerk', Float),
                Column('werknummerID', None, ForeignKey('werken.werknummerID')))
                              
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            
            mboekd = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
            s = select([orders_inkoop_diensten]).where(and_(orders_inkoop_diensten.c.\
              orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
              orders_inkoop_diensten.c.werkomschr == msoort, orders_inkoop_diensten.\
              c.werknummerID == mwerknr))
            rps = con.execute(s).first()
            if not rps:
                foutCombinatie() 

            elif data[0] and msoort[0] == '1' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '1. Hiring More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('1. Inhuur'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('1. Hiring'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_inhuur = werken.c.kosten_inhuur+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '1':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '1. Hiring work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('1. Inhuur'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('1. Hiring'+'%'))))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_inhuur = werken.c.kosten_inhuur+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '2' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '2. Direction More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('2. Leiding'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('2. Direction'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_leiding = werken.c.kosten_leiding+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '2':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '2. Direction work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('2. Leiding'+'%'), \
                 (orders_inkoop_diensten.c.werkomschr.ilike('2. Direction'+'%'))))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_leiding = werken.c.kosten_leiding+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '3' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '3. Housing More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('3. Huisvesting'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('3. Housing'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_huisv = werken.c.kosten_huisv+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '3':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                     type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '3. Housing work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('3. Huisvesting'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('3. Housing'+'%'))))))\
                .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_huisv = werken.c.kosten_huisv+mbedrag)
                con.execute(stmt)
                invoerOK()
 
            elif data[0] and msoort[0] == '4' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                     type_=Integer).label('mutatienr')])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '4. Cable work More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('4. Kabelwerk'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('4. Cable work'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kabelwerk = werken.c.kabelwerk+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '4':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '4. Cable work work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('4. Kabelwerk'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('4. Cable work'+'%'))))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kabelwerk = werken.c.kabelwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '5' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '5. Earth-moving More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('5. Grondverzet'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('5. Earth-moving'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(grondverzet = werken.c.grondverzet+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '5':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '5. Earth-moving work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('5. Grondverzet'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('5. Earth-moving'+'%'))))))\
                 .values(acceptatie_gereed=orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum=mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(grondverzet = werken.c.grondverzet+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '6' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '6. Concrete work More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('6. Betonwerk'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('6. Concrete work'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(beton_bvl = werken.c.beton_bvl+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '6':
                    sel = select([orders_inkoop])\
                      .where(orders_inkoop.c.orderinkoopID == minkordernr)
                    rp = con.execute(sel).first()
                    mlevnr = rp[1]
                    try:
                        mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                         type_=Integer)])).scalar())
                        mutatienr += 1
                    except:
                        mutatienr = 1
                        
                    inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                                  werknummerID = mwerknr, orderinkoopID = minkordernr,\
                                  boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                                  '6. Concrete work work-scope', leverancierID = mlevnr,\
                                  btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                    con.execute(inscb)
                    upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                     c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel, \
                     filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('6. Betonwerk'+'%'),\
                     (orders_inkoop_diensten.c.werkomschr.ilike('6. Concrete work'+'%')))))) \
                      .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                     + mbedrag, acceptatie_datum = mboekd)
                    con.execute(upd)
                    stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                       values(beton_bvl = werken.c.beton_bvl+mbedrag)
                    con.execute(stmt)
                    invoerOK()
            elif data[0] and msoort[0] == '7' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                     type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '7. Transport More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('7. Vervoer'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('7. Transport'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_vervoer = werken.c.kosten_vervoer+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '7':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                     type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '7. Transport work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('7. Vervoer'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('7. Transport'+'%'))))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_vervoer = werken.c.kosten_vervoer+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == '8' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '8. Remaining More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('8. Overig'+'%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('8. Remaining'+'%'))))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_overig = werken.c.kosten_overig+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort [0]== '8':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              '8. Remaining work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('8. Overig' + '%'),\
                 (orders_inkoop_diensten.c.werkomschr.ilike('8. Remaining'+'%'))))))\
                    .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_overig = werken.c.kosten_overig+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'A' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = int(minkordernr),\
                              boekbedrag = -mbedrag, boekdatum = mboekd, werkomschr =\
                              'A. Trencher More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel, omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 orders_inkoop_diensten.c.werkomschr.ilike('A. Sleuvengraver'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('A. Trencher'+'%')))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'A':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                        werknummerID = mwerknr, orderinkoopID = minkordernr,\
                        boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                       'A. Trencher work-scope', leverancierID = mlevnr,\
                        btw_hoog = mbedrag*.21, regel = mregel, omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('A. Sleuvengraver'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('A. Trencher'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'B' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'B. Pressing device More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('B. Persapparaat'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('B. Pressing device'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'B':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'B. Pressing device work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('B. Persapparaat' + '%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('B. Pressing device' + '%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'C' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'C. Atlas crane More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel, \
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('C. Atlaskraan'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('C. Atlas crane'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'C':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                    type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'C. Atlas crane work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('C. Atlaskraan' + '%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('C. Atlas crane'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'D' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'D. Crane big More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel, \
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('D. Kraan groot'+'%'), \
                 orders_inkoop_diensten.c.werkomschr.ilike('D. Crane big'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'D':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'D. Kraan groot work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('D. Kraan groot'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('D. Crane big'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'E' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'E. Mainliner More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 orders_inkoop_diensten.c.werkomschr.ilike('E. Mainliner'+'%')))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'E':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'E. Mainliner work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('E. Mainliner'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('E. Mainliner'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'F' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'F. Ballast clearing machine More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('F. Hormachine'+'%'),
                 orders_inkoop_diensten.c.werkomschr.ilike('F. Ballast clearing machine'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'F':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'F. Hormachine work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel, \
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('F. Hormachine'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('F. Ballast clearing machine' + '%'))))) \
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'G' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'G. Wagon More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('G. Wagon'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('G. Wagon'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'G':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'G. Wagon work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel, \
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('G. Wagon'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('G. Wagon'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'H' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'H. Locomotor More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('H. Locomotor'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('H. Locomotor'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'H':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                      type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'H. Locomotor work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('H. Locomotor'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('H. Locomotor'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'J' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'J. Locomotive More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('J. Locomotief'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('J. Locomotive'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'J':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'J. Locomotive work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('J. Locomotief'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('J. Locomotive'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'K' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'K. Assembly trolley More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('K. Montagewagen'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('K. Assembly trolley' + '%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'K':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1 
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'K. Assembly trolley work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('K. Montagewagen'+'%'),\
                orders_inkoop_diensten.c.werkomschr.ilike('K. Assembly trolley'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'L' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'L. Stormobile More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('L. Stormobiel'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('L. Stormobile'+'%')))))\
                 .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'L':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'L. Stormobile work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('L. Stormobiel'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('L. Stormobile'+'%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()            
            elif data[0] and msoort[0] == 'M' and mmmwerk:
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'M. Robel train More/less work', leverancierID = mlevnr,\
                               btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('M. Robeltrein'+'%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('M. Robel train'+'%'))))) \
                    .values(acceptatie_datum = mboekd, meerminderwerk =\
                 orders_inkoop_diensten.c.meerminderwerk + mbedrag)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag,
                       meerminderwerk = werken.c.meerminderwerk+mbedrag)
                con.execute(stmt)
                invoerOK()
            elif data[0] and msoort[0] == 'M':
                sel = select([orders_inkoop])\
                  .where(orders_inkoop.c.orderinkoopID == minkordernr)
                rp = con.execute(sel).first()
                mlevnr = rp[1]
                try:
                    mutatienr=(con.execute(select([func.max(dienstenmutaties.c.mutatieID,\
                       type_=Integer)])).scalar())
                    mutatienr += 1
                except:
                    mutatienr = 1
                    
                inscb = insert(dienstenmutaties).values(mutatieID = mutatienr,\
                              werknummerID = mwerknr, orderinkoopID = minkordernr,\
                              boekbedrag = mbedrag, boekdatum = mboekd, werkomschr =\
                              'M. Robeltrein work-scope', leverancierID = mlevnr,\
                              btw_hoog = mbedrag*.21, regel = mregel,  omschrijving = momschr)
                con.execute(inscb)
                upd = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.\
                 c.orderinkoopID == minkordernr, orders_inkoop_diensten.c.regel == mregel,\
                 filter(or_(orders_inkoop_diensten.c.werkomschr.ilike('M. Robeltrein' + '%'),\
                 orders_inkoop_diensten.c.werkomschr.ilike('M. Robel train' + '%')))))\
                 .values(acceptatie_gereed = orders_inkoop_diensten.c.acceptatie_gereed\
                 + mbedrag, acceptatie_datum = mboekd)
                con.execute(upd)
                stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                   values(kosten_materieel = werken.c.kosten_materieel+mbedrag)
                con.execute(stmt)
                invoerOK()
            con.close
    
    win = MyWindow(data_list, header)
    win.exec_()
    mutatieKeuze(m_email)
    
