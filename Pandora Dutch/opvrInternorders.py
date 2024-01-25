from login import hoofdMenu
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
     QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit    
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, and_, update

def jaarweek():
    dt = datetime.datetime.now()
    week = ('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
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
 
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Werkgeleidebrief printen')
    msg.exec_()
    
def printWerkbrief(mwerkorder, rpord, header):
    from sys import platform
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('werknummerID', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('subtotaal', Float),
         Column('resterend', Float))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('art_eenheid', String),
         Column('locatie_magazijn', String))
                                    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selmat = select([materiaallijsten, artikelen])\
      .where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.werknummerID == mwerkorder)).order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)
    mblad = 1
    rgl = 0
    if platform == 'win32':
        filename = '.\\forms\\Werkbrieven\\materiaallijst_werkgeleidebrief_'+str(mwerkorder)+'.txt'
    else:
        filename = './forms/Werkbrieven/materiaallijst_werkgeleidebrief_'+str(mwerkorder)+'.txt'
    kop=\
    ('Materiaallijst van Werkorder:   '+ str(mwerkorder)+'   Datum: '+str(datetime.datetime.now())[0:10]+'  Blad :  '+str(mblad)+'\n'+
    '=====================================================================================================\n'+
    'Regel Artikelnr    Omschrijving                       Eenheid       Aantal      Ontvangen            \n'+
    '=====================================================================================================\n')
    for row in rpmat:
        if rgl == 0 or rgl%57 == 0:
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
        rgl += 1
        open(filename,'a').write('{:>5d}'.format(rgl)+' '+'{:<13d}'.\
            format(row[7])+'{:<35.33s}'.format(row[8])+'{:<8.6s}'.format(row[9])+\
            '  '+'{:10.2f}'.format(row[4])+'     '+'{:10.2f}'.format(row[4]-row[6])+'\n')
    
    mblad = 1
    rgl = 0
    k = 0
    if platform == 'win32':
        filename1 = '.\\forms\\Werkbrieven\\werkgeleidebrief_'+str(mwerkorder)+'.txt' 
    else:
        filename1 = './forms/Werkbrieven/werkgeleidebrief_'+str(mwerkorder)+'.txt'
    kop1=\
     ('Werkorder: '+str(mwerkorder)+' Werkgeleidebrief  Datum: '+str(datetime.datetime.now())[0:10]+' Blad : '+str(mblad)+'\n'\
     '=====================================================================================================\n'+
     'Regel Omschrijving bewerking   Aantal  Steltijd  Stuktijd  Totaaluren  Gemaakte uren                 \n'+
     '=====================================================================================================\n')
    for column in rpord:
        if rgl == 0 or rgl%57 == 0:
            if rgl == 0:
                open(filename1, 'w').write(kop1)
            elif rgl%57 == 0:
                open(filename1, 'a').write(kop1)
            mblad += 1
        if k == 3 and column:
            mhoev = column
        if k>17 and k<90 and column:
            if header[k][0] == 'S':
                mstel = column
            elif header[k][0] == 'B':
                rgl += 1
                mstuk = column
                mgemaakt = rpord[k+1]
                msubtot=mstuk*mhoev+mstel
                mbewerking = header[k][1:].title()
                open(filename1,'a').write('{:>5s}'.format(str(rgl))+' '+'{:<23.23s}'\
                  .format(mbewerking)+'{:>8.2f}'.format(mhoev)+'  '+'{:>8.2f}'.format(mstel)+\
                   '  '+'{:>8.2f}'.format(mstuk)+'    '+'{:>8.2f}'.format(msubtot)+'{:>15.2f}'\
                   .format(mgemaakt)+'\n')
                    
        k += 1
    if platform == 'win32':
           os.startfile(filename, "print")
           os.startfile(filename1, "print")
    else:
        os.system("lpr "+filename)
        os.system("lpr "+filename1)
 
    printing()
            
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
            k0Edit.setFont(QFont("Arial", 10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('        Sorteersleutel Orders Intern')
            k0Edit.addItem('1. Alle Interne Orders')
            k0Edit.addItem('2. Gefilterd op Werordernummer')
            k0Edit.addItem('3. Gefilterd op Artikelnummer')
            k0Edit.addItem('4. Gefilterd op (deel) startdatum')
            k0Edit.addItem('5. Gefilterd op (deel) datum afgemeld')
            k0Edit.addItem('6. Gefilterd op voorgangstatus A-H')
            k0Edit.addItem('7. Gefilterd op (deel) omschrijving')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp('^.{0,40}$')
            input_validator = QRegExpValidator(reg_ex, zktermEdit)
            zktermEdit.setValidator(input_validator)
            zktermEdit.textChanged.connect(self.zktermChanged)
         
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                           
            grid.addWidget(k0Edit, 2, 1)   
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                
            grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(120)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))

            grid.addWidget(cancelBtn, 4, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(120)
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

def toonOrders(keuze,zoekterm, m_email):
    import validZt
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1700, 900)
            self.setWindowTitle('Interne orders opvragen')
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
            table_view.clicked.connect(ShowSelection)
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
              
    header = ['Werkorder', 'Omschrijving','Artikelnummer','Hoeveelheid',\
               'Werkbrief','Besteldatum', 'Voortgangstatus','Statusweek','Boekdatum',\
               'Startdatum', 'Afgemeld','Begroot Totaal','Werkelijk Totaal',\
               'Begroot Materialen','Werkelijk Materialen','Begroot Lonen',\
               'Werkelijk Lonen', 'Meerminderwerk', 'Szagen','Bzagen', 'Wzagen',\
               'Sschaven','Bschaven', 'Wschaven', 'Ssteken','Bsteken', 'Wsteken',\
               'Sboren','Bboren', 'Wboren','Sfrezen','Bfrezen','WFrezen',\
               'Sdraaien klein', 'Bdraaien klein','Wdraaien klein','Sdraaien groot',\
               'Bdraaien groot','Wdraaien groot','Stappen','Btappen','Wtappen',\
               'Snube draaien','Bnube draaien','Wnube draaien','Snube bewerken',\
               'Bnube bewerken', 'Wnube bewerken', 'Sknippen','Bknippen', 'Wknippen',\
               'Skanten', 'Bkanten', 'Wkanten','Sstansen','Bstansen', 'Wstansen',\
               'Slassen Co2', 'Blassen Co2', 'Wlassen Co2','Slassen hand','Blassen hand',\
               'Wlassen hand','Sverpakken','Bverpakken','Wverpakken', 'Sverzinken',\
               'Bverzinken','Wverzinken','Smoffelen','Bmoffelen', 'Wmoffelen',\
               'Sschilderen','Bschilderen', 'Wschilderen','Sspuiten','Bspuiten',\
               'Wspuiten','Sponsen','Bponsen', 'Wponsen','Spersen','Bpersen',\
               'Wpersen','Sgritstralen','Bgritstralen','Wgritstralen','Smontage',\
               'Bmontage','Wmontage', 'Wreisuren', 'Gereed', 'Goedgekeurd']
    
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
    seloi = select([orders_intern]).order_by(orders_intern.c.werkorderID)
    rpoi = con.execute(seloi)
    
    for row in rpoi:
        mvg = row[6]
        btotaal = row[13]+row[15] +row[17]
        wtotaal = row[14]+row[16]
        mstatwk = row[4]
        if mvg == 'A':
            if wtotaal > 0:
                mvg = 'B'
                mstatwk = jaarweek()
        elif mvg == 'B':      
            if wtotaal > btotaal/3:
                mvg = 'C'
                mstatwk = jaarweek()
        elif mvg == 'C':
            if wtotaal > btotaal/2:
                mvg = 'D'
                mstatwk = jaarweek()
        elif mvg == 'D':
            if wtotaal > btotaal/1.5:
                mvg = 'E'
                mstatwk = jaarweek()
        elif mvg == 'E':
            if wtotaal >= btotaal:
                mvg = 'F'
                mstatwk = jaarweek()
                    
        updordink = update(orders_intern).where(orders_intern.c.werkorderID == row[0])\
         .values(voortgangstatus=mvg,statusweek=mstatwk,begroot_totaal=btotaal,\
                 werk_totaal=wtotaal)
        con.execute(updordink)
       
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
    
    if con.execute(sel).first():
        rp = con.execute(sel)
    else:
        geenRecord()
        zoeken(m_email)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def ShowSelection(idx):
        mwerkorder = idx.data()
        if  idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selord = select([orders_intern]).where(orders_intern.c.werkorderID == mwerkorder)
            rpord = con.execute(selord).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(16)
                    
                    self.setWindowTitle("Opvragen Orders Intern")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint)
                    
                    self.setFont(QFont('Arial', 10))   
 
                    q1Edit = QLineEdit(str(rpord[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setDisabled(True)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    
                    q2Edit = QLineEdit(rpord[1])
                    q2Edit.setFixedWidth(400)
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        
                    q3Edit = QLineEdit(str(rpord[2]))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    q4Edit = QLineEdit('{:12.2f}'.format(rpord[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
           
                    q5Edit = QLineEdit(rpord[4])
                    q5Edit.setFixedWidth(200)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)   

                    q6Edit = QLineEdit(rpord[5])
                    q6Edit.setFixedWidth(100)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)   

                    q7Edit = QLineEdit(rpord[6])
                    q7Edit.setFixedWidth(20)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)                        
                    
                    q8Edit = QLineEdit(rpord[7])
                    q8Edit.setFixedWidth(100)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    q9Edit = QLineEdit(rpord[8])
                    q9Edit.setFixedWidth(100)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                
                    q10Edit = QLineEdit(rpord[9])
                    q10Edit.setFixedWidth(100)
                    q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                                                         
                    q11Edit = QLineEdit(rpord[10])
                    q11Edit.setFixedWidth(100)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                      
                    q12Edit = QLineEdit('{:12.2f}'.format(rpord[11]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    q13Edit = QLineEdit('{:12.2f}'.format(rpord[12]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
  
                    q14Edit = QLineEdit('{:12.2f}'.format(rpord[13]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                                    
                    q15Edit = QLineEdit('{:12.2f}'.format(rpord[14]))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                   
                    q16Edit = QLineEdit('{:12.2f}'.format(rpord[15]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                    
                    q17Edit = QLineEdit('{:12.2f}'.format(rpord[16]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    q18Edit =QLineEdit('{:12.2f}'.format(rpord[17]))
                    q18Edit.setFixedWidth(100)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                    
                    q19Edit = QLineEdit('{:12.2f}'.format(rpord[91]))
                    q19Edit.setFixedWidth(100)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)

                    q20Edit = QLineEdit('{:12.2f}'.format(rpord[92]))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                                
                    u1Edit = QLineEdit('{:12.2f}'.format(rpord[18]))
                    u1Edit.setFixedWidth(100)
                    u1Edit.setAlignment(Qt.AlignRight)
                    u1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u1Edit.setDisabled(True)
                    
                    u2Edit = QLineEdit('{:12.2f}'.format(rpord[19]))
                    u2Edit.setFixedWidth(100)
                    u2Edit.setAlignment(Qt.AlignRight)
                    u2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u2Edit.setDisabled(True)
                    
                    u3Edit = QLineEdit('{:12.2f}'.format(rpord[20]))
                    u3Edit.setFixedWidth(100)
                    u3Edit.setAlignment(Qt.AlignRight)
                    u3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u3Edit.setDisabled(True)
                    
                    u4Edit = QLineEdit('{:12.2f}'.format(rpord[21]))
                    u4Edit.setFixedWidth(100)
                    u4Edit.setAlignment(Qt.AlignRight)
                    u4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u4Edit.setDisabled(True)
                    
                    u5Edit = QLineEdit('{:12.2f}'.format(rpord[22]))
                    u5Edit.setFixedWidth(100)
                    u5Edit.setAlignment(Qt.AlignRight)
                    u5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u5Edit.setDisabled(True)
                    
                    u6Edit = QLineEdit('{:12.2f}'.format(rpord[23]))
                    u6Edit.setFixedWidth(100)
                    u6Edit.setAlignment(Qt.AlignRight)
                    u6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u6Edit.setDisabled(True)
                    
                    u7Edit = QLineEdit('{:12.2f}'.format(rpord[24]))
                    u7Edit.setFixedWidth(100)
                    u7Edit.setAlignment(Qt.AlignRight)
                    u7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u7Edit.setDisabled(True)
                    
                    u8Edit = QLineEdit('{:12.2f}'.format(rpord[25]))
                    u8Edit.setFixedWidth(100)
                    u8Edit.setAlignment(Qt.AlignRight)
                    u8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u8Edit.setDisabled(True)
                    
                    u9Edit = QLineEdit('{:12.2f}'.format(rpord[26]))
                    u9Edit.setFixedWidth(100)
                    u9Edit.setAlignment(Qt.AlignRight)
                    u9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u9Edit.setDisabled(True)
                    
                    u10Edit = QLineEdit('{:12.2f}'.format(rpord[27]))
                    u10Edit.setFixedWidth(100)
                    u10Edit.setAlignment(Qt.AlignRight)
                    u10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u10Edit.setDisabled(True)
                    
                    u11Edit = QLineEdit('{:12.2f}'.format(rpord[28]))
                    u11Edit.setFixedWidth(100)
                    u11Edit.setAlignment(Qt.AlignRight)
                    u11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u11Edit.setDisabled(True)
                    
                    u12Edit = QLineEdit('{:12.2f}'.format(rpord[29]))
                    u12Edit.setFixedWidth(100)
                    u12Edit.setAlignment(Qt.AlignRight)
                    u12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u12Edit.setDisabled(True)
                    
                    u13Edit = QLineEdit('{:12.2f}'.format(rpord[30]))
                    u13Edit.setFixedWidth(100)
                    u13Edit.setAlignment(Qt.AlignRight)
                    u13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u13Edit.setDisabled(True)
                    
                    u14Edit = QLineEdit('{:12.2f}'.format(rpord[31]))
                    u14Edit.setFixedWidth(100)
                    u14Edit.setAlignment(Qt.AlignRight)
                    u14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u14Edit.setDisabled(True)
                    
                    u15Edit = QLineEdit('{:12.2f}'.format(rpord[32]))
                    u15Edit.setFixedWidth(100)
                    u15Edit.setAlignment(Qt.AlignRight)
                    u15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u15Edit.setDisabled(True)
                    
                    u16Edit = QLineEdit('{:12.2f}'.format(rpord[33]))
                    u16Edit.setFixedWidth(100)
                    u16Edit.setAlignment(Qt.AlignRight)
                    u16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u16Edit.setDisabled(True)
                    
                    u17Edit = QLineEdit('{:12.2f}'.format(rpord[34]))
                    u17Edit.setFixedWidth(100)
                    u17Edit.setAlignment(Qt.AlignRight)
                    u17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u17Edit.setDisabled(True)
                    
                    u18Edit = QLineEdit('{:12.2f}'.format(rpord[35]))
                    u18Edit.setFixedWidth(100)
                    u18Edit.setAlignment(Qt.AlignRight)
                    u18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u18Edit.setDisabled(True)
                    
                    u19Edit = QLineEdit('{:12.2f}'.format(rpord[36]))
                    u19Edit.setFixedWidth(100)
                    u19Edit.setAlignment(Qt.AlignRight)
                    u19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u19Edit.setDisabled(True)
                    
                    u20Edit = QLineEdit('{:12.2f}'.format(rpord[37]))
                    u20Edit.setFixedWidth(100)
                    u20Edit.setAlignment(Qt.AlignRight)
                    u20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u20Edit.setDisabled(True)
                    
                    u21Edit = QLineEdit('{:12.2f}'.format(rpord[38]))
                    u21Edit.setFixedWidth(100)
                    u21Edit.setAlignment(Qt.AlignRight)
                    u21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u21Edit.setDisabled(True)
                                          
                    u22Edit = QLineEdit('{:12.2f}'.format(rpord[39]))
                    u22Edit.setFixedWidth(100)
                    u22Edit.setAlignment(Qt.AlignRight)
                    u22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u22Edit.setDisabled(True)
                    
                    u23Edit = QLineEdit('{:12.2f}'.format(rpord[40]))
                    u23Edit.setFixedWidth(100)
                    u23Edit.setAlignment(Qt.AlignRight)
                    u23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u23Edit.setDisabled(True)
                    
                    u24Edit = QLineEdit('{:12.2f}'.format(rpord[41]))
                    u24Edit.setFixedWidth(100)
                    u24Edit.setAlignment(Qt.AlignRight)
                    u24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u24Edit.setDisabled(True)
                    
                    u25Edit = QLineEdit('{:12.2f}'.format(rpord[42]))
                    u25Edit.setFixedWidth(100)
                    u25Edit.setAlignment(Qt.AlignRight)
                    u25Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u25Edit.setDisabled(True)
                    
                    u26Edit = QLineEdit('{:12.2f}'.format(rpord[43]))
                    u26Edit.setFixedWidth(100)
                    u26Edit.setAlignment(Qt.AlignRight)
                    u26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u26Edit.setDisabled(True)
                    
                    u27Edit = QLineEdit('{:12.2f}'.format(rpord[44]))
                    u27Edit.setFixedWidth(100)
                    u27Edit.setAlignment(Qt.AlignRight)
                    u27Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u27Edit.setDisabled(True)
                    
                    u28Edit = QLineEdit('{:12.2f}'.format(rpord[45]))
                    u28Edit.setFixedWidth(100)
                    u28Edit.setAlignment(Qt.AlignRight)
                    u28Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u28Edit.setDisabled(True)
                    
                    u29Edit = QLineEdit('{:12.2f}'.format(rpord[46]))
                    u29Edit.setFixedWidth(100)
                    u29Edit.setAlignment(Qt.AlignRight)
                    u29Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u29Edit.setDisabled(True)
                    
                    u30Edit = QLineEdit('{:12.2f}'.format(rpord[47]))
                    u30Edit.setFixedWidth(100)
                    u30Edit.setAlignment(Qt.AlignRight)
                    u30Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u30Edit.setDisabled(True)
                    
                    u31Edit = QLineEdit('{:12.2f}'.format(rpord[48]))
                    u31Edit.setFixedWidth(100)
                    u31Edit.setAlignment(Qt.AlignRight)
                    u31Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u31Edit.setDisabled(True)
                    
                    u32Edit = QLineEdit('{:12.2f}'.format(rpord[49]))
                    u32Edit.setFixedWidth(100)
                    u32Edit.setAlignment(Qt.AlignRight)
                    u32Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u32Edit.setDisabled(True)
                    
                    u33Edit = QLineEdit('{:12.2f}'.format(rpord[50]))
                    u33Edit.setFixedWidth(100)
                    u33Edit.setAlignment(Qt.AlignRight)
                    u33Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u33Edit.setDisabled(True)
                    
                    u34Edit = QLineEdit('{:12.2f}'.format(rpord[51]))
                    u34Edit.setFixedWidth(100)
                    u34Edit.setAlignment(Qt.AlignRight)
                    u34Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u34Edit.setDisabled(True)
                                              
                    u35Edit = QLineEdit('{:12.2f}'.format(rpord[52]))
                    u35Edit.setFixedWidth(100)
                    u35Edit.setAlignment(Qt.AlignRight)
                    u35Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u35Edit.setDisabled(True)
                    
                    u36Edit = QLineEdit('{:12.2f}'.format(rpord[53]))
                    u36Edit.setFixedWidth(100)
                    u36Edit.setAlignment(Qt.AlignRight)
                    u36Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u36Edit.setDisabled(True)
                    
                    u37Edit = QLineEdit('{:12.2f}'.format(rpord[54]))
                    u37Edit.setFixedWidth(100)
                    u37Edit.setAlignment(Qt.AlignRight)
                    u37Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u37Edit.setDisabled(True)
                    
                    u38Edit = QLineEdit('{:12.2f}'.format(rpord[55]))
                    u38Edit.setFixedWidth(100)
                    u38Edit.setAlignment(Qt.AlignRight)
                    u38Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u38Edit.setDisabled(True)
                    
                    u39Edit = QLineEdit('{:12.2f}'.format(rpord[56]))
                    u39Edit.setFixedWidth(100)
                    u39Edit.setAlignment(Qt.AlignRight)
                    u39Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u39Edit.setDisabled(True)
                    
                    u40Edit = QLineEdit('{:12.2f}'.format(rpord[57]))
                    u40Edit.setFixedWidth(100)
                    u40Edit.setAlignment(Qt.AlignRight)
                    u40Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u40Edit.setDisabled(True)
                    
                    u41Edit = QLineEdit('{:12.2f}'.format(rpord[58]))
                    u41Edit.setFixedWidth(100)
                    u41Edit.setAlignment(Qt.AlignRight)
                    u41Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u41Edit.setDisabled(True)
                    
                    u42Edit = QLineEdit('{:12.2f}'.format(rpord[59]))
                    u42Edit.setFixedWidth(100)
                    u42Edit.setAlignment(Qt.AlignRight)
                    u42Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u42Edit.setDisabled(True)
                    
                    u43Edit = QLineEdit('{:12.2f}'.format(rpord[60]))
                    u43Edit.setFixedWidth(100)
                    u43Edit.setAlignment(Qt.AlignRight)
                    u43Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u43Edit.setDisabled(True)
                    
                    u44Edit = QLineEdit('{:12.2f}'.format(rpord[61]))
                    u44Edit.setFixedWidth(100)
                    u44Edit.setAlignment(Qt.AlignRight)
                    u44Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u44Edit.setDisabled(True)
                    
                    u45Edit = QLineEdit('{:12.2f}'.format(rpord[62]))
                    u45Edit.setFixedWidth(100)
                    u45Edit.setAlignment(Qt.AlignRight)
                    u45Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u45Edit.setDisabled(True)
                    
                    u46Edit = QLineEdit('{:12.2f}'.format(rpord[63]))
                    u46Edit.setFixedWidth(100)
                    u46Edit.setAlignment(Qt.AlignRight)
                    u46Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u46Edit.setDisabled(True)
                    
                    u47Edit = QLineEdit('{:12.2f}'.format(rpord[64]))
                    u47Edit.setFixedWidth(100)
                    u47Edit.setAlignment(Qt.AlignRight)
                    u47Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u47Edit.setDisabled(True)
                    
                    u48Edit = QLineEdit('{:12.2f}'.format(rpord[65]))
                    u48Edit.setFixedWidth(100)
                    u48Edit.setAlignment(Qt.AlignRight)
                    u48Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u48Edit.setDisabled(True)
                    
                    u49Edit = QLineEdit('{:12.2f}'.format(rpord[66]))
                    u49Edit.setFixedWidth(100)
                    u49Edit.setAlignment(Qt.AlignRight)
                    u49Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u49Edit.setDisabled(True)
                    
                    u50Edit = QLineEdit('{:12.2f}'.format(rpord[67]))
                    u50Edit.setFixedWidth(100)
                    u50Edit.setAlignment(Qt.AlignRight)
                    u50Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u50Edit.setDisabled(True)
                    
                    u51Edit = QLineEdit('{:12.2f}'.format(rpord[68]))
                    u51Edit.setFixedWidth(100)
                    u51Edit.setAlignment(Qt.AlignRight)
                    u51Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u51Edit.setDisabled(True)
                    
                    u52Edit = QLineEdit('{:12.2f}'.format(rpord[69]))
                    u52Edit.setFixedWidth(100)
                    u52Edit.setAlignment(Qt.AlignRight)
                    u52Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u52Edit.setDisabled(True)
                    
                    u53Edit = QLineEdit('{:12.2f}'.format(rpord[70]))
                    u53Edit.setFixedWidth(100)
                    u53Edit.setAlignment(Qt.AlignRight)
                    u53Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u53Edit.setDisabled(True)
                    
                    u54Edit = QLineEdit('{:12.2f}'.format(rpord[71]))
                    u54Edit.setFixedWidth(100)
                    u54Edit.setAlignment(Qt.AlignRight)
                    u54Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u54Edit.setDisabled(True)
                    
                    u55Edit = QLineEdit('{:12.2f}'.format(rpord[72]))
                    u55Edit.setFixedWidth(100)
                    u55Edit.setAlignment(Qt.AlignRight)
                    u55Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u55Edit.setDisabled(True)
                    
                    u56Edit = QLineEdit('{:12.2f}'.format(rpord[73]))
                    u56Edit.setFixedWidth(100)
                    u56Edit.setAlignment(Qt.AlignRight)
                    u56Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u56Edit.setDisabled(True)
                    
                    u57Edit = QLineEdit('{:12.2f}'.format(rpord[74]))
                    u57Edit.setFixedWidth(100)
                    u57Edit.setAlignment(Qt.AlignRight)
                    u57Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u57Edit.setDisabled(True)
                    
                    u58Edit = QLineEdit('{:12.2f}'.format(rpord[75]))
                    u58Edit.setFixedWidth(100)
                    u58Edit.setAlignment(Qt.AlignRight)
                    u58Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u58Edit.setDisabled(True)
                    
                    u59Edit = QLineEdit('{:12.2f}'.format(rpord[76]))
                    u59Edit.setFixedWidth(100)
                    u59Edit.setAlignment(Qt.AlignRight)
                    u59Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u59Edit.setDisabled(True)
                    
                    u60Edit = QLineEdit('{:12.2f}'.format(rpord[77]))
                    u60Edit.setFixedWidth(100)
                    u60Edit.setAlignment(Qt.AlignRight)
                    u60Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u60Edit.setDisabled(True)
                    
                    u61Edit = QLineEdit('{:12.2f}'.format(rpord[78]))
                    u61Edit.setFixedWidth(100)
                    u61Edit.setAlignment(Qt.AlignRight)
                    u61Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u61Edit.setDisabled(True)
                    
                    u62Edit = QLineEdit('{:12.2f}'.format(rpord[79]))
                    u62Edit.setFixedWidth(100)
                    u62Edit.setAlignment(Qt.AlignRight)
                    u62Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u62Edit.setDisabled(True)
                    
                    u63Edit = QLineEdit('{:12.2f}'.format(rpord[80]))
                    u63Edit.setFixedWidth(100)
                    u63Edit.setAlignment(Qt.AlignRight)
                    u63Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u63Edit.setDisabled(True)
                    
                    u64Edit = QLineEdit('{:12.2f}'.format(rpord[81]))
                    u64Edit.setFixedWidth(100)
                    u64Edit.setAlignment(Qt.AlignRight)
                    u64Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u64Edit.setDisabled(True)
                    
                    u65Edit = QLineEdit('{:12.2f}'.format(rpord[82]))
                    u65Edit.setFixedWidth(100)
                    u65Edit.setAlignment(Qt.AlignRight)
                    u65Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u65Edit.setDisabled(True)
                    
                    u66Edit = QLineEdit('{:12.2f}'.format(rpord[83]))
                    u66Edit.setFixedWidth(100)
                    u66Edit.setAlignment(Qt.AlignRight)
                    u66Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u66Edit.setDisabled(True)
                    
                    u67Edit = QLineEdit('{:12.2f}'.format(rpord[84]))
                    u67Edit.setFixedWidth(100)
                    u67Edit.setAlignment(Qt.AlignRight)
                    u67Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u67Edit.setDisabled(True)
                    
                    u68Edit = QLineEdit('{:12.2f}'.format(rpord[85]))
                    u68Edit.setFixedWidth(100)
                    u68Edit.setAlignment(Qt.AlignRight)
                    u68Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u68Edit.setDisabled(True)
                    
                    u69Edit = QLineEdit('{:12.2f}'.format(rpord[86]))
                    u69Edit.setFixedWidth(100)
                    u69Edit.setAlignment(Qt.AlignRight)
                    u69Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u69Edit.setDisabled(True)
                    
                    u70Edit = QLineEdit('{:12.2f}'.format(rpord[87]))
                    u70Edit.setFixedWidth(100)
                    u70Edit.setAlignment(Qt.AlignRight)
                    u70Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u70Edit.setDisabled(True)
                    
                    u71Edit = QLineEdit('{:12.2f}'.format(rpord[88]))
                    u71Edit.setFixedWidth(100)
                    u71Edit.setAlignment(Qt.AlignRight)
                    u71Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u71Edit.setDisabled(True)
                    
                    u72Edit = QLineEdit('{:12.2f}'.format(rpord[89]))
                    u72Edit.setFixedWidth(100)
                    u72Edit.setAlignment(Qt.AlignRight)
                    u72Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u72Edit.setDisabled(True)
                    
                    u73Edit = QLineEdit('{:12.2f}'.format(rpord[90]))
                    u73Edit.setFixedWidth(100)
                    u73Edit.setAlignment(Qt.AlignRight)
                    u73Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u73Edit.setDisabled(True)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 11, 1, 1, Qt.AlignRight)
                    
                    grid.addWidget(QLabel('Interne order opvragen / werkbrief printen'), 0, 0, 1, 12, Qt.AlignCenter)

                    self.setFont(QFont('Arial', 10))
                    
                    grid.addWidget(QLabel('Werkorder'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1) 
                    
                    grid.addWidget(QLabel('Werkomschrijving'), 1, 2)
                    grid.addWidget(q2Edit, 1, 3, 1, 3) 
                                                        
                    grid.addWidget(QLabel('Artikelnummer'), 2, 0)
                    grid.addWidget(q3Edit, 2, 1)
                    
                    grid.addWidget(QLabel('Hoeveelheid'), 2, 2)
                    grid.addWidget(q4Edit, 2, 3, 1, 2) 
      
                    grid.addWidget(QLabel('Voortgangstatus'), 3, 0)
                    grid.addWidget(q7Edit, 3, 1)
                    
                    grid.addWidget(QLabel('Statusweek'), 3, 2)
                    grid.addWidget(q8Edit, 3, 3)
                    
                    grid.addWidget(QLabel('Afgemeld'), 3, 4)
                    grid.addWidget(q11Edit, 3, 5) 
                    
                    grid.addWidget(QLabel('Gereed'), 2, 4)
                    grid.addWidget(q19Edit, 2, 5)
                    
                    grid.addWidget(QLabel('Goedgekeurd'), 2, 6)
                    grid.addWidget(q20Edit, 2, 7)
                    
                    grid.addWidget(QLabel('Reisuren'), 3, 6)
                    grid.addWidget(u73Edit, 3,7)
                   
                    grid.addWidget(QLabel('Boekdatum'), 4, 0)
                    grid.addWidget(q9Edit, 4, 1) 
                    
                    grid.addWidget(QLabel('Besteldatum'), 4, 2)
                    grid.addWidget(q6Edit, 4, 3)
     
                    grid.addWidget(QLabel('Startdatum'), 4, 4)
                    grid.addWidget(q10Edit, 4, 5) 
                            
                    lbl1 = QLabel('Financiële totaal bedragen')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 6, 0, 1, 2)
                                        
                    grid.addWidget(QLabel('Begroot'), 7, 1)
                    grid.addWidget(QLabel('Werkelijk'), 7, 2)
                    grid.addWidget(QLabel('Begroot'), 7, 4)
                    grid.addWidget(QLabel('Werkelijk'), 7, 5)
                    grid.addWidget(QLabel('Begroot'), 7, 7)
                    grid.addWidget(QLabel('Werkelijk'), 7, 8)
                    grid.addWidget(QLabel('Werkelijk'), 7, 10)
                                                 
                    grid.addWidget(QLabel('Totaal'), 8, 0)
                    grid.addWidget(q12Edit, 8, 1) 
                    grid.addWidget(q13Edit, 8, 2) 
                    
                    grid.addWidget(QLabel('Materialen'), 8, 3)
                    grid.addWidget(q14Edit, 8, 4) 
                    grid.addWidget(q15Edit, 8, 5) 
                                   
                    grid.addWidget(QLabel('Lonen'), 8, 6)
                    grid.addWidget(q16Edit, 8, 7) 
                    grid.addWidget(q17Edit, 8, 8) 
                    
                    grid.addWidget(QLabel('meerminderwerk'), 8, 9)    
                    grid.addWidget(q18Edit, 8, 10)
                                      
                    lbl2 = QLabel('Werkuren verbruik')
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl2, 10, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Steltijd'), 11, 1)
                    grid.addWidget(QLabel('Begroot'), 11, 2)
                    grid.addWidget(QLabel('Werkelijk'), 11, 3)
                    grid.addWidget(QLabel('Steltijd'), 11, 5)
                    grid.addWidget(QLabel('Begroot'), 11, 6)
                    grid.addWidget(QLabel('Werkelijk'), 11, 7) 
                    grid.addWidget(QLabel('Steltijd'), 11, 9)
                    grid.addWidget(QLabel('Begroot'), 11, 10)
                    grid.addWidget(QLabel('Werkelijk'), 11, 11) 
                                      
                    grid.addWidget(QLabel('Zagen'), 12, 0)
                    grid.addWidget(u1Edit, 12,1)
                    grid.addWidget(u2Edit, 12,2)
                    grid.addWidget(u3Edit, 12,3)

                    grid.addWidget(QLabel('Schaven'), 12, 4)
                    grid.addWidget(u4Edit, 12,5)
                    grid.addWidget(u5Edit, 12,6) 
                    grid.addWidget(u6Edit, 12,7)
                    
                    grid.addWidget(QLabel('Steken'), 12, 8)
                    grid.addWidget(u7Edit, 12,9)
                    grid.addWidget(u8Edit, 12,10) 
                    grid.addWidget(u9Edit, 12,11)
                    
                    grid.addWidget(QLabel('Boren'), 13, 0)
                    grid.addWidget(u10Edit, 13,1)
                    grid.addWidget(u11Edit, 13,2) 
                    grid.addWidget(u12Edit, 13,3)
                    
                    grid.addWidget(QLabel('Frezen'), 13, 4)
                    grid.addWidget(u13Edit, 13,5)
                    grid.addWidget(u14Edit, 13,6)
                    grid.addWidget(u15Edit, 13,7)
                    
                    grid.addWidget(QLabel('Draaien klein'), 13, 8)
                    grid.addWidget(u16Edit, 13,9)
                    grid.addWidget(u17Edit, 13,10)
                    grid.addWidget(u18Edit, 13,11)
                    
                    grid.addWidget(QLabel('Draaien groot'), 14, 0)
                    grid.addWidget(u19Edit, 14,1)
                    grid.addWidget(u20Edit, 14,2)
                    grid.addWidget(u21Edit, 14,3)
                    
                    grid.addWidget(QLabel('Tappen'), 14, 4)
                    grid.addWidget(u22Edit, 14, 5)
                    grid.addWidget(u23Edit, 14, 6)
                    grid.addWidget(u24Edit, 14, 7)
                    
                    grid.addWidget(QLabel('Nube draaien'), 14, 8)
                    grid.addWidget(u25Edit, 14,9)
                    grid.addWidget(u26Edit, 14,10)
                    grid.addWidget(u27Edit, 14,11)
                    
                    grid.addWidget(QLabel('Nube bewerken'), 15, 0)
                    grid.addWidget(u28Edit, 15,1)
                    grid.addWidget(u29Edit, 15,2)
                    grid.addWidget(u30Edit, 15,3)
                    
                    grid.addWidget(QLabel('Knippen'), 15, 4)
                    grid.addWidget(u31Edit, 15, 5)
                    grid.addWidget(u32Edit, 15, 6)
                    grid.addWidget(u33Edit, 15, 7)
                    
                    grid.addWidget(QLabel('Kanten'), 15, 8)
                    grid.addWidget(u34Edit, 15,9)
                    grid.addWidget(u35Edit, 15,10)
                    grid.addWidget(u36Edit, 15,11)
                    
                    grid.addWidget(QLabel('Stansen'), 16, 0)
                    grid.addWidget(u37Edit, 16,1)
                    grid.addWidget(u38Edit, 16,2)
                    grid.addWidget(u39Edit, 16,3)
                    
                    grid.addWidget(QLabel('Lassen co2'), 16, 4)
                    grid.addWidget(u40Edit, 16,5)
                    grid.addWidget(u41Edit, 16,6)
                    grid.addWidget(u42Edit, 16,7)
                     
                    grid.addWidget(QLabel('Lassen hand'), 16,8)
                    grid.addWidget(u43Edit, 16,9)
                    grid.addWidget(u44Edit, 16,10)
                    grid.addWidget(u45Edit, 16,11)
                    
                    grid.addWidget(QLabel('Verpakken'), 17,0)
                    grid.addWidget(u46Edit, 17,1)
                    grid.addWidget(u47Edit, 17,2)
                    grid.addWidget(u48Edit, 17,3)
                    
                    grid.addWidget(QLabel('Verzinken'), 17,4)
                    grid.addWidget(u49Edit, 17,5)
                    grid.addWidget(u50Edit, 17,6)
                    grid.addWidget(u51Edit, 17,7)
                    
                    grid.addWidget(QLabel('Moffelen'), 17,8)
                    grid.addWidget(u52Edit, 17,9)
                    grid.addWidget(u53Edit, 17,10)
                    grid.addWidget(u54Edit, 17,11)
                    
                    grid.addWidget(QLabel('Schilderen'), 18,0)
                    grid.addWidget(u55Edit, 18,1)
                    grid.addWidget(u56Edit, 18,2)
                    grid.addWidget(u57Edit, 18,3)
                    
                    grid.addWidget(QLabel('Spuiten'), 18,4)
                    grid.addWidget(u58Edit, 18,5)
                    grid.addWidget(u59Edit, 18,6)
                    grid.addWidget(u60Edit, 18,7)
                    
                    grid.addWidget(QLabel('Ponsen'), 18,8)
                    grid.addWidget(u61Edit, 18,9)
                    grid.addWidget(u62Edit, 18,10)
                    grid.addWidget(u63Edit, 18,11)
                    
                    grid.addWidget(QLabel('Persen'), 19,0)
                    grid.addWidget(u64Edit, 19,1)
                    grid.addWidget(u65Edit, 19,2)
                    grid.addWidget(u66Edit, 19,3)
                    
                    grid.addWidget(QLabel('Gritstralen'), 19,4)
                    grid.addWidget(u67Edit, 19,5)
                    grid.addWidget(u68Edit, 19,6)
                    grid.addWidget(u69Edit, 19,7)
                    
                    grid.addWidget(QLabel('Montage'), 19,8)
                    grid.addWidget(u70Edit, 19,9)
                    grid.addWidget(u71Edit, 19,10)
                    grid.addWidget(u72Edit, 19,11)
                                     
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 350, 300)
                                                                            
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 20, 11, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial", 10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    werkbriefBtn = QPushButton('Werkbrief')
                    werkbriefBtn.clicked.connect(lambda: printWerkbrief(mwerkorder, rpord, header))
                
                    grid.addWidget(werkbriefBtn, 20, 10, 1, 1, Qt.AlignRight)
                    werkbriefBtn.setFont(QFont("Arial", 10))
                    werkbriefBtn.setFixedWidth(100)
                    werkbriefBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 21, 0, 1, 12, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(100, 50, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
        
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)
