from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QStyledItemDelegate,\
      QComboBox, QDialog, QLineEdit, QMessageBox , QVBoxLayout, QTableView
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
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

def artKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen artikelen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(340)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('                    Sorteersleutel zoeken')
            k0Edit.addItem('1. Gesorteerd op artikelnr')
            k0Edit.addItem('2. Gesorteerd op voorraad')
            k0Edit.addItem('3. Gefilterd omschrijving')
            k0Edit.addItem('4. Gefilterd artikelgroep.')
            k0Edit.addItem('5. Gefilterd opslaglocatie.')
            k0Edit.addItem('6. Incourant na jjjj-mm-dd')
            k0Edit.addItem('7. Te bestellen via reserveringen')
            k0Edit.addItem('8. Te bestellen voorraadgestuurd')
            k0Edit.addItem('9. Min.voorraad + bestelgrootte < reservering')
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
            lbl1 = QLabel('Zoekterm')  
            grid.addWidget(lbl1, 2, 0 , 1, 1, Qt.AlignRight)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1 , 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
            cancelBtn = QPushButton('Sluiten')
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
    toonArtikelen(keuze,zoekterm, m_email)
    
def toonArtikelen(keuze,zoekterm, m_email):
    import validZt  
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('barcode', String),
        Column('artikelomschrijving', String),
        Column('thumb_artikel', String(70)),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float),
        Column('locatie_magazijn', String(10)),
        Column('artikelgroep', String),
        Column('categorie', Integer),
        Column('afmeting', String),
        Column('mutatiedatum', String),
        Column('bestelsaldo', Float),
        Column('reserveringsaldo', Float),
        Column('jaarverbruik_1', Float),
        Column('jaarverbruik_2', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
     
    if keuze == 1:
        sel = select([artikelen]).order_by(artikelen.c.artikelID)
    elif keuze == 2:
        sel = select([artikelen]).order_by(artikelen.c.art_voorraad.desc())
    elif keuze == 3:
        sel = select([artikelen]).where(artikelen.c.artikelomschrijving.ilike('%'+zoekterm+'%'))
    elif keuze == 4:
        sel = select([artikelen]).where(artikelen.c.artikelgroep.ilike('%'+zoekterm+'%'))
    elif keuze == 5:
        sel = select([artikelen]).where(artikelen.c.locatie_magazijn.ilike('%'+zoekterm+'%'))
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        sel = select([artikelen]).where(artikelen.c.mutatiedatum >= (zoekterm+'%')).\
          order_by(artikelen.c.artikelID)
    elif keuze == 7:
        sel = select([artikelen]).where(and_(artikelen.c.reserveringsaldo > 0,\
                     artikelen.c.art_voorraad+artikelen.c.bestelsaldo < \
                     artikelen.c.reserveringsaldo,artikelen.c.categorie > 4))
    elif keuze == 8:
        sel = select([artikelen]).where(and_(artikelen.c.art_voorraad < artikelen.c.art_min_voorraad,\
                    artikelen.c.categorie < 5))
    elif keuze == 9:
        sel = select([artikelen]).where(and_(artikelen.c.art_min_voorraad+artikelen.c.\
            art_bestelgrootte < artikelen.c.reserveringsaldo,artikelen.c.categorie > 4)) 
    else:
        ongInvoer()
        artKeuze(m_email)
    
    if con.execute(sel).fetchone():    
        rpartikelen = con.execute(sel)
    else:
        geenRecord()
        artKeuze(m_email)

    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Artikelen opvragen')
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
            table_view.setItemDelegateForColumn(3, showImage(self))
            table_view.setColumnWidth(3, 100)
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
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            #elif index.column() == 9 and role == Qt.DecorationRole: # alternatief picture echter
                                                                     # met tekst rechts van path
            #    return QPixmap(index.data())
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
                                       
    header = ['Artikelnr', 'Barcodenummer','Omschrijving', 'Afbeelding', 'Prijs', 'Voorraad', 'Eenheid',\
          'MinVrd', 'BestGr', 'Locatie', 'Groep', 'Categorie',\
          'Afmeting', 'Mutatie\ndatum', 'Bestelsaldo' ,'Reservering\nsaldo', \
          'Jaarverbruik\neven jaren','Jaarverbruik\noneven jaren']    
        
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
                def __init__(self):
                    super(Widget, self).__init__()
                
                    self.setWindowTitle("Artikelen opvragen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                    self.setFont(QFont('Arial', 10))
                               
                    self.Artikelnummer = QLabel()
                    q1Edit = QLineEdit(str(rpartikel[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                    
                    self.Barcode = QLabel()
                    q1aEdit = QLineEdit(str(rpartikel[1]))
                    q1aEdit.setFixedWidth(130)
                    q1aEdit.setAlignment(Qt.AlignRight)
                    q1aEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1aEdit.setDisabled(True)
    
                    self.Artikelomschrijving = QLabel()
                    q2Edit = QLineEdit(str(rpartikel[2]))
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setFixedWidth(400)
                    q2Edit.setDisabled(True)
                    
                    self.Artikelprijs = QLabel()
                    q3Edit = QLineEdit('{:12.2f}'.format(rpartikel[4]))
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setFixedWidth(100)
                    q3Edit.setDisabled(True)
                                    
                    self.Artikelvoorraad = QLabel()
                    q4Edit = QLineEdit('{:12.2f}'.format(rpartikel[5]))
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setFixedWidth(100)
                    q4Edit.setDisabled(True)
                     
                    self.Bestelsaldo = QLabel()
                    q16Edit = QLineEdit('{:12.2f}'.format(rpartikel[14]))
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setFixedWidth(100)
                    q16Edit.setDisabled(True)
                    
                    self.Artikeleenheid = QLabel()
                    q5Edit = QLineEdit(rpartikel[6])
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setFixedWidth(100)
                    q5Edit.setDisabled(True)
          
                    self.Minimumvoorraad = QLabel()
                    q6Edit = QLineEdit('{:12.2f}'.format(rpartikel[7]))
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setFixedWidth(100)
                    q6Edit.setDisabled(True)
         
                    self.Bestelgrootte = QLabel()
                    q7Edit = QLineEdit('{:12.2f}'.format(rpartikel[8]))
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setFixedWidth(100)
                    q7Edit.setDisabled(True)
                    
                    self.Reserveringsaldo = QLabel()
                    q12Edit = QLineEdit('{:12.2f}'.format(rpartikel[15]))
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setFixedWidth(100)
                    q12Edit.setDisabled(True)
                                   
                    self.Magazijnlocatie = QLabel()
                    q8Edit = QLineEdit(str(rpartikel[9]))
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setFixedWidth(100)
                    q8Edit.setDisabled(True)
                    
                    self.Artikelgroep = QLabel()
                    q9Edit = QLineEdit(str(rpartikel[10]))
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setFixedWidth(200)
                    q9Edit.setDisabled(True)
             
                    self.Artikelthumbnail = QLabel()
                    q11Edit = QLineEdit(str(rpartikel[3]))
                    q11Edit.setFixedWidth(400)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                           
                    self.Categorie = QLabel()
                    q13Edit = QLineEdit(str(rpartikel[11]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
                    
                    self.Afmeting = QLabel()
                    q14Edit = QLineEdit(str(rpartikel[12]))
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setFixedWidth(100)
                    q14Edit.setDisabled(True)
                    
                    self.Mutatiedatum = QLabel()
                    q15Edit = QLineEdit(str(rpartikel[13]))
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q15Edit.setFixedWidth(100)
                    q15Edit.setDisabled(True)
                            
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
                    
                    grid.addWidget(QLabel('Barcodenummer'), 1, 2, 2, 1)
                    grid.addWidget(q1aEdit, 1, 3, 2, 1)
                
                    grid.addWidget(QLabel('Artikelomschrijving'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1, 1 ,3)
                    
                    grid.addWidget(QLabel('Artikelgroep'), 4, 0)
                    grid.addWidget(q9Edit, 4, 1, 1, 3) 
                    
                    grid.addWidget(QLabel('Afmeting'),5, 0)
                    grid.addWidget(q14Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Eenheid'), 5, 2)
                    grid.addWidget(q5Edit, 5, 3)
                    
                    grid.addWidget(QLabel('Magazijnlocatie'), 6, 0)
                    grid.addWidget(q8Edit, 6, 1)
         
                    grid.addWidget(QLabel('Artikelprijs'), 6, 2)
                    grid.addWidget(q3Edit, 6 , 3) 
                
                    grid.addWidget(QLabel('Artikelvoorraad'), 7, 0)
                    grid.addWidget(q4Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Minimumvoorraad'), 7, 2)
                    grid.addWidget(q6Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Bestelsaldo'), 8, 0)
                    grid.addWidget(q16Edit, 8, 1)
                    
                    grid.addWidget(QLabel('Reserveringsaldo '), 8, 2)
                    grid.addWidget(q12Edit, 8, 3)
                    
                    grid.addWidget(QLabel('Bestelgrootte '), 9, 0)
                    grid.addWidget(q7Edit, 9, 1)
                    
                    grid.addWidget(QLabel('Categorie'),9 ,2)
                    grid.addWidget(q13Edit, 9, 3)
        
                    grid.addWidget(QLabel('Mutatiedatum'),10, 0)
                    grid.addWidget(q15Edit, 10, 1)
          
                    pixmap = QPixmap(rpartikel[9])
                    lbl2 = QLabel(self)
                    lbl2.setPixmap(pixmap)
                    grid.addWidget(lbl2 , 1, 2, 2, 2, Qt.AlignRight)
                
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 12, 0, 1, 4, Qt.AlignCenter)
                        
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 11, 3, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                  
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 350, 300)
            win = Widget()
            win.exec_()      
                                   
    win = MyWindow(data_list, header)
    win.exec_()
    artKeuze(m_email)