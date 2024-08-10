from login import hoofdMenu
from datetime import date
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QStyledItemDelegate,\
      QDialog, QLineEdit, QVBoxLayout, QTableView, QMessageBox
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, select, update, and_, or_)

def ongKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Ongeldige keuze')
    msg.setWindowTitle('Artikel Bestelling')               
    msg.exec_()

def bestelStatus():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setWindowTitle('Bestelbrief printen')
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Bestelbrief is reeds aangemaakt!')
    msg.exec_()
    
def handle_paint_request(self, printer):
    painter = QPainter(printer)
    painter.setViewport(self.view.rect())
    painter.setWindow(self.view.rect())                        
    self.view.render(painter)
    painter.end()

def printBrief(rpartikel):
    from sys import platform
    vandaag = str(date.today())[0:10]
    metadata =  MetaData()
    params_system = Table('params_system', metadata,
       Column('systemID', Integer, primary_key=True),
       Column('system_value', Integer))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params_system]).where(params_system.c.systemID == 1)
    rppar = con.execute(selpar).first()
    bestnr = int(rppar[1])
    updpar = update(params_system).where(params_system.c.systemID == 1).values(system_value=int(bestnr + 1))
    con.execute(updpar)
    if rpartikel[9] == 1:
        besteltekst = 'Bestelgrootte voorraadgestuurd: '+str(round(rpartikel[11],2))+'\n\n' 
        termijn = ' 3 weken'
    elif rpartikel[9] == 2:
        besteltekst = 'Bestelgrootte voorraadgestuurd: '+str(round(rpartikel[11],2))+'\n\n' 
        termijn = ' 8 weken'
    elif rpartikel[9] == 3:
        besteltekst = 'Bestelgrootte voorraadgestuurd: '+str(round(rpartikel[11],2))+'\n\n'
        termijn = ' 26 weken'
    elif rpartikel[9] == 4:
        besteltekst = 'Bestelgrootte voorraadgestuurd: '+str(round(rpartikel[11],2))+'\n\n' 
        termijn = ' 1 jaar'
    elif rpartikel[9] == 5:
        besteltekst = 'Minimale bestelgrootte reserveringgestuurd: '+str(round(rpartikel[8]-rpartikel[3]-rpartikel[6],2))+'\n\n'
        termijn = ' 3 weken'
    elif rpartikel[9] == 6:
        besteltekst = 'Minimale bestelgrootte reserveringgestuurd: '+str(round(rpartikel[8]-rpartikel[3]-rpartikel[6],2))+'\n\n'
        termijn = ' 6 weken'
    elif rpartikel[9] == 7:
        besteltekst = 'Minimale bestelgrootte reserveringgestuurd: '+str(round(rpartikel[8]-rpartikel[3]-rpartikel[6],2))+'\n\n'
        termijn = ' 12 weken'
    elif rpartikel[9] == 8:
        besteltekst = 'Minimale bestelgrootte reserveringgestuurd: '+str(round(rpartikel[8]-rpartikel[3]-rpartikel[6],2))+'\n\n'
        termijn = ' 24 weken'
    elif rpartikel[9] == 9:
        besteltekst = 'Minimale bestelgrootte reserveringgestuurd: '+str(round(rpartikel[8]-rpartikel[3]-rpartikel[6],2))+'\n\n'
        termijn = ' 1 jaar'
    if platform == 'win32':
        filename = '.\\forms\\Intern_Orderbrieven\\Orderbriefnr_'+str(bestnr)+'.txt'
    else:
        filename = './forms/Intern_Orderbrieven/Orderbriefnr_'+str(bestnr)+'.txt'
    open(filename,"w").write('\n\n\nDatum: '+str(vandaag)+'\n')
    gegevens = ('\n\n'+\
    'Interne orderbrief volgnummer: '+str(bestnr)+'\n\n\n\n'+\
    'Bestelbrief voor magazijnartikel: '+str(rpartikel[0])+'\n\n'+\
    'Artikelomschrijving: '+str(rpartikel[1])+'\n\n'+\
    'Artikelprijs inclusief opslagen: '+str(round(rpartikel[2],2))+'\n\n'+\
    'Artikelvoorraad : '+str(round(rpartikel[3],2))+'\n\n'+\
    'Artikel eenheid: '+str(rpartikel[4])+'\n\n'+\
    'Artikel miminimum voorraad:  '+str(round(rpartikel[5],2))+'\n\n'+\
    'Bestelsaldo: '+str(round(rpartikel[6],2))+'\n\n'+\
    'Bestelstatus: '+str(rpartikel[7])+'\n\n'+\
    'Reserveringssaldo: '+str(round(rpartikel[8],2))+'\n\n'+\
    'Categorie: '+str(rpartikel[9])+'\n\n'+\
    str(besteltekst)+'Levertermijn : '+str(termijn)+'\n\n')
    open(filename,"a").write(gegevens+'\n')

    class Window(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Printen interne orderbrief") 
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
        'Datum: '+str(vandaag)+'\n\n\n'+\
        'Interne orderbrief volgnummer: '+str(bestnr)+'\n\n\n\n'+\
        'Bestelbrief voor magazijnartikel: '+str(rpartikel[0])+'\n\n'+\
        'Artikelomschrijving: '+rpartikel[1]+'\n\n'+\
        'Artikelprijs inclusief opslagen: '+str(round(rpartikel[2],2))+'\n\n'+\
        'Artikelvoorraad : '+str(round(rpartikel[3],2))+'\n\n'+\
        'Artikel eenheid: '+rpartikel[4]+'\n\n'+
        'Artikel miminimum voorraad:  '+str(round(rpartikel[5],2))+'\n\n'+\
        'Bestelsaldo: '+str(round(rpartikel[6],2))+'\n\n'+\
        'Bestelstatus: '+str(rpartikel[7])+'\n\n'+\
        'Reserveringssaldo: '+str(round(rpartikel[8],2))+'\n\n'+\
        'Categorie: '+str(rpartikel[9])+'\n\n'+\
        besteltekst+\
        'Levertermijn : ' + termijn)
            
            if platform == 'win32':
                lblinfo.setStyleSheet("font: 72pt 'Comic Sans MS'")
            else:
                lblinfo.setStyleSheet("font: 144pt 'Comic Sans MS'")
            return(lblinfo)
                    
    Window()
            
