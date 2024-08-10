import datetime
from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QGridLayout, QDialog,\
                  QWidget,QTableView, QStyledItemDelegate, QMessageBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, select, update, and_)

def refresh(m_email, keuze, self):
    self.close()
    jaarVerbruik(m_email, keuze)

def artVerwerkt(rpartikelen, mbestgr, minvrd):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setWindowTitle('Stock control')
    msg.setIcon(QMessageBox.Information)
    msg.setText('Article: '+str(rpartikelen[0])+'\nDescription: '+rpartikelen[1]+'\nMinimum stock changed to '+str(minvrd)+'\nOrder size changed to '+str(mbestgr))
    msg.exec_()
    
def bestelStatus():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setWindowTitle('Order letter printing')
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Order letter is already processed!')
    msg.exec_()
    
def handle_paint_request(self, printer):
    painter = QPainter(printer)
    painter.setViewport(self.view.rect())
    painter.setWindow(self.view.rect())                        
    self.view.render(painter)
    painter.end()

def printBrief(rpartikel, bestelhoeveelheid, bestelBtn):
    from sys import platform
    vandaag = str(datetime.date.today())[0:10]
    metadata =  MetaData()
    params_system = Table('params_system', metadata,
        Column('systemID', Integer, primary_key=True),
        Column('system_value', Float))
         
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params_system]).where(params_system.c.systemID == 1)
    rppar = con.execute(selpar).first()
    bestnr = int(rppar[1])
    updpar = update(params_system).where(params_system.c.systemID == 1).values(system_value = int(bestnr+1))
    con.execute(updpar)
    if rpartikel[9] == 1:
        besteltekst = 'Order size stock controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 3 weeks'
    elif rpartikel[9] == 2:
        besteltekst = 'Order size stock controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 12 weeks'
    elif rpartikel[9] == 3:
        besteltekst = 'Order size stock controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 26 weeks'
    elif rpartikel[9] == 4:
        besteltekst = 'Order size stock controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 52 weeks'
    elif rpartikel[9] == 5:
        besteltekst = 'Minimum order size reservation controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 3 weeks'
    elif rpartikel[9] == 6:
        besteltekst = 'Minimum order size reservation controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 6 weeks'
    elif rpartikel[9] == 7:
        besteltekst = 'Minimum order size reservation controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 12 weeks'
    elif rpartikel[9] == 8:
        besteltekst = 'Minimum order size reservation controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 24 weeks'
    elif rpartikel[9] == 9:
        besteltekst = 'Minimum order size reservation controlled: '+'{:12.2f}'.format(bestelhoeveelheid)+'\n\n'
        termijn = ' 52 weeks'
    if platform == 'win32':
        filename = '.\\forms\\Intern_Orderbrieven\\Order_letter_number_'+str(bestnr)+'.txt'
    else:
        filename = './forms/Intern_Orderbrieven/Order_letter_number_'+str(bestnr)+'.txt'
    open(filename,"w").write('\n\n\nDate: '+str(vandaag)+'\n')
    gegevens = ('\n\n'+\
    'Internal order slip serial number: '+str(bestnr)+'\n\n\n\n'+\
    'Order letter for warehouse item: '+str(rpartikel[0])+'\n\n'+\
    'Article description: '+str(rpartikel[1])+'\n\n'+\
    'Article price including surcharges: '+'{:12.2f}'.format(rpartikel[2])+'\n\n'+\
    'Article stock : '+'{:12.2f}'.format(rpartikel[3])+'\n\n'+\
    'Article unit: '+str(rpartikel[4])+'\n\n'+\
    'Article miminimum stock:  '+'{:12.2f}'.format(rpartikel[5])+'\n\n'+\
    'Order balance: '+'{:12.2f}'.format(rpartikel[6])+'\n\n'+\
    'Order status: '+str(rpartikel[7])+'\n\n'+\
    'Reservation balance: '+'{:12.2f}'.format(rpartikel[8])+'\n\n'+\
    'Category: '+str(rpartikel[9])+'\n\n'+\
    str(besteltekst)+'Delivery term : '+str(termijn)+'\n\n')
    open(filename,"a").write(gegevens+'\n')

    class Window(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Printing internal order letter")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            self.view = QLabel(self)
            self.view = self.create_view()
            layout = QGridLayout(self)
            layout.addWidget(self.view, 0, 0, 1, 2)
            printer = QPrinter(QPrinter.HighResolution)
            #printer.setPageMargins(12, 16, 12, 20, QPrinter.Millimeter)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                handle_paint_request(self, printer)
       
        def create_view(self):
            lblinfo = QLabel(
        '\n\n\n'+\
        'Date: '+str(vandaag)+'\n\n\n'+\
        'Internal order letter serial number: '+str(bestnr)+'\n\n\n\n'+\
        'Order letter for warehouse article: '+str(rpartikel[0])+'\n\n'+\
        'Article description: '+rpartikel[1]+'\n\n'+\
        'Article price including surcharges: '+'{:12.2f}'.format(rpartikel[2])+'\n\n'+\
        'Article stock : '+'{:12.2f}'.format(rpartikel[3])+'\n\n'+\
        'Article unit: '+rpartikel[4]+'\n\n'+
        'Article miminimum stock:  '+'{:12.2f}'.format(rpartikel[5])+'\n\n'+\
        'Order balance: '+'{:12.2f}'.format(rpartikel[6])+'\n\n'+\
        'Order status: '+str(rpartikel[7])+'\n\n'+\
        'Reservation balance: '+'{:12.2f}'.format(rpartikel[8])+'\n\n'+\
        'Category: '+str(rpartikel[9])+'\n\n'+\
        besteltekst+\
        'Delivery term: ' + termijn)
            
            if platform == 'win32':
                lblinfo.setStyleSheet("font: 72pt 'Comic Sans MS'")
            else:
                lblinfo.setStyleSheet("font: 144pt 'Comic Sans MS'")
            return(lblinfo)
         
    Window()
            
def bestelBrief(rpartikel, bestelhoeveelheid, bestelBtn):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('bestelstatus', Boolean),
        Column('bestelsaldo', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if rpartikel[7]:
        updart = update(artikelen).where(artikelen.c.artikelID == rpartikel[0])\
        .values(bestelstatus = False, bestelsaldo = artikelen.c.bestelsaldo+bestelhoeveelheid)
        con.execute(updart)
        bestelBtn.setDisabled(True)
        printBrief(rpartikel, bestelhoeveelheid, bestelBtn)
    else:
        bestelStatus()

def vrdKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Requesting articles")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(280)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                  Your choice ')
            k0Edit.addItem('1. By reservation to order')
            k0Edit.addItem('2. By minimum stock to order')
            k0Edit.addItem('3. Articles on order')
   
            k0Edit.activated[str].connect(self.k0Changed)
              
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 0 ,1, 2, Qt.AlignRight)
            
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
    
            grid.addWidget(cancelBtn, 3, 0, 1, 1, Qt.AlignRight)
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
        vrdKeuze(m_email)
    elif data[0]:
        keuze = int(data[0][0])
        jaarVerbruik(m_email, keuze)
    else:
        vrdKeuze(m_email)
  
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def jaarVerbruik(m_email, keuze):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String),
        Column('art_min_voorraad', Float),
        Column('bestelsaldo', Float),
        Column('bestelstatus', Boolean),
        Column('reserveringsaldo', Float),
        Column('categorie', Integer),
        Column('thumb_artikel', String),
        Column('art_bestelgrootte', Float),
        Column('jaarverbruik_1', Float),
        Column('jaarverbruik_2', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
            
    if keuze == 1:
        sel = select([artikelen]).where(and_(artikelen.c.art_voorraad + artikelen.c.bestelsaldo\
            < artikelen.c.reserveringsaldo, artikelen.c.categorie > 4)).order_by(artikelen.c.artikelID)
    elif keuze == 2:
        sel = select([artikelen]).where(and_(artikelen.c.art_voorraad+artikelen.c.bestelsaldo\
            < artikelen.c.art_min_voorraad, artikelen.c.categorie < 5)).order_by(artikelen.c.artikelID)
    elif keuze == 3:
        sel = select([artikelen]).where(artikelen.c.bestelstatus == False)
          
    rpartikelen = conn.execute(sel)
   
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Annual consumption last year')
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
            table_view.setItemDelegateForColumn(10, showImage(self))
            table_view.setColumnWidth(10, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.clicked.connect(aanpMinvoorraad)
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
            freshBtn.clicked.connect(lambda: refresh(m_email, keuze, self))

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
            #elif index.column() == 9 and role == Qt.DecorationRole: # alternatief picture echter
            #    return QPixmap(index.data())                        # met tekst rechts van path
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
                                       
    header = ['Article number', 'Description', 'Price', 'Stock', 'Unit','Minimum stock',\
              'Order balance', 'Order status', 'Reservation balance', 'Category', 'Image',\
              'To order','Annual consumption-1', 'Annual consumption-2']
        
    data_list=[]
    for row in rpartikelen:
        data_list += [(row)] 
        
    def aanpMinvoorraad(idx):
        martikelnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
            rpartikel = con.execute(sel).first() 
            mjaar = int(str(datetime.datetime.now())[0:4])
                             
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                
                    self.setWindowTitle("Adjust minimum stock / order size")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                    self.setFont(QFont('Arial', 10))
                               
                    self.Artikelnummer = QLabel()
                    q1Edit = QLineEdit(str(rpartikel[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    self.Artikelomschrijving = QLabel()
                    q2Edit = QLineEdit(str(rpartikel[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                    
                    self.Artikelprijs = QLabel()
                    q3Edit = QLineEdit('{:12.2f}'.format(rpartikel[2]))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                                    
                    self.Artikelvoorraad = QLabel()
                    q4Edit = QLineEdit('{:12.2f}'.format(rpartikel[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    self.Artikeleenheid = QLabel()
                    q5Edit = QLineEdit(rpartikel[4])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    self.Minimumvoorraad = QLabel()
                    q6Edit = QLineEdit('{:12.2f}'.format(rpartikel[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                     
                    self.Bestelsaldo = QLabel()
                    q16Edit = QLineEdit('{:12.2f}'.format(rpartikel[6]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
    
                    self.Bestelstatus = QLabel()
                    q7Edit = QLineEdit(str(rpartikel[7]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    self.Reserveringsaldo = QLabel()
                    q12Edit = QLineEdit('{:12.2f}'.format(rpartikel[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                                   
                    self.Categorie = QLabel()
                    q8Edit = QLineEdit(str(rpartikel[9]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
 
                    self.Bestelgrootte = QLabel()
                    q9Edit = QLineEdit('{:12.2f}'.format(rpartikel[11]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                          
                    if mjaar%2 == 1:
                        self.Jaarverbruik = QLabel()
                        q13Edit = QLineEdit('{:12.2f}'.format(rpartikel[12]))
                        q13Edit.setFixedWidth(100)
                        q13Edit.setAlignment(Qt.AlignRight)
                        q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q13Edit.setDisabled(True) 
                    else:
                        self.Jaarverbruik = QLabel()
                        q13Edit = QLineEdit('{:12.2f}'.format(rpartikel[13]))
                        q13Edit.setFixedWidth(100)
                        q13Edit.setAlignment(Qt.AlignRight)
                        q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q13Edit.setDisabled(True)  
                         
                    grid = QGridLayout()
                    grid.setSpacing(20)
                
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl , 0, 0, 1, 2)
                
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 2, 1, 3, Qt.AlignRight) 
                  
                    grid.addWidget(QLabel('Article number'), 1, 0, 2, 1)
                    grid.addWidget(q1Edit, 1, 1, 2, 1)
                
                    grid.addWidget(QLabel('Article description'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1, 1 ,3)
                    
                    grid.addWidget(QLabel('Unit'), 5, 0)
                    grid.addWidget(q5Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Article price'), 5, 2)
                    grid.addWidget(q3Edit, 5 , 3) 
                    
                    grid.addWidget(QLabel('Stock'), 6, 0)
                    grid.addWidget(q4Edit, 6, 1)
                    
                    grid.addWidget(QLabel('Order balance'), 7, 0)
                    grid.addWidget(q16Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Reservation balance'), 8, 0)
                    grid.addWidget(q12Edit, 8, 1)
                                       
                    grid.addWidget(QLabel('Order status'),7 ,2)
                    grid.addWidget(q7Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Category'),8 ,2)
                    grid.addWidget(q8Edit, 8,3)
                    
                    if rpartikel[9] > 4:
                        bestelhoeveelheid = rpartikel[8]+rpartikel[6]-rpartikel[3]
                        grid.addWidget(QLabel('To order'), 10, 0)
                        if rpartikel[7]:
                            grid.addWidget(QLabel('{:12.2f}'.format(bestelhoeveelheid, 2)), 10, 1, 1, 1, Qt.AlignRight)
                        else:
                            grid.addWidget(QLabel('On order'), 10, 1)
                        grid.addWidget(QLabel('Reservation controlled'), 9, 2)
                    else:
                        grid.addWidget(QLabel('Order size'),9 ,0)
                        grid.addWidget(q9Edit, 9,1)
                        grid.addWidget(QLabel('Minimum stock'), 6, 2)
                        grid.addWidget(q6Edit, 6, 3)
                        
                        bestelhoeveelheid = rpartikel[11]
                        grid.addWidget(QLabel('To order'), 10, 0)
                        if rpartikel[7]:
                            grid.addWidget(QLabel('{:12.2f}'.format(bestelhoeveelheid, 2)), 10, 1, 1, 1, Qt.AlignRight)
                        else:
                            grid.addWidget(QLabel('On order'), 10, 1)
                        grid.addWidget(QLabel('Stock controlled'), 9, 2)
                    
                    grid.addWidget(QLabel('Annual consumption'),10, 2)
                    grid.addWidget(q13Edit, 10, 3)

                    pixmap = QPixmap(rpartikel[10])
                    lbl2 = QLabel(self)
                    lbl2.setPixmap(pixmap)
                    grid.addWidget(lbl2 , 1, 2, 2, 2, Qt.AlignRight)
                    
                    bestelBtn = QPushButton('Order letter')
                    bestelBtn.clicked.connect(lambda: bestelBrief(rpartikel, bestelhoeveelheid, bestelBtn))
                    
                    grid.addWidget(bestelBtn, 12, 3, 1, 1, Qt.AlignRight)
                    bestelBtn.setFont(QFont("Arial",10))
                    bestelBtn.setFixedWidth(100) 
                    bestelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    if rpartikel[7]:
                        bestelBtn.setEnabled(True)
                    else:
                        bestelBtn.setEnabled(False)
                    
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 12, 2, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
                                   
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 350, 300)
                
            window = Widget()
            window.exec_()
                                                        
    win = MyWindow(data_list, header)
    win.exec_()
    vrdKeuze(m_email)