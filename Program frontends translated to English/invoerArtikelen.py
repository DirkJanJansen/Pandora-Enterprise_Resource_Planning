from login import hoofdMenu
from datetime import date
from sys import platform
import barcode
from barcode.writer import ImageWriter #for barcode as png
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                            QDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import  QRegExp, Qt
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                            create_engine, func, Float)
from sqlalchemy.sql import select

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Articles')
    msg.exec_()
    return

def geenGegevens():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Not (all) required data inserted!')
    msg.setWindowTitle('Data')
    msg.exec_()
    
def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalArtikelnr():
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    try:
        martikelnr=(conn.execute(select([func.max(artikelen.c.artikelID,\
                type_=Integer)])).scalar())
        martikelnr=int(maak11proef(martikelnr))
    except:
        martikelnr = 200000019
        
    conn.close
    return(martikelnr)
 
def invArtikel(m_email): 
    martikelnr = bepaalArtikelnr()
    ean = barcode.get('ean13', '800'+str(martikelnr), writer=ImageWriter()) # for barcode as png
    mbarcode = ean.get_fullcode()  
    
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Insert Articles")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Artikelnummer = QLabel()
            q1Edit = QLineEdit(str(martikelnr))
            q1Edit.setFixedWidth(100)
            q1Edit.setDisabled(True)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed)
            
            self.Artikelomschrijving = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(400)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed)
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
            
            self.Artikelprijs = QLabel()
            q3Edit = QLineEdit('0')
            q3Edit.setFixedWidth(100)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
                           
            self.Artikelvoorraad = QLabel()
            q4Edit = QLineEdit('0')
            q4Edit.setFixedWidth(100)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.setDisabled(True)
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.Artikeleenheid = QLabel()
            q5Edit = QComboBox()
            q5Edit.setFixedWidth(160)
            q5Edit.setStyleSheet("color: black;  background-color: #D9E1D")
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.addItem(' Make your choice')
            q5Edit.addItem('piece')
            q5Edit.addItem('100')
            q5Edit.addItem('meter')
            q5Edit.addItem('kg')
            q5Edit.addItem('liter')
            q5Edit.addItem('m²')
            q5Edit.addItem('m³')
            q5Edit.activated[str].connect(self.q5Changed)      
                    
            self.Minimumvoorraad = QLabel()
            q6Edit = QLineEdit('0')
            q6Edit.setFixedWidth(100)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
          
            self.Bestelgrootte = QLabel()
            q7Edit = QLineEdit('0')
            q7Edit.setFixedWidth(100)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
                         
            self.Magazijnlocatie = QLabel()
            q8Edit = QLineEdit()
            q8Edit.setFixedWidth(100)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed)
            
            self.Artikelgroep = QLabel()
            q9Edit = QLineEdit()
            q9Edit.setFixedWidth(200)
            q9Edit.setFont(QFont("Arial",10))
            q9Edit.textChanged.connect(self.q9Changed)
            
            self.Barcode = QLabel()
            q10Edit = QLineEdit(mbarcode)
            q10Edit.setFixedWidth(130)
            q10Edit.setFont(QFont("Arial",10))
            q10Edit.textChanged.connect(self.q10Changed)
            reg_ex = QRegExp('^[1-9]{1,13}$')
            input_validator = QRegExpValidator(reg_ex, q10Edit)
            q10Edit.setValidator(input_validator)
    
            self.Artikelthumbnail = QLabel()
            q11Edit = QLineEdit('./images/thumbs/')
            q11Edit.setFixedWidth(400)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.textChanged.connect(self.q11Changed)
                    
            self.Artikelfoto = QLabel()
            q12Edit = QLineEdit('./images/')
            q12Edit.setFixedWidth(400)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed)
         
            self.Categorie = QLabel()
            q13Edit = QComboBox()
            q13Edit.setFixedWidth(320)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setStyleSheet("color: black;  background-color: #D9E1D")
            q13Edit.addItem('                    Make your choice')
            q13Edit.addItem('1. Stock controlled < 3 weeks')
            q13Edit.addItem('2. Stock controlled < 12 weeks')
            q13Edit.addItem('3. Stock controlled < 26 weeks')
            q13Edit.addItem('4. Stock controlled < 52 weeks')
            q13Edit.addItem('5. Reservation < 3 weeks')
            q13Edit.addItem('6. Reservation < 6 weeks')
            q13Edit.addItem('7. Reservation < 12 weeks')
            q13Edit.addItem('8. Reservation < 24 weeks')
            q13Edit.addItem('9. Reservation < 52 weeks')
            q13Edit.activated[str].connect(self.q13Changed)     
                    
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 2, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Insert New Article'), 1, 1)
    
            grid.addWidget(QLabel('                                *'),2 , 0)
            grid.addWidget(QLabel('Required fields  '), 2, 1)
    
            grid.addWidget(QLabel('Articlenumber'), 3, 0)
            grid.addWidget(q1Edit, 3, 1)
    
            grid.addWidget(QLabel('ArticleDescription       *'), 4, 0)
            grid.addWidget(q2Edit, 4, 1)
    
            grid.addWidget(QLabel('Articleprice                 *'), 5, 0)
            grid.addWidget(q3Edit, 5 , 1) 
    
            grid.addWidget(QLabel('Articlestock   '), 6, 0)
            grid.addWidget(q4Edit, 6, 1)
    
            grid.addWidget(QLabel('ArticleUnit                  *'), 7, 0)
            grid.addWidget(q5Edit, 7, 1)
    
            grid.addWidget(QLabel('Minimumstock            *'), 8, 0)
            grid.addWidget(q6Edit, 8, 1)
    
            grid.addWidget(QLabel('Ordersize                   *'), 9, 0)
            grid.addWidget(q7Edit, 9, 1)
    
            grid.addWidget(QLabel('WarehouseLocation    *'), 10, 0)
            grid.addWidget(q8Edit, 10, 1)
    
            grid.addWidget(QLabel('ArticleGroup               *'), 11, 0)
            grid.addWidget(q9Edit, 11, 1) 
    
            grid.addWidget(QLabel('Barcode'), 12, 0)
            grid.addWidget(q10Edit, 12, 1)
    
            grid.addWidget(QLabel('ArticleThumbnail'), 13, 0)
            grid.addWidget(q11Edit, 13, 1)
    
            grid.addWidget(QLabel('ArticlePhoto'), 14, 0)
            grid.addWidget(q12Edit, 14, 1)
            
            grid.addWidget(QLabel('Category                     *'), 15, 0)
            grid.addWidget(q13Edit, 15, 1)
    
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16, 1)

            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 15, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
            
            grid.addWidget(cancelBtn, 14, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
    
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 100)
    
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
            dialog = Widget(parent)
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
    martomschr = data[1]
    martprijs = data[2] 
    if data[2]:
        martprijs = float(martprijs)
    else:
        martprijs = float(0)
    martvrd = data[3]
    if data[3]:
        martvrd = float(martvrd)
    else:
        martvrd = float(0)
    marteenh = data[4]
    martminvrd = data[5]
    if data[5]:
        martminvrd = float(martminvrd)
    else:
        martminvrd = float(0)
    martbestgr = data[6]
    if data[6]:
        martbestgr = float(martbestgr)
    else:
        martbestgr = float(0)
    mlocmag = data[7]
    martgr = data[8]
    mbarc = data[9]
    if data[9]:
        mbarc = int(mbarc)
    else:
        mbarc = int(0)
    mthumb = data[10]
    mfotoart = data[11]
    mcat = 0
    if data[12]:
        mcat = data[12]
        mcat = int(mcat[0])
    if martomschr and martprijs and marteenh and martminvrd and martbestgr and \
               mlocmag and martgr and mcat:
 
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
            Column('afmeting', String),
            Column('mutatiedatum', String))
    
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        martikelnr=bepaalArtikelnr()
        metadata.create_all(engine)
        insart = artikelen.insert().values(
        artikelID = martikelnr,
        barcode = mbarcode,
        artikelomschrijving = martomschr,
        artikelprijs = martprijs,
        art_voorraad = martvrd,
        art_eenheid = marteenh,
        art_min_voorraad = martminvrd,
        art_bestelgrootte = martbestgr,
        locatie_magazijn = mlocmag,
        artikelgroep = martgr,
        thumb_artikel = mthumb,
        foto_artikel = mfotoart,
        categorie = mcat,
        mutatiedatum = str(date.today())[0:10])
    
        conn = engine.connect()
        conn.execute(insart)
        conn.close
        ean = barcode.get('ean13', '800'+str(martikelnr), writer=ImageWriter()) # for barcode as png
        if platform == 'win32':
            ean.save('.\\forms\\Barcodelabels\\'+str(martikelnr))
        else:
            ean.save('./forms/Barcodelabels/'+str(martikelnr))
        Invoer()
        invArtikel(m_email)
    else:
        geenGegevens()
        invArtikel(m_email)
    hoofdMenu(m_email)