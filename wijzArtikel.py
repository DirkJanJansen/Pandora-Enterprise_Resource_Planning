from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                            QDialog, QMessageBox, QComboBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import  QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                                create_engine, Float)
from sqlalchemy.sql import select, update

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def wijzSluit(self, m_email):
    self.close()
    zoekArtikel(m_email)
   
def foutArtnr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Item number\nNot present!')
    msg.setWindowTitle('Article don\'t exist')
    msg.exec_()
       
def progSluit():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Program closed\nGoodbye!')
    msg.setWindowTitle('Close')
    msg.exec_()
    
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Your data have been adjusted!')
    msg.setWindowTitle('Data!')
    msg.exec_()
           
def _11check(martikelnr):
    number = str(martikelnr)
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
    
def zoekArtikel(m_email):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify articles.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Artikelnummer = QLabel()
            artEdit = QLineEdit()
            artEdit.setFixedWidth(100)
            artEdit.setFont(QFont("Arial",10))
            artEdit.textChanged.connect(self.artChanged)
            reg_ex = QRegExp('^[2]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, artEdit)
            artEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight) 
        
    
            self.setFont(QFont('Arial', 10))
    
            grid.addWidget(QLabel('Articlenumber'), 1, 1)
            grid.addWidget(artEdit, 1, 2)
       
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
        def artChanged(self, text):
            self.Artikelnummer.setText(text)
    
        def returnArtikelnummer(self):
            return self.Artikelnummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnArtikelnummer()]
       
    window = Widget()
    data = window.getData()
    if data[0]:
        martikelnr = data[0]
    else:
        martikelnr = 0
    
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True))
  
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
   
    s = select([artikelen]).where(artikelen.c.artikelID == int(martikelnr))
    rp = conn.execute(s).first()
    if len(martikelnr) == 9 and _11check(martikelnr) and rp:
        martikelnr = int(martikelnr)
    else:
        foutArtnr()
        zoekArtikel(m_email)
    wijzArt(m_email, martikelnr)
        
        
