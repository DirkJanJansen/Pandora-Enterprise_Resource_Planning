from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage
from PyQt5.QtWidgets import  QLabel, QPushButton, QWidget, QGridLayout, QStyledItemDelegate,\
      QComboBox, QDialog, QLineEdit, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, ForeignKey,  Integer, String, MetaData,\
                       create_engine, Float)
from sqlalchemy.sql import select, and_ 

def windowSluit(self, m_email):
    self.setAttribute(Qt.WA_DeleteOnClose)
    self.close()
    hoofdMenu(m_email)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Inkooporders opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Inkooporders opvragen')               
    msg.exec_() 

def inkooporderKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen inkooporders materialen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(330)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('              Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Alle inkooporders op artikelnr gesorteerd')
            k0Edit.addItem('2. Alle inkooporders op ordernr gesorteerd')
            k0Edit.addItem('3. Filter op bedrijfsnaam')
            k0Edit.addItem('4. Filter op artikelomschrijving')
            k0Edit.addItem('5. Filter op ordernummer')
            k0Edit.addItem('6. Filter op levering start yyyy(-mm(-dd))')
            k0Edit.addItem('7. Filter op levering eind yyyy(-mm(-dd))')
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
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 2, 0, 1, 1, Qt. AlignRight)
            grid.addWidget(zktermEdit, 2, 1, 1, 2, Qt.AlignRight)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)            
            self.setLayout(grid)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)
            
            self.setGeometry(500, 300, 150, 150)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
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
    del window
    opvrOrder(keuze,zoekterm,m_email)
    
