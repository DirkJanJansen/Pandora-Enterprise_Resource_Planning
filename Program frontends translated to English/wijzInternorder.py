from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QDialog, QLabel, QGridLayout,\
       QPushButton, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean, ForeignKey,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, update, insert, func, and_

def refresh(keuze, zoekterm, m_email, self):
    self.close()
    toonOrders(keuze, zoekterm, m_email)

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
            
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Modify internal order')
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found, take another selection please!')
    msg.setWindowTitle('Requesting articles')             
    msg.exec_() 
 
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Modify successful!') 
    msg.setWindowTitle('Work order data')
    msg.exec_()

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)

def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Orders_ Intern")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
   
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 1, Qt.AlignRight)
            
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(280)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('        Sort key orders internal')
            k0Edit.addItem('1. All internal orders')
            k0Edit.addItem('2. Filtered by work order number')
            k0Edit.addItem('3. Filtered by article number')
            k0Edit.addItem('4. Filtered by (part) date of start')
            k0Edit.addItem('5. Filtered by (part) date of finish')
            k0Edit.addItem('6. Filtered by progress status A-H')
            k0Edit.addItem('7. Filtered by (part) description')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp('^.{0,40}$')
            input_validator = QRegExpValidator(reg_ex, zktermEdit)
            zktermEdit.setValidator(input_validator)
            zktermEdit.textChanged.connect(self.zktermChanged)
         
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                           
            grid.addWidget(k0Edit, 2, 1)   
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(110)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(cancelBtn, 4, 0 , 1 , 2, Qt.AlignCenter)
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
    toonOrders(keuze, zoekterm, m_email)  

def selectRow(index):
    #print('Recordnummer is: ', index.row())
    pass  
       