def wijzArt(m_email, martikelnr):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float),
        Column('locatie_magazijn', String(10)),
        Column('artikelgroep', String),
        Column('barcode', Integer),
        Column('thumb_artikel', String(70)),
        Column('foto_artikel', String(70)),
        Column('categorie', String(10)),
        Column('afmeting', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
    rpartikel = conn.execute(sel).first()
    conn.close()
                
    class Widget(QDialog):
        def __init__(self):
            super(Widget, self).__init__()
        
            self.setWindowTitle("Modify articles")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        
            self.setFont(QFont('Arial', 10))
                       
            self.Artikelnummer = QLabel()
            q1Edit = QLineEdit(str(rpartikel[0]))
            q1Edit.setFixedWidth(100)
            q1Edit.setDisabled(True)
            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q1Edit.textChanged.connect(self.q1Changed)
        
            self.Artikelomschrijving = QLabel()
            q2Edit = QLineEdit(str(rpartikel[1]))
            q2Edit.setFixedWidth(400)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed)
            
            self.Artikelprijs = QLabel()
            q3Edit = QLineEdit(str(rpartikel[2]))
            q3Edit.setFixedWidth(100)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.setAlignment(Qt.AlignRight)
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
                           
            self.Artikelvoorraad = QLabel()
            q4Edit = QLineEdit(str(round(rpartikel[3],2)))
            q4Edit.setFixedWidth(100)
            q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q4Edit.setDisabled(True)
            q4Edit.setAlignment(Qt.AlignRight)
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.Artikeleenheid = QLabel()
            q5Edit = QComboBox()
            q5Edit.setFixedWidth(140)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            q5Edit.addItem('piece')
            q5Edit.addItem('stuk')
            q5Edit.addItem('100')
            q5Edit.addItem('meter')
            q5Edit.addItem('kg')
            q5Edit.addItem('liter')
            q5Edit.addItem('m²')
            q5Edit.addItem('m³')
            q5Edit.setCurrentIndex(q5Edit.findText(rpartikel[4]))
            q5Edit.activated[str].connect(self.q5Changed)        
                    
            self.Minimumvoorraad = QLabel()
            q6Edit = QLineEdit(str(round(rpartikel[5],2)))
            q6Edit.setFixedWidth(100)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.setAlignment(Qt.AlignRight)
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
          
            self.Bestelgrootte = QLabel()
            q7Edit = QLineEdit(str(round(rpartikel[6],2)))
            q7Edit.setFixedWidth(100)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.setAlignment(Qt.AlignRight)
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
                         
            self.Magazijnlocatie = QLabel()
            q8Edit = QLineEdit(str(rpartikel[7]))
            q8Edit.setFixedWidth(100)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            
            self.Artikelgroep = QLabel()
            q9Edit = QLineEdit(str(rpartikel[8]))
            q9Edit.setFixedWidth(200)
            q9Edit.setFont(QFont("Arial",10))
            q9Edit.textChanged.connect(self.q9Changed)
            
            self.Barcode = QLabel()
            q10Edit = QLineEdit(str(rpartikel[9]))
            q10Edit.setFixedWidth(130)
            q10Edit.setFont(QFont("Arial",10))
            q10Edit.textChanged.connect(self.q10Changed)
            reg_ex = QRegExp('^[1-9]{1,13}$')
            input_validator = QRegExpValidator(reg_ex, q10Edit)
            q10Edit.setValidator(input_validator)
        
            self.Artikelthumbnail = QLabel()
            q11Edit = QLineEdit(str(rpartikel[10]))
            q11Edit.setFixedWidth(400)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.textChanged.connect(self.q11Changed)
                    
            self.Artikelfoto = QLabel()
            q12Edit = QLineEdit(str(rpartikel[11]))
            q12Edit.setFixedWidth(400)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed)
         
            self.Categorie = QLabel()
            q13Edit = QComboBox()
            q13Edit.setFixedWidth(320)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            q13Edit.addItem('1. Stock controlled < 3 weeks')
            q13Edit.addItem('2. Stock controlled < 12 weeks')
            q13Edit.addItem('3. Stock controlled < 26 weeks')
            q13Edit.addItem('4. Stock controlled < 52 weeks')
            q13Edit.addItem('5. Reservation < 3 weeks')
            q13Edit.addItem('6. Reservation < 6 weeks')
            q13Edit.addItem('7. Reservation < 12 weeks')
            q13Edit.addItem('8. Reservation < 24 weeks')
            q13Edit.addItem('9. Reservation < 52 weeks')        
            q13Edit.setCurrentIndex(rpartikel[12]-1)
            q13Edit.activated[str].connect(self.q13Changed)        
                    
            grid = QGridLayout()
            grid.setSpacing(20)
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
        
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight) 
        
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Modify article'), 1, 1)
        
            grid.addWidget(QLabel('                                 *'), 2, 0)
            grid.addWidget(QLabel('Required fields'), 2, 1)
        
            grid.addWidget(QLabel('Article number'), 3, 0)
            grid.addWidget(q1Edit, 3, 1)
        
            grid.addWidget(QLabel('Article description       *'), 4, 0)
            grid.addWidget(q2Edit, 4, 1)
        
            grid.addWidget(QLabel('Article price                *'), 5, 0)
            grid.addWidget(q3Edit, 5 , 1) 
        
            grid.addWidget(QLabel('Article stock'), 6, 0)
            grid.addWidget(q4Edit, 6, 1)
          
            grid.addWidget(QLabel('Unit                            *'), 7, 0)
            grid.addWidget(q5Edit, 7, 1)
        
            grid.addWidget(QLabel('Minimum stock            *'), 8, 0)
            grid.addWidget(q6Edit, 8, 1)
        
            grid.addWidget(QLabel('Order size                   *'), 9, 0)
            grid.addWidget(q7Edit, 9, 1)
        
            grid.addWidget(QLabel('Warehouse location     *'), 10, 0)
            grid.addWidget(q8Edit, 10, 1)
        
            grid.addWidget(QLabel('Article group               *'), 11, 0)
            grid.addWidget(q9Edit, 11, 1) 
        
            grid.addWidget(QLabel('Barcode'), 12, 0)
            grid.addWidget(q10Edit, 12, 1)
        
            grid.addWidget(QLabel('Article thumbnail'), 13, 0)
            grid.addWidget(q11Edit, 13, 1)
        
            grid.addWidget(QLabel('Artikel photo'), 14, 0)
            grid.addWidget(q12Edit, 14, 1)
            
            grid.addWidget(QLabel('Category                    *'),15,0)
            grid.addWidget(q13Edit, 15, 1) 
        
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 1)
                
            applyBtn = QPushButton('Modify')
            applyBtn.clicked.connect(self.accept)
        
            grid.addWidget(applyBtn, 15, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: wijzSluit(self, m_email))
        
            grid.addWidget(cancelBtn, 14, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                          
            self.setLayout(grid)
            self.setGeometry(500, 100, 350, 300)
        
        def q1Changed(self, text):
            self.Artikelnummer.setText(text)
        
        def q2Changed(self, text):
            self.Artikelomschrijving.setText(text)
        
        def q3Changed(self, text):
            self.Artikelprijs.setText(text)
        
        def q4Changed(self, text):
            self.Artikelvoorraad.setText(text)
        
        def q5Changed(self, text):
            self.Artikeleenheid.setText(text)
        
        def q6Changed(self, text):
            self.Minimumvoorraad.setText(text)
        
        def q7Changed(self, text):
            self.Bestelgrootte.setText(text)
        
        def q8Changed(self, text):
            self.Magazijnlocatie.setText(text)
        
        def q9Changed(self, text):
            self.Artikelgroep.setText(text)
        
        def q10Changed(self, text):
            self.Barcode.setText(text)
        
        def q11Changed(self, text):
            self.Artikelthumbnail.setText(text)
        
        def q12Changed(self, text):
            self.Artikelfoto.setText(text)
            
        def q13Changed(self, text):
            self.Categorie.setText(text)
        
        def returnArtikelnummer(self):
            return self.Artikelnummer.text()
        
        def returnArtikelomschrijving(self):
            return self.Artikelomschrijving.text()
        
        def returnArtikelprijs(self):
            return self.Artikelprijs.text()
        
        def returnArtikelvoorraad(self):
            return self.Artikelvoorraad.text()
        
        def returnArtikeleenheid(self):
            return self.Artikeleenheid.text()
        
        def returnMinimumvoorraad(self):
            return self.Minimumvoorraad.text()
        
        def returnBestelgrootte(self):
            return self.Bestelgrootte.text()
        
        def returnMagazijnlocatie(self):
            return self.Magazijnlocatie.text()
        
        def returnArtikelgroep(self):
            return self.Artikelgroep.text()
        
        def returnBarcode(self):
            return self.Barcode.text()
        
        def returnArtikelthumbnail(self):
            return self.Artikelthumbnail.text()
        
        def returnArtikelfoto(self):
            return self.Artikelfoto.text()
        
        def returnCategorie(self):
            return self.Categorie.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget()
            dialog.exec_()
            return [dialog.returnArtikelnummer(),dialog.returnArtikelomschrijving(),\
                    dialog.returnArtikelprijs(), dialog.returnArtikelvoorraad(),\
                    dialog.returnArtikeleenheid(), dialog.returnMinimumvoorraad(),\
                    dialog.returnBestelgrootte(), dialog.returnMagazijnlocatie(),\
                    dialog.returnArtikelgroep(), dialog.returnBarcode(),\
                    dialog.returnArtikelthumbnail(),dialog.returnArtikelfoto(),\
                    dialog.returnCategorie()]
            
    window = Widget()
    data = window.getData()
    if data[1]:
        martomschr = data[1]
    else:
        martomschr = rpartikel[1]
    if data[2]:
        martprijs = str(data[2])
    else:
        martprijs = str(rpartikel[2])
    if data[3]:
        martvrd = str(data[3])
    else:
        martvrd = str(rpartikel[3])
    if data[4]:
        marteenh = data[4]
    else:
        marteenh = rpartikel[4]
    if data[5]:
        martminvrd = str(data[5])
    else:
        martminvrd = str(rpartikel[5])
    if data[6]:
        martbestgr = str(data[6])
    else:
        martbestgr = str(rpartikel[6])
    if data[7]:
        mlocmag = data[7]
    else:
        mlocmag = rpartikel[7]
    if data[8]:
        martgr = data[8]
    else:
        martgr = rpartikel[8]
    if data[9]:
        mbarc = int(data[9])
    else:
        mbarc = int(rpartikel[9])
    if data[10]:
        mthumb = data[10]
    else:
        mthumb = rpartikel[10]                             
    if data[11]:
        mfotoart = data[11]
    else:
        mfotoart = rpartikel[11]
    if data[12]:
        mcat = str(data[12])[0]
    else:
        mcat = str(rpartikel[12])
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()    
        
    u = update(artikelen).where(artikelen.c.artikelID == martikelnr).\
    values(artikelomschrijving = martomschr, artikelprijs = martprijs,\
    art_voorraad = martvrd, art_eenheid = marteenh, art_min_voorraad = \
    martminvrd, art_bestelgrootte = martbestgr, locatie_magazijn = mlocmag,\
    artikelgroep = martgr, barcode = mbarc, thumb_artikel = mthumb,\
    foto_artikel = mfotoart, categorie = mcat)  
    conn.execute(u)
    conn.close()
    updateOK()
    zoekArtikel(m_email)