def bestelBrief(rpartikel, bestelBtn):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('bestelstatus', Boolean))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if rpartikel[7] == False:
        bestelStatus()
    else:
        updart = update(artikelen).where(artikelen.c.artikelID == rpartikel[0])\
        .values(bestelstatus = False)
        con.execute(updart)
        
        printBrief(rpartikel)
        bestelBtn.setEnabled(False)

def toonArtikellijst(m_email):
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
        Column('art_bestelgrootte', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([artikelen]).where(or_(and_(artikelen.c.art_voorraad+artikelen.c.bestelsaldo\
         -artikelen.c.reserveringsaldo < artikelen.c.art_min_voorraad, artikelen.c.categorie < 5),\
         and_(artikelen.c.art_voorraad+artikelen.c.bestelsaldo < artikelen.c.reserveringsaldo,\
         artikelen.c.categorie > 4))).order_by(artikelen.c.artikelID)
    rpartikelen = conn.execute(sel)
    updart = update(artikelen).where(and_(artikelen.c.art_voorraad+artikelen.c.bestelsaldo\
         < artikelen.c.reserveringsaldo, artikelen.c.categorie > 4))\
          .values(art_bestelgrootte = artikelen.c.reserveringsaldo \
          - artikelen.c.art_voorraad - artikelen.c.bestelsaldo)
    conn.execute(updart)
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Artikelen bestellijst')
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
            table_view.setItemDelegateForColumn(10, showImage(self))
            table_view.setColumnWidth(10, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.clicked.connect(showArtikel)
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
            if not index.isValid():
                return None
            #elif index.column() == 9 and role == Qt.DecorationRole: # alternatief picture echter
            #    return QPixmap(index.data())                        # met tekst rechts van path
            elif role != Qt.DisplayRole:
                return None
            return str(self.mylist[index.row()][index.column()])
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
                                       
    header = ['Artikelnr', 'Omschrijving', 'Prijs', 'Voorraad', 'Eenheid','MinVrd',\
              'BestelSaldo', 'Bestelstatus', 'ReserveringSaldo', 'Categorie', 'Afbeelding',\
              'Te bestellen']    
        
    data_list=[]
    for row in rpartikelen:
        data_list += [(row)] 
        
    def showArtikel(idx):
        martikelnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
            rpartikel = con.execute(sel).first()
              
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                
                    self.setWindowTitle("Artikelen Bestellijst")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                    self.setFont(QFont('Arial', 10))
                               
                    self.Artikelnummer = QLabel()
                    q1Edit = QLineEdit(str(rpartikel[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setDisabled(True)
                    q1Edit.setFont(QFont("Arial",10))
                
                    self.Artikelomschrijving = QLabel()
                    q2Edit = QLineEdit(str(rpartikel[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.setDisabled(True)
                    
                    self.Artikelprijs = QLabel()
                    q3Edit = QLineEdit(str(rpartikel[2]))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                                    
                    self.Artikelvoorraad = QLabel()
                    q4Edit = QLineEdit(str(rpartikel[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setDisabled(True)
                    
                    self.Artikeleenheid = QLabel()
                    q5Edit = QLineEdit(rpartikel[4])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)
                    
                    self.Minimumvoorraad = QLabel()
                    q6Edit = QLineEdit(str(rpartikel[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.setDisabled(True)
                     
                    self.Bestelsaldo = QLabel()
                    q16Edit = QLineEdit(str(rpartikel[6]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
    
                    self.Bestelstatus = QLabel()
                    q7Edit = QLineEdit(str(rpartikel[7]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setFont(QFont("Arial",10))
                    q7Edit.setDisabled(True)
                    
                    self.Reserveringsaldo = QLabel()
                    q12Edit = QLineEdit(str(rpartikel[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.setDisabled(True)
                                   
                    self.Categorie = QLabel()
                    q8Edit = QLineEdit(str(rpartikel[9]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
                    
                    self.Bestelhoeveelheid = QLabel()
                    if rpartikel[9] > 4:
                        q9Edit = QLineEdit(str(rpartikel[8]-rpartikel[6]-rpartikel[3]))
                    elif rpartikel[9] < 5:
                        q9Edit = QLineEdit(str(rpartikel[11]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.setDisabled(True)
                    
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
                  
                    grid.addWidget(QLabel('Artikelnummer'), 1, 0, 2, 1)
                    grid.addWidget(q1Edit, 1, 1, 2, 1)
                
                    grid.addWidget(QLabel('Artikelomschrijving'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1, 1 ,3)
                    
                    grid.addWidget(QLabel('Eenheid'), 5, 0)
                    grid.addWidget(q5Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Artikelprijs'), 5, 2)
                    grid.addWidget(q3Edit, 5 , 3) 
                    
                    grid.addWidget(QLabel('Voorraad'), 6, 0)
                    grid.addWidget(q4Edit, 6, 1)
                                  
                    grid.addWidget(QLabel('Minimumvoorraad'), 6, 2)
                    grid.addWidget(q6Edit, 6, 3)
                    
                    grid.addWidget(QLabel('Bestelsaldo'), 7, 0)
                    grid.addWidget(q16Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Reserveringsaldo '), 8, 0)
                    grid.addWidget(q12Edit, 8, 1)
                                       
                    grid.addWidget(QLabel('BestelStatus'),7 ,2)
                    grid.addWidget(q7Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Categorie'),8 ,2)
                    grid.addWidget(q8Edit, 8,3)
                    
                    grid.addWidget(QLabel('Te Bestellen'),9 ,0)
                    grid.addWidget(q9Edit, 9,1)
                    
                    pixmap = QPixmap(rpartikel[10])
                    lbl2 = QLabel(self)
                    lbl2.setPixmap(pixmap)
                    grid.addWidget(lbl2 , 1, 2, 2, 2, Qt.AlignRight)
                
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 4, Qt.AlignCenter)
                    
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 10, 2, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    bestelBtn = QPushButton('Bestelbrief')
                    bestelBtn.clicked.connect(lambda: bestelBrief(rpartikel, bestelBtn))
                                
                    grid.addWidget(bestelBtn, 10, 3, 1, 1, Qt.AlignRight)
                    bestelBtn.setFont(QFont("Arial",10))
                    bestelBtn.setFixedWidth(100) 
                    bestelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 350, 300)
                
            window = Widget()
            window.exec_()
                                            
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)