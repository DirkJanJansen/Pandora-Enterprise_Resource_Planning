from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap
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
    msg.setText('Please re-enter incorrect input\nsearchterm!')
    msg.setWindowTitle('Request external works')
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request external works')
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
            self.setWindowTitle("Financial Overview Works")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Times', 10))
    
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(330)
            k4Edit.setFont(QFont("Times", 10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem('              Search sort key')
            k4Edit.addItem('1. Alle works')
            k4Edit.addItem('2. Worknumber')
            k4Edit.addItem('3. Workdescription')
            k4Edit.addItem('4. Voortgangstatus.')
            k4Edit.addItem('5. Contract price >')
            k4Edit.addItem('6. Contract price <')
            k4Edit.addItem('7. Payed in % >')
            k4Edit.activated[str].connect(self.k4Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(210)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k4Edit, 1, 0, 1, 2, Qt.AlignRight)
            lbl1 = QLabel('Searchterm')
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
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
            
            sluitBtn = QPushButton('Close')
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
        Column('werk_reis_uren', Float))

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
            self.setWindowTitle('Request external works')
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
  
    header = ['Worknumber','Workdescription', 'Progress status','Status week',\
              'Start week','Order date','Contract price','Amount payed','Budgeted materials',\
              'Realised materials', 'Budgeted wages', 'Realised wages', 'Budgeted equipment',\
              'Realised equipment','Budgeted direction', 'Realised direction','Budgeted housing',\
              'Realised housing', 'Budgeted hiring','Realised hiring','Budgeted remaining',\
              'Realised remaining', 'Budgeted transport', 'Realised transport', 'Budgeted\nconcrete work',\
              'Realised\nconcrete work','Budgeted\ncable work', 'Realised\ncable work','Budgeted\nearth-moving',\
              'Realised\nearth-moving', 'More/less work','Budgeted\nconstruction hours','Realised\nconstruction hours',\
              'Budgeted\nmounting hours', 'Realised\nmounting hours', 'Budgeted return\nwelding hours', 'Realised return\nwelding hours',\
              'Budgeted\ntelecom hours','Realised\ntelecom hours', 'Budgeted\nchief mechanic','Realised\nchief mechanic',\
              'Budgeted\nOCL hours', 'Realised\nOCL hours','Budgeted\npower-supply hours','Realised\npower-supply hours',\
              'Budgeted track\nlaying hours','Realised track\nlaying hours', 'Budgeted track\nwelding hours',\
              'Realised track\nwelding hours', 'Budgeted\ntravel hours', 'Realised\ntravel hours']
   
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
                    self.setWindowTitle("Request external work data")
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
                                                  
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 8, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    
                    grid.addWidget(QLabel('Worknumber'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1) 
                    
                    grid.addWidget(QLabel('Workdescription'), 1, 2)
                    grid.addWidget(q2Edit, 1, 3, 1, 3) 
                                                        
                    grid.addWidget(QLabel('Progress status'), 1, 6)
                    grid.addWidget(q3Edit, 1, 7)
                    
                    grid.addWidget(QLabel('Statusweek'), 1, 7, 1, 1, Qt.AlignRight)
                    grid.addWidget(q4Edit, 1, 8) 
                     
                    grid.addWidget(QLabel('Startweek'), 2, 2)
                    grid.addWidget(q5Edit, 2, 3)
                                                              
                    grid.addWidget(QLabel('Contract price'), 2, 4)
                    grid.addWidget(q8Edit, 2, 5)
                    
                    grid.addWidget(QLabel('More/less work'), 2, 6)
                    grid.addWidget(q9Edit, 2,7)
                          
                    lbl1 = QLabel('Total financial amounts')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 3, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Total revenues'), 4, 0)
                    grid.addWidget(q21Edit, 4, 1)
                    
                    grid.addWidget(QLabel('Total costs'), 4, 2)
                    grid.addWidget(q22Edit, 4, 3)
                    
                    grid.addWidget(QLabel('Amount payed'), 4, 4)
                    grid.addWidget(q11Edit, 4, 5)
                    
                    grid.addWidget(QLabel('To be invoiced'), 4,  6)
                    grid.addWidget(q26Edit, 4, 7)
                    
                    grid.addWidget(QLabel('Budgeted'), 5, 1)
                    grid.addWidget(QLabel('Realised'), 5, 2)
                    grid.addWidget(QLabel('Budgeted'), 5, 4)
                    grid.addWidget(QLabel('Realised'), 5, 5)
                    grid.addWidget(QLabel('Budgeted'), 5, 7)
                    grid.addWidget(QLabel('Realised'), 5, 8)
           
                    grid.addWidget(QLabel('Materials'), 6, 0)
                    grid.addWidget(q12Edit, 6, 1) 
                    grid.addWidget(q13Edit, 6, 2) 
                    
                    grid.addWidget(QLabel('Wages'), 6, 3)
                    grid.addWidget(q19Edit, 6, 4)
                    grid.addWidget(q14Edit, 6, 5)
                                                
                    grid.addWidget(QLabel('Equipment'), 6, 6)
                    grid.addWidget(q15Edit, 6, 7)                           
                    grid.addWidget(q16Edit, 6, 8)
                    
                    grid.addWidget(QLabel('Third parties'), 7, 0)
                    grid.addWidget(q23Edit, 7, 1)
                    grid.addWidget(q24Edit, 7, 2)
                     
                    grid.addWidget(QLabel('Direction'), 7, 3)
                    grid.addWidget(q18Edit, 7, 4) 
                    grid.addWidget(q17Edit, 7,5) 
                        
                    lbl2 = QLabel('Working hours consumption')
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl2, 8, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Budgeted'), 9, 1)
                    grid.addWidget(QLabel('Realised'), 9, 2)
                    grid.addWidget(QLabel('Budgeted'), 9, 4)
                    grid.addWidget(QLabel('Realised'), 9, 5)
                    grid.addWidget(QLabel('Budgeted'), 9, 7)
                    grid.addWidget(QLabel('Realised'), 9, 8)
                    
                    grid.addWidget(QLabel('Construction'), 10, 0)
                    grid.addWidget(u1Edit, 10,1)
                    grid.addWidget(u2Edit, 10,2) 

                    grid.addWidget(QLabel('Mounting'), 10, 3)
                    grid.addWidget(u3Edit, 10,4)
                    grid.addWidget(u4Edit, 10,5) 
                    
                    grid.addWidget(QLabel('Return welding'), 10, 6)
                    grid.addWidget(u5Edit, 10,7)
                    grid.addWidget(u6Edit, 10,8) 
                    
                    grid.addWidget(QLabel('Telecom'), 11, 0)
                    grid.addWidget(u7Edit, 11,1)
                    grid.addWidget(u8Edit, 11,2) 
                    
                    grid.addWidget(QLabel('Chief mechanic'), 11, 3)
                    grid.addWidget(u9Edit, 11,4)
                    grid.addWidget(u10Edit, 11,5)
                    
                    grid.addWidget(QLabel('OCL'), 11, 6)
                    grid.addWidget(u11Edit, 11,7)
                    grid.addWidget(u12Edit, 11,8)
                    
                    grid.addWidget(QLabel('Power-supply'), 12, 0)
                    grid.addWidget(u13Edit, 12,1)
                    grid.addWidget(u14Edit, 12,2)
                    
                    grid.addWidget(QLabel('Track laying'), 12, 3)
                    grid.addWidget(u15Edit, 12,4)
                    grid.addWidget(u16Edit, 12,5)
                    
                    grid.addWidget(QLabel('Track welding'), 12, 6)
                    grid.addWidget(u17Edit, 12,7)
                    grid.addWidget(u18Edit, 12,8)
                    
                    grid.addWidget(QLabel('Travel hours'), 13, 0)
                    grid.addWidget(u19Edit, 13,1)
                    grid.addWidget(u20Edit, 13,2)
                    
                    lbl3 = QLabel('Services third parties')
                    lbl3.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl3, 14, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Budgeted'), 15, 1)
                    grid.addWidget(QLabel('Realised'), 15, 2)
                    grid.addWidget(QLabel('Budgeted'), 15, 4)
                    grid.addWidget(QLabel('Realised'), 15, 5)
                    grid.addWidget(QLabel('Budgeted'), 15, 7)
                    grid.addWidget(QLabel('Realised'), 15, 8)
                      
                    grid.addWidget(QLabel('Housing'), 16, 0)
                    grid.addWidget(d1Edit, 16,1)
                    grid.addWidget(d2Edit, 16,2)
                    
                    grid.addWidget(QLabel('Hiring'), 16, 3)
                    grid.addWidget(d3Edit, 16,4)
                    grid.addWidget(d4Edit, 16,5)
                    
                    grid.addWidget(QLabel('Remaining'), 16, 6)
                    grid.addWidget(d5Edit, 16,7)
                    grid.addWidget(d6Edit, 16,8)
                    
                    grid.addWidget(QLabel('Transport'), 17, 0)
                    grid.addWidget(d7Edit, 17,1)
                    grid.addWidget(d8Edit, 17,2)
                    
                    grid.addWidget(QLabel('Concrete work'), 17, 3)
                    grid.addWidget(d9Edit, 17,4)
                    grid.addWidget(d10Edit, 17,5)
                    
                    grid.addWidget(QLabel('Cable work'), 17, 6)
                    grid.addWidget(d11Edit, 17,7)
                    grid.addWidget(d12Edit, 17,8)
                    
                    grid.addWidget(QLabel('Earth-moving'), 18, 0)
                    grid.addWidget(d13Edit, 18,1)
                    grid.addWidget(d14Edit, 18,2)
                     
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 20, 0, 1, 8, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 350, 300)
                                                                            
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 19, 8, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_() 
                       
    win = MyWindow(data_list, header)
    win.exec_()
    werkenKeuze(m_email)  