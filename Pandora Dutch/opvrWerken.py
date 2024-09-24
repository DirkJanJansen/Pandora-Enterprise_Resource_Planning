from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QTableView,\
          QComboBox, QDialog, QLineEdit, QMessageBox, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float)
from sqlalchemy.sql import select, update

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Opnieuw juiste gegevens invoeren\nzoek term!')
    msg.setWindowTitle('Opvragen externe werken')
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie!')
    msg.setWindowTitle('Opvragen externe werken')
    msg.exec_() 

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def werkenKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Financieel overzicht werken")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Times', 10))
    
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(330)
            k4Edit.setFont(QFont("Times", 10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem('                     Search sort key')
            k4Edit.addItem('1. Alle werken')
            k4Edit.addItem('2. Werknummer')
            k4Edit.addItem('3. Werk omschrijving')
            k4Edit.addItem('4. Voortgang status')
            k4Edit.addItem('5. Aanneemsom >')
            k4Edit.addItem('6. Aanneemsom <')
            k4Edit.addItem('7. Betaald in % >')
            k4Edit.activated[str].connect(self.k4Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(210)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 0, 0, 1, 2)

            grid.addWidget(k4Edit, 1, 0, 1, 2, Qt.AlignRight)
            lbl1 = QLabel('Zoek term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 2, Qt.AlignRight)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(lambda: windowSluit(self, m_email))
            
            grid.addWidget(applyBtn, 5, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(sluitBtn, 5, 1)
            sluitBtn.setFont(QFont("Arial", 10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
        def k4Changed(self, text):
            self.Keuze4.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk4(self):
            return self.Keuze4.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk4(), dialog.returnzkterm()]       

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
    toonWerken(keuze,zoekterm, m_email)
 
def toonWerken(keuze,zoekterm, m_email): 
    import validZt      
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('voortgangstatus', String),
        Column('statusweek',  String),
        Column('startweek', String),
        Column('opdracht_datum', String),
        Column('aanneemsom', Float),
        Column('betaald_bedrag', Float),
        Column('begr_materialen', Float),
        Column('kosten_materialen', Float),
        Column('begr_lonen', Float),
        Column('kosten_lonen', Float),
        Column('begr_materieel',Float),
        Column('kosten_materieel', Float), 
        Column('begr_leiding', Float),
        Column('kosten_leiding', Float),
        Column('begr_huisv', Float),
        Column('kosten_huisv', Float),
        Column('begr_inhuur', Float),
        Column('kosten_inhuur', Float),
        Column('begr_overig', Float),
        Column('kosten_overig', Float),
        Column('begr_vervoer', Float),
        Column('kosten_vervoer', Float),
        Column('begr_beton_bvl', Float),
        Column('beton_bvl', Float),
        Column('begr_kabelwerk', Float),
        Column('kabelwerk', Float),
        Column('begr_grondverzet', Float),
        Column('grondverzet', Float),
        Column('meerminderwerk', Float),
        Column('begr_constr_uren', Float),
        Column('werk_constr_uren', Float),
        Column('begr_mont_uren', Float),
        Column('werk_mont_uren', Float),
        Column('begr_retourlas_uren', Float),
        Column('werk_retourlas_uren', Float),
        Column('begr_telecom_uren', Float),
        Column('werk_telecom_uren', Float),
        Column('begr_bfi_uren', Float),
        Column('werk_bfi_uren', Float),
        Column('begr_bvl_uren', Float),
        Column('werk_bvl_uren', Float),
        Column('begr_voeding_uren', Float),
        Column('werk_voeding_uren', Float),
        Column('begr_spoorleg_uren',  Float),
        Column('werk_spoorleg_uren', Float),
        Column('begr_spoorlas_uren', Float),
        Column('werk_spoorlas_uren', Float),
        Column('begr_reis_uren', Float),
        Column('werk_reis_uren', Float),
        Column('begr_sleuvengraver_uren', Float),
        Column('werk_sleuvengraver_uren', Float),
        Column('begr_persapparaat_uren', Float),
        Column('werk_persapparaat_uren', Float),
        Column('begr_atlaskraan_uren', Float),
        Column('werk_atlaskraan_uren', Float),
        Column('begr_kraan_groot_uren', Float),
        Column('werk_kraan_groot_uren', Float),
        Column('begr_mainliner_uren', Float),
        Column('werk_mainliner_uren', Float),
        Column('begr_hormachine_uren', Float),
        Column('werk_hormachine_uren', Float),
        Column('begr_wagon_uren', Float),
        Column('werk_wagon_uren', Float),
        Column('begr_locomotor_uren', Float),
        Column('werk_locomotor_uren', Float),
        Column('begr_locomotief_uren', Float),
        Column('werk_locomotief_uren', Float),
        Column('begr_montagewagen_uren', Float),
        Column('werk_montagewagen_uren', Float),
        Column('begr_stormobiel_uren', Float),
        Column('werk_stormobiel_uren', Float),
        Column('begr_robeltrein_uren', Float),
        Column('werk_robeltrein_uren', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
  
    if keuze == 1:
        sel = select([werken]).order_by(werken.c.werknummerID)
    elif keuze == 2 and validZt.zt(zoekterm, 8):
        sel = select([werken]).where(werken.c.werknummerID == int(zoekterm))
    elif keuze == 3:
        sel = select([werken]).where(werken.c.werkomschrijving.ilike('%'+zoekterm+'%'))
    elif keuze == 4 and validZt.zt(zoekterm, 18):
        sel = select([werken]).where(werken.c.voortgangstatus == zoekterm.upper())
    elif keuze == 5 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.aanneemsom > float(zoekterm))
    elif keuze == 6 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.aanneemsom < float(zoekterm))
    elif keuze == 7 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.betaald_bedrag/werken.c.aanneemsom > float(zoekterm)/100)
    else:
        ongInvoer()
        werkenKeuze(m_email)
    
    if con.execute(sel).fetchone():
        rpwerken = con.execute(sel)
    else:
        geenRecord()
        werkenKeuze(m_email)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1800, 900)
            self.setWindowTitle('Opvragen externe werken')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.hideColumn(24)
            table_view.hideColumn(25)
            table_view.hideColumn(26)
            table_view.hideColumn(27)
            for i in range (51, 75):
                table_view.hideColumn(i)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showWerk)
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
  
    header = ['Werknummer','Werkomschrijving', 'Voortgang status','Status week',\
              'Start week','Order datum','Aanneemsom','Bedrag betaald','Begrote materialen',\
              'Werkelijke materialen', 'Begrote lonen', 'Werkelijke lonen', 'Begroot materieel',\
              'Werkelijk materieel','Begroot leiding', 'Werkelijk leiding','Begroot huisvesting',\
              'Werkelijk huisvesting', 'Begrote inhuur','Werkelijk inhuur','Begroot overig',\
              'Werkelijk overig', 'Begroot transport', 'Werkelijk transport', '',\
              '','', '','Begroot\ngrondverzet',\
              'Werkelijk\ngrondverzet', 'Meer/minder werk','Begrote\nconstructie uren','Werkelijke\nconstructie uren',\
              'Begrote\nmontage uren', 'Werkelijke\nmontage uren', 'Begrote retour\nlas uren', 'Werkelijke retour\nlas uren',\
              'Begrote\ntelecom uren','Werkelijke\ntelecom uren', 'Begrote\nbfi uren','Werkelijke\nbfi uren',\
              'Begrote\nbovenleiding uren', 'Werkelijke\nbovenleiding uren','Begrote\nvoeding uren','Werkelijke\nvoeding uren',\
              'Begrote spoor\nleg uren','Werkelijke spoor\nleg uren', 'Begrote spoor\nlas uren',\
              'Werkelijke spoor\nlas uren', 'Begrote\nreisuren', 'Werkelijke\nreisuren','','','','','','','','',\
               '','','','','','','','','','','','','','','','']
   
    data_list=[]
    for row in rpwerken:
        data_list += [(row)] 
     
    def showWerk(idx):
        mwerknr = idx.data()
        if idx.column() == 0:
            selwerk = select([werken]).where(werken.c.werknummerID == mwerknr) 
            rpwerk = con.execute(selwerk).first()
            msom = rpwerk[6]
            mtotopbr = rpwerk[6]+rpwerk[30]
            mbtot = rpwerk[8]+rpwerk[10]+rpwerk[12]+rpwerk[14]+rpwerk[16]+rpwerk[18]+\
              rpwerk[20]+rpwerk[22]+rpwerk[24]+rpwerk[26]+rpwerk[28]+rpwerk[30]
            mktotal=rpwerk[9]+rpwerk[11]+rpwerk[13]+rpwerk[15]+rpwerk[17]+rpwerk[19]+rpwerk[21]+rpwerk[23]\
             +rpwerk[25]+rpwerk[27]+rpwerk[29]
            mbderden = rpwerk[16]+rpwerk[18]+rpwerk[20]+rpwerk[22]+rpwerk[24]+rpwerk[26]+rpwerk[28]
            mkderden = rpwerk[17]+rpwerk[19]+rpwerk[21]+rpwerk[23]+rpwerk[25]+rpwerk[27]+rpwerk[29]                     
            mbetaald = rpwerk[7]
            mvgangst = rpwerk[2]
            mstatwk = rpwerk[3]
            mfact = 0
            flag = 0
            mwerknr = rpwerk[0]
            mmeerwerk = float(rpwerk[30])
            if mvgangst == 'A':
                if mktotal > 0:
                    mvgangst = 'B'
                    mstatwk = jaarweek()
                    flag = 1
            elif mvgangst == 'B':      
                if mktotal > msom/3:
                    mvgangst = 'C'
                    mstatwk = jaarweek()
                    flag = 1
            elif mvgangst == 'C':
                if mktotal > msom/2:
                    mvgangst = 'D'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = msom/3-mbetaald
            elif mvgangst == 'D':
                if mktotal > msom/1.5:
                    mvgangst = 'E'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = 0
            elif mvgangst == 'E':
                if mktotal >= msom:
                    mvgangst = 'F'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = msom/1.5-mbetaald
            elif mvgangst == 'F':
                mfact = msom-mbetaald*0.9
            elif mvgangst == 'G':
                mfact = msom+mmeerwerk-mbetaald 
            if flag:
                werkupd = update(werken).where(werken.c.werknummerID == mwerknr)\
                    .values(statusweek = mstatwk, voortgangstatus = mvgangst)
                con.execute(werkupd)
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Opvragen externe werkengegevens")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                       
                    q1Edit = QLineEdit(str(rpwerk[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setDisabled(True)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    
                    q2Edit = QLineEdit(str(rpwerk[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setDisabled(True)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        
                    q3Edit = QLineEdit(rpwerk[2])
                    q3Edit.setFixedWidth(20)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                    
                    q4Edit = QLineEdit(rpwerk[3])
                    q4Edit.setFixedWidth(100)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
           
                    q5Edit = QLineEdit(rpwerk[4])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)                              
                    
                    q8Edit = QLineEdit('{:12.2f}'.format(rpwerk[6]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    q9Edit = QLineEdit('{:12.2f}'.format(rpwerk[30]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                                                         
                    q11Edit = QLineEdit('{:12.2f}'.format(rpwerk[7]))
                    q11Edit.setFixedWidth(100)
                    q11Edit.setAlignment(Qt.AlignRight)
                    q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q11Edit.setDisabled(True)
                      
                    q12Edit = QLineEdit('{:12.2f}'.format(rpwerk[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setAlignment(Qt.AlignRight)
                    q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q12Edit.setDisabled(True)
                     
                    q13Edit = QLineEdit('{:12.2f}'.format(rpwerk[9]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setAlignment(Qt.AlignRight)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q13Edit.setDisabled(True)
             
                    q19Edit = QLineEdit('{:12.2f}'.format(rpwerk[10]))
                    q19Edit.setFixedWidth(100)
                    q19Edit.setAlignment(Qt.AlignRight)
                    q19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q19Edit.setDisabled(True)
             
                    q14Edit = QLineEdit('{:12.2f}'.format(rpwerk[11]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q14Edit.setDisabled(True)
                                    
                    q15Edit = QLineEdit('{:12.2f}'.format(rpwerk[12]))
                    q15Edit.setDisabled(True)
                    q15Edit.setAlignment(Qt.AlignRight)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                   
                    q16Edit = QLineEdit('{:12.2f}'.format(rpwerk[13]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setAlignment(Qt.AlignRight)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q16Edit.setDisabled(True)
                        
                    q18Edit = QLineEdit('{:12.2f}'.format(rpwerk[14]))
                    q18Edit.setFixedWidth(100)
                    q18Edit.setAlignment(Qt.AlignRight)
                    q18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q18Edit.setDisabled(True)
                    
                    q17Edit = QLineEdit('{:12.2f}'.format(rpwerk[15]))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setAlignment(Qt.AlignRight)
                    q17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q17Edit.setDisabled(True)
                    
                    q20Edit = QLineEdit('{:12.2f}'.format(mtotopbr))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setAlignment(Qt.AlignRight)
                    q20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q20Edit.setDisabled(True)
                    
                    q21Edit = QLineEdit('{:12.2f}'.format(mbtot))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setAlignment(Qt.AlignRight)
                    q21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q21Edit.setDisabled(True)
    
                    q22Edit = QLineEdit('{:12.2f}'.format(mktotal))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setAlignment(Qt.AlignRight)
                    q22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q22Edit.setDisabled(True)
    
                    q23Edit = QLineEdit('{:12.2f}'.format(mbderden))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setAlignment(Qt.AlignRight)
                    q23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q23Edit.setDisabled(True)
                    
                    q24Edit = QLineEdit('{:12.2f}'.format(mkderden))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setAlignment(Qt.AlignRight)
                    q24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q24Edit.setDisabled(True)
                                                  
                    q26Edit = QLineEdit('{:12.2f}'.format(mfact))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setAlignment(Qt.AlignRight)
                    q26Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q26Edit.setDisabled(True)
                    
                    u1Edit = QLineEdit('{:12.2f}'.format(rpwerk[31]))
                    u1Edit.setFixedWidth(100)
                    u1Edit.setAlignment(Qt.AlignRight)
                    u1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u1Edit.setDisabled(True)
                    
                    u2Edit = QLineEdit('{:12.2f}'.format(rpwerk[32]))
                    u2Edit.setFixedWidth(100)
                    u2Edit.setAlignment(Qt.AlignRight)
                    u2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u2Edit.setDisabled(True)
                    
                    u3Edit = QLineEdit('{:12.2f}'.format(rpwerk[33]))
                    u3Edit.setFixedWidth(100)
                    u3Edit.setAlignment(Qt.AlignRight)
                    u3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u3Edit.setDisabled(True)
                    
                    u4Edit = QLineEdit('{:12.2f}'.format(rpwerk[34]))
                    u4Edit.setFixedWidth(100)
                    u4Edit.setAlignment(Qt.AlignRight)
                    u4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u4Edit.setDisabled(True)
                    
                    u5Edit = QLineEdit('{:12.2f}'.format(rpwerk[35]))
                    u5Edit.setFixedWidth(100)
                    u5Edit.setAlignment(Qt.AlignRight)
                    u5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u5Edit.setDisabled(True)
                    
                    u6Edit = QLineEdit('{:12.2f}'.format(rpwerk[36]))
                    u6Edit.setFixedWidth(100)
                    u6Edit.setAlignment(Qt.AlignRight)
                    u6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u6Edit.setDisabled(True)
                    
                    u7Edit = QLineEdit('{:12.2f}'.format(rpwerk[37]))
                    u7Edit.setFixedWidth(100)
                    u7Edit.setAlignment(Qt.AlignRight)
                    u7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u7Edit.setDisabled(True)
                    
                    u8Edit = QLineEdit('{:12.2f}'.format(rpwerk[38]))
                    u8Edit.setFixedWidth(100)
                    u8Edit.setAlignment(Qt.AlignRight)
                    u8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u8Edit.setDisabled(True)
                    
                    u9Edit = QLineEdit('{:12.2f}'.format(rpwerk[39]))
                    u9Edit.setFixedWidth(100)
                    u9Edit.setAlignment(Qt.AlignRight)
                    u9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u9Edit.setDisabled(True)
                    
                    u10Edit = QLineEdit('{:12.2f}'.format(rpwerk[40]))
                    u10Edit.setFixedWidth(100)
                    u10Edit.setAlignment(Qt.AlignRight)
                    u10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u10Edit.setDisabled(True)
                    
                    u11Edit = QLineEdit('{:12.2f}'.format(rpwerk[41]))
                    u11Edit.setFixedWidth(100)
                    u11Edit.setAlignment(Qt.AlignRight)
                    u11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u11Edit.setDisabled(True)
                    
                    u12Edit = QLineEdit('{:12.2f}'.format(rpwerk[42]))
                    u12Edit.setFixedWidth(100)
                    u12Edit.setAlignment(Qt.AlignRight)
                    u12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u12Edit.setDisabled(True)
                    
                    u13Edit = QLineEdit('{:12.2f}'.format(rpwerk[43]))
                    u13Edit.setFixedWidth(100)
                    u13Edit.setAlignment(Qt.AlignRight)
                    u13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u13Edit.setDisabled(True)
                    
                    u14Edit = QLineEdit('{:12.2f}'.format(rpwerk[44]))
                    u14Edit.setFixedWidth(100)
                    u14Edit.setAlignment(Qt.AlignRight)
                    u14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u14Edit.setDisabled(True)
                    
                    u15Edit = QLineEdit('{:12.2f}'.format(rpwerk[45]))
                    u15Edit.setFixedWidth(100)
                    u15Edit.setAlignment(Qt.AlignRight)
                    u15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u15Edit.setDisabled(True)
                    
                    u16Edit = QLineEdit('{:12.2f}'.format(rpwerk[46]))
                    u16Edit.setFixedWidth(100)
                    u16Edit.setAlignment(Qt.AlignRight)
                    u16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u16Edit.setDisabled(True)
                    
                    u17Edit = QLineEdit('{:12.2f}'.format(rpwerk[47]))
                    u17Edit.setFixedWidth(100)
                    u17Edit.setAlignment(Qt.AlignRight)
                    u17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u17Edit.setDisabled(True)
                    
                    u18Edit = QLineEdit('{:12.2f}'.format(rpwerk[48]))
                    u18Edit.setFixedWidth(100)
                    u18Edit.setAlignment(Qt.AlignRight)
                    u18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u18Edit.setDisabled(True)
                    
                    u19Edit = QLineEdit('{:12.2f}'.format(rpwerk[49]))
                    u19Edit.setFixedWidth(100)
                    u19Edit.setAlignment(Qt.AlignRight)
                    u19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u19Edit.setDisabled(True)
                    
                    u20Edit = QLineEdit('{:12.2f}'.format(rpwerk[50]))
                    u20Edit.setFixedWidth(100)
                    u20Edit.setAlignment(Qt.AlignRight)
                    u20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    u20Edit.setDisabled(True)
                    
                    d1Edit = QLineEdit('{:12.2f}'.format(rpwerk[16]))
                    d1Edit.setFixedWidth(100)
                    d1Edit.setAlignment(Qt.AlignRight)
                    d1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d1Edit.setDisabled(True)
                                          
                    d2Edit = QLineEdit('{:12.2f}'.format(rpwerk[17]))
                    d2Edit.setFixedWidth(100)
                    d2Edit.setAlignment(Qt.AlignRight)
                    d2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d2Edit.setDisabled(True)
                    
                    d3Edit = QLineEdit('{:12.2f}'.format(rpwerk[18]))
                    d3Edit.setFixedWidth(100)
                    d3Edit.setAlignment(Qt.AlignRight)
                    d3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d3Edit.setDisabled(True)
                    
                    d4Edit = QLineEdit('{:12.2f}'.format(rpwerk[19]))
                    d4Edit.setFixedWidth(100)
                    d4Edit.setAlignment(Qt.AlignRight)
                    d4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d4Edit.setDisabled(True)
                    
                    d5Edit = QLineEdit('{:12.2f}'.format(rpwerk[20]))
                    d5Edit.setFixedWidth(100)
                    d5Edit.setAlignment(Qt.AlignRight)
                    d5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d5Edit.setDisabled(True)
                    
                    d6Edit = QLineEdit('{:12.2f}'.format(rpwerk[21]))
                    d6Edit.setFixedWidth(100)
                    d6Edit.setAlignment(Qt.AlignRight)
                    d6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d6Edit.setDisabled(True)
                    
                    d7Edit = QLineEdit('{:12.2f}'.format(rpwerk[22]))
                    d7Edit.setFixedWidth(100)
                    d7Edit.setAlignment(Qt.AlignRight)
                    d7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d7Edit.setDisabled(True)
                    
                    d8Edit = QLineEdit('{:12.2f}'.format(rpwerk[23]))
                    d8Edit.setFixedWidth(100)
                    d8Edit.setAlignment(Qt.AlignRight)
                    d8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d8Edit.setDisabled(True)
                    
                    d9Edit = QLineEdit('{:12.2f}'.format(rpwerk[24]))
                    d9Edit.setFixedWidth(100)
                    d9Edit.setAlignment(Qt.AlignRight)
                    d9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d9Edit.setDisabled(True)
                    
                    d10Edit = QLineEdit('{:12.2f}'.format(rpwerk[25]))
                    d10Edit.setFixedWidth(100)
                    d10Edit.setAlignment(Qt.AlignRight)
                    d10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d10Edit.setDisabled(True)
                    
                    d11Edit = QLineEdit('{:12.2f}'.format(rpwerk[26]))
                    d11Edit.setFixedWidth(100)
                    d11Edit.setAlignment(Qt.AlignRight)
                    d11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d11Edit.setDisabled(True)
                    
                    d12Edit = QLineEdit('{:12.2f}'.format(rpwerk[27]))
                    d12Edit.setFixedWidth(100)
                    d12Edit.setAlignment(Qt.AlignRight)
                    d12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d12Edit.setDisabled(True)
                    
                    d13Edit = QLineEdit('{:12.2f}'.format(rpwerk[28]))
                    d13Edit.setFixedWidth(100)
                    d13Edit.setAlignment(Qt.AlignRight)
                    d13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d13Edit.setDisabled(True)
                    
                    d14Edit = QLineEdit('{:12.2f}'.format(rpwerk[29]))
                    d14Edit.setFixedWidth(100)
                    d14Edit.setAlignment(Qt.AlignRight)
                    d14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    d14Edit.setDisabled(True)

                    m1Edit = QLineEdit('{:12.2f}'.format(rpwerk[51]))
                    m1Edit.setFixedWidth(100)
                    m1Edit.setAlignment(Qt.AlignRight)
                    m1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m1Edit.setDisabled(True)

                    m2Edit = QLineEdit('{:12.2f}'.format(rpwerk[52]))
                    m2Edit.setFixedWidth(100)
                    m2Edit.setAlignment(Qt.AlignRight)
                    m2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m2Edit.setDisabled(True)

                    m3Edit = QLineEdit('{:12.2f}'.format(rpwerk[53]))
                    m3Edit.setFixedWidth(100)
                    m3Edit.setAlignment(Qt.AlignRight)
                    m3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m3Edit.setDisabled(True)

                    m4Edit = QLineEdit('{:12.2f}'.format(rpwerk[54]))
                    m4Edit.setFixedWidth(100)
                    m4Edit.setAlignment(Qt.AlignRight)
                    m4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m4Edit.setDisabled(True)

                    m5Edit = QLineEdit('{:12.2f}'.format(rpwerk[55]))
                    m5Edit.setFixedWidth(100)
                    m5Edit.setAlignment(Qt.AlignRight)
                    m5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m5Edit.setDisabled(True)

                    m6Edit = QLineEdit('{:12.2f}'.format(rpwerk[56]))
                    m6Edit.setFixedWidth(100)
                    m6Edit.setAlignment(Qt.AlignRight)
                    m6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m6Edit.setDisabled(True)

                    m7Edit = QLineEdit('{:12.2f}'.format(rpwerk[57]))
                    m7Edit.setFixedWidth(100)
                    m7Edit.setAlignment(Qt.AlignRight)
                    m7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m7Edit.setDisabled(True)

                    m8Edit = QLineEdit('{:12.2f}'.format(rpwerk[58]))
                    m8Edit.setFixedWidth(100)
                    m8Edit.setAlignment(Qt.AlignRight)
                    m8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m8Edit.setDisabled(True)

                    m9Edit = QLineEdit('{:12.2f}'.format(rpwerk[59]))
                    m9Edit.setFixedWidth(100)
                    m9Edit.setAlignment(Qt.AlignRight)
                    m9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m9Edit.setDisabled(True)

                    m10Edit = QLineEdit('{:12.2f}'.format(rpwerk[60]))
                    m10Edit.setFixedWidth(100)
                    m10Edit.setAlignment(Qt.AlignRight)
                    m10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m10Edit.setDisabled(True)

                    m11Edit = QLineEdit('{:12.2f}'.format(rpwerk[61]))
                    m11Edit.setFixedWidth(100)
                    m11Edit.setAlignment(Qt.AlignRight)
                    m11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m11Edit.setDisabled(True)

                    m12Edit = QLineEdit('{:12.2f}'.format(rpwerk[62]))
                    m12Edit.setFixedWidth(100)
                    m12Edit.setAlignment(Qt.AlignRight)
                    m12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m12Edit.setDisabled(True)

                    m13Edit = QLineEdit('{:12.2f}'.format(rpwerk[63]))
                    m13Edit.setFixedWidth(100)
                    m13Edit.setAlignment(Qt.AlignRight)
                    m13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m13Edit.setDisabled(True)

                    m14Edit = QLineEdit('{:12.2f}'.format(rpwerk[64]))
                    m14Edit.setFixedWidth(100)
                    m14Edit.setAlignment(Qt.AlignRight)
                    m14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m14Edit.setDisabled(True)

                    m15Edit = QLineEdit('{:12.2f}'.format(rpwerk[65]))
                    m15Edit.setFixedWidth(100)
                    m15Edit.setAlignment(Qt.AlignRight)
                    m15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m15Edit.setDisabled(True)

                    m16Edit = QLineEdit('{:12.2f}'.format(rpwerk[66]))
                    m16Edit.setFixedWidth(100)
                    m16Edit.setAlignment(Qt.AlignRight)
                    m16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m16Edit.setDisabled(True)

                    m17Edit = QLineEdit('{:12.2f}'.format(rpwerk[67]))
                    m17Edit.setFixedWidth(100)
                    m17Edit.setAlignment(Qt.AlignRight)
                    m17Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m17Edit.setDisabled(True)

                    m18Edit = QLineEdit('{:12.2f}'.format(rpwerk[68]))
                    m18Edit.setFixedWidth(100)
                    m18Edit.setAlignment(Qt.AlignRight)
                    m18Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m18Edit.setDisabled(True)

                    m19Edit = QLineEdit('{:12.2f}'.format(rpwerk[69]))
                    m19Edit.setFixedWidth(100)
                    m19Edit.setAlignment(Qt.AlignRight)
                    m19Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m19Edit.setDisabled(True)

                    m20Edit = QLineEdit('{:12.2f}'.format(rpwerk[70]))
                    m20Edit.setFixedWidth(100)
                    m20Edit.setAlignment(Qt.AlignRight)
                    m20Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m20Edit.setDisabled(True)

                    m21Edit = QLineEdit('{:12.2f}'.format(rpwerk[71]))
                    m21Edit.setFixedWidth(100)
                    m21Edit.setAlignment(Qt.AlignRight)
                    m21Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m21Edit.setDisabled(True)

                    m22Edit = QLineEdit('{:12.2f}'.format(rpwerk[72]))
                    m22Edit.setFixedWidth(100)
                    m22Edit.setAlignment(Qt.AlignRight)
                    m22Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m22Edit.setDisabled(True)

                    m23Edit = QLineEdit('{:12.2f}'.format(rpwerk[73]))
                    m23Edit.setFixedWidth(100)
                    m23Edit.setAlignment(Qt.AlignRight)
                    m23Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m23Edit.setDisabled(True)

                    m24Edit = QLineEdit('{:12.2f}'.format(rpwerk[74]))
                    m24Edit.setFixedWidth(100)
                    m24Edit.setAlignment(Qt.AlignRight)
                    m24Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    m24Edit.setDisabled(True)

                    grid = QGridLayout()
                    grid.setSpacing(20)

                    pyqt = QLabel()
                    movie = QMovie('./images/logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(160, 60))
                    movie.start()
                    grid.addWidget(pyqt, 0, 0, 1, 2)

                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 11, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    
                    grid.addWidget(QLabel('Werknummer'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1) 
                    
                    grid.addWidget(QLabel('Werkomschrijving'), 1, 2)
                    grid.addWidget(q2Edit, 1, 3, 1, 3) 
                                                        
                    grid.addWidget(QLabel('Voortgang status'), 1, 6)
                    grid.addWidget(q3Edit, 1, 7)
                    
                    grid.addWidget(QLabel('       Status week'), 1, 7, 1, 1, Qt.AlignRight)
                    grid.addWidget(q4Edit, 1, 8) 
                     
                    grid.addWidget(QLabel('Start week'), 1, 9)
                    grid.addWidget(q5Edit, 1, 10)

                    lbl1 = QLabel('Totaal financiele bedragen')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 3, 0, 1, 2)

                    grid.addWidget(QLabel('Aanneemsom'), 4, 0)
                    grid.addWidget(q8Edit, 4, 1)

                    grid.addWidget(QLabel('Totaal inkomsten'), 4, 2)
                    grid.addWidget(q21Edit, 4, 3)
                    
                    grid.addWidget(QLabel('Totaal kosten'), 4, 4)
                    grid.addWidget(q22Edit, 4, 5)

                    grid.addWidget(QLabel('Meer/minder werk'), 4, 6)
                    grid.addWidget(q9Edit, 4, 7)
                    
                    grid.addWidget(QLabel('Bedrag betaald'), 4, 8)
                    grid.addWidget(q11Edit, 4, 9)
                    
                    grid.addWidget(QLabel('Te factureren'), 4, 10)
                    grid.addWidget(q26Edit, 4, 11)
                    
                    grid.addWidget(QLabel('Begroot'), 5, 1)
                    grid.addWidget(QLabel('Werkelijk'), 5, 2)
                    grid.addWidget(QLabel('Begroot'), 5, 4)
                    grid.addWidget(QLabel('Werkelijk'), 5, 5)
                    grid.addWidget(QLabel('Begroot'), 5, 7)
                    grid.addWidget(QLabel('Werkelijk'), 5, 8)
                    grid.addWidget(QLabel('Begroot'), 5, 10)
                    grid.addWidget(QLabel('Werkelijk'), 5, 11)

                    grid.addWidget(QLabel('Materialen'), 6, 0)
                    grid.addWidget(q12Edit, 6, 1) 
                    grid.addWidget(q13Edit, 6, 2) 
                    
                    grid.addWidget(QLabel('Lonen'), 6, 3)
                    grid.addWidget(q19Edit, 6, 4)
                    grid.addWidget(q14Edit, 6, 5)
                                                
                    grid.addWidget(QLabel('Materieel'), 6, 6)
                    grid.addWidget(q15Edit, 6, 7)                           
                    grid.addWidget(q16Edit, 6, 8)
                    
                    grid.addWidget(QLabel('Stelposten'), 6, 9)
                    grid.addWidget(q23Edit, 6, 10)
                    grid.addWidget(q24Edit, 6, 11)

                    lbl2 = QLabel('Gewerkte uren verbruik')
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl2, 8, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Begroot'), 9, 1)
                    grid.addWidget(QLabel('Werkelijk'), 9, 2)
                    grid.addWidget(QLabel('Begroot'), 9, 4)
                    grid.addWidget(QLabel('Werkelijk'), 9, 5)
                    grid.addWidget(QLabel('Begroot'), 9, 7)
                    grid.addWidget(QLabel('Werkelijk'), 9, 8)
                    grid.addWidget(QLabel('Begroot'), 9, 10)
                    grid.addWidget(QLabel('Werkelijk'), 9, 11)
                    
                    grid.addWidget(QLabel('Constructie'), 10, 0)
                    grid.addWidget(u1Edit, 10,1)
                    grid.addWidget(u2Edit, 10,2) 

                    grid.addWidget(QLabel('Montage'), 10, 3)
                    grid.addWidget(u3Edit, 10,4)
                    grid.addWidget(u4Edit, 10,5) 
                    
                    grid.addWidget(QLabel('Retourlassen'), 10, 6)
                    grid.addWidget(u5Edit, 10,7)
                    grid.addWidget(u6Edit, 10,8) 
                    
                    grid.addWidget(QLabel('Telecom'), 10, 9)
                    grid.addWidget(u7Edit, 10,10)
                    grid.addWidget(u8Edit, 10,11)
                    
                    grid.addWidget(QLabel('BFI monteur'), 11, 0)
                    grid.addWidget(u9Edit, 11,1)
                    grid.addWidget(u10Edit, 11,2)
                    
                    grid.addWidget(QLabel('Bovenleding'), 11, 3)
                    grid.addWidget(u11Edit, 11,4)
                    grid.addWidget(u12Edit, 11,5)
                    
                    grid.addWidget(QLabel('Voeding'), 11, 6)
                    grid.addWidget(u13Edit, 11,7)
                    grid.addWidget(u14Edit, 11,8)
                    
                    grid.addWidget(QLabel('Spoorleggen'), 11, 9)
                    grid.addWidget(u15Edit, 11,10)
                    grid.addWidget(u16Edit, 11,11)
                    
                    grid.addWidget(QLabel('Spoorlassen'), 12, 0)
                    grid.addWidget(u17Edit, 12,1)
                    grid.addWidget(u18Edit, 12,2)
                    
                    grid.addWidget(QLabel('Reisuren'), 12, 3)
                    grid.addWidget(u19Edit, 12,4)
                    grid.addWidget(u20Edit, 12,5)

                    lbl2m = QLabel('Materieel uren verbruik')
                    lbl2m.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl2m, 13, 0, 1, 2)

                    grid.addWidget(QLabel('Begroot'), 14, 1)
                    grid.addWidget(QLabel('Werkelijk'), 14, 2)
                    grid.addWidget(QLabel('Begroot'), 14, 4)
                    grid.addWidget(QLabel('Werkelijk'), 14, 5)
                    grid.addWidget(QLabel('Begroot'), 14, 7)
                    grid.addWidget(QLabel('Werkelijk'), 14, 8)
                    grid.addWidget(QLabel('Begroot'), 14, 10)
                    grid.addWidget(QLabel('Werkelijk'), 14, 11)

                    grid.addWidget(QLabel('Sleuvengraver'), 15, 0)
                    grid.addWidget(m1Edit, 15, 1)
                    grid.addWidget(m2Edit, 15, 2)

                    grid.addWidget(QLabel('Persmachine'), 15, 3)
                    grid.addWidget(m3Edit, 15, 4)
                    grid.addWidget(m4Edit, 15, 5)

                    grid.addWidget(QLabel('Atlaskraan'), 15, 6)
                    grid.addWidget(m5Edit, 15, 7)
                    grid.addWidget(m6Edit, 15, 8)

                    grid.addWidget(QLabel('Kraan groot'), 15, 9)
                    grid.addWidget(m7Edit, 15, 10)
                    grid.addWidget(m8Edit, 15, 11)

                    grid.addWidget(QLabel('Mainliner'), 16, 0)
                    grid.addWidget(m9Edit, 16, 1)
                    grid.addWidget(m10Edit, 16, 2)

                    grid.addWidget(QLabel('Hormachine'), 16, 3)
                    grid.addWidget(m11Edit, 16, 4)
                    grid.addWidget(m12Edit, 16, 5)

                    grid.addWidget(QLabel('Wagon'), 16, 6)
                    grid.addWidget(m13Edit, 16, 7)
                    grid.addWidget(m14Edit, 16, 8)

                    grid.addWidget(QLabel('Locomotor'), 16, 9)
                    grid.addWidget(m15Edit, 16, 10)
                    grid.addWidget(m16Edit, 16, 11)

                    grid.addWidget(QLabel('Locomotief'), 17, 0)
                    grid.addWidget(m17Edit, 17, 1)
                    grid.addWidget(m18Edit, 17, 2)

                    grid.addWidget(QLabel('Montagewagen'), 17, 3)
                    grid.addWidget(m19Edit, 17, 4)
                    grid.addWidget(m20Edit, 17, 5)

                    grid.addWidget(QLabel('Stormobiel'), 17, 6)
                    grid.addWidget(m21Edit, 17, 7)
                    grid.addWidget(m22Edit, 17, 8)

                    grid.addWidget(QLabel('Robeltrein'), 17, 9)
                    grid.addWidget(m23Edit, 17, 10)
                    grid.addWidget(m24Edit, 17, 11)

                    lbl3 = QLabel('Stelpost werk / Stelpost bedrag')
                    lbl3.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl3, 18, 0, 1, 2)

                    grid.addWidget(QLabel('Begroot'), 19, 1)
                    grid.addWidget(QLabel('Werkelijk'), 19, 2)
                    grid.addWidget(QLabel('Begroot'), 19, 4)
                    grid.addWidget(QLabel('Werkelijk'), 19, 5)
                    grid.addWidget(QLabel('Begroot'), 19, 7)
                    grid.addWidget(QLabel('Werkelijk'), 19, 8)
                    grid.addWidget(QLabel('Begroot'), 19, 10)
                    grid.addWidget(QLabel('Werkelijk'), 19, 11)

                    grid.addWidget(QLabel('Huisvesting'), 20, 0)
                    grid.addWidget(d1Edit, 20, 1)
                    grid.addWidget(d2Edit, 20, 2)

                    grid.addWidget(QLabel('Leiding'), 20, 3)
                    grid.addWidget(q18Edit, 20, 4)
                    grid.addWidget(q17Edit, 20, 5)

                    grid.addWidget(QLabel('Inhuur'), 20, 6)
                    grid.addWidget(d3Edit, 20, 7)
                    grid.addWidget(d4Edit, 20, 8)

                    grid.addWidget(QLabel('Overig'), 20, 9)
                    grid.addWidget(d5Edit, 20, 10)
                    grid.addWidget(d6Edit, 20, 11)

                    grid.addWidget(QLabel('Transport'), 21, 0)
                    grid.addWidget(d7Edit, 21, 1)
                    grid.addWidget(d8Edit, 21, 2)

                    grid.addWidget(QLabel('Grondverzet'), 21, 3)
                    grid.addWidget(d13Edit, 21, 4)
                    grid.addWidget(d14Edit, 21, 5)

                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 0, 1, 11, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(100, 30, 450, 300)
                                                                            
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 22, 11, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_() 
                       
    win = MyWindow(data_list, header)
    win.exec_()
    werkenKeuze(m_email)  