def toonOrders(keuze, zoekterm, m_email):
    import validZt                       
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Modify internal orders')
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
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
            table_view.clicked.connect(wijzigOrder)
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
             
    header = ['Work order', 'Description','Article number','Amount',\
               'Workletter','Order date', 'Progress status','Status week','Book date',\
               'Start date', 'Finished', 'Budgeted total','Realised total',\
               'Budgeted materials','Realised materials','Budgeted wages',\
               'Realised wages', 'More/Less work', 'Ssawing','Bsawing', 'Rsawing',\
               'Splaning','Bplaning', 'Rplaning', 'Sstabbing','Bstabbing', 'Rstabbing',\
               'Sdrilling','Bdrilling', 'Rdrilling','Smilling','Bmilling','Rmilling',\
               'Sturning small', 'Bturning small','Rturning small','Sturning big',\
               'Bturning big','Rturning big','Sthreading','Bthreading','Rthreading',\
               'SCNC turning','BCNC turning','RCNC turning','SCNC milling',\
               'BCNC milling', 'RCNC milling', 'Scutting','Bcutting', 'Rcutting',\
               'Sbending', 'Bbending', 'RBending','Ssizing','Bsizing', 'Rsizing',\
               'Swelding Co2', 'Bwelding Co2', 'Rwelding Co2','Swelding hand','Bwelding hand',\
               'Rwelding hand','Spacking','Bpacking','Rpacking', 'Sgalvanize',\
               'Bgalvanize','Rgalvanize','Smuffling','Bmuffling', 'Rmuffling',\
               'Spainting','Bpainting', 'Rpainting','Sspraying','Bspraying',\
               'Rspraying','Sstamping','Bstamping', 'Rstamping','Spressing','Bpressing',\
               'Rpressing','Sgritblasting','Bgritblasting','Rgritblasting','Smounting',\
               'Bmounting','Rmounting', 'Wtravelhours','Finished', 'Approved']
    
    metadata = MetaData()
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('hoeveelheid', Float),
        Column('werkbrief', String),
        Column('besteldatum', String),
        Column('voortgangstatus', String),
        Column('statusweek', String),
        Column('boekdatum', String),
        Column('startdatum', String),
        Column('afgemeld', String),
        Column('begroot_totaal', Float),
        Column('werk_totaal', Float),
        Column('begr_materialen', Float),
        Column('werk_materialen', Float),
        Column('begr_lonen', Float),
        Column('werk_lonen', Float),
        Column('meerminderwerk', Float),
        Column('szagen', Float),
        Column('bzagen', Float),
        Column('wzagen', Float),
        Column('sschaven', Float),
        Column('bschaven', Float),
        Column('wschaven', Float),
        Column('ssteken', Float),
        Column('bsteken', Float),
        Column('wsteken', Float),
        Column('sboren', Float),
        Column('bboren', Float),
        Column('wboren', Float),
        Column('sfrezen', Float),       
        Column('bfrezen', Float),
        Column('wfrezen', Float),
        Column('sdraaien_klein', Float),
        Column('bdraaien_klein', Float),
        Column('wdraaien_klein', Float),
        Column('sdraaien_groot', Float),        
        Column('bdraaien_groot', Float),
        Column('wdraaien_groot', Float),
        Column('stappen', Float),
        Column('btappen', Float),
        Column('wtappen', Float),
        Column('snube_draaien', Float),
        Column('bnube_draaien', Float),
        Column('wnube_draaien', Float),
        Column('snube_bewerken', Float),
        Column('bnube_bewerken', Float),
        Column('wnube_bewerken', Float),
        Column('sknippen', Float),
        Column('bknippen', Float),
        Column('wknippen', Float),
        Column('skanten', Float),
        Column('bkanten', Float),
        Column('wkanten', Float),
        Column('sstansen', Float),
        Column('bstansen', Float),
        Column('wstansen', Float),
        Column('slassen_co2', Float),
        Column('blassen_co2', Float),
        Column('wlassen_co2', Float),
        Column('slassen_hand', Float),
        Column('blassen_hand', Float),
        Column('wlassen_hand', Float),
        Column('sverpakken', Float),
        Column('bverpakken', Float),
        Column('wverpakken', Float),
        Column('sverzinken', Float),
        Column('bverzinken', Float),
        Column('wverzinken', Float),
        Column('smoffelen', Float),       
        Column('bmoffelen', Float),
        Column('wmoffelen', Float),
        Column('sschilderen', Float),
        Column('bschilderen', Float),
        Column('wschilderen', Float),
        Column('sspuiten', Float),
        Column('bspuiten', Float),
        Column('wspuiten', Float),
        Column('sponsen', Float),
        Column('bponsen', Float),
        Column('wponsen', Float),
        Column('spersen', Float),
        Column('bpersen', Float),
        Column('wpersen', Float),
        Column('sgritstralen', Float),
        Column('bgritstralen', Float),
        Column('wgritstralen', Float),
        Column('smontage', Float),
        Column('bmontage', Float),
        Column('wmontage', Float),
        Column('werk_reis_uren', Float),
        Column('gereed', Float),
        Column('goedgekeurd', Float))
       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
        
    if keuze == 1:
        sel = select([orders_intern]).order_by(orders_intern.c.werkorderID)
    elif keuze == 2 and validZt.zt(zoekterm, 7):
        sel = select([orders_intern]).where(orders_intern.c.werkorderID== int(zoekterm))
    elif keuze == 3 and validZt.zt(zoekterm, 2):
        sel = select([orders_intern]).where(orders_intern.c.artikelID == int(zoekterm))
    elif keuze == 4 and validZt.zt(zoekterm, 10):
        sel = select([orders_intern]).where(orders_intern.c.startdatum == (zoekterm+'%'))
    elif keuze == 5 and validZt.zt(zoekterm, 10):
        sel = select([orders_intern]).where(orders_intern.c.afgemeld == (zoekterm+'%'))
    elif keuze == 6 and validZt.zt(zoekterm, 18):
        sel = select([orders_intern]).where(orders_intern.c.voortgangstatus == (zoekterm.upper()[0]))
    elif keuze == 7:
        sel = select([orders_intern]).where(orders_intern.c.werkomschrijving.ilike('%'+zoekterm+'%'))
    else:
        ongInvoer()
        zoeken(m_email)
        
    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
        zoeken(m_email)
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def wijzigOrder(idx):
        mwerkorder = idx.data()
        if  idx.column() == 0:
            metadata = MetaData()
            orders_intern = Table('orders_intern', metadata,
                Column('werkorderID', Integer(), primary_key=True),
                Column('werkomschrijving', String),
                Column('besteldatum', String),
                Column('voortgangstatus', String),
                Column('statusweek', String),
                Column('boekdatum', String),
                Column('startdatum', String),
                Column('afgemeld', String),
                Column('begroot_totaal', Float),
                Column('werk_totaal', Float),
                Column('begr_materialen', Float),
                Column('werk_materialen', Float),
                Column('begr_lonen', Float),
                Column('werk_lonen', Float),
                Column('meerminderwerk', Float),
                Column('werk_reis_uren', Float),
                Column('artikelID', None, ForeignKey('artikelen.c.artikelID')),
                Column('hoeveelheid', Float),
                Column('goedgekeurd', Float),
                Column('gereed', Float))
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('art_voorraad', Float),
                Column('bestelstatus'),
                Column('artikelprijs', Float),
                Column('bestelsaldo', Float))
            artikelmutaties = Table('artikelmutaties', metadata,
                Column('mutatieID', Integer, primary_key=True),
                Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                Column('hoeveelheid', Float),
                Column('boekdatum', String),
                Column('tot_mag_prijs', Float),
                Column('btw_hoog', Float),
                Column('werkorderID', Integer))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selord = select([orders_intern]).where(orders_intern.c.werkorderID == mwerkorder)
            rpord = con.execute(selord).first()
        
            class Widget(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(12)
                    
                    self.setWindowTitle("Modify workorder internal")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                      
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 1, 1, 2, Qt.AlignRight) 
                    
                    grid.addWidget(QLabel('Modify orders internal'), 0, 0, 1, 3, Qt.AlignCenter)
                        
                    self.Werkordernummer = QLabel()
                    q1Edit = QLineEdit(str(rpord[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                    q1Edit.setFont(QFont("Arial",10))
                 
                    self.Omschrijving = QLabel()
                    q2Edit = QLineEdit(str(rpord[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.textChanged.connect(self.q2Changed)
                    
                    self.Voorgangstatus = QLabel()
                    q3Edit = QLineEdit(str(rpord[3]))
                    q3Edit.setFixedWidth(20)
                    font = QFont("Arial",10)
                    font.setCapitalization(QFont.AllUppercase)
                    q3Edit.setFont(font)
                    if str(rpord[3]) < 'G':
                        q3Edit.setDisabled(True)
                        q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.textChanged.connect(self.q3Changed)
                    reg_ex = QRegExp('^[A-Ha-h]{1}$')
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                                   
                    self.Startdatum = QLabel()
                    q4Edit = QLineEdit(str(rpord[6]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.textChanged.connect(self.q4Changed)
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                                            
                    self.Afgemeld = QLabel()
                    q5Edit = QLineEdit(str(rpord[7]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.textChanged.connect(self.q5Changed)
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, q5Edit)
                    q5Edit.setValidator(input_validator)
                  
                    self.Gereed = QLabel()
                    q6Edit = QLineEdit(str(round(float(rpord[19]),2)))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.textChanged.connect(self.q6Changed)
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q6Edit)
                    q6Edit.setValidator(input_validator)
                                    
                    self.Goedgekeurd = QLabel()
                    q7Edit = QLineEdit(str(round(float(rpord[18]),2)))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setFont(QFont("Arial",10))
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.textChanged.connect(self.q7Changed)
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q7Edit)
                    q7Edit.setValidator(input_validator)
                    
                    lbl1 = QLabel('Work order number')
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                    
                    lbl2 = QLabel('Work description')
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(q2Edit, 2, 1, 1, 2)
                    
                    lbl3 = QLabel('Progress status')
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(q3Edit, 3, 1)
                    lbl4 = QLabel('Status week: '+rpord[4])
                    grid.addWidget(lbl4, 3, 1, 1, 2, Qt.AlignRight)
                    
                    lbl5 = QLabel('Start date')
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q4Edit, 4, 1)
                    
                    lbl6 = QLabel('Finished')
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q5Edit, 5, 1)
                    
                    lbl7 = QLabel('Amount\nFinished')
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q6Edit, 6, 1)
                    lbl8 = QLabel('                           Article: '+str(rpord[16]))
                    grid.addWidget(lbl8, 5, 1, 1, 2, Qt.AlignRight)
                    lbl9 = QLabel('                 Order size       : '+'{:12.2f}'.format(rpord[17]))
                    grid.addWidget(lbl9, 6, 1, 1, 2, Qt.AlignRight)
                    
                    lbl10 = QLabel('Amount\nApproved')
                    grid.addWidget(lbl10, 7, 0)
                    grid.addWidget(q7Edit, 7, 1)
              
                    wijzig = QPushButton('Modify')
                    wijzig.clicked.connect(self.accept)
    
                    grid.addWidget(wijzig, 9, 2, 1 , 1, Qt.AlignRight)
                    wijzig.setFont(QFont("Arial",10))
                    wijzig.setFixedWidth(100)
                    
                    sluit = QPushButton('Close')
                    sluit.clicked.connect(self.close)
    
                    grid.addWidget(sluit, 9, 1 , 1 , 2, Qt.AlignCenter)
                    sluit.setFont(QFont("Arial",10))
                    sluit.setFixedWidth(100)  
                                                   
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 3, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
                    
                def q2Changed(self,text):
                    self.Omschrijving.setText(text)
            
                def q3Changed(self,text):
                    self.Voortgangstatus.setText(text)
            
                def q4Changed(self,text):
                    self.Startdatum.setText(text)
                    
                def q5Changed(self,text):
                    self.Afgemeld.setText(text)

                def q6Changed(self,text):
                    self.Gereed.setText(text)
                               
                def q7Changed(self,text):
                    self.Goedgekeurd.setText(text)
              
                def returnq2(self):
                    return self.Omschrijving.text()
                
                def returnq3(self):
                    return self.Voorgangstatus.text()
                
                def returnq4(self):
                    return self.Startdatum.text()
                    
                def returnq5(self):
                    return self.Afgemeld.text()
                
                def returnq6(self):
                    return self.Gereed.text()
                      
                def returnq7(self):
                    return self.Goedgekeurd.text()
                
                @staticmethod
                def getData(parent=None):
                    dialog = Widget()
                    dialog.exec_()
                    return [dialog.returnq2(), dialog.returnq3(), dialog.returnq4(),\
                            dialog.returnq5(), dialog.returnq6(), dialog.returnq7()]  
                            
            window = Widget()
            data = window.getData()
            if not(data[0] or data[1] or data[2] or data[3] or data[4] or data[5]):       
                return()
            if data[0]:
                momschr = data[0]
            else:
                momschr = rpord[1]
            if data[1]:
                mvgst = data[1]
            else:
                mvgst = rpord[3]
            if data[2]:
                mstart = data[2]
            else:
                mstart = rpord[6]
            if data[3]:
                mafgem = data[3]
            else:
                mafgem = rpord[7]
            if data[4]:
                mgereed = float(data[4])
            else:
                mgereed = rpord[19]
            if data[5]:
                mgoedg = float(data[5])
            else:
                mgoedg = rpord[18]
            mboekd = str(datetime.datetime.now())[0:10] 
            mgoedgversch = mgoedg - rpord[18]
            
            updio = update(orders_intern).where(orders_intern.c.werkorderID == mwerkorder)\
             .values(werkomschrijving = momschr, voortgangstatus = mvgst, startdatum = mstart,\
                    afgemeld = mafgem, boekdatum = mboekd, gereed = mgereed, goedgekeurd = mgoedg)
            con.execute(updio)
            updart = update(artikelen).where(and_(orders_intern.c.werkorderID == mwerkorder,\
              orders_intern.c.artikelID == artikelen.c.artikelID)).values(art_voorraad =\
              artikelen.c.art_voorraad + mgoedgversch, bestelsaldo = artikelen.c.bestelsaldo -\
              mgoedgversch)
            con.execute(updart)
            try:
                mutnr=(con.execute(select([func.max(artikelmutaties.c.mutatieID,\
                        type_=Integer)])).scalar())
                mutnr += 1
            except:
                mutnr = 1
            params = Table('params', metadata,
                Column('paramID', Integer, primary_key=True),
                Column('tarief', Float),
                Column('item', String),
                Column('lock', Boolean),
                Column('ondergrens', Float),
                Column('bovengrens', Float))
            
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
            selart = select([artikelen]).where(rpord[16]==artikelen.c.artikelID)
            rpart = con.execute(selart).first()
            martprijs = rpart[3] 
            
            ins = insert(artikelmutaties).values(mutatieID = mutnr, artikelID =\
            rpord[16], werkorderID = mwerkorder, hoeveelheid = mgoedgversch,\
            boekdatum = mboekd, tot_mag_prijs = mgoedgversch*martprijs,\
            btw_hoog = mgoedgversch*martprijs*(rppar[0][1]))
            con.execute(ins)
            invoerOK()
     
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)