def opvrOrder(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    orders_inkoop_artikelen = Table('orders_inkoop_artikelen', metadata,
        Column('ordartlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('bestelaantal', Float),
        Column('inkoopprijs', Float),
        Column('levering_start', String),
        Column('levering_eind', String),
        Column('reclamatie', String),
        Column('aantal_reclamaties', Integer),
        Column('ontvangstdatum', String),
        Column('ontvangen_hoeveelheid', Float),
        Column('acceptatie_datum', String),
        Column('hoeveelheid_acceptatie', Float),
        Column('betaald', Float),
        Column('regel', Integer))
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
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('thumb_artikel', String(70)))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    if keuze == 1:
        sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen]).\
         where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
           leverancierID, orders_inkoop_artikelen.c.artikelID == artikelen.c.\
           artikelID, orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.\
           orderinkoopID)).order_by(orders_inkoop_artikelen.c.artikelID)
    elif keuze == 2:
        sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen]).\
         where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
           leverancierID, orders_inkoop_artikelen.c.artikelID == artikelen.c.\
           artikelID, orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.\
           orderinkoopID)).order_by(orders_inkoop_artikelen.c.orderinkoopID,\
            orders_inkoop_artikelen.c.regel)
    elif keuze == 3:
       sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen])\
        .where(and_(orders_inkoop_artikelen.c.orderinkoopID==orders_inkoop.c.orderinkoopID,\
          orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
          orders_inkoop_artikelen.c.artikelID == artikelen.c.artikelID,\
          orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
          leveranciers.c.bedrijfsnaam.ilike('%'+zoekterm+'%')))
    elif keuze == 4:
       sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
         orders_inkoop_artikelen.c.artikelID == artikelen.c.artikelID,\
          artikelen.c.artikelomschrijving.ilike('%'+zoekterm+'%')))
    elif keuze == 5 and validZt.zt(zoekterm, 4):
        sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
            orders_inkoop_artikelen.c.artikelID == artikelen.c.artikelID,\
         orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_artikelen.c.orderinkoopID == int(zoekterm))).order_by(\
             orders_inkoop_artikelen.c.orderinkoopID, orders_inkoop_artikelen.c.regel)
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_artikelen.c.artikelID == artikelen.c.artikelID,\
         orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_artikelen.c.levering_start.like(zoekterm+'%')))
    elif keuze == 7 and validZt.zt(zoekterm, 10):
        sel = select([orders_inkoop_artikelen,orders_inkoop, leveranciers,artikelen])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_artikelen.c.artikelID == artikelen.c.artikelID,\
         orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_artikelen.c.levering_eind.like(zoekterm+'%')))
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
            self.setWindowTitle('Inkooporders opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnHidden(1,True)
            table_view.setColumnHidden(2,True)
            table_view.setColumnHidden(16,True)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setColumnWidth(28, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.setItemDelegateForColumn(28, showImage(self))
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
        
    class showImage(QStyledItemDelegate):  
       def __init__(self, parent):
           QStyledItemDelegate.__init__(self, parent)
       def paint(self, painter, option, index):        
            painter.fillRect(option.rect,QColor(255,255,255))
            image = QImage(index.data())
            pixmap = QPixmap(image)
            pixmap.scaled(256,256)  
            return(painter.drawPixmap(option.rect, pixmap))
   
    header = ['OrderartikelID','Orderinkoopnummer','Artikelnummer', 'Bestelaantal',\
              'Inkoopprijs','Levering start','Levering eind', 'Recl.Datum', 'Recl.aantal', \
              'Ontvangsdatum', 'Ontv.aantal', 'Acceptatiedatum','Geacc.hoeveelheid',\
              'Betaald', 'Regelnummer','Orderinkoopnummer', 'Leveranciernummer',\
              'Besteldatum', 'Goedgekeeurd','Betaald', 'Afgemeld','Leveranciernummer',\
              'Bedrijfsnaam', 'Rechtsvorm', 'Artikelnummer','Artikelomschr',\
              'Artikelvoorraad', 'Artikeleenheid', 'Afbeelding',]    
        
    data_list=[]
    for row in rpinkorders:
        data_list += [(row)]  
        
    def showOrder(idx):
        mordartlevnr = idx.data()
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        if idx.column() == 0:
            seloal = select([orders_inkoop_artikelen, orders_inkoop, leveranciers, artikelen]).\
               where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
               leverancierID, orders_inkoop_artikelen.c.artikelID == artikelen.c.\
               artikelID, orders_inkoop_artikelen.c.orderinkoopID == orders_inkoop.c.\
               orderinkoopID, orders_inkoop_artikelen.c.ordartlevID == mordartlevnr))
            rpordartlev = con.execute(seloal).first()
            
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Inkooporders materialen opvragen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                        
                    self.Orderinkoopnummer = QLabel()
                    q2Edit = QLineEdit(str(rpordartlev[15]))
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setFixedWidth(90)
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
        
                    self.Leveranciernummer = QLabel()
                    q4Edit = QLineEdit(str(rpordartlev[16]))
                    q4Edit.setFixedWidth(90)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
         
                    self.Besteldatum = QLabel()
                    q5Edit = QLineEdit(str(rpordartlev[17]))
                    q5Edit.setFixedWidth(90)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)                              
                    
                    self.Goedgekeurd = QLabel()
                    q8Edit = QLineEdit(str(rpordartlev[18]))
                    q8Edit.setFixedWidth(90)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                                                         
                    self.Betaald = QLabel()
                    q11Edit = QLineEdit(str(rpordartlev[19]))
                    q11Edit.setFixedWidth(90)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                      
                    self.Afgemeld = QLabel()
                    q12Edit = QLineEdit(str(rpordartlev[20]))
                    q12Edit.setFixedWidth(90)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    self.Leveranciernummer = QLabel()
                    q13Edit = QLineEdit(str(rpordartlev[21]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
             
                    self.Bedrijfsnaam = QLabel()
                    q19Edit = QLineEdit(str(rpordartlev[22]))
                    q19Edit.setFixedWidth(380)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
             
                    self.Rechtsvorm = QLabel()
                    q14Edit = QLineEdit(str(rpordartlev[23]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                                    
                    self.Artikelnummer= QLabel()
                    q15Edit = QLineEdit(str(rpordartlev[24]))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setDisabled(True)
          
                    self.Artikelomschrijving = QLabel()
                    q16Edit = QLineEdit(str(rpordartlev[25]))
                    q16Edit.setFixedWidth(370)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                        
                    self.Bestelaantal = QLabel()
                    q18Edit = QLineEdit('{:12.2f}'.format(rpordartlev[3]))
                    q18Edit.setFixedWidth(90)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                    
                    self.Inkoopprijs = QLabel()
                    q17Edit = QLineEdit('{:12.2f}'.format(rpordartlev[4]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    self.Levering_start = QLabel()
                    q20Edit = QLineEdit(str(rpordartlev[5]))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                                   
                    self.Levering_eind = QLabel()
                    q28Edit = QLineEdit(str(rpordartlev[6]))
                    q28Edit.setFixedWidth(100)
                    q28Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q28Edit.setDisabled(True)
                    
                    self.Reclamatiedatum = QLabel()
                    q21Edit = QLineEdit(str(rpordartlev[7]))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q21Edit.setDisabled(True)
        
                    self.Reclamatieaantal = QLabel()
                    q22Edit = QLineEdit('{:12.2f}'.format(rpordartlev[8]))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q22Edit.setDisabled(True)
        
                    self.Ontvangdatum = QLabel()
                    q23Edit = QLineEdit(str(rpordartlev[9]))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q23Edit.setDisabled(True)
                    
                    self.Ontvangstaantal = QLabel()
                    q24Edit = QLineEdit('{:12.2f}'.format(rpordartlev[10]))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q24Edit.setDisabled(True)
                    
                    self.Acceptatiedatum = QLabel()
                    q25Edit = QLineEdit(str(rpordartlev[11]))
                    q25Edit.setFixedWidth(100)
                    q25Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q25Edit.setDisabled(True)
                    
                    self.Aantalgeaccepteerd = QLabel()
                    q26Edit = QLineEdit('{:12.2f}'.format(rpordartlev[12]))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q26Edit.setDisabled(True)
                    
                    self.Betaaldaantal = QLabel()
                    q27Edit = QLineEdit('{:12.2f}'.format(rpordartlev[13]))
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
                    
                    lbl1 = QLabel('Ordergegevens')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(QLabel('Orderinkoopnummer'), 2, 0)
                    grid.addWidget(q2Edit, 2, 1) 
                                                        
                    grid.addWidget(QLabel('Leveranciernummer'), 2, 2)
                    grid.addWidget(q4Edit, 2, 3)
                    
                    grid.addWidget(QLabel('Besteldatum'), 2, 4)
                    grid.addWidget(q5Edit, 2 , 5) 
                     
                    grid.addWidget(QLabel('Goedgekeurd'), 3, 0)
                    grid.addWidget(q8Edit, 3, 1)
                                                              
                    grid.addWidget(QLabel('Betaaldatum'), 3, 2)
                    grid.addWidget(q11Edit, 3, 3)
                                              
                    grid.addWidget(QLabel('Afgemeld'), 3, 4)
                    grid.addWidget(q12Edit, 3, 5)
         
                    lbl2 = QLabel('Orderregelgegevens'+' - regelnummer: '+str(rpordartlev[14]))
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")               
                    grid.addWidget(lbl2, 5, 0, 1, 4)
                    grid.addWidget(QLabel('Leveranciernummer'), 6, 0)
                    grid.addWidget(q13Edit, 6, 1) 
                    
                    grid.addWidget(QLabel('Bedrijfsnaam'), 7, 0)
                    grid.addWidget(q19Edit, 7, 1, 1, 4) 
                                   
                    grid.addWidget(q14Edit, 7, 4) 
               
                    grid.addWidget(QLabel('Artikelnummer'), 8, 0)
                    grid.addWidget(q15Edit, 8, 1) 
                     
                    pixmap = QPixmap(rpordartlev[28])
                    lbl3 = QLabel()
                    lbl3.setPixmap(pixmap)
                    grid.addWidget(lbl3 , 8, 3, 2, 3, Qt.AlignTop)
                            
                    grid.addWidget(QLabel('Artikelomschrijving'), 10, 0)
                    grid.addWidget(q16Edit, 10, 1, 1, 4)
                    
                    grid.addWidget(QLabel('Bestelaantal'), 11, 0)
                    grid.addWidget(q18Edit, 11, 1)
                    
                    grid.addWidget(QLabel('Inkoopprijs'), 11, 2)
                    grid.addWidget(q17Edit, 11, 3)
                    
                    grid.addWidget(QLabel('Levering start'), 11, 4)
                    grid.addWidget(q20Edit, 11, 5)
                    
                    grid.addWidget(QLabel('Levering eind'), 12, 0)
                    grid.addWidget(q28Edit, 12, 1)
                                   
                    grid.addWidget(QLabel('Reclamatiedatum'), 12, 2)
                    grid.addWidget(q21Edit, 12, 3)
                    
                    grid.addWidget(QLabel('Reclamaties aantal'), 12, 4)
                    grid.addWidget(q22Edit, 12, 5)
                    
                    grid.addWidget(QLabel('Ontvangstdatum'), 13, 0)
                    grid.addWidget(q23Edit, 13, 1)
                    
                    grid.addWidget(QLabel('Ontvangen aantal'), 13, 2)
                    grid.addWidget(q24Edit, 13, 3)
                    
                    grid.addWidget(QLabel('Acceptatie datum'), 13,  4)
                    grid.addWidget(q25Edit, 13, 5)
                    
                    grid.addWidget(QLabel('Acceptatie aantal'), 14, 0)
                    grid.addWidget(q26Edit, 14, 1)
                    
                    grid.addWidget(QLabel('Betaald aantal'), 14, 2)
                    grid.addWidget(q27Edit, 14, 3)
                                                              
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 0, 1, 6, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 350, 300)
                                               
                    cancelBtn = QPushButton('Sluiten')
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